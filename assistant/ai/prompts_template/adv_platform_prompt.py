from typing import Dict, Optional
from pathlib import Path
from ai.utils.language_util import LanguageService
from app.config.logger import translate_logger, app_logger

class ADVPlatformTemplate:
    def __init__(self, data_dir: str = "ai/data/adv"):
        self.data_dir = Path(data_dir)
        self.platform_data = self._load_platform_data()
        self.language_util = LanguageService()
    
    def _load_platform_data(self) -> Dict:
        """Charge les données de la plateforme ADV depuis un fichier texte"""
        data = {"description": ""}
        try:
            with open(self.data_dir / "site_info.txt", "r", encoding="utf-8") as f:
                data['description'] = f.read().strip()
        except Exception as e:
            app_logger.error(f"Erreur lors du chargement des données: {str(e)}")
            raise
        return data
    
    async def build_prompt(self, question: str, context: str = "") -> str:
        """
        Génère un prompt structuré avec gestion des réponses inconnues
        
        Args:
            question: La question posée par l'utilisateur
            context: Contexte supplémentaire (slide actuelle, etc.)
        """
        lang = await self.language_util.get_language_instruction()
        translate_logger.info(f"Langue détectée: {lang}")
        
        prompt_template = f"""
=== PRÉSENTATION ADV - ASSISTANT POWERPOINT ===
[CONTEXTE DU PROJET]
{self.platform_data['description']}

[CONTEXTE ACTUEL]
{context if context else "Aucun contexte spécifique fourni"}

[QUESTION UTILISATEUR]
{question}

[DIRECTIVES DE RÉPONSE]
1. Si l'information existe dans le contexte :
   - Réponse concise (15-30 mots)
   - Format direct sans préambule
   - Termes techniques appropriés

2. Si l'information EST INCONNUE :
   - Répondre strictement : "Je n'ai pas d'information concernant ce point dans la présentation actuelle."
   - Ne pas inventer de réponse
   - Ne pas proposer de rechercher

[EXEMPLES]
- Bonne réponse : "Le déploiement est prévu pour Q2 2024 (voir slide 15)."
- Réponse absente : "Je n'ai pas d'information concernant ce point dans la présentation actuelle."

[INTERDICTIONS]
✖ Pas de "Je suis un assistant..."
✖ Pas d'excuses ou justifications
✖ Pas de hors-sujet
✖ Maximum 40 mots

# DIRECTIVES LINGUISTIQUES
{lang}

[RÉPONSE ATTENDUE]
"""
        return prompt_template
