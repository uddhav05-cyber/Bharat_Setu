"""
Village Cluster Model
Maps to design doc: VillageCluster Schema (Updated for Frugal Edge)
Includes vital signs for Boolean threshold crisis detection.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from database import Base


class VillageCluster(Base):
    __tablename__ = "village_clusters"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)

    # Villages in cluster
    villages = Column(JSON, default=[])  # List of village IDs/names

    # Geometry (simplified bounding box, not MultiPolygon)
    centroid_lat = Column(Float)
    centroid_lon = Column(Float)
    geometry = Column(JSON)  # GeoJSON MultiPolygon

    # Statistics
    total_farmers = Column(Integer, default=0)
    total_vles = Column(Integer, default=0)
    total_farm_plots = Column(Integer, default=0)
    total_carbon_tons = Column(Float, default=0.0)
    average_ndvi = Column(Float, default=0.0)
    critical_alerts_active = Column(Integer, default=0)

    # Cost Tracking (per design: $2.50/village/month budget)
    monthly_budget = Column(Float, default=2.50)
    current_month_spend = Column(Float, default=0.0)
    cost_breakdown = Column(JSON, default={})

    # Vital Signs (for Boolean Threshold checks)
    rainfall_percentage = Column(Float, default=100.0)
    water_access_percentage = Column(Float, default=100.0)
    avg_health_expenditure = Column(Float, default=0.0)
    avg_household_income = Column(Float, default=10000.0)
    avg_ndvi_decline = Column(Float, default=0.0)
    debt_to_income_ratio = Column(Float, default=0.0)
    vital_signs_last_updated = Column(DateTime, default=datetime.utcnow)

    # Population
    total_population = Column(Integer, default=0)
    farmer_population = Column(Integer, default=0)
    households_in_debt = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
