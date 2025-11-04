from sentence_transformers import SentenceTransformer
from typing import Dict, Optional
import logging
import warnings

logger = logging.getLogger(__name__)

class ModelManager:
    _instances: Dict[str, SentenceTransformer] = {}
    _initialized = False

    @classmethod
    def initialize(cls):
        """Charge tous les modèles nécessaires au démarrage"""
        if not cls._initialized:
            logger.info("Initialisation des modèles...")
            
            # Modèle d'embedding pour la recherche
            cls.get_model(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_type="embedding",
                device="cpu",
                max_seq_length=256
            )
            
            # Modèle Whisper pour ASR (si nécessaire)
            cls.get_model(
                model_name="openai/whisper-medium",
                model_type="asr",
                device="cpu",
                token=False
            )
            
            cls._initialized = True

    @classmethod
    def get_model(cls, 
                 model_name: str,
                 model_type: Optional[str] = None,
                 **kwargs) -> SentenceTransformer:
        """Récupère ou charge un modèle avec configuration spécifique"""
        if model_name not in cls._instances:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                logger.info(f"Chargement du modèle: {model_name}")
                model = SentenceTransformer(model_name, **kwargs)
                
                # Configuration spécifique par type
                if model_type == "embedding":
                    model.max_seq_length = kwargs.get('max_seq_length', 256)
                elif model_type == "asr":
                    model.tokenizer.clean_up_tokenization_spaces = False
                
                cls._instances[model_name] = model
        
        return cls._instances[model_name]

    @classmethod
    def cleanup(cls):
        """Libère la mémoire des modèles"""
        cls._instances.clear()
        cls._initialized = False