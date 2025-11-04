from sentence_transformers import SentenceTransformer
from typing import Dict
import warnings
import torch

class ModelLoader:
    _instances: Dict[str, SentenceTransformer] = {}
    _initialized = False

    @classmethod
    def get_model(cls, 
                  model_name: str = "sentence-transformers/all-MiniLM-L6-v2", 
                  device: str = None, 
                  **kwargs) -> SentenceTransformer:
        if model_name not in cls._instances:
            if device is None:
                device = "cuda" if torch.cuda.is_available() else "cpu"

            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                model = SentenceTransformer(
                    model_name,
                    device=device,
                    tokenizer_kwargs={'clean_up_tokenization_spaces': False},
                    **kwargs
                )
                model.max_seq_length = 512  # Optional
                cls._instances[model_name] = model
        return cls._instances[model_name]
    
    @classmethod
    def initialize(cls):
        # Charge les modèles au démarrage
        if not cls._initialized:
            # Modèle d'embedding
            cls.get_model(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_type="embedding",
                device="cpu",
                max_seq_length=256
            )
            
            # Modèle Whisper pour ASR
            cls.get_model(
                model_name="openai/whisper-medium",
                model_type="asr",
                device="cpu",
                token=False
            )