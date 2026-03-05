"""
Role-Based Access Control (RBAC)
Free alternative to AWS Cognito RBAC.
Implements per-role permissions per Requirement 8.
"""
import logging
from functools import wraps
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from auth.jwt_handler import decode_token
from database import get_db
from models.user import User

logger = logging.getLogger(__name__)
security = HTTPBearer()

# Role-based permissions matrix (from Requirements 8.2-8.5)
ROLE_PERMISSIONS = {
    "FARMER": {
        "allowed": ["farms", "certificates", "voice", "verification_status"],
        "denied": ["migration_shield", "admin", "dashboard_admin", "user_financials"],
    },
    "VLE": {
        "allowed": ["farms", "certificates", "voice", "verification", "commission"],
        "denied": ["migration_shield", "admin", "user_financials"],
    },
    "SARPANCH": {
        "allowed": ["twin", "hotspot", "farms_aggregated"],
        "denied": ["farmer_financials", "admin", "individual_farmer_data"],
    },
    "DISTRICT_OFFICIAL": {
        "allowed": ["dashboard", "alerts", "crisis_map", "reports", "migration_shield"],
        "denied": ["farmer_bank_accounts", "admin"],
    },
    "ADMIN": {
        "allowed": ["*"],  # All access
        "denied": [],
    },
}


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    """Extract and verify current user from JWT token."""
    token = credentials.credentials
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


def require_role(*allowed_roles: str):
    """Dependency to enforce role-based access control."""

    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles and current_user.role != "ADMIN":
            # Log unauthorized access attempt (Requirement 8.5)
            logger.warning(
                f"Unauthorized access attempt: user={current_user.id}, "
                f"role={current_user.role}, required={allowed_roles}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}",
            )
        return current_user

    return role_checker


def check_resource_access(user_role: str, resource: str) -> bool:
    """Check if a role has access to a specific resource."""
    permissions = ROLE_PERMISSIONS.get(user_role, {})
    allowed = permissions.get("allowed", [])
    denied = permissions.get("denied", [])

    if "*" in allowed:
        return True
    if resource in denied:
        return False
    if resource in allowed:
        return True
    return False
