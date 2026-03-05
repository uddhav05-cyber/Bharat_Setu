"""
Satellite Service (Mock)
Free alternative to Amazon SageMaker + Copernicus Hub.
Generates realistic mock satellite data for pilot demonstration.
"""
import random
import math
import uuid
import os
import json
import logging
from datetime import datetime, timedelta
from typing import Optional
from config import settings

logger = logging.getLogger(__name__)


class SatelliteService:
    """Mock satellite data service replacing Copernicus Hub + SageMaker."""

    def acquire_imagery(
        self,
        farm_plot_id: str,
        centroid_lat: float,
        centroid_lon: float,
        preferred_source: str = "AUTO",
    ) -> dict:
        """
        Simulate satellite imagery acquisition.
        Returns mock tile data with realistic values.
        """
        # Simulate cloud cover (seasonal variation)
        month = datetime.utcnow().month
        # Monsoon months (Jun-Sep) have higher cloud cover
        if 6 <= month <= 9:
            cloud_cover = random.uniform(40, 90)
        else:
            cloud_cover = random.uniform(5, 50)

        # Determine satellite source based on cloud cover or preference
        if preferred_source == "OPTICAL" or (preferred_source == "AUTO" and cloud_cover < 30):
            satellite_source = "SENTINEL_2_OPTICAL"
        else:
            satellite_source = "SENTINEL_1_SAR"

        # Generate mock tile ID & storage path
        tile_id = f"tile-{farm_plot_id[:8]}-{datetime.utcnow().strftime('%Y%m%d')}"
        storage_path = os.path.join(
            settings.SATELLITE_STORAGE_PATH, farm_plot_id, f"{tile_id}.json"
        )

        # Create mock tile data
        tile_data = {
            "tile_id": tile_id,
            "farm_plot_id": farm_plot_id,
            "satellite_source": satellite_source,
            "acquisition_date": datetime.utcnow().isoformat(),
            "cloud_cover": cloud_cover if satellite_source == "SENTINEL_2_OPTICAL" else None,
            "centroid_lat": centroid_lat,
            "centroid_lon": centroid_lon,
            "quality_score": random.uniform(70, 100),
        }

        if satellite_source == "SENTINEL_2_OPTICAL":
            # Mock Sentinel-2 bands (B4 Red, B8 NIR)
            tile_data["bands"] = {
                "B4_RED": random.uniform(0.02, 0.15),
                "B8_NIR": random.uniform(0.15, 0.70),
            }
        else:
            # Mock Sentinel-1 SAR polarization
            tile_data["bands"] = {
                "VV": random.uniform(-20, -5),  # dB
                "VH": random.uniform(-25, -10),  # dB
            }

        # Store tile data locally
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)
        with open(storage_path, "w") as f:
            json.dump(tile_data, f, indent=2)

        return {
            "tile_ids": [tile_id],
            "acquisition_dates": [tile_data["acquisition_date"]],
            "cloud_cover_percentages": [cloud_cover],
            "satellite_source": satellite_source,
            "storage_paths": [storage_path],
            "quality_score": tile_data["quality_score"],
        }

    def calculate_ndvi(self, red_band: float, nir_band: float) -> float:
        """
        Calculate NDVI from Sentinel-2 optical bands.
        Formula: NDVI = (NIR - Red) / (NIR + Red)
        Returns value between 0 and 1 (clamped).
        """
        if (nir_band + red_band) == 0:
            return 0.0
        ndvi = (nir_band - red_band) / (nir_band + red_band)
        return max(0.0, min(1.0, ndvi))

    def calculate_sar_biomass(self, vv: float, vh: float) -> float:
        """
        Calculate biomass from Sentinel-1 SAR backscatter.
        Uses simplified model: biomass = f(VV, VH)
        Returns value between 0 and 1 (normalized).
        """
        # Simplified biomass model from SAR backscatter (dB scale)
        # Higher backscatter (less negative) = more biomass
        vv_norm = (vv + 25) / 20  # Normalize from [-25, -5] to [0, 1]
        vh_norm = (vh + 30) / 20  # Normalize from [-30, -10] to [0, 1]
        biomass = 0.6 * max(0, min(1, vv_norm)) + 0.4 * max(0, min(1, vh_norm))
        return max(0.0, min(1.0, biomass))

    def calculate_carbon_sequestration(
        self,
        biomass_change: float,
        plot_area_hectares: float,
        crop_type: str,
    ) -> float:
        """
        Calculate carbon sequestration in tons CO2 equivalent.
        Formula: (biomass_change × area × 3.67 × biomass_factor)
        """
        biomass_factors = {
            "trees": 0.5,
            "crops": 0.2,
            "grassland": 0.15,
            "rice": 0.2,
            "wheat": 0.2,
            "cotton": 0.18,
            "sugarcane": 0.22,
        }
        factor = biomass_factors.get(crop_type.lower(), 0.2)
        carbon_tons = biomass_change * plot_area_hectares * 3.67 * factor
        return max(0.0, carbon_tons)


satellite_service = SatelliteService()
