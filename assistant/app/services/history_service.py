from typing import Optional, List, Dict, Any
from datetime import datetime
from app.schemas.history import History
from app.enum.QueryType import QueryType
from app.config.logger import error_logger
from app.utils.redis_manager import RedisManager

class HistoryService:
    """
    Service simplifié pour la gestion de l'historique dans Redis.
    Fournit une interface CRUD complète avec des méthodes spécifiques pour chaque champ.
    """
    
    def __init__(self):
        self.redis_manager = RedisManager()

    
    async def create(self) -> History:
        """Crée un nouvel historique vide"""
        new_history = History(
            session_id=self.redis_manager.session_id,
            timestamp=datetime.now().isoformat()
        )
        await self.update(new_history)
        return new_history
    
    async def get(self) -> History:
        """
        Récupère l'historique complet depuis Redis.
        Crée un nouvel historique s'il n'existe pas.
        """
        try:
            history_data = await self.redis_manager.get_data()
            if history_data:
                return self._deserialize(history_data)
            return await self.create()
        except Exception as e:
            error_logger.error(f"Error getting history: {str(e)}", exc_info=True)
            return await self.create()
    
    async def update(self, history: History) -> bool:
        """Met à jour l'historique complet dans Redis"""
        try:
            history.timestamp = datetime.now().isoformat()
            return await self.redis_manager.save_data(self._serialize(history))
        except Exception as e:
            error_logger.error(f"Error updating history: {str(e)}", exc_info=True)
            return False
    
    async def delete(self) -> bool:
        """Supprime complètement l'historique de Redis"""
        try:
            return await self.redis_manager.delete_data()
        except Exception as e:
            error_logger.error(f"Error deleting history: {str(e)}", exc_info=True)
            return False
    
    # --------------------------------------------------------------------------
    # Méthodes spécifiques par champ 
    # --------------------------------------------------------------------------
    
    # -- Gestion des requêtes utilisateur --
    async def add_query(self, query: str) -> bool:
        """Ajoute une requête à l'historique"""
        history = await self.get()
        if not history.user_queries:
            history.user_queries = []
        history.user_queries.append(query)
        return await self.update(history)
    
    async def get_queries(self) -> List[str]:
        """Récupère toutes les requêtes"""
        return (await self.get()).user_queries or []
    
    async def clear_queries(self) -> bool:
        """Efface toutes les requêtes"""
        history = await self.get()
        history.user_queries = []
        return await self.update(history)
    
    # -- Gestion du type de requête --
    async def set_query_type(self, query_type: QueryType) -> bool:
        """Définit le type de requête"""
        history = await self.get()
        history.query_type = query_type
        return await self.update(history)
    
    async def get_query_type(self) -> Optional[QueryType]:
        """Récupère le type de requête"""
        return (await self.get()).query_type
    
    # -- Gestion de la langue --
    async def set_language(self, lang: str) -> bool:
        """Définit la langue"""
        history = await self.get()
        history.lang = lang
        return await self.update(history)
    
    async def get_language(self) -> Optional[str]:
        """Récupère la langue"""
        return (await self.get()).lang
    
    # --------------------------------------------------------------------------
    # Méthodes utilitaires
    # --------------------------------------------------------------------------
    
    def _serialize(self, history: History) -> Dict[str, Any]:
        """Sérialise l'objet History pour Redis"""
        return {
            "timestamp": history.timestamp,
            "session_id": history.session_id,
            "query_type": history.query_type.value if history.query_type else None,
            "lang": history.lang,
            "user_queries": history.user_queries or []
        }
    
    def _deserialize(self, data: Dict[str, Any]) -> History:
        """Désérialise les données Redis en objet History"""
        return History(
            timestamp=data.get("timestamp"),
            session_id=data.get("session_id"),
            query_type=QueryType(data["query_type"]) if data.get("query_type") else None,
            product_filters=ProductFilters(**data["product_filters"]) if data.get("product_filters") else None,
            lang=data.get("lang"),
            user_queries=data.get("user_queries", []),
          
        )