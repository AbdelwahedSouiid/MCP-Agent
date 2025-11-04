from pydantic import BaseModel
from typing import Optional, List
from app.enum.QueryType import QueryType


class History(BaseModel):
    """Modèle pour l'historique des sessions stocké dans Redis"""
    timestamp: Optional[str] = None
    session_id: Optional[str] = None
    query_type: Optional[QueryType] = None
    lang: Optional[str] = None
    user_queries: Optional[List[str]] = None
 
