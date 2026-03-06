"""
Certificate Service
Generates GCP-compliant service payment certificates as PDF documents.
Uses ReportLab for PDF generation (free alternative to Bedrock + S3).
"""
import os
import uuid
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from config import settings
from models.certificate import Certificate
from models.verification import Verification
from models.farm_plot import FarmPlot
from models.user import User
from adapters.payment_adapter import payment_gateway

logger = logging.getLogger(__name__)


class CertificateService:
    """Generates GCP-compliant service payment certificates."""

    async def generate_certificate(
        self,
        db: Session,
        verification_id: str,
        payment_source: str = "CSR",
    ) -> dict:
        """
        Generate a certificate after a successful verification.
        Links verification → certificate → payment.
        """
        # 1. Load verification
        verification = (
            db.query(Verification)
            .filter(Verification.id == verification_id)
            .first()
        )
        if not verification:
            return {"error": "Verification not found"}

        if verification.traffic_light_status != "GREEN":
            return {"error": f"Cannot issue certificate for {verification.traffic_light_status} status"}

        # 2. Load related entities
        farm = db.query(FarmPlot).filter(FarmPlot.id == verification.farm_plot_id).first()
        farmer = db.query(User).filter(User.id == farm.farmer_id).first() if farm else None
        vle = db.query(User).filter(User.id == verification.vle_id).first() if verification.vle_id else None

        if not farm or not farmer:
            return {"error": "Farm or farmer not found"}

        # 3. Process payment via adapter
        carbon_tons = verification.carbon_sequestration_tons or 0
        amount = carbon_tons * 500  # ₹500 per ton fixed service payment
        payment_info = None

        try:
            payment = await payment_gateway.issue_voucher(
                farmer_id=farmer.id,
                verification_id=verification_id,
                carbon_tons=carbon_tons,
                payment_source=payment_source,
                amount=amount,
            )
            payment_info = payment.to_dict()
        except Exception as e:
            logger.error(f"Payment processing failed: {e}")

        # 4. Create certificate record
        cert = Certificate(
            farmer_id=farmer.id,
            farm_plot_id=farm.id,
            verification_id=verification_id,
            vle_id=verification.vle_id,
            carbon_tons=carbon_tons,
            verification_start_date=verification.requested_at,
            verification_end_date=verification.completed_at,
            expires_at=datetime.utcnow() + timedelta(days=365),
            payment_type=payment_info["payment_type"] if payment_info else None,
            payment_source=payment_source,
            fixed_service_payment=amount,
            voucher_code=payment_info.get("voucher_code") if payment_info else None,
            pfms_batch_id=payment_info.get("pfms_batch_id") if payment_info else None,
            traffic_light_status=verification.traffic_light_status,
            traffic_light_variance=verification.variance,
            satellite_confidence=verification.confidence_score,
            vle_commission_status=verification.commission_status,
            audit_trail=[
                {
                    "event": "CERTIFICATE_GENERATED",
                    "timestamp": datetime.utcnow().isoformat(),
                    "verification_id": verification_id,
                },
                {
                    "event": "PAYMENT_INITIATED",
                    "timestamp": datetime.utcnow().isoformat(),
                    "payment_id": payment_info["payment_id"] if payment_info else None,
                },
            ],
        )

        db.add(cert)
        db.commit()
        db.refresh(cert)

        # 5. Generate PDF
        pdf_path = self._generate_pdf(cert, farmer, farm, vle, verification, payment_info)
        cert.file_path = pdf_path
        cert.download_url = f"/certificates/{cert.id}/download"
        db.commit()

        return {
            "certificate_id": cert.id,
            "file_path": pdf_path,
            "download_url": cert.download_url,
            "carbon_tons": carbon_tons,
            "payment": payment_info,
            "status": cert.status,
        }

    def _generate_pdf(
        self, cert, farmer, farm, vle, verification, payment_info
    ) -> str:
        """Generate a GCP-compliant PDF certificate."""
        # Ensure directory exists
        cert_dir = settings.CERTIFICATE_STORAGE_PATH
        os.makedirs(cert_dir, exist_ok=True)
        pdf_path = os.path.join(cert_dir, f"{cert.id}.pdf")

        doc = SimpleDocTemplate(
            pdf_path, pagesize=A4,
            topMargin=20 * mm, bottomMargin=20 * mm,
            leftMargin=20 * mm, rightMargin=20 * mm,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CertTitle", parent=styles["Title"],
            fontSize=16, textColor=HexColor("#1a5276"),
            spaceAfter=6 * mm,
        )
        heading_style = ParagraphStyle(
            "CertHeading", parent=styles["Heading2"],
            fontSize=12, textColor=HexColor("#2e7d32"),
            spaceBefore=4 * mm, spaceAfter=2 * mm,
        )
        body_style = styles["Normal"]

        elements = []

        # Header
        elements.append(Paragraph(
            "Green Credit Programme (GCP)<br/>Service Payment Certificate",
            title_style,
        ))
        elements.append(Paragraph(
            f"Certificate ID: {cert.id}", body_style
        ))
        elements.append(Paragraph(
            f"Issued: {cert.issued_at.strftime('%d %B %Y') if cert.issued_at else 'N/A'}", body_style
        ))
        elements.append(HRFlowable(width="100%", thickness=1, color=HexColor("#2e7d32")))
        elements.append(Spacer(1, 4 * mm))

        # Farmer Details
        elements.append(Paragraph("Farmer Details", heading_style))
        farmer_data = [
            ["Name", farmer.name],
            ["Phone", farmer.phone],
            ["Village", farmer.village or "N/A"],
            ["District", farmer.district or "N/A"],
        ]
        elements.append(self._make_table(farmer_data))
        elements.append(Spacer(1, 3 * mm))

        # VLE Details
        if vle:
            elements.append(Paragraph("VLE Details", heading_style))
            vle_data = [
                ["Name", vle.name],
                ["Trust Score", f"{vle.trust_score:.1f}%"],
                ["Commission Status", cert.vle_commission_status or "N/A"],
            ]
            elements.append(self._make_table(vle_data))
            elements.append(Spacer(1, 3 * mm))

        # Plot Details
        elements.append(Paragraph("Plot Details", heading_style))
        plot_data = [
            ["Size", f"{farm.size_acres} acres"],
            ["Crop Type", farm.crop_type],
            ["Location", f"{farm.centroid_lat:.4f}°N, {farm.centroid_lon:.4f}°E" if farm.centroid_lat else "N/A"],
        ]
        elements.append(self._make_table(plot_data))
        elements.append(Spacer(1, 3 * mm))

        # Verification Details
        elements.append(Paragraph("Verification Details", heading_style))
        verify_data = [
            ["Satellite Source", verification.satellite_source or "N/A"],
            ["Biomass Score", f"{verification.biomass_score:.3f}" if verification.biomass_score else "N/A"],
            ["Carbon Sequestration", f"{cert.carbon_tons:.3f} tons CO₂"],
            ["Traffic Light", cert.traffic_light_status or "N/A"],
            ["Variance", f"{cert.traffic_light_variance:.1f}%" if cert.traffic_light_variance else "N/A"],
            ["Confidence", f"{cert.satellite_confidence:.1f}%" if cert.satellite_confidence else "N/A"],
        ]
        elements.append(self._make_table(verify_data))
        elements.append(Spacer(1, 3 * mm))

        # Payment Details
        elements.append(Paragraph("Payment Details", heading_style))
        payment_data = [
            ["Payment Type", cert.payment_type or "N/A"],
            ["Amount", f"₹{cert.fixed_service_payment:.2f}" if cert.fixed_service_payment else "N/A"],
            ["Voucher Code", cert.voucher_code or "N/A"],
            ["Purpose", cert.purpose_code or "AGRI_INPUT"],
        ]
        elements.append(self._make_table(payment_data))
        elements.append(Spacer(1, 6 * mm))

        # Compliance Footer
        elements.append(HRFlowable(width="100%", thickness=1, color=HexColor("#2e7d32")))
        elements.append(Paragraph(
            f"Standard: {cert.compliance_standard}", body_style
        ))
        elements.append(Paragraph(
            f"Methodology: {cert.compliance_methodology}", body_style
        ))
        elements.append(Paragraph(
            f"Verification: {cert.verification_body}", body_style
        ))

        doc.build(elements)
        logger.info(f"Certificate PDF generated: {pdf_path}")
        return pdf_path

    def _make_table(self, data):
        """Create a styled table for certificate sections."""
        table = Table(data, colWidths=[120, 300])
        table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("TEXTCOLOR", (0, 0), (0, -1), HexColor("#555555")),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
        ]))
        return table

    def get_certificate(self, db: Session, cert_id: str) -> Certificate | None:
        """Get a certificate by ID."""
        return db.query(Certificate).filter(Certificate.id == cert_id).first()

    def list_certificates(
        self, db: Session, farmer_id: str = None, skip: int = 0, limit: int = 50
    ) -> list:
        """List certificates, optionally filtered by farmer."""
        query = db.query(Certificate)
        if farmer_id:
            query = query.filter(Certificate.farmer_id == farmer_id)
        return query.order_by(Certificate.issued_at.desc()).offset(skip).limit(limit).all()


certificate_service = CertificateService()
