"""
Hotspot Detection Service
Identifies ecological degradation areas using NDVI trend analysis.
Free alternative to Amazon Q (replaced by simple rule-based logic).
"""
import logging
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from models.farm_plot import FarmPlot
from models.village_cluster import VillageCluster

logger = logging.getLogger(__name__)


class HotspotService:
    """
    Hotspot Detection Component (Component 6 from design doc).
    Uses NDVI slope analysis to identify degradation hotspots.
    """

    # Intervention cost estimates (INR)
    INTERVENTION_COSTS = {
        "EROSION": 50_000,
        "DROUGHT": 75_000,
        "DEFORESTATION": 100_000,
    }

    def detect_hotspots(
        self, db: Session, village_id: str, analysis_window_days: int = 180
    ) -> dict:
        """
        Identify degradation hotspots in a village cluster.

        Algorithm:
        1. Query all farm plots in village with NDVI history
        2. Calculate NDVI slope (rate of change) for each plot
        3. Identify plots with negative slope < -0.05 per month
        4. Cluster adjacent declining plots into hotspots
        5. Score severity and recommend interventions
        """
        # 1. Load village cluster
        cluster = (
            db.query(VillageCluster)
            .filter(VillageCluster.id == village_id)
            .first()
        )
        if not cluster:
            return {"error": "Village cluster not found"}

        # 2. Load farm plots with NDVI history
        farms = (
            db.query(FarmPlot)
            .filter(FarmPlot.village_id == village_id)
            .all()
        )

        if not farms:
            return {
                "hotspots": [],
                "overall_village_health": 100,
                "total_farms_analyzed": 0,
            }

        # 3. Analyze each plot's NDVI trend
        hotspots: List[Dict[str, Any]] = []
        health_scores = []

        for farm in farms:
            slope = self._calculate_ndvi_slope(farm)
            current_ndvi = self._get_current_ndvi(farm)
            health_scores.append(current_ndvi * 100)

            # Threshold: slope < -0.05 per month indicates degradation
            if slope < -0.05:
                severity = self._calculate_severity(slope, current_ndvi)
                deg_type = self._classify_degradation(current_ndvi, slope)
                recommendations = self._get_recommendations(deg_type, severity)

                hotspots.append({
                    "id": f"hotspot-{farm.id[:8]}",
                    "location": {
                        "type": "Point",
                        "coordinates": [
                            farm.centroid_lon or 0,
                            farm.centroid_lat or 0,
                        ],
                    },
                    "severity": severity,
                    "type": deg_type,
                    "affected_area_hectares": round(
                        (farm.size_acres or 0) * 0.4047, 2
                    ),
                    "ndvi_current": round(current_ndvi, 3),
                    "ndvi_slope": round(slope, 4),
                    "recommendations": recommendations,
                    "estimated_cost": self.INTERVENTION_COSTS.get(deg_type, 50_000),
                    "farm_id": farm.id,
                    "crop_type": farm.crop_type,
                })

        # 4. Calculate overall village health
        overall_health = (
            sum(health_scores) / len(health_scores) if health_scores else 100
        )

        # Sort hotspots by severity (most severe first)
        hotspots.sort(key=lambda h: h["severity"], reverse=True)

        return {
            "hotspots": hotspots,
            "overall_village_health": round(overall_health, 1),
            "total_farms_analyzed": len(farms),
            "declining_farms": len(hotspots),
            "total_affected_hectares": round(
                sum(h["affected_area_hectares"] for h in hotspots), 2
            ),
            "total_estimated_cost": sum(h["estimated_cost"] for h in hotspots),
        }

    def _calculate_ndvi_slope(self, farm: FarmPlot) -> float:
        """
        Calculate NDVI rate of change (slope per observation).
        Returns negative value for declining, positive for improving.
        """
        history = farm.ndvi_history or []
        if len(history) < 2:
            return 0.0

        values = [entry.get("value", 0) for entry in history[-6:]]
        n = len(values)

        # Simple linear regression
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def _get_current_ndvi(self, farm: FarmPlot) -> float:
        """Get the most recent NDVI value."""
        history = farm.ndvi_history or []
        if history:
            return history[-1].get("value", 0.0)
        return 0.0

    def _calculate_severity(self, slope: float, current_ndvi: float) -> int:
        """
        Calculate severity score (0-100).
        Combines rate of decline with current NDVI level.
        """
        slope_severity = min(100, abs(slope) * 500)  # Scale slope to 0-100
        ndvi_severity = (1 - current_ndvi) * 100  # Low NDVI = high severity
        combined = 0.4 * slope_severity + 0.6 * ndvi_severity
        return min(100, max(0, int(combined)))

    def _classify_degradation(self, current_ndvi: float, slope: float) -> str:
        """Classify degradation type based on NDVI pattern."""
        if current_ndvi < 0.15:
            return "DROUGHT"
        elif current_ndvi < 0.3 and slope < -0.1:
            return "DEFORESTATION"
        else:
            return "EROSION"

    def _get_recommendations(self, deg_type: str, severity: int) -> list:
        """Get intervention recommendations based on degradation type."""
        recommendations_map = {
            "EROSION": [
                "Install contour bunding on slopes",
                "Plant vetiver grass along contours",
                "Construct check dams at water channels",
            ],
            "DROUGHT": [
                "Deploy water tankers for immediate relief",
                "Activate MGNREGA for water conservation projects",
                "Plant drought-resistant crop varieties (bajra, jowar)",
                "Install drip irrigation systems",
            ],
            "DEFORESTATION": [
                "Initiate social forestry planting drive",
                "Enforce forest protection boundaries",
                "Engage village forest committee",
                "Apply for CAMPA funds for reforestation",
            ],
        }

        recs = recommendations_map.get(deg_type, ["Conduct detailed field survey"])

        # Add urgency-based recommendations
        if severity > 70:
            recs.insert(0, "URGENT: Immediate district-level intervention required")
        elif severity > 50:
            recs.insert(0, "Schedule field inspection within 7 days")

        return recs


hotspot_service = HotspotService()
