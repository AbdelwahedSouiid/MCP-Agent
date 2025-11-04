# app/api/voice_router.py
from fastapi import APIRouter, UploadFile, HTTPException
from app.services.voice_service import VoiceService
from app.schemas.voice import TranscriptionResponse
from fastapi.responses import StreamingResponse
from app.services.streaming_generator_service import StreamingGenerator

router = APIRouter()
voice_service = VoiceService()
streamer = StreamingGenerator()

@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(file: UploadFile):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Un fichier audio est requis (.wav, .mp3, etc)")
    
    try:
        return await voice_service.transcribe(file)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de transcription: {str(e)}")

    
@router.post("/bot_query")
async def bot_query(file:UploadFile):

    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="Un fichier audio est requis (.wav, .mp3, etc)")
    
    try:
        result = await voice_service.transcribe(file)

        # Concaténer tous les textes des segments
        full_text = " ".join(segment["text"] for segment in result["segments"])

        return StreamingResponse(
        streamer.generate_stream(full_text),
        media_type="text/event-stream"
    )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur de transcription: {str(e)}")
    
@router.get("/api/system/gpu-info")
async def get_gpu_info():
    return voice_service.get_device_info()
