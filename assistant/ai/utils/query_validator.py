# ai/utils/classifier_util.py
import re
from unidecode import unidecode
from typing import List
from app.config.logger import classifier_logger as logger

class QueryValidator:
    def __init__(self):
        self._init_validation_patterns()
        
    def _init_validation_patterns(self):
        """Initialise les patterns pour détecter les requêtes non-significatives"""
        self.non_sense_patterns = [
            r'^\W*$',                     # Que des caractères spéciaux
            r'^[0-9\s]+$',                # Que des chiffres
            r'^[a-z]{1,2}$',              # 1-2 lettres seules
            r'^(\w)\1+$',                 # Répétition (ex: "aaaaa")
            r'^[^a-z0-9]{3,}$',           # 3+ caractères non alphanum
        ]
        
        self.stop_words = {
            "le", "la", "de", "un", "une", 
            "quoi", "comment", "etc", "salut"
        }
        
        self.min_length = 3
        self.min_words = 2

    def is_meaningful_query(self, text: str) -> bool:
        """
        Détermine si une requête est suffisamment significative pour être traitée.
        Retourne False pour les requêtes non-significatives.
        """
        if not isinstance(text, str):
            return False
            
        cleaned = self._normalize_text(text)
        
        # Tests basiques
        if len(cleaned) < self.min_length:
            logger.debug(f"Texte trop court: '{text}'")
            return False
            
        words = cleaned.split()
        if len(words) < self.min_words:
            logger.debug(f"Pas assez de mots: '{text}'")
            return False
            
        # Vérification des patterns
        for pattern in self.non_sense_patterns:
            if re.fullmatch(pattern, cleaned, re.IGNORECASE):
                logger.debug(f"Pattern non-significatif détecté: '{text}'")
                return False
                
        # Mots vides uniquement
        if all(word in self.stop_words for word in words):
            logger.debug(f"Stop words uniquement: '{text}'")
            return False
            
        return True

    def _normalize_text(self, text: str) -> str:
        """Normalise le texte pour l'analyse"""
        return unidecode(text.lower().strip())