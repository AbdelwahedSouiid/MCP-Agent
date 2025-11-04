
from ai.prompts_template.generale_prompt import GeneralDiscussionTemplate
from app.config.logger import  error_logger
import re
import asyncio
from typing import AsyncGenerator
from ai.llm.ollama_client import OllamaClient
from ai.prompts_template.adv_platform_prompt import ADVPlatformTemplate

class ResponseService:
    """Service responsable de la génération des réponses avec llm.
    - Few-shot pour les requêtes sur le site
    """
    def __init__(self):
        """Initialise les templates et le modèle LLM"""
        self.adv_template = ADVPlatformTemplate()
        self.general_template = GeneralDiscussionTemplate()
        self.ollama_client = OllamaClient()
    
    async def _generate_site_response(self, query: str):
      
        prompt = await self.adv_template.build_prompt(query)

        return await self._handle_generation(prompt, True)
      
    async def _generate_general_response(self,query :str) -> AsyncGenerator[str, None]:
        """
        Génère une réponse générale pour les requêtes inconnues
        """
        prompt = await self.general_template.build_prompt(query)
        return  await self._handle_generation(prompt, True)

    async def _handle_generation(self, prompt: str, stream: bool) -> AsyncGenerator[str, None]:
        """Gère la génération de réponse avec streaming"""
        
        if stream:
            async def generate():
                try:
                    response_gen = await self.ollama_client.generate_response( prompt, stream)
                    async for chunk in response_gen:
                        yield chunk
                        await asyncio.sleep(0.01)
                except Exception as e:
                    error_logger.error(f"Erreur streaming: {str(e)}", exc_info=True)
                    yield "Erreur de service"
            return generate()
        else:
            try:
                response = await self.ollama_client.generate_response(prompt, stream)
                content = response.get('message', {}).get('content', '')
                cleaned = self._clean_response(content) if content else "Aucune réponse générée"
                return cleaned
            except Exception as e:
                error_logger.error(f" Erreur génération: {str(e)}", exc_info=True)
                return "Erreur de service"

    def _clean_response(self, text: str) -> str:
        text = re.sub(r"\[.*?\]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text
    