import os
import requests

STT_URL = "https://api.vachana.ai/stt/v3"
TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"

def _api_key():
    key = os.getenv("GNANI_API_KEY_ID", "").strip()
    return key or None

def transcribe_audio(audio_file):
    """
    Uses the documented Prisma v3.0 REST endpoint when GNANI_API_KEY_ID exists.
    Otherwise returns a clear message: voice transcription needs API access.
    """
    key = _api_key()
    if not key:
        raise RuntimeError(
            "Gnani API key not configured. Add GNANI_API_KEY_ID to your .env file. "
            "You can still test the app by typing a question."
        )

    audio_file.seek(0)
    files = {
        "audio_file": (
            getattr(audio_file, "name", "farmer_audio.wav"),
            audio_file.getvalue(),
            getattr(audio_file, "type", None) or "audio/wav"
        )
    }
    data = {
        "model": "prisma-v3.0",
        "language_code": "te-IN",
        "format": "transcribe"
    }
    response = requests.post(
        STT_URL,
        headers={"X-API-Key-ID": key},
        files=files,
        data=data,
        timeout=90
    )
    response.raise_for_status()
    result = response.json()

    transcript = result.get("transcript")
    if not result.get("success", True) or not transcript:
        raise RuntimeError(f"Prisma did not return a transcript: {result}")

    return transcript, "Gnani Prisma v3.0"

def synthesize_telugu(text):
    """
    Uses Gnani Timbre v2.5 REST inference.
    Voice 'Suhana' is listed in Gnani's Telugu v2.5 voice catalog.
    """
    key = _api_key()
    if not key:
        raise RuntimeError(
            "Gnani API key not configured. Add GNANI_API_KEY_ID to your .env file."
        )

    payload = {
        "text": text,
        "voice": "Suhana",
        "model": "timbre-v2.5",
        "language": "te-IN",
        "speed": 1.0,
        "audio_config": {
            "sample_rate": 48000,
            "num_channels": 1,
            "sample_width": 2,
            "encoding": "linear_pcm",
            "container": "wav"
        }
    }

    response = requests.post(
        TTS_URL,
        headers={
            "X-API-Key-ID": key,
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=90
    )
    response.raise_for_status()
    return response.content, "Gnani Timbre v2.5 (Suhana)"
