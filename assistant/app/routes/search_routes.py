from fastapi import APIRouter, HTTPException

from app.services.response_service import ResponseService 

from app.config.logger import error_logger

from fastapi.responses import StreamingResponse

# Initialiser le routeur
router = APIRouter()

# Services
response_service = ResponseService()


@router.post("/search/site")
async def site_question_stream(request: str):
    try:
        stream_generator = await response_service._generate_site_response(
            query=request,
            stream=True
        )
        return StreamingResponse(
            stream_generator,
            media_type="text/event-stream"
        )
        
    except Exception as e:
        error_logger.error(f"Erreur streaming : {str(e)}")
        raise HTTPException(status_code=500, detail="Erreur de streaming")


