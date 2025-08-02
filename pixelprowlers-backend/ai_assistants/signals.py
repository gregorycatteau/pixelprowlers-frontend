# ai_assistants/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import (
    AgentMessageLog,
    AgentProfile,
    Manifesto,
    AgentSystemContext
)

from .utils.impact_analyzer import analyze_message_impact
from .utils.db_loader import build_context_for_agent


# ===============================
# 🔄 PROPAGATION DES MESSAGES "SHARED"
# ===============================
@receiver(post_save, sender=AgentMessageLog)
def handle_shared_agent_message(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.tags and "auto-generated" in instance.tags:
        return
    if instance.scope != 'shared':
        return

    agents = AgentProfile.objects.filter(is_active=True)
    for agent in agents:
        if agent == instance.agent:
            continue

        AgentMessageLog.objects.create(
            user=instance.user,
            agent=agent,
            message=f"📢 Message partagé par {instance.user.username} :\n\n{instance.message}",
            response="💡 Analyse requise pour évaluer l’impact sur tes tâches.",
            scope='shared',
            tags="communication partagée,impact,auto-generated",
            archived=False,
        )

        analyze_message_impact(agent, instance)


# ===============================
# 🧠 REGENERATION DU CONTEXTE SYSTEME D’UN AGENT
# ===============================
@receiver(post_save, sender=AgentProfile)
def regenerate_context_on_profile_update(sender, instance, **kwargs):
    """
    Si un profil d’agent est modifié, on régénère son contexte système.
    """
    context, _ = AgentSystemContext.objects.get_or_create(agent=instance)
    context.context_text = build_context_for_agent(instance.name)
    context.save()


@receiver(post_save, sender=Manifesto)
def regenerate_context_on_manifesto_update(sender, instance, **kwargs):
    """
    Si le manifeste global actif est modifié, on met à jour tous les contextes agents.
    """
    if not instance.current:
        return  # on n’actualise que le manifeste actif

    for agent in AgentProfile.objects.filter(is_active=True):
        context, _ = AgentSystemContext.objects.get_or_create(agent=agent)
        context.context_text = build_context_for_agent(agent.name)
        context.save()
