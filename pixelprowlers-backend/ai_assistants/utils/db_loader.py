# ai_assistants/utils/db_loader.py

import json
from ai_assistants.models import Manifesto, AgentProfile, AgentSystemContext


def get_current_manifest() -> str:
    """
    Récupère le contenu du manifeste global courant (ou une version par défaut).
    """
    try:
        current = Manifesto.objects.get(current=True)
        return current.content
    except Manifesto.DoesNotExist:
        return "🚧 Aucun manifeste défini pour le moment."


def get_agent_full_profile(agent_name: str) -> dict:
    """
    Récupère le profil enrichi (JSON) de l'agent par son nom.
    """
    try:
        agent = AgentProfile.objects.get(name__iexact=agent_name)
        return {
            "name": agent.name,
            "description": agent.description,
            "model": agent.model,
            "instructions": agent.instructions,
            "tools": agent.tools,
            "security_protocol": agent.security_protocol,
            "communication_style": agent.communication_style,
            "context_enrichment": agent.context_enrichment,
            "integrations": agent.integrations,
            "learning_protocol": agent.learning_protocol,
            "usage_scope": agent.usage_scope,
            "activation_mode": agent.activation_mode,
            "dependency_matrix": agent.dependency_matrix,
            "ethical_constraints": agent.ethical_constraints,
            "execution_metrics": agent.execution_metrics,
            "emotion_profile": agent.emotion_profile,
        }
    except AgentProfile.DoesNotExist:
        return {}


def get_agent_system_context(agent_name: str) -> str:
    """
    Récupère le contexte système stocké pour un agent donné.
    """
    try:
        agent = AgentProfile.objects.get(name__iexact=agent_name)
        return agent.system_context.context_text
    except AgentProfile.DoesNotExist:
        return f"❌ Agent '{agent_name}' introuvable."
    except AgentSystemContext.DoesNotExist:
        return f"⚠️ Aucun contexte système enregistré pour l’agent '{agent_name}'."


def build_context_for_agent(agent_name: str) -> str:
    """
    Construit dynamiquement le contexte système pour un agent donné :
    - Inclut le profil enrichi de l’agent (formaté JSON)
    - Ajoute le manifeste global courant
    Résultat : string structuré prêt à être utilisé dans une requête ou enregistré.
    """
    agent_profile = get_agent_full_profile(agent_name)
    manifesto = get_current_manifest()

    if not agent_profile:
        return f"❌ Impossible de générer le contexte : agent '{agent_name}' introuvable."

    context_parts = []

    context_parts.append("🧠 PROFIL COMPLET DE L'AGENT :")
    context_parts.append(json.dumps(agent_profile, indent=2, ensure_ascii=False))

    context_parts.append("\n📜 MANIFESTE GLOBAL PARTAGÉ :")
    context_parts.append(manifesto)

    return "\n\n".join(context_parts)
