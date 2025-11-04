import asyncio
import logging
import httpx
from typing import AsyncGenerator, Dict, Any
from app.config.settings import settings
import json 

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepseekClient:
    def __init__(self) -> None:
        self.model = settings.Deepseek_Model  
        self.api_key = settings.DEEPSEEK_API_KEY 
        self.base_url = "https://api.deepseek.com/v1/chat/completions"  # URL corrigée
        self.timeout = 60.0  # Timeout plus long pour les requêtes streaming
    
    async def generate_response(self, prompt: str, stream: bool = False) -> AsyncGenerator[str, None] | Dict[str, Any]:
        """
        Génère une réponse avec DeepSeek
        
        Args:
            prompt: Le prompt à envoyer
            stream: Si True, retourne un générateur async pour le streaming
            
        Returns:
            AsyncGenerator pour streaming ou dict pour réponse complète
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": stream,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        if stream:
            return self._stream_response(headers, payload)
        else:
            return await self._single_response(headers, payload)
    
    async def _stream_response(self, headers: Dict[str, str], payload: Dict[str, Any]) -> AsyncGenerator[str, None]:
        """Gère la réponse streaming"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                async with client.stream(
                    "POST",
                    self.base_url,  # URL corrigée
                    json=payload,
                    headers=headers
                ) as response:
                    response.raise_for_status()
                    
                    async for line in response.aiter_lines():
                        line = line.strip()
                        
                        # Traiter les lignes SSE
                        if line.startswith("data:"):
                            data_content = line[5:].strip()
                            
                            # Fin du stream
                            if data_content == "[DONE]":
                                break
                            
                            # Parser le JSON
                            if data_content:
                                try:
                                    data = json.loads(data_content)
                                    
                                    # Extraire le contenu du delta
                                    choices = data.get("choices", [])
                                    if choices:
                                        delta = choices[0].get("delta", {})
                                        content = delta.get("content", "")
                                        
                                        if content:
                                            yield content
                                            
                                except json.JSONDecodeError as e:
                                    logger.warning(f"Erreur parsing JSON: {data_content} - {e}")
                                    continue
                                except Exception as e:
                                    logger.error(f"Erreur traitement chunk: {e}")
                                    continue
                        
                        # Petit délai pour éviter la surcharge
                        await asyncio.sleep(0.01)
                        
        except httpx.TimeoutException:
            logger.error("Timeout lors du streaming DeepSeek")
            yield "Erreur: Timeout de la requête"
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP DeepSeek: {e.response.status_code} - {e.response.text}")
            yield f"Erreur API: {e.response.status_code}"
        except Exception as e:
            logger.error(f"Erreur streaming DeepSeek: {e}", exc_info=True)
            yield "Erreur lors de la génération de la réponse"
    
    async def _single_response(self, headers: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, Any]:
        """Gère la réponse simple (non-streaming)"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                data = response.json()
                
                # Extraire le contenu de la réponse
                choices = data.get("choices", [])
                if choices:
                    message_content = choices[0].get("message", {}).get("content", "")
                    return {
                        'message': {
                            'content': message_content
                        },
                        'usage': data.get('usage', {}),
                        'model': data.get('model', self.model)
                    }
                else:
                    return {
                        'message': {
                            'content': 'Aucune réponse générée'
                        }
                    }
                    
        except httpx.TimeoutException:
            logger.error("Timeout lors de la requête DeepSeek")
            return {'message': {'content': 'Erreur: Timeout de la requête'}}
        except httpx.HTTPStatusError as e:
            logger.error(f"Erreur HTTP DeepSeek: {e.response.status_code}")
            try:
                error_detail = e.response.json()
                error_msg = error_detail.get('error', {}).get('message', 'Erreur API')
            except:
                error_msg = f"Erreur HTTP {e.response.status_code}"
            return {'message': {'content': f'Erreur API: {error_msg}'}}
        except Exception as e:
            logger.error(f"Erreur DeepSeek: {e}", exc_info=True)
            return {'message': {'content': 'Erreur lors de la génération de la réponse'}}
    
    async def generate_with_context(self, messages: list, stream: bool = False) -> AsyncGenerator[str, None] | Dict[str, Any]:
        """
        Génère une réponse avec un contexte de conversation
        
        Args:
            messages: Liste des messages [{"role": "user/assistant", "content": "..."}]
            stream: Si True, retourne un générateur async
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "temperature": 0.7,
            "max_tokens": 2000
        }
        
        if stream:
            return self._stream_response(headers, payload)
        else:
            return await self._single_response(headers, payload)
    
    def validate_api_key(self) -> bool:
        """Valide si la clé API est configurée"""
        return bool(self.api_key and self.api_key.strip())
    
    async def test_connection(self) -> Dict[str, Any]:
        """Test de connexion à l'API DeepSeek"""
        if not self.validate_api_key():
            return {
                'success': False,
                'error': 'Clé API manquante ou invalide'
            }
        
        try:
            result = await self.generate_response("Test de connexion", stream=False)
            return {
                'success': True,
                'model': self.model,
                'response_length': len(result.get('message', {}).get('content', ''))
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
