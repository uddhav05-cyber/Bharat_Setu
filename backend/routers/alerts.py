"""
Alerts Router
Crisis alert endpoints for district officials.
Implements Boolean threshold crisis detection (Requirement 6, 19).
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.village_cluster import VillageCluster
from models.crisis_alert import CrisisAlert
from auth.rbac import get_current_user, require_role
from services.threshold_service import threshold_service

router = APIRouter(prefix="/alerts", tags=["Crisis Alerts"])


@router.post("/check/{village_cluster_id}")
async def check_thresholds(
    village_cluster_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("DISTRICT_OFFICIAL", "ADMIN")),
):
    """
    Run Boolean threshold checks on a village cluster.
    Creates crisis alert if any threshold is breached (one-strike logic).
    """
    cluster = db.query(VillageCluster).filter(VillageCluster.id == village_cluster_id).first()
    if not cluster:
        raise HTTPException(status_code=404, detail="Village cluster not found")

    # Build village data from cluster
    village_data = {
        "rainfall_percentage": cluster.rainfall_percentage,
        "water_access_percentage": cluster.water_access_percentage,
        "avg_health_expenditure": cluster.avg_health_expenditure,
        "avg_household_income": cluster.avg_household_income,
        "avg_ndvi_decline": cluster.avg_ndvi_decline,
        "debt_to_income_ratio": cluster.debt_to_income_ratio,
        "total_population": cluster.total_population,
        "farmer_population": cluster.farmer_population,
        "households_in_debt": cluster.households_in_debt,
    }

    # Run threshold checks
    result = threshold_service.check_critical_thresholds(village_data)

    # Create alert if any thresholds breached
    if result["triggered_thresholds"] > 0:
        alert = CrisisAlert(
            village_cluster_id=village_cluster_id,
            overall_status=result["overall_status"],
            triggered_thresholds=result["triggered_thresholds"],
            critical_alerts=result["critical_alerts"],
            vital_signs=village_data,
            notified_officials=[current_user.id],
        )
        db.add(alert)

        # Update cluster alert count
        cluster.critical_alerts_active = (cluster.critical_alerts_active or 0) + 1
        db.commit()
        db.refresh(alert)

        return {
            "alert_id": alert.id,
            "overall_status": result["overall_status"],
            "triggered_thresholds": result["triggered_thresholds"],
            "critical_alerts": result["critical_alerts"],
            "village_cluster": cluster.name,
        }

    return {
        "alert_id": None,
        "overall_status": "SAFE",
        "triggered_thresholds": 0,
        "critical_alerts": [],
        "village_cluster": cluster.name,
    }


@router.get("/")
def list_alerts(
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("DISTRICT_OFFICIAL", "ADMIN")),
):
    """List all crisis alerts, optionally filtered by status."""
    query = db.query(CrisisAlert)
    if status:
        query = query.filter(CrisisAlert.status == status)
    alerts = query.order_by(CrisisAlert.generated_at.desc()).limit(100).all()

    return [
        {
            "id": a.id,
            "village_cluster_id": a.village_cluster_id,
            "overall_status": a.overall_status,
            "triggered_thresholds": a.triggered_thresholds,
            "critical_alerts": a.critical_alerts,
            "status": a.status,
            "generated_at": a.generated_at,
        }
        for a in alerts
    ]


@router.post("/{alert_id}/acknowledge")
def acknowledge_alert(
    alert_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("DISTRICT_OFFICIAL", "ADMIN")),
):
    """Acknowledge a crisis alert."""
    alert = db.query(CrisisAlert).filter(CrisisAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = "ACKNOWLEDGED"
    if current_user.id not in (alert.notified_officials or []):
        alert.notified_officials = (alert.notified_officials or []) + [current_user.id]

    db.commit()
    return {"message": "Alert acknowledged", "alert_id": alert_id}


@router.post("/{alert_id}/resolve")
def resolve_alert(
    alert_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("DISTRICT_OFFICIAL", "ADMIN")),
):
    """Resolve a crisis alert."""
    alert = db.query(CrisisAlert).filter(CrisisAlert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    alert.status = "RESOLVED"
    alert.resolution_date = datetime.utcnow()
    db.commit()
    return {"message": "Alert resolved", "alert_id": alert_id}
