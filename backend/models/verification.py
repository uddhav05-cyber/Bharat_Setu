"""
Verification Model
Maps to design doc: Carbon Verification + Traffic Light protocol.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, ForeignKey
from database import Base


class Verification(Base):
    __tablename__ = "verifications"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    farm_plot_id = Column(String, ForeignKey("farm_plots.id"), nullable=False)
    vle_id = Column(String, ForeignKey("users.id"))

    # Satellite data
    satellite_source = Column(String)  # SENTINEL_2_OPTICAL | SENTINEL_1_SAR
    s3_tile_keys = Column(JSON, default=[])  # Local file paths (S3 replacement)

    # Biomass results
    biomass_score = Column(Float)  # 0 to 1 (normalized)
    biomass_baseline = Column(Float)
    biomass_change = Column(Float)
    carbon_sequestration_tons = Column(Float)
    confidence_score = Column(Float)  # 0-100

    # Traffic Light Protocol
    traffic_light_status = Column(String)  # GREEN | YELLOW | RED
    variance = Column(Float)  # Percentage difference VLE vs satellite
    vle_estimated_biomass = Column(Float)  # VLE's visual assessment

    # VLE Data
    vle_gps_polygon = Column(JSON)  # GPS polygon from VLE
    vle_photos = Column(JSON, default=[])  # Evidence photo paths

    # Status
    verification_status = Column(String, default="PENDING")  # PENDING | APPROVED | REJECTED | NEEDS_REVIEW
    action = Column(String)  # AUTO_APPROVE | FLAG_FOR_CALL | FREEZE_ACCOUNT
    reasoning = Column(String)

    # Commission
    commission_status = Column(String, default="HELD")  # APPROVED | HELD | FORFEITED
    commission_amount = Column(Float, default=0.0)

    # Trust score update applied
    trust_score_update = Column(Float, default=0.0)

    # Timestamps
    requested_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    cloud_cover = Column(Float)  # For satellite source selection
