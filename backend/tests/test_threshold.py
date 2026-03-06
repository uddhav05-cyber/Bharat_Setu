"""
Threshold Service Tests
Tests each of the 5 Boolean thresholds independently,
one-strike logic, and boundary values.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.threshold_service import ThresholdService


def get_service():
    return ThresholdService()


def safe_village():
    """Returns village data where ALL thresholds are within safe range."""
    return {
        "rainfall_percentage": 80.0,
        "water_access_percentage": 60.0,
        "avg_health_expenditure": 3000,
        "avg_household_income": 10000,
        "avg_ndvi_decline": 10.0,
        "debt_to_income_ratio": 1.0,
        "total_population": 2000,
        "farmer_population": 600,
        "households_in_debt": 100,
    }


class TestIndividualThresholds:
    """Each threshold must fire independently."""

    def test_rainfall_failure_triggers(self):
        svc = get_service()
        data = safe_village()
        data["rainfall_percentage"] = 40.0  # Below 50% threshold
        result = svc.check_critical_thresholds(data)
        assert result["triggered_thresholds"] == 1
        assert result["critical_alerts"][0]["type"] == "RAINFALL_FAILURE"

    def test_water_crisis_triggers(self):
        svc = get_service()
        data = safe_village()
        data["water_access_percentage"] = 20.0  # Below 30% threshold
        result = svc.check_critical_thresholds(data)
        assert result["triggered_thresholds"] == 1
        assert result["critical_alerts"][0]["type"] == "WATER_CRISIS"

    def test_health_shock_triggers(self):
        svc = get_service()
        data = safe_village()
        data["avg_health_expenditure"] = 15000  # Above income
        data["avg_household_income"] = 10000
        result = svc.check_critical_thresholds(data)
        assert result["triggered_thresholds"] == 1
        assert result["critical_alerts"][0]["type"] == "HEALTH_SHOCK"

    def test_crop_failure_triggers(self):
        svc = get_service()
        data = safe_village()
        data["avg_ndvi_decline"] = 40.0  # Above 30% threshold
        result = svc.check_critical_thresholds(data)
        assert result["triggered_thresholds"] == 1
        assert result["critical_alerts"][0]["type"] == "CROP_FAILURE"

    def test_debt_crisis_triggers(self):
        svc = get_service()
        data = safe_village()
        data["debt_to_income_ratio"] = 2.5  # Above 2.0 threshold
        result = svc.check_critical_thresholds(data)
        assert result["triggered_thresholds"] == 1
        assert result["critical_alerts"][0]["type"] == "DEBT_CRISIS"


class TestOneStrikeLogic:
    """One threshold breach → CRITICAL status."""

    def test_safe_village_no_alerts(self):
        svc = get_service()
        result = svc.check_critical_thresholds(safe_village())
        assert result["overall_status"] == "SAFE"
        assert result["triggered_thresholds"] == 0

    def test_single_critical_breach(self):
        svc = get_service()
        data = safe_village()
        data["rainfall_percentage"] = 30.0  # CRITICAL severity
        result = svc.check_critical_thresholds(data)
        assert result["overall_status"] == "CRITICAL"

    def test_single_high_breach_is_warning(self):
        svc = get_service()
        data = safe_village()
        data["avg_ndvi_decline"] = 35.0  # HIGH severity (crop failure)
        result = svc.check_critical_thresholds(data)
        assert result["overall_status"] == "WARNING"

    def test_multiple_breaches_still_critical(self):
        svc = get_service()
        data = safe_village()
        data["rainfall_percentage"] = 30.0
        data["water_access_percentage"] = 20.0
        data["debt_to_income_ratio"] = 3.0
        result = svc.check_critical_thresholds(data)
        assert result["overall_status"] == "CRITICAL"
        assert result["triggered_thresholds"] == 3

    def test_all_thresholds_breached(self):
        svc = get_service()
        data = {
            "rainfall_percentage": 20.0,
            "water_access_percentage": 10.0,
            "avg_health_expenditure": 20000,
            "avg_household_income": 5000,
            "avg_ndvi_decline": 50.0,
            "debt_to_income_ratio": 4.0,
            "total_population": 2000,
            "farmer_population": 600,
            "households_in_debt": 400,
        }
        result = svc.check_critical_thresholds(data)
        assert result["triggered_thresholds"] == 5
        assert result["overall_status"] == "CRITICAL"


class TestBoundaryValues:
    """Test exact threshold boundary values."""

    def test_rainfall_at_50_is_safe(self):
        svc = get_service()
        data = safe_village()
        data["rainfall_percentage"] = 50.0
        result = svc.check_critical_thresholds(data)
        assert all(a["type"] != "RAINFALL_FAILURE" for a in result["critical_alerts"])

    def test_rainfall_at_49_triggers(self):
        svc = get_service()
        data = safe_village()
        data["rainfall_percentage"] = 49.9
        result = svc.check_critical_thresholds(data)
        assert any(a["type"] == "RAINFALL_FAILURE" for a in result["critical_alerts"])

    def test_water_at_30_is_safe(self):
        svc = get_service()
        data = safe_village()
        data["water_access_percentage"] = 30.0
        result = svc.check_critical_thresholds(data)
        assert all(a["type"] != "WATER_CRISIS" for a in result["critical_alerts"])

    def test_debt_at_2_is_safe(self):
        svc = get_service()
        data = safe_village()
        data["debt_to_income_ratio"] = 2.0
        result = svc.check_critical_thresholds(data)
        assert all(a["type"] != "DEBT_CRISIS" for a in result["critical_alerts"])

    def test_debt_at_2_01_triggers(self):
        svc = get_service()
        data = safe_village()
        data["debt_to_income_ratio"] = 2.01
        result = svc.check_critical_thresholds(data)
        assert any(a["type"] == "DEBT_CRISIS" for a in result["critical_alerts"])

    def test_ndvi_at_30_is_safe(self):
        svc = get_service()
        data = safe_village()
        data["avg_ndvi_decline"] = 30.0
        result = svc.check_critical_thresholds(data)
        assert all(a["type"] != "CROP_FAILURE" for a in result["critical_alerts"])

    def test_health_equal_income_is_safe(self):
        """Health expenditure must EXCEED income, not equal."""
        svc = get_service()
        data = safe_village()
        data["avg_health_expenditure"] = 10000
        data["avg_household_income"] = 10000
        result = svc.check_critical_thresholds(data)
        assert all(a["type"] != "HEALTH_SHOCK" for a in result["critical_alerts"])


class TestAlertMetadata:
    """Test that alerts contain proper metadata."""

    def test_alert_has_recommended_action(self):
        svc = get_service()
        data = safe_village()
        data["rainfall_percentage"] = 30.0
        result = svc.check_critical_thresholds(data)
        alert = result["critical_alerts"][0]
        assert "recommended_action" in alert
        assert len(alert["recommended_action"]) > 0

    def test_alert_has_affected_population(self):
        svc = get_service()
        data = safe_village()
        data["rainfall_percentage"] = 30.0
        result = svc.check_critical_thresholds(data)
        alert = result["critical_alerts"][0]
        assert "affected_population" in alert
