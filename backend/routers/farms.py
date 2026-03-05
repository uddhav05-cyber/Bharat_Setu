"""
Farm CRUD Router
Endpoints for farm plot registration and management.
Implements Requirements 1 (Voice-Based Farm Registration).
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.farm_plot import FarmPlot
from models.user import User
from auth.rbac import get_current_user, require_role
from events.event_bus import event_bus, Events

router = APIRouter(prefix="/farms", tags=["Farm Plots"])


# ----- Schemas -----

class FarmCreateRequest(BaseModel):
    farmer_id: str
    size_acres: float
    crop_type: str
    village_id: str | None = None
    geometry: dict  # GeoJSON Polygon
    centroid_lat: float
    centroid_lon: float
    bbox_min_lat: float | None = None
    bbox_min_lon: float | None = None
    bbox_max_lat: float | None = None
    bbox_max_lon: float | None = None


class FarmResponse(BaseModel):
    id: str
    farmer_id: str
    vle_id: str | None
    size_acres: float
    crop_type: str
    village_id: str | None
    geometry: dict
    centroid_lat: float | None
    centroid_lon: float | None
    status: str
    carbon_credits_total: float
    ndvi_history: list
    registration_date: datetime | None

    class Config:
        from_attributes = True


# ----- Endpoints -----

@router.post("/", response_model=FarmResponse)
async def create_farm(
    req: FarmCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Register a new farm plot (VLE-assisted or direct)."""
    # Determine VLE if current user is a VLE
    vle_id = current_user.id if current_user.role == "VLE" else None

    farm = FarmPlot(
        farmer_id=req.farmer_id,
        vle_id=vle_id,
        size_acres=req.size_acres,
        crop_type=req.crop_type,
        village_id=req.village_id,
        geometry=req.geometry,
        centroid_lat=req.centroid_lat,
        centroid_lon=req.centroid_lon,
        bbox_min_lat=req.bbox_min_lat,
        bbox_min_lon=req.bbox_min_lon,
        bbox_max_lat=req.bbox_max_lat,
        bbox_max_lon=req.bbox_max_lon,
    )

    db.add(farm)
    db.commit()
    db.refresh(farm)

    # Publish event for satellite subscription
    await event_bus.publish(Events.FARM_REGISTERED, {
        "farm_plot_id": farm.id,
        "farmer_id": farm.farmer_id,
        "geometry": farm.geometry,
        "centroid_lat": farm.centroid_lat,
        "centroid_lon": farm.centroid_lon,
    })

    return farm


@router.get("/{farm_id}", response_model=FarmResponse)
def get_farm(
    farm_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific farm plot by ID."""
    farm = db.query(FarmPlot).filter(FarmPlot.id == farm_id).first()
    if not farm:
        raise HTTPException(status_code=404, detail="Farm plot not found")

    # RBAC: Farmers can only see their own farms
    if current_user.role == "FARMER" and farm.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return farm


@router.get("/village/{village_id}", response_model=List[FarmResponse])
def get_farms_by_village(
    village_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("VLE", "SARPANCH", "DISTRICT_OFFICIAL", "ADMIN")),
):
    """Get all farm plots in a village."""
    farms = db.query(FarmPlot).filter(FarmPlot.village_id == village_id).all()
    return farms


@router.get("/", response_model=List[FarmResponse])
def list_farms(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List farm plots. Farmers see only their own; VLEs/admins see all."""
    query = db.query(FarmPlot)

    if current_user.role == "FARMER":
        query = query.filter(FarmPlot.farmer_id == current_user.id)
    elif current_user.role == "VLE":
        query = query.filter(FarmPlot.vle_id == current_user.id)

    return query.offset(skip).limit(limit).all()
