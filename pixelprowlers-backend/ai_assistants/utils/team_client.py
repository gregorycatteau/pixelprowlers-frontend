# ai_assistants/utils/team_client.py

import os
import time
import json
import openai
from dotenv import load_dotenv
from openai import OpenAIError

# 📦 Chargement des variables d'environnement depuis le dossier agents/
AGENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agents")
load_dotenv(dotenv_path=os.path.join(AGENTS_DIR, ".env"))

# 🔐 Clé API
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📥 Fonctions de cache pour manifeste, profil agent et contexte
from .context_cache import (
    get_cached_manifest,
    get_cached_agent_profile,
    get_cached_agent_context
)

# 🔁 Récupération de l'ID OpenAI d’un agent depuis .env
def get_agent_id(agent_name: str) -> str:
    """
    Récupère l'ID OpenAI de l'agent à partir de son nom.
    """
    var_name = f"{agent_name.upper()}_ASSISTANT_ID"
    assistant_id = os.getenv(var_name)
    if not assistant_id:
        raise ValueError(f"Assistant ID non trouvé pour l'agent : {agent_name}")
    return assistant_id


# 🧠 Fonction principale : appel à l’agent
def ask_agent(agent_name: str, message: str) -> str:
    """
    Envoie un message à l'agent IA spécifié et retourne la réponse textuelle enrichie avec :
    - le manifeste global
    - le profil complet de l’agent
    - le contexte système de l’agent
    """
    try:
        assistant_id = get_agent_id(agent_name)

        # 🔄 Récupération des données contextuelles
        manifesto = get_cached_manifest()
        agent_profile = get_cached_agent_profile(agent_name)
        agent_context = get_cached_agent_context(agent_name)

        # 🧠 Construction du contexte system
        system_context = f"""
        # 📜 Manifeste global :
        {manifesto}

        # 👤 Profil complet de l'agent :
        {json.dumps(agent_profile, indent=2, ensure_ascii=False)}

        # 🧩 Contexte système spécifique :
        {agent_context}
        """

        # 🧵 Création du thread
        thread = openai.beta.threads.create()

        # 📤 Envoi du message utilisateur enrichi avec le contexte système
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"{message}\n\n---\n\n🧠 Contexte :\n{system_context.strip()}"
        )

        # ▶️ Lancement du run
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # ⏳ Attente de complétion
        while True:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            if run_status.status == "completed":
                break
            elif run_status.status in ["failed", "cancelled", "expired"]:
                raise RuntimeError(f"Le run a échoué : {run_status.status}")
            time.sleep(0.5)

        # 💬 Récupération du dernier message de l'agent
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        last_message = messages.data[0].content[0].text.value
        return last_message.strip()

    except OpenAIError as e:
        return f"❌ Erreur OpenAI : {str(e)}"
    except Exception as e:
        return f"❌ Erreur inattendue avec l’agent {agent_name} : {str(e)}"
