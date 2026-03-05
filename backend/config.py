"""
Bharat-Setu Configuration
Free/Open-Source alternative to AWS-based config.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Bharat-Setu"
    APP_VERSION: str = "1.0.0-pilot"
    ENVIRONMENT: str = "PILOT"  # PILOT | PRODUCTION
    DEBUG: bool = True

    # Database (SQLite - free alternative to Aurora PostgreSQL)
    DATABASE_URL: str = "sqlite:///./bharat_setu.db"

    # Auth (PyJWT - free alternative to AWS Cognito)
    SECRET_KEY: str = "bharat-setu-pilot-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Storage (Local filesystem - free alternative to S3)
    STORAGE_BASE_PATH: str = "./storage"
    SATELLITE_STORAGE_PATH: str = "./storage/satellite"
    CERTIFICATE_STORAGE_PATH: str = "./storage/certificates"
    EVIDENCE_STORAGE_PATH: str = "./storage/evidence"

    # Payment Adapters (Mock for pilot)
    PAYMENT_ADAPTER: str = "MOCK"  # MOCK | LIVE
    PM_KISAN_ADAPTER: str = "MOCK"
    E_NAM_ADAPTER: str = "MOCK"

    # External API Keys (not needed for pilot with mocks)
    BHASHINI_API_KEY: Optional[str] = None
    MAPMYINDIA_API_KEY: Optional[str] = None
    NPCI_API_KEY: Optional[str] = None

    # Cost Tracking
    MONTHLY_BUDGET_PER_VILLAGE: float = 2.50  # USD

    # Frugal Edge Settings
    VOSK_CONFIDENCE_THRESHOLD: float = 0.80
    SATELLITE_CACHE_DAYS: int = 30
    MAP_TILE_CACHE_DAYS: int = 7

    class Config:
        env_file = ".env"


settings = Settings()
