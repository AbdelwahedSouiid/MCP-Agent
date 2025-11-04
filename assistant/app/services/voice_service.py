from fastapi import UploadFile, HTTPException
from faster_whisper import WhisperModel
import torch
import os
import uuid

from pathlib import Path
from typing import Dict, Any
from app.schemas.voice import Segment, TranscriptionResponse
from app.config.logger import voice_logger, error_logger,models_logger

class VoiceService:
    def __init__(self, model_size: str = "small", compute_type: str = "float16"):
        """Initialize the VoiceService with the specified model configuration.
        Args:
            model_size (str): Size of the model to use ("small", "base", "large", etc.)
            compute_type (str): Numerical precision to use ("float16", "float32", etc.)
        """
        # Configuration optimisée
        self.cuda_available = torch.cuda.is_available()
        self.compute_type = compute_type if self.cuda_available else "float32"
        self.device_name = "cuda" if self.cuda_available else "cpu"
        self.torch_device = torch.device(self.device_name)

        # Optimisation du choix du modèle
        self.model_size = model_size
        if not self.cuda_available and model_size == "small":
            models_logger.warning("GPU non détecté - Downgrade automatique au modèle 'base'")
            self.model_size = "base"
                
        voice_logger.info(f"Initialisation VoiceService - Modèle: {self.model_size}, Dispositif: {self.device_name}")
        
        # Préparation du répertoire temporaire
        self.temp_dir = Path("data/audio")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # Chargement du modèle avec les bons types de paramètres
        try:
            # Utilisation de la chaîne de caractères pour device au lieu de l'objet torch.device
            self.model = WhisperModel(
                self.model_size, 
                device=self.device_name,  # Chaîne de caractères ("cuda" ou "cpu")
                compute_type=self.compute_type
            )
            voice_logger.info("Modèle Whisper chargé avec succès")
        except Exception as e:
            error_logger.error(f"Erreur chargement modèle: {str(e)}", exc_info=True)
            raise RuntimeError(f"Erreur initialisation modèle: {str(e)}") from e

    async def transcribe(self, file: UploadFile, **kwargs) -> Dict[str, Any]:
        """Transcribe an audio file using the Whisper model.
        
        Args:
            file (UploadFile): The audio file to transcribe
            **kwargs: Additional parameters for the transcription model
            
        Returns:
            Dict[str, Any]: The transcription result
            
        Raises:
            HTTPException: If any error occurs during transcription
        """
        transaction_id = uuid.uuid4().hex[:8]
        voice_logger.info(f"[{transaction_id}] Début transcription - Fichier: {file.filename}")
        
        temp_file_path = None
        try:
            # Validation du fichier
            file_bytes = await file.read()
            if not file_bytes:
                error_logger.error(f"[{transaction_id}] Fichier audio vide")
                raise HTTPException(status_code=400, detail="Fichier audio vide")
            
            # Création du fichier temporaire
            temp_file_name = f"{uuid.uuid4()}.wav"
            temp_file_path = self.temp_dir / temp_file_name
                
            with open(temp_file_path, "wb") as f:
                f.write(file_bytes)
            
            # Configuration des paramètres de transcription
            params = {
                "beam_size": 5,
                "language": None,
                "task": "transcribe",
                "initial_prompt": None
            }
            params.update(kwargs)
            
            voice_logger.debug(f"[{transaction_id}] Paramètres transcription: {params}")
            
            # Exécution de la transcription
            segments, info = self.model.transcribe(str(temp_file_path), **params)
            
            # Construction de la réponse
            segment_list = [
                Segment(start=segment.start, end=segment.end, text=segment.text)
                for segment in segments
            ]
            
            response = TranscriptionResponse(
                language=info.language,
                language_probability=info.language_probability,
                segments=segment_list,
                model=self.model_size,
                device=self.device_name,  # Utilisation de la chaîne de caractères
                cuda_available=self.cuda_available
            )
            
            voice_logger.info(f"[{transaction_id}] Transcription réussie - Langue: {info.language}")
            return response.dict()
            
        except HTTPException:
            # Réémission des exceptions HTTP
            raise
        except Exception as e:
            error_msg = f"Erreur lors de la transcription: {str(e)}"
            error_logger.error(f"[{transaction_id}] {error_msg}", exc_info=True)
            raise HTTPException(status_code=500, detail=error_msg)
        finally:
            # Nettoyage du fichier temporaire si existant
            if temp_file_path and temp_file_path.exists():
                try:
                    os.remove(temp_file_path)
                    voice_logger.debug(f"[{transaction_id}] Fichier temporaire supprimé")
                except OSError as e:
                    error_logger.warning(f"[{transaction_id}] Impossible de supprimer le fichier temporaire: {str(e)}")
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get information about the current device and hardware configuration.
        
        Returns:
            Dict[str, Any]: Device information including CUDA availability
        """
        info = {
            "device": self.device_name,  # Utilisation de la chaîne de caractères
            "cuda_available": self.cuda_available,
            "model_size": self.model_size,
            "compute_type": self.compute_type
        }
        
        if self.cuda_available:
            info.update({
                "gpu_name": torch.cuda.get_device_name(0),
                "gpu_count": torch.cuda.device_count(),
                "cuda_version": torch.version.cuda
            })
        
        return info