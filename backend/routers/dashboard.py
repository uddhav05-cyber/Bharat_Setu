"""
Dashboard Router
District official dashboard with metrics, crisis map, and data export.
Implements Requirement 15 (Crisis Map Dashboard for Officials).
"""
import csv
import io
from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.user import User
from models.farm_plot import FarmPlot
from models.verification import Verification
from models.certificate import Certificate
from models.village_cluster import VillageCluster
from models.crisis_alert import CrisisAlert
from auth.rbac import require_role

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/metrics")
def get_dashboard_metrics(
    village_id: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("DISTRICT_OFFICIAL", "ADMIN")),
):
    """
    Get dashboard metrics overview.
    Requirement 15.1: total service payments, active farmers, active VLEs, crisis distribution.
    """
    # Base queries
    farmers_query = db.query(User).filter(User.role == "FARMER")
    vles_query = db.query(User).filter(User.role == "VLE")
    farms_query = db.query(FarmPlot)
    verifications_query = db.query(Verification)
    alerts_query = db.query(CrisisAlert)

    if village_id:
        farms_query = farms_query.filter(FarmPlot.village_id == village_id)

    # Counts
    total_farmers = farmers_query.count()
    active_vles = vles_query.filter(User.account_status == "ACTIVE").count()
    total_farms = farms_query.count()
    total_verifications = verifications_query.count()

    # Carbon & payment stats
    approved_verifications = verifications_query.filter(
        Verification.verification_status == "APPROVED"
    ).all()
    total_carbon_tons = sum(v.carbon_sequestration_tons or 0 for v in approved_verifications)
    total_payments = total_carbon_tons * 500  # ₹500/ton fixed

    # Traffic light distribution
    green_count = verifications_query.filter(Verification.traffic_light_status == "GREEN").count()
    yellow_count = verifications_query.filter(Verification.traffic_light_status == "YELLOW").count()
    red_count = verifications_query.filter(Verification.traffic_light_status == "RED").count()

    # Crisis distribution
    active_alerts = alerts_query.filter(CrisisAlert.status == "ACTIVE").count()
    critical_alerts = alerts_query.filter(
        CrisisAlert.overall_status == "CRITICAL",
        CrisisAlert.status == "ACTIVE",
    ).count()

    return {
        "total_farmers": total_farmers,
        "active_vles": active_vles,
        "total_farms": total_farms,
        "total_verifications": total_verifications,
        "total_carbon_tons": round(total_carbon_tons, 2),
        "total_service_payments_inr": round(total_payments, 2),
        "traffic_light": {
            "green": green_count,
            "yellow": yellow_count,
            "red": red_count,
        },
        "crisis": {
            "active_alerts": active_alerts,
            "critical_alerts": critical_alerts,
        },
    }


@router.get("/crisis-map")
def get_crisis_map(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("DISTRICT_OFFICIAL", "ADMIN")),
):
    """
    Get crisis map data showing villages color-coded by status.
    Requirement 15.2: Green=Safe, Yellow=Warning, Red=Critical with crisis types.
    """
    clusters = db.query(VillageCluster).all()

    map_data = []
    for cluster in clusters:
        # Get latest alert for cluster
        latest_alert = (
            db.query(CrisisAlert)
            .filter(
                CrisisAlert.village_cluster_id == cluster.id,
                CrisisAlert.status.in_(["ACTIVE", "ACKNOWLEDGED"]),
            )
            .order_by(CrisisAlert.generated_at.desc())
            .first()
        )

        status = "GREEN"
        crisis_types = []
        if latest_alert:
            status = "RED" if latest_alert.overall_status == "CRITICAL" else "YELLOW"
            crisis_types = [
                a.get("type", "") for a in (latest_alert.critical_alerts or [])
            ]

        map_data.append({
            "cluster_id": cluster.id,
            "name": cluster.name,
            "district": cluster.district,
            "state": cluster.state,
            "centroid_lat": cluster.centroid_lat,
            "centroid_lon": cluster.centroid_lon,
            "status": status,
            "crisis_types": crisis_types,
            "total_farmers": cluster.total_farmers,
            "total_carbon_tons": cluster.total_carbon_tons,
            "vital_signs": {
                "rainfall": cluster.rainfall_percentage,
                "water_access": cluster.water_access_percentage,
                "ndvi_decline": cluster.avg_ndvi_decline,
                "debt_ratio": cluster.debt_to_income_ratio,
            },
        })

    return {"villages": map_data}


@router.get("/export")
def export_data(
    format: str = "csv",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("DISTRICT_OFFICIAL", "ADMIN")),
):
    """
    Export dashboard data as CSV.
    Requirement 15.4: CSV/PDF reports with all displayed metrics.
    """
    clusters = db.query(VillageCluster).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Village Cluster", "District", "State", "Total Farmers",
        "Total Carbon (tons)", "Rainfall %", "Water Access %",
        "NDVI Decline %", "Debt Ratio", "Active Alerts", "Status"
    ])

    for c in clusters:
        # Determine status
        active = db.query(CrisisAlert).filter(
            CrisisAlert.village_cluster_id == c.id,
            CrisisAlert.status == "ACTIVE",
        ).count()
        status = "CRITICAL" if active > 0 else "SAFE"

        writer.writerow([
            c.name, c.district, c.state, c.total_farmers,
            round(c.total_carbon_tons or 0, 2),
            c.rainfall_percentage, c.water_access_percentage,
            c.avg_ndvi_decline, c.debt_to_income_ratio,
            active, status
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=bharat_setu_report_{datetime.utcnow().strftime('%Y%m%d')}.csv"},
    )
