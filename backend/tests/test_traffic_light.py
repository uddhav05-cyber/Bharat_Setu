"""
Traffic Light Service Tests
Tests variance calculation, GREEN/YELLOW/RED status, trust score updates,
commission status, and account suspension logic.
"""
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.traffic_light_service import TrafficLightService


def get_service():
    return TrafficLightService()


class TestVarianceCalculation:
    """Tests for variance calculation edge cases."""

    def test_zero_variance(self):
        svc = get_service()
        assert svc.calculate_variance(0.5, 0.5) == 0.0

    def test_positive_variance(self):
        svc = get_service()
        result = svc.calculate_variance(0.7, 0.5)
        assert abs(result - 40.0) < 0.01  # |0.7-0.5|/0.5 * 100 = 40%

    def test_negative_variance_same_magnitude(self):
        svc = get_service()
        result = svc.calculate_variance(0.3, 0.5)
        assert abs(result - 40.0) < 0.01  # |0.3-0.5|/0.5 * 100 = 40%

    def test_zero_satellite_biomass(self):
        """When satellite shows no biomass, any VLE claim is suspicious (100%)."""
        svc = get_service()
        assert svc.calculate_variance(0.5, 0.0) == 100.0

    def test_variance_capped_at_100(self):
        svc = get_service()
        result = svc.calculate_variance(10.0, 0.1)
        assert result == 100.0

    def test_small_variance(self):
        svc = get_service()
        result = svc.calculate_variance(0.48, 0.5)
        assert abs(result - 4.0) < 0.01  # 4% variance


class TestStatusDetermination:
    """Tests for GREEN/YELLOW/RED status assignment."""

    def test_green_low_variance_high_confidence(self):
        svc = get_service()
        status, action, _ = svc.determine_status(5.0, 90.0)
        assert status == "GREEN"
        assert action == "AUTO_APPROVE"

    def test_yellow_moderate_variance(self):
        svc = get_service()
        status, action, _ = svc.determine_status(20.0, 90.0)
        assert status == "YELLOW"
        assert action == "FLAG_FOR_CALL"

    def test_red_high_variance(self):
        svc = get_service()
        status, action, _ = svc.determine_status(40.0, 90.0)
        assert status == "RED"
        assert action == "FREEZE_ACCOUNT"

    def test_yellow_low_confidence_overrides_green(self):
        """Low confidence should force YELLOW even with low variance."""
        svc = get_service()
        status, action, _ = svc.determine_status(5.0, 70.0)
        assert status == "YELLOW"
        assert action == "FLAG_FOR_CALL"

    def test_boundary_10_percent(self):
        """At exactly 10%, status should be YELLOW."""
        svc = get_service()
        status, _, _ = svc.determine_status(10.0, 90.0)
        assert status == "YELLOW"

    def test_boundary_30_percent(self):
        """At exactly 30%, status should be YELLOW."""
        svc = get_service()
        status, _, _ = svc.determine_status(30.0, 90.0)
        assert status == "YELLOW"

    def test_just_above_30(self):
        """Just above 30% should be RED."""
        svc = get_service()
        status, _, _ = svc.determine_status(30.1, 90.0)
        assert status == "RED"

    def test_boundary_confidence_80(self):
        """At exactly 80 confidence, should NOT force YELLOW."""
        svc = get_service()
        status, _, _ = svc.determine_status(5.0, 80.0)
        assert status == "GREEN"


class TestTrustScoreUpdates:
    """Tests for VLE trust score +2/-15 updates."""

    def test_green_adds_2(self):
        svc = get_service()
        assert svc.update_trust_score(50.0, "GREEN") == 52.0

    def test_yellow_no_change(self):
        svc = get_service()
        assert svc.update_trust_score(50.0, "YELLOW") == 50.0

    def test_red_subtracts_15(self):
        svc = get_service()
        assert svc.update_trust_score(50.0, "RED") == 35.0

    def test_green_capped_at_100(self):
        svc = get_service()
        assert svc.update_trust_score(99.0, "GREEN") == 100.0

    def test_red_floored_at_0(self):
        svc = get_service()
        assert svc.update_trust_score(10.0, "RED") == 0.0

    def test_red_does_not_go_negative(self):
        svc = get_service()
        assert svc.update_trust_score(5.0, "RED") == 0.0


class TestCommissionStatus:
    """Tests for commission approval logic."""

    def test_red_always_forfeited(self):
        svc = get_service()
        assert svc.determine_commission_status("RED", 90, 80) == "FORFEITED"

    def test_green_high_confidence_high_trust_approved(self):
        svc = get_service()
        assert svc.determine_commission_status("GREEN", 90, 80) == "APPROVED"

    def test_green_low_confidence_held(self):
        svc = get_service()
        assert svc.determine_commission_status("GREEN", 70, 80) == "HELD"

    def test_green_low_trust_held(self):
        svc = get_service()
        assert svc.determine_commission_status("GREEN", 90, 30) == "HELD"

    def test_yellow_always_held(self):
        svc = get_service()
        assert svc.determine_commission_status("YELLOW", 90, 80) == "HELD"


class TestAccountSuspension:
    """Tests for VLE account suspension threshold."""

    def test_trust_below_40_suspended(self):
        svc = get_service()
        assert svc.check_account_suspension(39.0) is True

    def test_trust_at_40_not_suspended(self):
        svc = get_service()
        assert svc.check_account_suspension(40.0) is False

    def test_trust_above_40_not_suspended(self):
        svc = get_service()
        assert svc.check_account_suspension(80.0) is False
