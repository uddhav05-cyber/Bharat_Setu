"""
Verification Calculation Tests
Tests NDVI biomass calculation, SAR biomass, and carbon sequestration formula.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.satellite_service import SatelliteService


def get_service():
    return SatelliteService()


class TestNDVICalculation:
    """Tests for NDVI = (NIR - Red) / (NIR + Red)."""

    def test_healthy_vegetation(self):
        svc = get_service()
        # NIR=0.5, Red=0.05 → NDVI ≈ 0.818
        result = svc.calculate_ndvi(0.05, 0.5)
        assert 0.8 < result <= 1.0

    def test_bare_soil(self):
        svc = get_service()
        # NIR=0.1, Red=0.1 → NDVI = 0.0
        result = svc.calculate_ndvi(0.1, 0.1)
        assert result == 0.0

    def test_water_body(self):
        svc = get_service()
        # Red > NIR → negative NDVI, clamped to 0
        result = svc.calculate_ndvi(0.3, 0.1)
        assert result == 0.0  # Clamped

    def test_result_in_0_to_1_range(self):
        svc = get_service()
        result = svc.calculate_ndvi(0.05, 0.7)
        assert 0.0 <= result <= 1.0

    def test_zero_bands(self):
        """Both bands zero should return 0."""
        svc = get_service()
        assert svc.calculate_ndvi(0.0, 0.0) == 0.0

    def test_low_vegetation(self):
        svc = get_service()
        # NIR=0.2, Red=0.15 → NDVI ≈ 0.143
        result = svc.calculate_ndvi(0.15, 0.2)
        assert 0.1 < result < 0.2


class TestSARBiomass:
    """Tests for Sentinel-1 SAR backscatter biomass calculation."""

    def test_high_biomass(self):
        svc = get_service()
        # VV=-5 (max), VH=-10 (max) → High biomass
        result = svc.calculate_sar_biomass(-5, -10)
        assert result > 0.7

    def test_low_biomass(self):
        svc = get_service()
        # VV=-25 (min), VH=-30 (min) → Low biomass
        result = svc.calculate_sar_biomass(-25, -30)
        assert result == 0.0

    def test_result_in_0_to_1_range(self):
        svc = get_service()
        for vv in [-25, -20, -15, -10, -5]:
            for vh in [-30, -25, -20, -15, -10]:
                result = svc.calculate_sar_biomass(vv, vh)
                assert 0.0 <= result <= 1.0, f"SAR biomass out of range for VV={vv}, VH={vh}: {result}"

    def test_medium_biomass(self):
        svc = get_service()
        result = svc.calculate_sar_biomass(-12, -18)
        assert 0.3 < result < 0.7


class TestCarbonSequestration:
    """Tests for carbon sequestration formula."""

    def test_positive_biomass_change(self):
        svc = get_service()
        # Δbiomass=0.2, area=1ha, crop factor=0.2
        result = svc.calculate_carbon_sequestration(0.2, 1.0, "crops")
        expected = 0.2 * 1.0 * 3.67 * 0.2  # = 0.1468
        assert abs(result - expected) < 0.001

    def test_negative_biomass_change_returns_zero(self):
        svc = get_service()
        result = svc.calculate_carbon_sequestration(-0.1, 1.0, "rice")
        assert result == 0.0  # No negative carbon credits

    def test_tree_crop_type_has_highest_factor(self):
        svc = get_service()
        trees = svc.calculate_carbon_sequestration(0.2, 1.0, "trees")
        crops = svc.calculate_carbon_sequestration(0.2, 1.0, "crops")
        assert trees > crops  # Trees (0.5) > Crops (0.2)

    def test_unknown_crop_type_uses_default(self):
        svc = get_service()
        result = svc.calculate_carbon_sequestration(0.2, 1.0, "unknown_crop")
        expected = 0.2 * 1.0 * 3.67 * 0.2  # Default factor = 0.2
        assert abs(result - expected) < 0.001

    def test_larger_area_produces_more_carbon(self):
        svc = get_service()
        small = svc.calculate_carbon_sequestration(0.2, 1.0, "rice")
        large = svc.calculate_carbon_sequestration(0.2, 5.0, "rice")
        assert abs(large - small * 5) < 0.001

    def test_zero_biomass_change_returns_zero(self):
        svc = get_service()
        result = svc.calculate_carbon_sequestration(0.0, 1.0, "wheat")
        assert result == 0.0

    def test_specific_crop_types(self):
        """Verify specific crop type factors are used."""
        svc = get_service()
        for crop, factor in [("trees", 0.5), ("grassland", 0.15), ("sugarcane", 0.22)]:
            result = svc.calculate_carbon_sequestration(1.0, 1.0, crop)
            expected = 1.0 * 1.0 * 3.67 * factor
            assert abs(result - expected) < 0.001, f"Failed for {crop}"
