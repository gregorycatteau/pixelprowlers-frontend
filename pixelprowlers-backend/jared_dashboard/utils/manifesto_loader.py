import json
from jared_dashboard.models import Manifesto

def get_current_manifesto_dict() -> dict:
    """
    Récupère le manifeste actif en tant que dictionnaire Python.
    Lève une erreur si aucun manifeste actif ou si contenu invalide.
    """
    current = Manifesto.objects.filter(current=True).first()
    if not current:
        raise ValueError("Aucun manifeste actif trouvé.")
    
    try:
        return json.loads(current.content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Contenu du manifeste invalide : {e}")
