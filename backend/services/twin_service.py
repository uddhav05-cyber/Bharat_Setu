"""
Digital Twin Service
Aggregates village-level farm data into GeoJSON for visualization.
Free alternative to PostGIS spatial aggregation + MapMyIndia API.
"""
import logging
from typing import Optional
from sqlalchemy.orm import Session
from models.farm_plot import FarmPlot
from models.village_cluster import VillageCluster
from models.verification import Verification

logger = logging.getLogger(__name__)


class TwinService:
    """
    Digital Twin Component (Component 5 from design doc).
    Aggregates village farm data for 3D map visualization.
    """

    def get_village_twin(
        self, db: Session, village_id: str, include_historical: bool = True
    ) -> dict:
        """
        Generate digital twin payload for a village.
        Returns GeoJSON FeatureCollection with farm plots, NDVI trends, and
        mock infrastructure data.
        """
        # 1. Load village cluster
        cluster = (
            db.query(VillageCluster)
            .filter(VillageCluster.id == village_id)
            .first()
        )
        if not cluster:
            return {"error": "Village cluster not found"}

        # 2. Load farm plots in village
        farms = (
            db.query(FarmPlot)
            .filter(FarmPlot.village_id == village_id)
            .all()
        )

        # 3. Build farm plot features
        farm_features = []
        total_carbon = 0.0
        ndvi_values = []

        for farm in farms:
            ndvi_current = self._get_current_ndvi(farm)
            ndvi_trend = self._calculate_ndvi_trend(farm) if include_historical else "STABLE"
            ndvi_values.append(ndvi_current)
            total_carbon += farm.carbon_credits_total or 0

            feature = {
                "type": "Feature",
                "properties": {
                    "id": farm.id,
                    "crop_type": farm.crop_type,
                    "size_acres": farm.size_acres,
                    "ndvi_current": ndvi_current,
                    "ndvi_trend": ndvi_trend,
                    "carbon_total": farm.carbon_credits_total or 0,
                    "status": farm.status,
                },
                "geometry": farm.geometry or {
                    "type": "Point",
                    "coordinates": [farm.centroid_lon or 0, farm.centroid_lat or 0],
                },
            }

            if include_historical and farm.ndvi_history:
                feature["properties"]["ndvi_history"] = farm.ndvi_history[-6:]  # Last 6 entries

            farm_features.append(feature)

        # 4. Generate degradation hotspots from NDVI data
        hotspots = self._detect_hotspots(farms)

        # 5. Mock infrastructure data
        infrastructure = self._get_mock_infrastructure(cluster)

        # 6. Assemble response
        avg_ndvi = sum(ndvi_values) / len(ndvi_values) if ndvi_values else 0

        return {
            "village_id": village_id,
            "village_name": cluster.name,
            "village_geometry": cluster.geometry,
            "centroid": {
                "lat": cluster.centroid_lat,
                "lon": cluster.centroid_lon,
            },
            "statistics": {
                "total_farms": len(farms),
                "total_carbon_tons": round(total_carbon, 3),
                "average_ndvi": round(avg_ndvi, 3),
                "total_area_acres": sum(f.size_acres or 0 for f in farms),
            },
            "farm_plots": {
                "type": "FeatureCollection",
                "features": farm_features,
            },
            "degradation_hotspots": hotspots,
            "infrastructure": infrastructure,
        }

    def _get_current_ndvi(self, farm: FarmPlot) -> float:
        """Get the most recent NDVI value for a farm."""
        if farm.ndvi_history and len(farm.ndvi_history) > 0:
            return farm.ndvi_history[-1].get("value", 0.0)
        return 0.0

    def _calculate_ndvi_trend(self, farm: FarmPlot) -> str:
        """
        Calculate NDVI trend: IMPROVING, STABLE, or DECLINING.
        Uses linear slope of recent NDVI values.
        """
        history = farm.ndvi_history or []
        if len(history) < 2:
            return "STABLE"

        recent = [entry.get("value", 0) for entry in history[-6:]]
        n = len(recent)

        # Simple linear regression slope
        x_mean = (n - 1) / 2
        y_mean = sum(recent) / n
        numerator = sum((i - x_mean) * (recent[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return "STABLE"

        slope = numerator / denominator

        if slope > 0.02:
            return "IMPROVING"
        elif slope < -0.02:
            return "DECLINING"
        return "STABLE"

    def _detect_hotspots(self, farms: list) -> list:
        """Identify degradation hotspots from declining farm plots."""
        hotspots = []
        for farm in farms:
            trend = self._calculate_ndvi_trend(farm)
            if trend == "DECLINING":
                current_ndvi = self._get_current_ndvi(farm)
                severity = min(100, max(0, int((1 - current_ndvi) * 100)))

                # Determine degradation type
                if current_ndvi < 0.2:
                    deg_type = "DROUGHT"
                elif current_ndvi < 0.4:
                    deg_type = "EROSION"
                else:
                    deg_type = "DEFORESTATION"

                hotspots.append({
                    "location": {
                        "type": "Point",
                        "coordinates": [
                            farm.centroid_lon or 0,
                            farm.centroid_lat or 0,
                        ],
                    },
                    "severity": severity,
                    "type": deg_type,
                    "affected_area_acres": farm.size_acres or 0,
                    "farm_id": farm.id,
                })
        return hotspots

    def _get_mock_infrastructure(self, cluster: VillageCluster) -> dict:
        """Mock infrastructure data for the village (replaces MapMyIndia API)."""
        lat = cluster.centroid_lat or 19.0
        lon = cluster.centroid_lon or 73.0

        return {
            "roads": {
                "type": "MultiLineString",
                "coordinates": [
                    [[lon - 0.01, lat - 0.01], [lon + 0.01, lat + 0.01]],
                    [[lon - 0.005, lat + 0.01], [lon + 0.005, lat - 0.01]],
                ],
            },
            "water_bodies": {
                "type": "MultiPolygon",
                "coordinates": [[
                    [
                        [lon + 0.005, lat + 0.005],
                        [lon + 0.008, lat + 0.005],
                        [lon + 0.008, lat + 0.008],
                        [lon + 0.005, lat + 0.008],
                        [lon + 0.005, lat + 0.005],
                    ]
                ]],
            },
            "buildings": {
                "type": "MultiPoint",
                "coordinates": [
                    [lon, lat],
                    [lon + 0.002, lat + 0.001],
                    [lon - 0.003, lat + 0.002],
                ],
            },
        }


twin_service = TwinService()
