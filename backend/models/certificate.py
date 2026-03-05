"""
Service Payment Certificate Model
Maps to design doc: Service Payment Certificate Schema (Updated - Not Tradeable)
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, DateTime, JSON, ForeignKey
from database import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    farmer_id = Column(String, ForeignKey("users.id"), nullable=False)
    farm_plot_id = Column(String, ForeignKey("farm_plots.id"), nullable=False)
    verification_id = Column(String, ForeignKey("verifications.id"), nullable=False)
    vle_id = Column(String, ForeignKey("users.id"))

    # Certificate data
    issued_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    carbon_tons = Column(Float, nullable=False)

    # Verification period
    verification_start_date = Column(DateTime)
    verification_end_date = Column(DateTime)

    # Compliance
    compliance_standard = Column(String, default="GCP (Green Credit Programme - MoEFCC)")
    compliance_methodology = Column(String, default="Domestic Green Credit Rules 2023")
    verification_body = Column(String, default="Satellite + Ground Truth Hybrid")

    # Storage
    file_path = Column(String)  # Local path (replaces S3 key)
    download_url = Column(String)

    # Status
    status = Column(String, default="ACTIVE")  # ACTIVE | EXPIRED | REVOKED

    # Payment Info
    payment_type = Column(String)  # E_RUPI_VOUCHER | PFMS_DBT
    payment_source = Column(String)  # CSR | GOVERNMENT_GRANT
    fixed_service_payment = Column(Float)  # INR
    voucher_code = Column(String)
    pfms_batch_id = Column(String)
    redemption_status = Column(String, default="PENDING")  # PENDING | REDEEMED | EXPIRED
    redemption_date = Column(DateTime)
    purpose_code = Column(String, default="AGRI_INPUT")

    # Traffic Light Verification
    traffic_light_status = Column(String)  # GREEN | YELLOW | RED
    traffic_light_variance = Column(Float)
    satellite_confidence = Column(Float)
    vle_commission_status = Column(String)  # APPROVED | HELD | FORFEITED

    # Audit Trail
    audit_trail = Column(JSON, default=[])
