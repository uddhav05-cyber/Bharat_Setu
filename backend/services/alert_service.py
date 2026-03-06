"""
Alert Notification Service
Console/log-based alert notifications for pilot.
Free alternative to Amazon SNS/SES.
"""
import logging
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from models.crisis_alert import CrisisAlert
from models.village_cluster import VillageCluster
from models.user import User

logger = logging.getLogger(__name__)


class AlertService:
    """
    Alert Notification Component (Component 9 from design doc).
    Sends alert notifications to district officials.
    For pilot: logs to console. For production: swap to SNS/SES.
    """

    def format_alert_message(self, alert: CrisisAlert, cluster_name: str) -> str:
        """Format a human-readable alert message."""
        lines = [
            f"🚨 CRISIS ALERT — {cluster_name}",
            f"Status: {alert.overall_status}",
            f"Thresholds Breached: {alert.triggered_thresholds}",
            f"Generated: {alert.generated_at.strftime('%d %b %Y %H:%M') if alert.generated_at else 'N/A'}",
            "",
        ]

        for crisis in (alert.critical_alerts or []):
            lines.append(
                f"  ⚠ {crisis.get('type', 'UNKNOWN')} "
                f"(severity: {crisis.get('severity', 'N/A')}) — "
                f"value: {crisis.get('value', 'N/A')} "
                f"(threshold: {crisis.get('threshold', 'N/A')})"
            )
            lines.append(f"    → {crisis.get('recommended_action', 'No recommendation')}")
            affected = crisis.get("affected_population", 0)
            if affected:
                lines.append(f"    → Affected population: {affected}")

        return "\n".join(lines)

    def notify_officials(
        self,
        db: Session,
        alert: CrisisAlert,
        cluster: VillageCluster,
    ) -> dict:
        """
        Notify district officials about a crisis alert.
        Pilot: logs to console. Production: SNS/SES.
        """
        # Find district officials for this area
        officials = (
            db.query(User)
            .filter(User.role == "DISTRICT_OFFICIAL")
            .filter(User.district == cluster.district)
            .all()
        )

        # Fallback: notify all officials if none match district
        if not officials:
            officials = (
                db.query(User)
                .filter(User.role.in_(["DISTRICT_OFFICIAL", "ADMIN"]))
                .all()
            )

        # Format the alert
        message = self.format_alert_message(alert, cluster.name)

        # Log notification (pilot mode)
        delivery_status = []
        for official in officials:
            logger.warning(
                f"\n{'=' * 60}\n"
                f"ALERT NOTIFICATION to {official.name} ({official.phone})\n"
                f"{'=' * 60}\n"
                f"{message}\n"
                f"{'=' * 60}"
            )
            delivery_status.append({
                "official_id": official.id,
                "official_name": official.name,
                "channel": "CONSOLE",  # Would be EMAIL/SMS in production
                "status": "SENT",
            })

        # Update alert with notified officials
        alert.notified_officials = [d["official_id"] for d in delivery_status]
        db.commit()

        return {
            "alert_id": alert.id,
            "notifications_sent": len(delivery_status),
            "delivery_status": delivery_status,
        }

    def get_active_alerts(
        self, db: Session, village_id: str = None, skip: int = 0, limit: int = 50
    ) -> list:
        """Get active alerts, optionally filtered by village."""
        query = db.query(CrisisAlert).filter(CrisisAlert.status == "ACTIVE")
        if village_id:
            query = query.filter(CrisisAlert.village_cluster_id == village_id)
        return (
            query.order_by(CrisisAlert.generated_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


alert_service = AlertService()
