"""
Escrow & Payment Adapter Tests
Tests mock payment adapter voucher generation, audit trail, and routing.
"""
import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adapters.payment_adapter import MockPaymentAdapter, create_payment_gateway


def run_async(coro):
    """Helper to run async functions in tests."""
    return asyncio.get_event_loop().run_until_complete(coro)


class TestMockPaymentAdapter:
    """Tests for the mock payment adapter."""

    def setup_method(self):
        self.adapter = MockPaymentAdapter()

    def test_csr_payment_type(self):
        result = run_async(self.adapter.issue_voucher(
            farmer_id="f1", verification_id="v1",
            carbon_tons=1.0, payment_source="CSR", amount=500,
        ))
        assert result.payment_type == "E_RUPI_VOUCHER"

    def test_government_payment_type(self):
        result = run_async(self.adapter.issue_voucher(
            farmer_id="f1", verification_id="v1",
            carbon_tons=1.0, payment_source="GOVERNMENT_GRANT", amount=500,
        ))
        assert result.payment_type == "PFMS_DBT"

    def test_voucher_code_generated(self):
        result = run_async(self.adapter.issue_voucher(
            farmer_id="f1", verification_id="v1",
            carbon_tons=1.0, payment_source="CSR", amount=500,
        ))
        assert result.voucher_code is not None
        assert result.voucher_code.startswith("DEMO-")

    def test_pfms_batch_id_generated(self):
        result = run_async(self.adapter.issue_voucher(
            farmer_id="f1", verification_id="v1",
            carbon_tons=1.0, payment_source="GOVERNMENT_GRANT", amount=500,
        ))
        assert result.pfms_batch_id is not None
        assert result.pfms_batch_id.startswith("MOCK-PFMS-")

    def test_payment_id_format(self):
        result = run_async(self.adapter.issue_voucher(
            farmer_id="f1", verification_id="v1",
            carbon_tons=1.0, payment_source="CSR", amount=500,
        ))
        assert result.payment_id.startswith("MOCK-ERUPI-")

    def test_audit_trail_present(self):
        result = run_async(self.adapter.issue_voucher(
            farmer_id="f1", verification_id="v1",
            carbon_tons=2.5, payment_source="CSR", amount=1250,
        ))
        trail = result.audit_trail
        assert trail["source"] == "CSR"
        assert trail["amount"] == 1250
        assert trail["purpose_code"] == "AGRI_INPUT"
        assert trail["carbon_tons"] == 2.5
        assert "timestamp" in trail

    def test_government_audit_trail(self):
        result = run_async(self.adapter.issue_voucher(
            farmer_id="f1", verification_id="v1",
            carbon_tons=1.0, payment_source="GOVERNMENT_GRANT", amount=500,
        ))
        trail = result.audit_trail
        assert trail["source"] == "GOVERNMENT_GRANT"
        assert trail["purpose_code"] == "VB_GRAM_G"

    def test_expiry_date_present(self):
        result = run_async(self.adapter.issue_voucher(
            farmer_id="f1", verification_id="v1",
            carbon_tons=1.0, payment_source="CSR", amount=500,
        ))
        assert result.expiry_date is not None
        assert len(result.expiry_date) > 0

    def test_to_dict_method(self):
        result = run_async(self.adapter.issue_voucher(
            farmer_id="f1", verification_id="v1",
            carbon_tons=1.0, payment_source="CSR", amount=500,
        ))
        d = result.to_dict()
        assert isinstance(d, dict)
        assert "payment_id" in d
        assert "payment_type" in d
        assert "voucher_code" in d
        assert "audit_trail" in d

    def test_check_status_returns_pending(self):
        result = run_async(self.adapter.check_status("any-id"))
        assert result["status"] == "PENDING"

    def test_unique_payment_ids(self):
        """Each payment should have a unique ID."""
        ids = set()
        for _ in range(10):
            result = run_async(self.adapter.issue_voucher(
                farmer_id="f1", verification_id="v1",
                carbon_tons=1.0, payment_source="CSR", amount=500,
            ))
            ids.add(result.payment_id)
        assert len(ids) == 10


class TestPaymentFactory:
    """Tests for the payment gateway factory."""

    def test_default_is_mock(self):
        gateway = create_payment_gateway()
        assert isinstance(gateway, MockPaymentAdapter)
