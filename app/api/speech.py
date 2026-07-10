from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
from app.speech.whisper_engine import transcribe_audio
from app.speech.tts_engine import generate_speech
from app.intent.parser import parser
import os

router = APIRouter()

class SpeakRequest(BaseModel):
    text: str

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    try:
        text = transcribe_audio(audio_bytes)
        intent_data = parser.parse(text)
        return {
            "text": text,
            "intent": intent_data["intent"],
            "entities": intent_data["entities"]
        }
    except Exception as e:
        return {"error": str(e)}

@router.post("/speak")
async def speak(request: SpeakRequest):
    if not request.text:
        return {"error": "No text provided"}
    try:
        audio_path = await generate_speech(request.text)
        return FileResponse(audio_path, media_type="audio/mpeg")
    except Exception as e:
        return {"error": str(e)}
