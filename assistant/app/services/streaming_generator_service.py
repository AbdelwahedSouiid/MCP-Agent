# streaming_generator.py - Version avec interface simplifiée
from typing import AsyncGenerator
from app.services.classifier_service import ClassifierService
from app.services.response_service import ResponseService
from app.enum.QueryType import QueryType
from app.config.logger import error_logger, app_logger as logger

from app.services.history_service import HistoryService
from ai.utils.language_util import LanguageService

class StreamingGenerator:
    def __init__(self):
        self.history_service = HistoryService()
        self._init_query_handlers()
        self.classifier = ClassifierService()
        self.response = ResponseService()
        self.language_util = LanguageService()

    def _init_query_handlers(self):
        """Initialise les gestionnaires de requêtes."""
        self.query_handlers = {
            QueryType.PLATFORM_INFO: self._platform_handler,
            QueryType.OTHER: self._handle_unknown_query,
        }

    async def generate_stream(self, query: str) -> AsyncGenerator[str, None]:
        """Génère un flux SSE pour la requête avec sauvegarde simplifiée"""
        try:
            
            queryType = QueryType.PLATFORM_INFO
            processed_query, lang = self.language_util.process_language(query) 

            await self.history_service.add_query(processed_query)
            await self.history_service.set_language(lang)
            await self.history_service.set_query_type(queryType)
            
            # Sélection du handler approprié
            handler = self.query_handlers.get(queryType, self._handle_unknown_query)

            # Streaming de la réponse
            async for chunk in handler(processed_query):
                yield chunk
                
        except Exception as e:
            logger.error(f"Erreur système: {str(e)}", exc_info=True)
            yield self._format_event("Erreur de traitement", "error")


    async def _platform_handler(self, query: str) -> AsyncGenerator[str, None]:
        """Gestion des requêtes de plateforme."""
        try:
            logger.info(f"Recherche de site pour la requête: {query}")
            response_gen = await self.response._generate_site_response(query)
            async for chunk in response_gen:
                yield self._format_event(chunk)
        except Exception as e:
            error_logger.error(f"Platform handler error: {str(e)}")
            yield self._format_event("Erreur lors du traitement", "error")

    async def _handle_unknown_query(self, query: str) -> AsyncGenerator[str, None]:
        """Gestion des requêtes inconnues."""
        try:
            logger.info(f"Classification de la requête: {query}")
            response_gen = await self.response._generate_general_response(query) 
            async for chunk in response_gen:
                yield self._format_event(chunk)
        except Exception as e:
            error_logger.error(f"Error in unknown query handler: {str(e)}")
            yield self._format_event("Erreur lors du traitement", "error")


    def _format_event(self, data: str, event_type: str = "message") -> str:
        return f"event: {event_type}\ndata: {data}\n\n"

