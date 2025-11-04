from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.streaming_generator_service import StreamingGenerator

# Initialisation des services
from app.services.streaming_generator_service import StreamingGenerator

router = APIRouter()

streamer = StreamingGenerator()

@router.get("/bot-query")
async def stream_bot_query(query: str):
    return StreamingResponse(
        streamer.generate_stream(query),
        media_type="text/event-stream",
        headers={
            "X-Stream-Source": "ollama-llama3",
            "Cache-Control": "no-store"
        }
    )


