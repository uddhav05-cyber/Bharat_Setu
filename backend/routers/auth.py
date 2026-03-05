"""
Auth Router
Endpoints: register, login, refresh token
Free alternative to AWS Cognito hosted UI.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from auth.jwt_handler import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


# ----- Request/Response Schemas -----

class RegisterRequest(BaseModel):
    name: str
    phone: str
    password: str
    role: str = "FARMER"  # FARMER | VLE | SARPANCH | DISTRICT_OFFICIAL | ADMIN
    language: str = "hi"
    village: str | None = None
    district: str | None = None
    state: str | None = None


class LoginRequest(BaseModel):
    phone: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str
    role: str
    name: str


# ----- Endpoints -----

@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user (farmer, VLE, sarpanch, district official)."""
    # Check if phone already exists
    existing = db.query(User).filter(User.phone == req.phone).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered",
        )

    # Validate role
    valid_roles = ["FARMER", "VLE", "SARPANCH", "DISTRICT_OFFICIAL", "ADMIN"]
    if req.role not in valid_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {', '.join(valid_roles)}",
        )

    # Create user
    user = User(
        name=req.name,
        phone=req.phone,
        password_hash=hash_password(req.password),
        role=req.role,
        language=req.language,
        village=req.village,
        district=req.district,
        state=req.state,
    )

    # Set VLE defaults
    if req.role == "VLE":
        user.trust_score = 50.0
        user.commission_rate = 5.0
        user.account_status = "ACTIVE"

    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate tokens
    token_data = {"sub": user.id, "role": user.role, "name": user.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        role=user.role,
        name=user.name,
    )


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    """Login with phone and password."""
    user = db.query(User).filter(User.phone == req.phone).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid phone number or password",
        )

    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()

    token_data = {"sub": user.id, "role": user.role, "name": user.name}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user_id=user.id,
        role=user.role,
        name=user.name,
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(req: RefreshRequest, db: Session = Depends(get_db)):
    """Refresh an expired access token."""
    payload = decode_token(req.refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )

    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    token_data = {"sub": user.id, "role": user.role, "name": user.name}
    access_token = create_access_token(token_data)
    new_refresh_token = create_refresh_token(token_data)

    return TokenResponse(
        access_token=access_token,
        refresh_token=new_refresh_token,
        user_id=user.id,
        role=user.role,
        name=user.name,
    )
