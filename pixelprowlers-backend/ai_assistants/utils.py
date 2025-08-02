# ai_assistants/utils.py

import os
from dotenv import dotenv_values

AGENTS_ENV_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "agents", ".env"
)

def get_registered_agents():
    """
    Scanne le fichier agents/.env et retourne un dictionnaire {nom_agent: id}
    pour chaque variable de type NOM_ASSISTANT_ID.
    """
    if not os.path.exists(AGENTS_ENV_PATH):
        raise FileNotFoundError(f"Le fichier .env agents est introuvable à {AGENTS_ENV_PATH}")

    env_vars = dotenv_values(AGENTS_ENV_PATH)
    agents = {}

    for key, value in env_vars.items():
        if key.endswith("_ASSISTANT_ID") and value:
            agent_name = key.replace("_ASSISTANT_ID", "").lower()
            agents[agent_name] = value

    return agents
