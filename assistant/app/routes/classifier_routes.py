from fastapi import APIRouter, HTTPException
from app.services.classifier_service import ClassifierService 
from app.config.logger import error_logger 
router = APIRouter()


# Initialisation du service de classification
classifier_service = ClassifierService()
@router.post("/classify-query")
async def classify_query(request: str):
    try:
        classification = await classifier_service.classify(request)
        return classification
    except Exception as e:
        error_logger.error(f"Erreur: {str(e)}")
        raise HTTPException(status_code=500, detail="Échec de classification")