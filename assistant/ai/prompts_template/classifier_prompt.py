from typing import List
from app.enum.QueryType import QueryType
from app.services.history_service import HistoryService

class ClassifierPromptTemplate:
    def __init__(self):
        self.query_types = [t.value for t in QueryType]
        self.history_service = HistoryService()
    
   
        
    async def build_prompt(self, query: str) -> str:
        # Récupération et analyse de l'historique
        history = await self.history_service.get()
        user_queries = history.user_queries if history else []
        last_query_type = history.query_type if history else ""
        
        # Historique condensé (max 2 dernières requêtes)
        recent_history = user_queries[-2:] if user_queries else []
        
        return f"""CLASSIFICATEUR - RÉPONSE JSON UNIQUEMENT

TYPES: PRODUCT_INFO | OTHER

CONTEXTE ACTUEL:
Requête: "{query}"
Dernières requêtes: {" → ".join(recent_history) if recent_history else "Aucune"}
Dernier type: {last_query_type}


FORMAT RÉPONSE:
{{"Type": "<TYPE>", "confidence": <0.7-1.0>}}

INSTRUCTION FINAL : 
- respecter le format de reponse json 
- ne donne pas des explication , ni votre raisonnment 

Classify:"""