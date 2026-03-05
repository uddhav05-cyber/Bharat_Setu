"""
Farm Plot Model (GeoJSON-compatible)
Maps to design doc: FarmPlot Schema
Uses JSON columns for geometry since SQLite doesn't have PostGIS.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, ForeignKey
from database import Base


class FarmPlot(Base):
    __tablename__ = "farm_plots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    farmer_id = Column(String, ForeignKey("users.id"), nullable=False)
    vle_id = Column(String, ForeignKey("users.id"))  # VLE who registered

    # Geometry (stored as JSON since we use SQLite instead of PostGIS)
    geometry = Column(JSON, nullable=False)  # GeoJSON Polygon
    centroid_lat = Column(Float)  # For quick spatial queries
    centroid_lon = Column(Float)

    # Properties
    size_acres = Column(Float, nullable=False)
    crop_type = Column(String, nullable=False)
    village_id = Column(String)
    registration_date = Column(DateTime, default=datetime.utcnow)
    last_verification_date = Column(DateTime)

    # NDVI History (stored as JSON array)
    ndvi_history = Column(JSON, default=[])

    # Carbon tracking
    carbon_credits_total = Column(Float, default=0.0)
    status = Column(String, default="PENDING_VERIFICATION")  # ACTIVE | INACTIVE | PENDING_VERIFICATION

    # Bounding box for satellite queries
    bbox_min_lat = Column(Float)
    bbox_min_lon = Column(Float)
    bbox_max_lat = Column(Float)
    bbox_max_lon = Column(Float)
