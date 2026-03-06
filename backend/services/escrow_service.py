"""
Escrow & Settlement Service
Wraps the payment adapter with certificate creation and payment tracking.
Links: Verification → Certificate → Payment.
"""
import logging
from sqlalchemy.orm import Session
from services.certificate_service import certificate_service
from adapters.payment_adapter import payment_gateway

logger = logging.getLogger(__name__)


class EscrowService:
    """
    Escrow & Settlement Engine (Component 11 from design doc).
    Coordinates certificate generation and payment processing.
    """

    async def process_settlement(
        self,
        db: Session,
        verification_id: str,
        payment_source: str = "CSR",
    ) -> dict:
        """
        Full settlement flow:
        1. Generate certificate
        2. Certificate includes payment processing via adapter
        3. Return combined result
        """
        result = await certificate_service.generate_certificate(
            db=db,
            verification_id=verification_id,
            payment_source=payment_source,
        )

        if "error" in result:
            logger.warning(f"Settlement failed: {result['error']}")
            return result

        logger.info(
            f"Settlement completed: cert={result['certificate_id']}, "
            f"carbon={result['carbon_tons']:.3f}t"
        )
        return result

    async def check_payment_status(self, payment_id: str) -> dict:
        """Check the status of a payment via the adapter."""
        return await payment_gateway.check_status(payment_id)


escrow_service = EscrowService()
