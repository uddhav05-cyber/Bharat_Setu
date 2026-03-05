"""
Payment Adapter (Mock)
Configurable Adapter Pattern from design doc (Component 11).
Mock e-RUPI and PFMS-DBT for pilot; hot-swappable to live APIs.
"""
import uuid
import random
import string
from datetime import datetime, timedelta
from typing import Optional
from config import settings


class PaymentResponse:
    def __init__(self, payment_id, payment_type, voucher_code=None,
                 pfms_batch_id=None, redemption_instructions="",
                 expiry_date="", audit_trail=None):
        self.payment_id = payment_id
        self.payment_type = payment_type
        self.voucher_code = voucher_code
        self.pfms_batch_id = pfms_batch_id
        self.redemption_instructions = redemption_instructions
        self.expiry_date = expiry_date
        self.audit_trail = audit_trail or {}

    def to_dict(self):
        return {
            "payment_id": self.payment_id,
            "payment_type": self.payment_type,
            "voucher_code": self.voucher_code,
            "pfms_batch_id": self.pfms_batch_id,
            "redemption_instructions": self.redemption_instructions,
            "expiry_date": self.expiry_date,
            "audit_trail": self.audit_trail,
        }


class IPaymentGateway:
    """Interface for payment adapters."""

    async def issue_voucher(self, farmer_id: str, verification_id: str,
                            carbon_tons: float, payment_source: str,
                            amount: float) -> PaymentResponse:
        raise NotImplementedError

    async def check_status(self, payment_id: str) -> dict:
        raise NotImplementedError


class MockPaymentAdapter(IPaymentGateway):
    """Mock adapter for demos and testing (pilot phase)."""

    async def issue_voucher(self, farmer_id: str, verification_id: str,
                            carbon_tons: float, payment_source: str,
                            amount: float) -> PaymentResponse:
        voucher_code = "DEMO-" + "".join(
            random.choices(string.ascii_uppercase + string.digits, k=9)
        )
        expiry = (datetime.utcnow() + timedelta(days=90)).isoformat()

        if payment_source == "CSR":
            return PaymentResponse(
                payment_id=f"MOCK-ERUPI-{uuid.uuid4().hex[:8]}",
                payment_type="E_RUPI_VOUCHER",
                voucher_code=voucher_code,
                redemption_instructions="Demo voucher - redeem at authorized agricultural input dealers",
                expiry_date=expiry,
                audit_trail={
                    "source": "CSR",
                    "amount": amount,
                    "purpose_code": "AGRI_INPUT",
                    "timestamp": datetime.utcnow().isoformat(),
                    "carbon_tons": carbon_tons,
                },
            )
        else:
            batch_id = f"MOCK-PFMS-{uuid.uuid4().hex[:8]}"
            return PaymentResponse(
                payment_id=batch_id,
                payment_type="PFMS_DBT",
                pfms_batch_id=batch_id,
                redemption_instructions="Demo - Direct Benefit Transfer to registered bank account",
                expiry_date=expiry,
                audit_trail={
                    "source": "GOVERNMENT_GRANT",
                    "amount": amount,
                    "purpose_code": "VB_GRAM_G",
                    "timestamp": datetime.utcnow().isoformat(),
                    "carbon_tons": carbon_tons,
                },
            )

    async def check_status(self, payment_id: str) -> dict:
        return {"status": "PENDING", "message": "Mock payment in demo mode"}


class LivePaymentAdapter(IPaymentGateway):
    """Placeholder for production with API Setu / NPCI."""

    async def issue_voucher(self, farmer_id: str, verification_id: str,
                            carbon_tons: float, payment_source: str,
                            amount: float) -> PaymentResponse:
        # TODO: Implement live API Setu integration
        raise NotImplementedError("Live payment adapter requires API Setu credentials")

    async def check_status(self, payment_id: str) -> dict:
        raise NotImplementedError("Live payment adapter requires API Setu credentials")


def create_payment_gateway() -> IPaymentGateway:
    """Factory: select adapter based on environment."""
    if settings.PAYMENT_ADAPTER == "LIVE":
        return LivePaymentAdapter()
    return MockPaymentAdapter()


payment_gateway = create_payment_gateway()
