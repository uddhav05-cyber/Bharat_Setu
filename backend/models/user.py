"""
User & VLE Profile Models
Maps to design doc: User Schema (Updated for VLE Support)
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, Enum, JSON
from database import Base
import enum


class UserRole(str, enum.Enum):
    FARMER = "FARMER"
    VLE = "VLE"
    SARPANCH = "SARPANCH"
    DISTRICT_OFFICIAL = "DISTRICT_OFFICIAL"
    ADMIN = "ADMIN"


class VLEAccountStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    TRAINING_REQUIRED = "TRAINING_REQUIRED"


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    role = Column(String, nullable=False)

    # Profile
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    language = Column(String, default="hi")  # hi | mr | ta
    village = Column(String)
    district = Column(String)
    state = Column(String)

    # Auth
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

    # Preferences
    voice_speed = Column(Float, default=1.0)
    notification_channels = Column(JSON, default=["SMS"])

    # VLE Profile (only populated for VLE role)
    trust_score = Column(Float, default=50.0)
    total_verifications = Column(Integer, default=0)
    successful_verifications = Column(Integer, default=0)
    fraud_detections = Column(Integer, default=0)
    account_status = Column(String, default="ACTIVE")
    commission_rate = Column(Float, default=5.0)  # 5-12%
    pending_commission = Column(Float, default=0.0)
    total_earnings = Column(Float, default=0.0)
    last_audit_date = Column(DateTime)
