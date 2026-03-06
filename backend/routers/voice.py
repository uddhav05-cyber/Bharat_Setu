"""
Voice Processing Router
Endpoints for voice-based interaction (mock Vosk + Bhashini).
Implements the Frugal Edge Protocol from design doc.
"""
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models.user import User
from auth.rbac import get_current_user
from services.voice_service import voice_service

router = APIRouter(prefix="/voice", tags=["Voice Processing"])


# ----- Schemas -----

class VoiceProcessRequest(BaseModel):
    transcribed_text: str
    language: str = "hi"  # hi | mr | ta
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    transcription_source: str = "VOSK_EDGE"  # VOSK_EDGE | BHASHINI_CLOUD
    battery_level: Optional[float] = None


class VoiceProcessResponse(BaseModel):
    intent: str
    extracted_data: dict
    response_text: str
    processing_time_ms: int
    transcription_source: str
    language: str
    confidence: float


# ----- Endpoints -----

@router.post("/process", response_model=VoiceProcessResponse)
async def process_voice(
    req: VoiceProcessRequest,
    current_user: User = Depends(get_current_user),
):
    """
    Process transcribed voice input and extract intent.

    Accepts pre-transcribed text (from Vosk on-device or Bhashini cloud)
    and returns structured intent + extracted data.

    Supported intents:
    - REGISTER_FARM: Register a new farm plot
    - REQUEST_VERIFICATION: Request satellite verification
    - VIEW_CERTIFICATE: View/download a certificate
    - QUERY_STATUS: Check status of any request
    """
    result = voice_service.process_voice(
        transcribed_text=req.transcribed_text,
        language=req.language,
        user_id=current_user.id,
        gps_lat=req.gps_latitude,
        gps_lon=req.gps_longitude,
        transcription_source=req.transcription_source,
    )
    return result
