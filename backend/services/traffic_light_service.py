"""
Traffic Light Service
Implements the adversarial trust verification protocol from the design doc.
Detects VLE fraud by comparing VLE-reported data against satellite verification.
"""
import logging
from typing import Tuple

logger = logging.getLogger(__name__)


class TrafficLightService:
    """
    Traffic Light Verifier (Component 10 from design doc).
    Compares VLE ground reports against satellite verification.
    """

    def calculate_variance(
        self, vle_biomass: float, satellite_biomass: float
    ) -> float:
        """
        Calculate variance between VLE estimate and satellite data.
        Formula: |VLE_biomass - Satellite_biomass| / Satellite_biomass * 100
        """
        if satellite_biomass <= 0:
            return 100.0  # If satellite shows no biomass, any VLE claim is suspicious
        variance = abs(vle_biomass - satellite_biomass) / satellite_biomass * 100
        return min(variance, 100.0)

    def determine_status(
        self, variance: float, confidence_score: float
    ) -> Tuple[str, str, str]:
        """
        Determine traffic light status based on variance and confidence.

        Returns: (status, action, reasoning)
        - GREEN: Auto-approve (variance < 10%, confidence > 80%)
        - YELLOW: Flag for call (variance 10-30% OR confidence < 80%)
        - RED: Freeze account (variance > 30%, confidence > 80%)
        """
        if confidence_score < 80:
            return (
                "YELLOW",
                "FLAG_FOR_CALL",
                f"Satellite data uncertain (confidence: {confidence_score:.1f}%). Manual review needed.",
            )

        if variance < 10:
            return (
                "GREEN",
                "AUTO_APPROVE",
                f"VLE data matches satellite verification (variance: {variance:.1f}%). Auto-approved.",
            )
        elif 10 <= variance <= 30:
            return (
                "YELLOW",
                "FLAG_FOR_CALL",
                f"Moderate variance detected ({variance:.1f}%). Flagged for verification call.",
            )
        else:
            return (
                "RED",
                "FREEZE_ACCOUNT",
                f"High variance detected ({variance:.1f}%). VLE account frozen for audit.",
            )

    def update_trust_score(self, current_score: float, status: str) -> float:
        """
        Update VLE trust score based on traffic light status.
        GREEN: +2 (reward accuracy)
        YELLOW: 0 (no change)
        RED: -15 (penalize fraud)
        """
        if status == "GREEN":
            return min(100.0, current_score + 2)
        elif status == "YELLOW":
            return current_score
        else:  # RED
            return max(0.0, current_score - 15)

    def determine_commission_status(
        self, status: str, confidence_score: float, trust_score: float
    ) -> str:
        """
        Determine commission status.
        Commission released only if confidence > 80 AND trust > 40.
        """
        if status == "RED":
            return "FORFEITED"
        elif confidence_score > 80 and trust_score > 40 and status == "GREEN":
            return "APPROVED"
        else:
            return "HELD"

    def check_account_suspension(self, trust_score: float) -> bool:
        """
        Check if VLE account should be suspended.
        Requirement 20.4: Trust score below 40 triggers suspension.
        """
        return trust_score < 40

    def check_performance_bonus(
        self, trust_score: float, months_above_90: int
    ) -> float:
        """
        Check if VLE qualifies for performance bonus.
        Requirement 20.5: Trust score > 90 for 6 months = +2% commission.
        """
        if trust_score > 90 and months_above_90 >= 6:
            return 2.0  # 2% commission increase
        return 0.0


traffic_light_service = TrafficLightService()
