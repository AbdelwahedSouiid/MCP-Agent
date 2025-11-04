from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.config.settings import Settings
from fastapi.middleware.cors import CORSMiddleware
from app.routes.search_routes import router as question_routes
from app.routes.classifier_routes import router as filter_query
from app.routes.chatBot_routes import router as bot_query
from app.routes.voice_routes import router as voice_routes

from app.config.logger import LoggerConfig

from app.routes.redis_routes import router as redis_routes

settings = Settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

######### ---------------------------------Chatbot API

app.include_router(question_routes, prefix="/v1/question", tags=["Search from ADV Information "])
app.include_router(filter_query, prefix="/classify", tags=["Classify User Query"])
app.include_router(voice_routes, prefix="/voice" ,tags=["Voice system"])
app.include_router(bot_query, prefix="/bot", tags=["Bot Response"])

######### ---------------------------------OTHER Api for testing fonctionnality

app.include_router(redis_routes, tags=["Redis Cache"])

######### ---------------------------------Log Managemnt

config = LoggerConfig()

@app.get("/clear-logs", summary="Clear all log files", tags=["Logging"])
def clear_logs():
    success = config.clear_logs()
    if success:
        return JSONResponse(content={"message": "Tous les fichiers de log ont été vidés."}, status_code=200)
    else:
        return JSONResponse(content={"message": "Une erreur est survenue lors du nettoyage des logs."}, status_code=500)

