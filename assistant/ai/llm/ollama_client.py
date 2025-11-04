import asyncio
import logging
import httpx
from typing import AsyncGenerator, Dict, Any
from app.config.settings import settings
import json

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self) -> None:
        self.model = settings.OLLAMA_MODEL  
        self.base_url = settings.OLLAMA_API_URL  
        self.timeout = 60.0
    
    async def generate_response(self, prompt: str, stream: bool = False) -> AsyncGenerator[str, None] | Dict[str, Any]:
        """
        Génère une réponse avec Ollama
        
        Args:
            prompt: Le prompt à envoyer
            stream: Si True, retourne un générateur async pour le streaming
            
        Returns:
            AsyncGenerator pour streaming ou dict pour réponse complète
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": stream,
            "options": {
                "temperature": 0.7,
                "num_predict": 2000  # Équivalent à max_tokens
            }
        }
        
        if stream:
            return self._stream_response(payload)
        else:
            return await self._single_response(payload)
    
    async def _stream_response(self, payload: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Gère la réponse streaming"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/generate",
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        line = line.strip()
                        if line:
                            try:
                                data = json.loads(line)
                                if "response" in data:
                                    yield data["response"]
                            except json.JSONDecodeError as e:
                                logger.warning(f"Erreur parsing JSON: {line} - {e}")
                                continue
                            except Exception as e:
                                logger.error(f"Erreur traitement chunk: {e}")
                                continue
                        
                        # Petit délai pour éviter la surcharge
                        await asyncio.sleep(0.01)
                        
        except httpx.TimeoutException:
            logger.error("Timeout lors du streaming Ollama")
            yield "Erreur: Timeout de la requête"
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP Ollama: {e.response.status_code} - {e.response.text}")
            yield f"Erreur API: {e.response.status_code}"
        except Exception as e:
            logger.error(f"Erreur streaming Ollama: {e}", exc_info=True)
            yield "Erreur lors de la génération de la réponse"
    
    async def _single_response(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la réponse simple (non-streaming)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/generate",
                    json=payload
                    )
                response.raise_for_status()
                data = response.json()
                
                return {
                    'message': {
                        'content': data.get("response", "")
                    },
                    'model': data.get("model", self.model),
                    'stats': data.get("stats", {})
                }
                
        except httpx.TimeoutException:
            logger.error("Timeout lors de la requête Ollama")
            return {'message': {'content': 'Erreur: Timeout de la requête'}}
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP Ollama: {e.response.status_code}")
            try:
                error_detail = e.response.json()
                error_msg = error_detail.get('error', 'Erreur API')
            except:
                error_msg = f"Erreur HTTP {e.response.status_code}"
            return {'message': {'content': f'Erreur API: {error_msg}'}}
        except Exception as e:
            logger.error(f"Erreur Ollama: {e}", exc_info=True)
            return {'message': {'content': 'Erreur lors de la génération de la réponse'}}
    
    async def generate_with_context(self, messages: list, stream: bool = False) -> AsyncGenerator[str, None] | Dict[str, Any]:
        """
        Génère une réponse avec un contexte de conversation
        
        Args:
            messages: Liste des messages [{"role": "user/assistant", "content": "..."}]
            stream: Si True, retourne un générateur async
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "options": {
                "temperature": 0.7,
                "num_predict": 2000
            }
        }
        
        if stream:
            return self._stream_chat_response(payload)
        else:
            return await self._single_chat_response(payload)
    
    async def _stream_chat_response(self, payload: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Gère la réponse streaming pour le chat"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/chat",
                    json=payload
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        line = line.strip()
                        if line:
                            try:
                                data = json.loads(line)
                                if "message" in data and "content" in data["message"]:
                                    yield data["message"]["content"]
                            except json.JSONDecodeError as e:
                                logger.warning(f"Erreur parsing JSON: {line} - {e}")
                                continue
                            except Exception as e:
                                logger.error(f"Erreur traitement chunk: {e}")
                                continue
                        
                        await asyncio.sleep(0.01)
                        
        except Exception as e:
            logger.error(f"Erreur streaming chat Ollama: {e}")
            yield "Erreur lors de la génération de la réponse"
    
    async def _single_chat_response(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la réponse simple pour le chat"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat",
                    json=payload
                )
                response.raise_for_status()
                data = response.json()
                
                return {
                    'message': data.get("message", {}),
                    'model': data.get("model", self.model),
                    'stats': data.get("stats", {})
                }
                
        except Exception as e:
            logger.error(f"Erreur chat Ollama: {e}")
            return {'message': {'content': 'Erreur lors de la génération de la réponse'}}
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test de connexion à l'API Ollama"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.head(self.base_url)
                response.raise_for_status()
                
                # Test supplémentaire avec une petite requête
                test_result = await self.generate_response("Test de connexion", stream=False)
                return {
                    'success': True,
                    'model': self.model,
                    'response_length': len(test_result.get('message', {}).get('content', ''))
                }
        except httpx.TimeoutException:
            return {
                'success': False,
                'error': 'Timeout - Le service Ollama ne répond pas'
            }
        except httpx.HTTPStatusError as e:
            return {
                'success': False,
                'error': f"Erreur HTTP {e.response.status_code}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }