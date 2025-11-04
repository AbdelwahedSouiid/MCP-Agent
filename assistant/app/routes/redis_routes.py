from fastapi import APIRouter, HTTPException
from typing import List, Optional

from app.schemas.history import History

from app.enum.QueryType import QueryType
from datetime import datetime



# app/api/history_routes.py
from app.services.history_service import HistoryService
from app.utils.redis_manager import RedisManager

router = APIRouter()
redis_manager = RedisManager()
history_service = HistoryService()

@router.post("/history/save")
async def save_history_endpoint(history_data: History):
    success = await history_service.update(history_data)
    return {"success": success}



@router.get("/history",response_model=History,responses={200: {"description": "Historique récupéré avec succès"},404: {"description": "Session non trouvée"}})
async def get_full_history():
    """
    Récupère l'historique complet pour la session actuelle.
    Inclut les requêtes utilisateur, la langue, les filtres, etc.
    """
    history = await history_service.get()
    if not history:
        raise HTTPException(
            status_code=404,
            detail="No history found for current session"
        )
    return history

@router.get("/last-queries",response_model=List[str])
async def get_last_user_queries(limit: int = 5):
    """
    Récupère les dernières requêtes utilisateur de la session actuelle.
    Args:
    - limit: Nombre maximum de requêtes à retourner (par défaut 5)
    """
    history = await history_service.get()
    if not history or not history.user_queries:
        raise HTTPException(
            status_code=404,
            detail="No user queries found for current session"
        )
    return history.user_queries[-limit:]

@router.post("/add-query",response_model=bool)
async def add_user_query(query: str):
    """
    Ajoute une nouvelle requête utilisateur à l'historique de la session actuelle.
    Args:
    - query: La requête textuelle à ajouter
    """
    try:
        history = await history_service.get() or History(
            session_id=redis_manager.session_id,
            timestamp=datetime.now().isoformat()
        )
        history.user_queries.append(query)
        return await history_service.update(history)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to add user query: {str(e)}"
        )

@router.post("/save-context",response_model=bool)
async def save_context(history: History):
    """
    Sauvegarde ou met à jour le contexte complet de la session.
    
    Args (History):
    - query_type: Type de requête (optionnel)
    - product_filters: Filtres de produits (optionnel)
    - lang: Langue (optionnel)
    - user_queries: Liste de requêtes (optionnel)
    """
    try:
        # On s'assure que la session_id est toujours celle du manager
        history.session_id = redis_manager.session_id
        return await history_service.update(history)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save context: {str(e)}"
        )



@router.put("/update-query-type",response_model=bool)
async def update_query_type(query_type: QueryType):
    """
    Met à jour le type de requête dans l'historique.
    """
    try:        
        return await history_service.set_query_type(query_type)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update query type: {str(e)}"
        )

@router.delete("/clear",response_model=bool)               
async def clear_history():
    """
    Supprime tout l'historique associé à la session actuelle.
    """
    try:
        return await history_service.delete()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to clear history: {str(e)}"
        )