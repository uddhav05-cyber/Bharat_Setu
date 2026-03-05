"""
Verification Router
Endpoints for triggering and monitoring carbon credit verifications.
Implements the full verification flow with Traffic Light protocol.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.verification import Verification
from auth.rbac import get_current_user, require_role
from services.verification_service import verification_service

router = APIRouter(prefix="/verify", tags=["Verification"])


class VerifyRequest(BaseModel):
    vle_estimated_biomass: float = 0.5  # VLE's visual assessment (0-1)


@router.post("/{farm_plot_id}")
async def trigger_verification(
    farm_plot_id: str,
    req: VerifyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Trigger a carbon credit verification for a farm plot.
    Runs the full pipeline: Satellite → Biomass → Traffic Light → Payment
    """
    result = await verification_service.run_verification(
        db=db,
        farm_plot_id=farm_plot_id,
        vle_estimated_biomass=req.vle_estimated_biomass,
    )

    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    return result


@router.get("/{verification_id}/status")
def get_verification_status(
    verification_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get the status of a specific verification."""
    verification = db.query(Verification).filter(Verification.id == verification_id).first()
    if not verification:
        raise HTTPException(status_code=404, detail="Verification not found")

    return {
        "id": verification.id,
        "farm_plot_id": verification.farm_plot_id,
        "status": verification.verification_status,
        "traffic_light": verification.traffic_light_status,
        "variance": verification.variance,
        "biomass_score": verification.biomass_score,
        "carbon_tons": verification.carbon_sequestration_tons,
        "satellite_source": verification.satellite_source,
        "confidence_score": verification.confidence_score,
        "action": verification.action,
        "reasoning": verification.reasoning,
        "commission_status": verification.commission_status,
        "completed_at": verification.completed_at,
    }


@router.get("/farm/{farm_plot_id}/history")
def get_verification_history(
    farm_plot_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all verifications for a farm plot."""
    verifications = (
        db.query(Verification)
        .filter(Verification.farm_plot_id == farm_plot_id)
        .order_by(Verification.requested_at.desc())
        .all()
    )
    return [
        {
            "id": v.id,
            "status": v.verification_status,
            "traffic_light": v.traffic_light_status,
            "biomass_score": v.biomass_score,
            "carbon_tons": v.carbon_sequestration_tons,
            "satellite_source": v.satellite_source,
            "completed_at": v.completed_at,
        }
        for v in verifications
    ]
