"""
Crisis Alert Model
Maps to design doc: Crisis Alert Schema (Updated - Boolean Threshold Logic)
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON, ForeignKey
from database import Base


class CrisisAlert(Base):
    __tablename__ = "crisis_alerts"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    village_cluster_id = Column(String, ForeignKey("village_clusters.id"), nullable=False)

    # Alert data
    generated_at = Column(DateTime, default=datetime.utcnow)
    overall_status = Column(String, nullable=False)  # SAFE | WARNING | CRITICAL
    triggered_thresholds = Column(Integer, default=0)

    # Critical alerts (JSON array of threshold breaches)
    critical_alerts = Column(JSON, default=[])
    # Each entry: { type, severity, value, threshold, affectedPopulation, recommendedAction }

    # Vital signs snapshot at time of alert
    vital_signs = Column(JSON, default={})
    # { rainfallPercentage, waterAccessPercentage, avgHealthExpenditure, avgHouseholdIncome, avgNDVIDecline, debtToIncomeRatio }

    # Notification tracking
    notified_officials = Column(JSON, default=[])

    # Status
    status = Column(String, default="ACTIVE")  # ACTIVE | ACKNOWLEDGED | RESOLVED

    # Interventions
    interventions_taken = Column(JSON, default=[])
    # Each entry: { type, date, officialId, notes, budgetAllocated }

    resolution_date = Column(DateTime)
