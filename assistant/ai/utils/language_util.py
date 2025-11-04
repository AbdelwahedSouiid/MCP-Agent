from deep_translator import GoogleTranslator
from app.config.logger import error_logger, translate_logger
import langid
from typing import Optional, Tuple


# history injection

from app.services.history_service import HistoryService


class LanguageService:
    def __init__(self):
        self.history_service = HistoryService()
        self.supported_languages = {
            "fr": "Répondez UNIQUEMENT en français. N'utilisez aucune autre langue.",
            "en": "STRICT LANGUAGE RULE: You MUST respond in ENGLISH only. Never use other languages.",
            "ar": ".رد باللغة العربية فقط. لا تستخدم أي لغة أخرى",
            "de": "Antworten Sie NUR auf Deutsch. Verwende keine andere Sprache."
        }
        # Mapping des codes de langue vers les codes utilisés par GoogleTranslator
        self.translation_mapping = {
            'en': 'en',
            'ar': 'ar',
            'de': 'de'
        }

    def process_language(self, query: str) -> Tuple[str, str]:
        """
        Traite la langue de la requête: détection et traduction si nécessaire.
        
        Args:
            query: Texte de la requête à traiter
            
        Returns:
            Tuple contenant:
            - la requête traitée (traduite si nécessaire)
            - le code de langue détecté
        """
        # Détection de la langue
        lang = self.detect_language(query)
        translate_logger.info(f"Langue detecté : {lang}")
        # Traduction si nécessaire (vers le français)
        processed_query = query
        if(lang == 'ar'):
            processed_query = self.translate_to_french(query, lang) 
    
        return processed_query, lang

    def translate_to_french(self, query: str, source_lang: str) -> Optional[str]:
        """
        Traduit un texte vers le français si la langue source n'est pas le français.
        
        Args:
            query: Texte à traduire
            source_lang: Code langue source (fr, en, ar, etc.)
            
        Returns:
            Texte traduit en français ou None en cas d'échec
        """
        if source_lang == 'fr':
            return query  # Pas besoin de traduction
            
        try:
            if source_lang not in self.translation_mapping:
                error_logger.warning(f"Langue non supportée pour la traduction: {source_lang}")
                return query
                
            translated = GoogleTranslator(
                source=self.translation_mapping[source_lang],
                target='fr'
            ).translate(query)
            
            translate_logger.info(f"Traduction réussie: {source_lang} -> fr")
            translate_logger.info(f"Nouvelle requete en francais : {translated}")
            return translated
            
        except Exception as e:
            error_logger.error(f"Échec de traduction: {str(e)}")
            return None

    def detect_language(self, text: str) -> str:
        """Détecte la langue du texte en utilisant langid et langdetect"""
    
        if not text or not isinstance(text, str):
            error_logger.warning("Texte vide ou invalide fourni pour la détection de langue")
            return "fr"  # Langue par défaut
        try:
            # Détection avec langid
            langid_result, langid_confidence = langid.classify(text)
            return langid_result

        except Exception as e:
            error_logger.error(f"Erreur de détection de langue: {str(e)}")
            return "fr"

    async def get_language_instruction(self) -> str:
        lang = await self.history_service.get_language()
        return self.supported_languages.get(lang, self.supported_languages["fr"])

