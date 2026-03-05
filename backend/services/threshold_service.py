"""
Threshold Service
Boolean threshold logic for crisis detection (Component 12 from design doc).
Replaces weighted-average risk scoring with one-strike detection.
"""
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class ThresholdService:
    """
    Threshold Monitor — detects acute crises using Boolean threshold logic.
    Any single threshold breach triggers an alert (one-strike).
    """

    def check_critical_thresholds(self, village_data: dict) -> dict:
        """
        Evaluate each critical threshold independently.
        Returns ThresholdResponse with all breached thresholds.
        """
        alerts: List[Dict[str, Any]] = []

        # Threshold 1: Rainfall Failure (< 50% of seasonal average)
        rainfall = village_data.get("rainfall_percentage", 100)
        if rainfall < 50:
            alerts.append({
                "type": "RAINFALL_FAILURE",
                "severity": "CRITICAL",
                "value": rainfall,
                "threshold": 50,
                "affected_population": village_data.get("total_population", 0),
                "recommended_action": "Deploy water tankers, activate MGNREGA for water conservation projects",
            })

        # Threshold 2: Water Access Crisis (< 30%)
        water_access = village_data.get("water_access_percentage", 100)
        if water_access < 30:
            affected = int(
                village_data.get("total_population", 0)
                * (1 - water_access / 100)
            )
            alerts.append({
                "type": "WATER_CRISIS",
                "severity": "CRITICAL",
                "value": water_access,
                "threshold": 30,
                "affected_population": affected,
                "recommended_action": "Emergency water supply, fast-track check dam construction",
            })

        # Threshold 3: Health Shock (health expenditure > income)
        health_exp = village_data.get("avg_health_expenditure", 0)
        income = village_data.get("avg_household_income", 10000)
        if health_exp > income:
            alerts.append({
                "type": "HEALTH_SHOCK",
                "severity": "CRITICAL",
                "value": health_exp,
                "threshold": income,
                "affected_population": village_data.get("households_in_debt", 0),
                "recommended_action": "Activate Ayushman Bharat coverage, provide interest-free loans",
            })

        # Threshold 4: Crop Failure (NDVI decline > 30%)
        ndvi_decline = village_data.get("avg_ndvi_decline", 0)
        if ndvi_decline > 30:
            alerts.append({
                "type": "CROP_FAILURE",
                "severity": "HIGH",
                "value": ndvi_decline,
                "threshold": 30,
                "affected_population": village_data.get("farmer_population", 0),
                "recommended_action": "Crop insurance claims, alternative livelihood programs",
            })

        # Threshold 5: Debt Ratio Crisis (> 2.0)
        debt_ratio = village_data.get("debt_to_income_ratio", 0)
        if debt_ratio > 2.0:
            alerts.append({
                "type": "DEBT_CRISIS",
                "severity": "CRITICAL",
                "value": debt_ratio,
                "threshold": 2.0,
                "affected_population": village_data.get("households_in_debt", 0),
                "recommended_action": "Debt restructuring, NABARD refinancing schemes",
            })

        # Determine overall status using ONE-STRIKE logic
        if any(a["severity"] == "CRITICAL" for a in alerts):
            overall_status = "CRITICAL"
        elif len(alerts) > 0:
            overall_status = "WARNING"
        else:
            overall_status = "SAFE"

        return {
            "critical_alerts": alerts,
            "overall_status": overall_status,
            "triggered_thresholds": len(alerts),
        }


threshold_service = ThresholdService()
