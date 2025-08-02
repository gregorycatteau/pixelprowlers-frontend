# ai_assistants/file_reader.py

import os

# Répertoire de base des composants Nuxt
FRONTEND_COMPONENTS_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../pixelprowlers-frontend/components')
)

def read_vue_file(filename: str) -> str:
    # Sécurité : éviter les traversals type "../../"
    if ".." in filename or filename.startswith("/"):
        return "❌ Nom de fichier invalide."

    full_path = os.path.join(FRONTEND_COMPONENTS_PATH, filename)

    if not os.path.exists(full_path):
        return f"❌ Le fichier '{filename}' n'existe pas."

    try:
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"❌ Erreur lors de la lecture : {str(e)}"
