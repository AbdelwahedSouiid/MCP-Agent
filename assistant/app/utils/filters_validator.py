from typing import Tuple, List
from app.schemas.product_filters import ProductFilters
from app.config.logger import error_logger

class FiltersValidator:
    """
    Classe utilitaire pour la validation des filtres de produits.
    Se concentre uniquement sur la validation et la détection des features manquantes.
    """
    
    @staticmethod
    async def check_missing_features(product_filters: ProductFilters) -> Tuple[bool, List[str]]:
        """
        Vérifie uniquement les features manquantes
        
        Args:
            product_filters (ProductFilters): Les filtres extraits
            
        Returns:
            Tuple[bool, List[str]]: (has_missing_features, missing_features)
        """
        missing_features = []
        
        # Vérifier chaque feature
        if not product_filters.name:
            missing_features.append("name")
        if not product_filters.brand:
            missing_features.append("brand")
        if not product_filters.price:
            missing_features.append("price")
        if not product_filters.description or len(product_filters.description) == 0:
            missing_features.append("description")
            
        return len(missing_features) > 0, missing_features

    @staticmethod
    async def validate_basic_filters(extracted_query: ProductFilters) -> bool:
        """
        Validation basique des filtres extraits.
        
        Args:
            extracted_query (ProductFilters): Les filtres à valider
            
        Returns:
            bool: True si valide(il existe au moin un feature), False sinon(tous sont NULL)
        """
        try:
            if not isinstance(extracted_query, ProductFilters):
                error_logger.error("Format invalide: pas une instance de ProductFilters")
                return False

            # Vérifier qu'au moins un filtre est rempli
            if not any([
                extracted_query.name,
                extracted_query.brand, 
                extracted_query.price,
                extracted_query.description
            ]):
                error_logger.error("Aucun filtre rempli")
                return False

            # Validation des types
            if extracted_query.price is not None and not isinstance(extracted_query.price, (int, float)):
                error_logger.error("Prix invalide")
                return False
                
            if extracted_query.description and not isinstance(extracted_query.description, list):
                error_logger.error("Description invalide")
                return False
                
            if extracted_query.name and not isinstance(extracted_query.name, str):
                error_logger.error("Nom invalide") 
                return False
                
            if extracted_query.brand and not isinstance(extracted_query.brand, str):
                error_logger.error("Marque invalide")
                return False

            return True

        except Exception as e:
            error_logger.error(f"Erreur validation: {str(e)}")
            return False