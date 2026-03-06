"""
Certificate Router
Endpoints for viewing and downloading service payment certificates.
"""
import os
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from models.certificate import Certificate
from models.user import User
from auth.rbac import get_current_user, require_role
from services.certificate_service import certificate_service
from services.escrow_service import escrow_service

router = APIRouter(prefix="/certificates", tags=["Certificates"])


# ----- Schemas -----

class CertificateResponse(BaseModel):
    id: str
    farmer_id: str
    farm_plot_id: str
    verification_id: str
    vle_id: Optional[str]
    carbon_tons: float
    issued_at: Optional[datetime]
    expires_at: Optional[datetime]
    status: str
    payment_type: Optional[str]
    payment_source: Optional[str]
    fixed_service_payment: Optional[float]
    voucher_code: Optional[str]
    traffic_light_status: Optional[str]
    traffic_light_variance: Optional[float]
    download_url: Optional[str]

    class Config:
        from_attributes = True


class GenerateCertificateRequest(BaseModel):
    verification_id: str
    payment_source: str = "CSR"  # CSR | GOVERNMENT_GRANT


# ----- Endpoints -----

@router.post("/generate")
async def generate_certificate(
    req: GenerateCertificateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("VLE", "ADMIN")),
):
    """
    Generate a certificate for a GREEN verification.
    Triggers payment processing via the escrow service.
    """
    result = await escrow_service.process_settlement(
        db=db,
        verification_id=req.verification_id,
        payment_source=req.payment_source,
    )

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@router.get("/", response_model=List[CertificateResponse])
def list_certificates(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List certificates. Farmers see only their own; VLEs/admins see all."""
    if current_user.role == "FARMER":
        certs = certificate_service.list_certificates(
            db, farmer_id=current_user.id, skip=skip, limit=limit
        )
    else:
        certs = certificate_service.list_certificates(db, skip=skip, limit=limit)
    return certs


@router.get("/{cert_id}", response_model=CertificateResponse)
def get_certificate(
    cert_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific certificate by ID."""
    cert = certificate_service.get_certificate(db, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    # RBAC: Farmers can only see their own
    if current_user.role == "FARMER" and cert.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return cert


@router.get("/{cert_id}/download")
def download_certificate(
    cert_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Download the certificate PDF."""
    cert = certificate_service.get_certificate(db, cert_id)
    if not cert:
        raise HTTPException(status_code=404, detail="Certificate not found")

    if current_user.role == "FARMER" and cert.farmer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    if not cert.file_path or not os.path.exists(cert.file_path):
        raise HTTPException(status_code=404, detail="Certificate PDF not found")

    return FileResponse(
        cert.file_path,
        media_type="application/pdf",
        filename=f"certificate-{cert_id}.pdf",
    )
