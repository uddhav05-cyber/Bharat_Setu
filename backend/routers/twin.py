"""
Digital Twin Router
Endpoints for village-level digital twin data visualization.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from auth.rbac import require_role
from services.twin_service import twin_service
from services.hotspot_service import hotspot_service

router = APIRouter(prefix="/twin", tags=["Digital Twin"])


# ----- Endpoints -----

@router.get("/{village_id}")
def get_village_twin(
    village_id: str,
    include_historical: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("VLE", "SARPANCH", "DISTRICT_OFFICIAL", "ADMIN")),
):
    """
    Get digital twin data for a village cluster.
    Returns GeoJSON FeatureCollection with farm plots, NDVI trends,
    degradation hotspots, and infrastructure data.
    """
    result = twin_service.get_village_twin(db, village_id, include_historical)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.get("/{village_id}/hotspots")
def get_village_hotspots(
    village_id: str,
    analysis_window_days: int = 180,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("VLE", "SARPANCH", "DISTRICT_OFFICIAL", "ADMIN")),
):
    """
    Get degradation hotspots for a village cluster.
    Uses NDVI trend analysis to identify areas needing intervention.
    """
    result = hotspot_service.detect_hotspots(db, village_id, analysis_window_days)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result
