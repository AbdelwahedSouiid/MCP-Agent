from pydantic import ValidationError
from ai.llm.ollama_client import OllamaClient
from app.schemas.classification import Classification
from ai.prompts_template.classifier_prompt import ClassifierPromptTemplate
from ai.utils.language_util import LanguageService
from app.config.logger import classifier_logger as logger
from typing import Tuple
from app.enum.QueryType import QueryType

class ClassifierService:
    def __init__(self):
        self.template = ClassifierPromptTemplate()
        self.language_util = LanguageService()
        self.ollama_client = OllamaClient()

    async def classify(self, query: str) -> Tuple[Classification, str]:
        try:
            static_queries = {
                "bonjour": QueryType.OTHER,
                "bonsoir": QueryType.OTHER,
                "salut": QueryType.OTHER,   
                "au revoir": QueryType.OTHER,
                "bye": QueryType.OTHER,
                "je veux poser une question sur le site": QueryType.PLATFORM_INFO,
 
            }

            key = query.strip().lower()
            query_type = static_queries.get(key)
            
            if query_type:
                classification = Classification(Type=query_type, confidence=1.0)
                return classification, "fr"
            processed_query, lang = self.language_util.process_language(query)
            prompt = await self.template.build_prompt(processed_query)
            response = await self._get_llm_response(prompt)
            
            try:
                return response,lang
            except ValidationError:
                logger.warning("LLM returned invalid classification, using fallback")
                return Classification(type=QueryType.OTHER, confidence=0.5), lang
                
        except Exception as e:
            logger.error(f"Classification error: {str(e)}", exc_info=True)
            return Classification(Type=QueryType.OTHER, confidence=0.1), "fr"

    async def _get_llm_response(self, prompt: str) -> str: 
        """
        Récupère la réponse de l'IA.
        """
        response = await self.ollama_client.generate_response(prompt, stream=False)
        return response['message']['content'] if isinstance(response, dict) else str(response)
    