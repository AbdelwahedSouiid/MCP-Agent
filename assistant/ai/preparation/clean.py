import re
from bs4 import BeautifulSoup

def clean_text(text: str) -> str:
    """Nettoie le texte en supprimant HTML, CSS et caractères spéciaux."""
    if not isinstance(text, str):
        return ""
    
    # Suppression HTML/CSS/JS
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text(separator=" ")
    text = re.sub(r'<(style|script).*?>.*?</\1>', '', text, flags=re.DOTALL)
    
    # Normalisation
    text = re.sub(r'\s+', ' ', text).strip()
    return text

