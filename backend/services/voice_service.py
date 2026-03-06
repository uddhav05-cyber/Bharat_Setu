"""
Voice Service (Mock)
Free alternative to Vosk-Lite (edge) + Bhashini API (cloud).
Accepts pre-transcribed text and extracts intent via keyword matching.
"""
import re
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class VoiceService:
    """Mock voice processing with intent extraction."""

    # Keyword patterns for intent detection
    INTENT_PATTERNS = {
        "REGISTER_FARM": [
            r"\b(register|add|new|create)\b.*\b(farm|plot|land|khet)\b",
            r"\b(farm|plot|land|khet)\b.*\b(register|add|new|create)\b",
            r"\b(start)\b.*\b(survey)\b",
        ],
        "REQUEST_VERIFICATION": [
            r"\b(verify|check|test|scan)\b.*\b(farm|plot|crop|biomass|carbon)\b",
            r"\b(farm|plot|crop|biomass|carbon)\b.*\b(verify|check|test|scan)\b",
            r"\b(satellite)\b.*\b(check|scan|verify)\b",
            r"\b(request)\b.*\b(verification)\b",
        ],
        "VIEW_CERTIFICATE": [
            r"\b(view|show|see|download|get)\b.*\b(certificate|cert|payment)\b",
            r"\b(certificate|cert|payment)\b.*\b(view|show|see|download|get)\b",
            r"\b(my)\b.*\b(certificate|payment)\b",
        ],
        "QUERY_STATUS": [
            r"\b(status|update|progress|result)\b",
            r"\b(what|how)\b.*\b(status|going|progress)\b",
            r"\b(check)\b.*\b(status|result)\b",
        ],
    }

    # Extraction patterns for structured data
    CROP_TYPES = [
        "rice", "wheat", "cotton", "sugarcane", "maize", "soybean",
        "millet", "bajra", "jowar", "tur", "groundnut",
    ]

    def process_voice(
        self,
        transcribed_text: str,
        language: str = "hi",
        user_id: str = "",
        gps_lat: Optional[float] = None,
        gps_lon: Optional[float] = None,
        transcription_source: str = "VOSK_EDGE",
    ) -> dict:
        """
        Process transcribed voice input and extract intent.
        In pilot mode, this uses keyword matching instead of Bedrock/Claude.
        """
        start = time.time()
        text_lower = transcribed_text.lower().strip()

        # 1. Detect intent
        intent = self._detect_intent(text_lower)

        # 2. Extract structured data
        extracted_data = self._extract_data(text_lower, gps_lat, gps_lon)

        # 3. Generate response text
        response_text = self._generate_response(intent, extracted_data)

        processing_time = int((time.time() - start) * 1000)

        return {
            "intent": intent,
            "extracted_data": extracted_data,
            "response_text": response_text,
            "processing_time_ms": processing_time,
            "transcription_source": transcription_source,
            "language": language,
            "confidence": 0.85 if intent != "QUERY_STATUS" else 0.70,
        }

    def _detect_intent(self, text: str) -> str:
        """Detect intent from text using keyword pattern matching."""
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    return intent
        return "QUERY_STATUS"  # Default fallback

    def _extract_data(
        self, text: str, gps_lat: Optional[float], gps_lon: Optional[float]
    ) -> dict:
        """Extract structured data from transcribed text."""
        data = {}

        # Extract farm size (acres)
        size_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:acres?|bigha|hectare)", text)
        if size_match:
            value = float(size_match.group(1))
            if "hectare" in text:
                value *= 2.471  # Convert hectares to acres
            elif "bigha" in text:
                value *= 0.62  # Approx conversion
            data["farm_size"] = round(value, 2)

        # Extract crop type
        for crop in self.CROP_TYPES:
            if crop in text:
                data["crop_type"] = crop
                break

        # Extract location
        location_match = re.search(
            r"(?:in|at|near|village)\s+([A-Za-z]+(?:\s+[A-Za-z]+)?)", text
        )
        if location_match:
            data["location"] = location_match.group(1).strip()

        # Use GPS if available
        if gps_lat is not None and gps_lon is not None:
            data["gps"] = {"latitude": gps_lat, "longitude": gps_lon}

        # Extract plot number if mentioned
        plot_match = re.search(r"(?:plot|survey)\s*(?:#|number|no\.?)\s*(\d+)", text)
        if plot_match:
            data["plot_number"] = plot_match.group(1)

        return data

    def _generate_response(self, intent: str, extracted_data: dict) -> str:
        """Generate a human-readable response (for TTS on device)."""
        responses = {
            "REGISTER_FARM": "Farm registration started. Please confirm the plot details.",
            "REQUEST_VERIFICATION": "Verification request submitted. Satellite check will run shortly.",
            "VIEW_CERTIFICATE": "Fetching your latest certificate. Please wait.",
            "QUERY_STATUS": "Checking status. Please wait a moment.",
        }

        response = responses.get(intent, "Request received. Processing now.")

        if "farm_size" in extracted_data:
            response += f" Farm size: {extracted_data['farm_size']} acres."
        if "crop_type" in extracted_data:
            response += f" Crop: {extracted_data['crop_type']}."

        return response


voice_service = VoiceService()
