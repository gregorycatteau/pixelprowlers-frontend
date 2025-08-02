# ai_assistants/views.py

import time
import openai

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now

from .models import AgentProfile, AgentMessageLog, Manifesto, AgentSystemContext


@csrf_protect
@user_passes_test(lambda u: u.is_superuser)
def ask_agent_view(request, agent_name=None):
    """
    Vue pour interagir avec un agent IA spécifique.
    Enregistre la requête dans le log avec scope = 'shared' pour activer les signaux.
    Injecte le manifeste global actif et le contexte système de l'agent sélectionné.
    """

    response_text = ""
    agents_queryset = AgentProfile.objects.filter(is_active=True).order_by('name')
    available_agents = {a.name.lower(): a for a in agents_queryset}

    selected_agent_name = agent_name.lower() if agent_name else None
    selected_agent = available_agents.get(selected_agent_name)

    manifest_content = None
    agent_system_context = None

    try:
        manifest_content = Manifesto.objects.get(current=True).content
    except Manifesto.DoesNotExist:
        manifest_content = "⚠️ Aucun manifeste global actif trouvé."

    if request.method == "POST":
        selected_agent_name = request.POST.get("agent", "").strip().lower()
        selected_agent = available_agents.get(selected_agent_name)

        if not selected_agent:
            raise Http404(f"Agent '{selected_agent_name}' introuvable ou inactif.")

        message = request.POST.get("message", "").strip()
        if not message:
            response_text = "⚠️ Le message est vide."
        else:
            try:
                # Création du thread
                thread = openai.beta.threads.create()

                # Envoi du message utilisateur
                openai.beta.threads.messages.create(
                    thread_id=thread.id,
                    role="user",
                    content=message
                )

                # Lancement du run
                run = openai.beta.threads.runs.create(
                    thread_id=thread.id,
                    assistant_id=selected_agent.assistant_id
                )

                # Attente de la complétion
                while True:
                    current = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                    if current.status in ["completed", "failed", "cancelled"]:
                        break
                    time.sleep(0.5)

                # Récupération de la réponse
                messages = openai.beta.threads.messages.list(thread_id=thread.id)
                response_text = messages.data[0].content[0].text.value

                # Enregistrement dans le log partagé
                AgentMessageLog.objects.create(
                    user=request.user,
                    agent=selected_agent,
                    message=message,
                    response=response_text,
                    scope="shared",
                    tags="via ask_agent_view",
                )

            except Exception as e:
                response_text = f"❌ Erreur avec l’agent {selected_agent.name} : {str(e)}"

    # Récupération du contexte système de l'agent, même en GET
    if selected_agent:
        try:
            agent_system_context = selected_agent.system_context.context_text
        except AgentSystemContext.DoesNotExist:
            agent_system_context = "⚠️ Aucun contexte système défini pour cet agent."

    return render(request, "ai_assistants/ask_agents.html", {
        "response": response_text,
        "agents": agents_queryset,
        "selected_agent": selected_agent_name,
        "manifest": manifest_content,
        "agent_context": agent_system_context,
    })
