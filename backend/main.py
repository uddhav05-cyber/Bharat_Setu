"""
Bharat-Setu Backend
FastAPI application entry point.
Free alternative to AWS Lambda + API Gateway.
"""
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import settings
from database import init_db, SessionLocal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def create_storage_dirs():
    """Create local storage directories (replaces S3 bucket creation)."""
    dirs = [
        settings.SATELLITE_STORAGE_PATH,
        settings.CERTIFICATE_STORAGE_PATH,
        settings.EVIDENCE_STORAGE_PATH,
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    logger.info("Storage directories created")


def seed_demo_data():
    """Seed database with demo data for pilot demonstration."""
    from models.user import User
    from models.farm_plot import FarmPlot
    from models.village_cluster import VillageCluster
    from auth.jwt_handler import hash_password

    db = SessionLocal()
    try:
        # Only seed if database is empty
        if db.query(User).count() > 0:
            logger.info("Database already seeded, skipping")
            return

        logger.info("Seeding demo data...")

        # Create demo users
        admin = User(
            id="admin-001",
            name="Admin User",
            phone="9000000001",
            password_hash=hash_password("admin123"),
            role="ADMIN",
            village="HQ",
            district="Pune",
            state="Maharashtra",
        )

        vle = User(
            id="vle-001",
            name="Ramesh Kumar",
            phone="9000000002",
            password_hash=hash_password("vle123"),
            role="VLE",
            village="Shivajinagar",
            district="Pune",
            state="Maharashtra",
            trust_score=75.0,
            commission_rate=7.0,
            account_status="ACTIVE",
        )

        farmer1 = User(
            id="farmer-001",
            name="Suresh Patil",
            phone="9000000003",
            password_hash=hash_password("farmer123"),
            role="FARMER",
            language="mr",
            village="Shivajinagar",
            district="Pune",
            state="Maharashtra",
        )

        farmer2 = User(
            id="farmer-002",
            name="Lakshmi Devi",
            phone="9000000004",
            password_hash=hash_password("farmer123"),
            role="FARMER",
            language="hi",
            village="Kothrud",
            district="Pune",
            state="Maharashtra",
        )

        sarpanch = User(
            id="sarpanch-001",
            name="Vijay Deshmukh",
            phone="9000000005",
            password_hash=hash_password("sarpanch123"),
            role="SARPANCH",
            village="Shivajinagar",
            district="Pune",
            state="Maharashtra",
        )

        official = User(
            id="official-001",
            name="Dr. Ananya Sharma",
            phone="9000000006",
            password_hash=hash_password("official123"),
            role="DISTRICT_OFFICIAL",
            district="Pune",
            state="Maharashtra",
        )

        db.add_all([admin, vle, farmer1, farmer2, sarpanch, official])
        db.flush()  # Flush users to DB so FK constraints are satisfied

        # Create demo farm plots
        farm1 = FarmPlot(
            id="farm-001",
            farmer_id="farmer-001",
            vle_id="vle-001",
            size_acres=1.5,
            crop_type="rice",
            village_id="village-001",
            geometry={
                "type": "Polygon",
                "coordinates": [[[73.85, 18.52], [73.86, 18.52], [73.86, 18.53], [73.85, 18.53], [73.85, 18.52]]],
            },
            centroid_lat=18.525,
            centroid_lon=73.855,
            bbox_min_lat=18.52,
            bbox_min_lon=73.85,
            bbox_max_lat=18.53,
            bbox_max_lon=73.86,
            status="ACTIVE",
            ndvi_history=[
                {"date": "2025-12-01T00:00:00", "value": 0.45, "satellite_source": "SENTINEL_2_OPTICAL"},
                {"date": "2026-01-01T00:00:00", "value": 0.52, "satellite_source": "SENTINEL_2_OPTICAL"},
                {"date": "2026-02-01T00:00:00", "value": 0.58, "satellite_source": "SENTINEL_1_SAR"},
            ],
            carbon_credits_total=1.2,
        )

        farm2 = FarmPlot(
            id="farm-002",
            farmer_id="farmer-002",
            vle_id="vle-001",
            size_acres=2.0,
            crop_type="wheat",
            village_id="village-002",
            geometry={
                "type": "Polygon",
                "coordinates": [[[73.80, 18.50], [73.82, 18.50], [73.82, 18.52], [73.80, 18.52], [73.80, 18.50]]],
            },
            centroid_lat=18.51,
            centroid_lon=73.81,
            bbox_min_lat=18.50,
            bbox_min_lon=73.80,
            bbox_max_lat=18.52,
            bbox_max_lon=73.82,
            status="ACTIVE",
            ndvi_history=[
                {"date": "2025-12-01T00:00:00", "value": 0.35, "satellite_source": "SENTINEL_2_OPTICAL"},
                {"date": "2026-01-01T00:00:00", "value": 0.40, "satellite_source": "SENTINEL_1_SAR"},
            ],
            carbon_credits_total=0.8,
        )

        db.add_all([farm1, farm2])

        # Create demo village clusters with vital signs
        cluster1 = VillageCluster(
            id="cluster-001",
            name="Shivajinagar Cluster",
            district="Pune",
            state="Maharashtra",
            villages=["village-001", "village-002"],
            centroid_lat=18.52,
            centroid_lon=73.85,
            total_farmers=45,
            total_vles=3,
            total_farm_plots=52,
            total_carbon_tons=28.5,
            average_ndvi=0.55,
            total_population=2500,
            farmer_population=800,
            households_in_debt=120,
            # Healthy vital signs
            rainfall_percentage=85.0,
            water_access_percentage=72.0,
            avg_health_expenditure=3500,
            avg_household_income=12000,
            avg_ndvi_decline=5.0,
            debt_to_income_ratio=0.8,
        )

        cluster2 = VillageCluster(
            id="cluster-002",
            name="Kothrud Cluster",
            district="Pune",
            state="Maharashtra",
            villages=["village-003", "village-004"],
            centroid_lat=18.50,
            centroid_lon=73.80,
            total_farmers=32,
            total_vles=2,
            total_farm_plots=38,
            total_carbon_tons=15.2,
            average_ndvi=0.38,
            total_population=1800,
            farmer_population=600,
            households_in_debt=280,
            # CRISIS vital signs (water crisis + debt crisis)
            rainfall_percentage=42.0,  # Below 50% threshold!
            water_access_percentage=25.0,  # Below 30% threshold!
            avg_health_expenditure=8000,
            avg_household_income=9000,
            avg_ndvi_decline=35.0,  # Above 30% threshold!
            debt_to_income_ratio=2.5,  # Above 2.0 threshold!
        )

        cluster3 = VillageCluster(
            id="cluster-003",
            name="Hadapsar Cluster",
            district="Pune",
            state="Maharashtra",
            villages=["village-005"],
            centroid_lat=18.48,
            centroid_lon=73.93,
            total_farmers=28,
            total_vles=2,
            total_farm_plots=30,
            total_carbon_tons=10.0,
            average_ndvi=0.48,
            total_population=1500,
            farmer_population=500,
            households_in_debt=80,
            # Warning vital signs
            rainfall_percentage=55.0,
            water_access_percentage=45.0,
            avg_health_expenditure=5000,
            avg_household_income=10000,
            avg_ndvi_decline=15.0,
            debt_to_income_ratio=1.2,
        )

        db.add_all([cluster1, cluster2, cluster3])
        db.commit()
        logger.info("Demo data seeded successfully!")

    except Exception as e:
        logger.error(f"Error seeding demo data: {e}")
        db.rollback()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION} ({settings.ENVIRONMENT})")
    init_db()
    create_storage_dirs()
    seed_demo_data()
    logger.info("Application ready!")
    yield
    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Bharat-Setu: Unified Rural Intelligence Platform. "
        "Carbon-Kosh | Gram-Twin | Migration-Shield. "
        "Built with free/open-source alternatives to AWS."
    ),
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
from routers import auth, farms, verification, alerts, dashboard, voice, certificates, twin

app.include_router(auth.router)
app.include_router(farms.router)
app.include_router(verification.router)
app.include_router(alerts.router)
app.include_router(dashboard.router)
app.include_router(voice.router)
app.include_router(certificates.router)
app.include_router(twin.router)


@app.get("/", tags=["Root"])
def root():
    """Root endpoint with platform info."""
    return {
        "platform": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "modules": {
            "carbon_kosh": "Active - Satellite-verified carbon credits",
            "gram_twin": "Active - Digital twin ecological planning",
            "migration_shield": "Active - Boolean threshold crisis detection",
        },
        "docs": "/docs",
        "status": "operational",
    }


@app.get("/health", tags=["Root"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": __import__("datetime").datetime.utcnow().isoformat()}
