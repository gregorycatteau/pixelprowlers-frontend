from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

# === 1. Manifeste global partagé ===

class Manifesto(models.Model):
    version = models.CharField(max_length=10, default="1.0")
    content = models.TextField(help_text="Contenu intégral du manifeste (JSON ou Markdown)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    current = models.BooleanField(default=True, help_text="Un seul manifeste actif à la fois")

    class Meta:
        verbose_name = "Manifeste Global"
        verbose_name_plural = "Manifestes"

    def __str__(self):
        return f"📜 Manifeste v{self.version} {'(actif)' if self.current else ''}"


# === 2. Profils des agents IA ===

class AgentProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    assistant_id = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    instructions = models.TextField()
    model = models.CharField(max_length=50, default="gpt-4o")
    temperature = models.FloatField(default=0.7)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    tools = models.JSONField(default=list, blank=True)
    security_protocol = models.JSONField(default=dict, blank=True)
    communication_style = models.JSONField(default=dict, blank=True)
    context_enrichment = models.JSONField(default=dict, blank=True)
    integrations = models.JSONField(default=dict, blank=True)
    learning_protocol = models.JSONField(default=dict, blank=True)
    usage_scope = models.JSONField(default=dict, blank=True)
    activation_mode = models.JSONField(default=dict, blank=True)
    dependency_matrix = models.JSONField(default=dict, blank=True)
    ethical_constraints = models.JSONField(default=dict, blank=True)
    execution_metrics = models.JSONField(default=dict, blank=True)
    emotion_profile = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Profil d'Agent IA"
        verbose_name_plural = "Profils des Agents IA"

    def __str__(self):
        return f"🤖 {self.name} ({self.model})"


# 👇 ajouté pour stocker le contexte system global des agents
class AgentSystemContext(models.Model):
    agent = models.OneToOneField(AgentProfile, on_delete=models.CASCADE, related_name='system_context')
    context_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"System Context for {self.agent.name}"
# ☝️ fin de l'ajout


# === 3. Journal d’activité de Jared ===

class JaredLog(models.Model):
    STATUT_CHOICES = [
        ('todo', 'À faire'),
        ('done', 'Terminé'),
        ('waiting', 'En attente'),
        ('alert', 'Alerte'),
        ('note', 'Note privée'),
        ('info', 'Information'),
    ]

    PRIORITE_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyenne'),
        ('high', 'Élevée'),
        ('critical', 'Critique'),
    ]

    horodatage = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    agent_cible = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    reponse = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='info')
    priorite = models.CharField(max_length=10, choices=PRIORITE_CHOICES, default='medium')
    tags = models.CharField(max_length=255, blank=True)
    deadline = models.DateTimeField(blank=True, null=True)
    suivi = models.BooleanField(default=True)
    confidentiel = models.BooleanField(default=False)

    class Meta:
        ordering = ['-horodatage']
        verbose_name = "Entrée du Journal de Jared"
        verbose_name_plural = "Journal Stratégique de Jared"

    def __str__(self):
        return f"[{self.horodatage.strftime('%Y-%m-%d %H:%M')}] {self.message[:60]}..."


# === 4. Journal des conversations agents/humains ===

class AgentMessageLog(models.Model):
    SCOPE_CHOICES = [
        ('private', 'Privé (hors contexte professionnel)'),
        ('personal', 'Personnel (lié à une mission de l’agent)'),
        ('shared', 'Partagé (visible par tous les agents et Jared)'),
    ]

    STATUT_CHOICES = [
        ('info', 'Info'),
        ('alert', 'Alerte'),
        ('decision', 'Décision'),
        ('todo', 'Tâche'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('critical', 'Critique'),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE, related_name="logs")
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    scope = models.CharField(max_length=20, choices=SCOPE_CHOICES, default='personal')
    tags = models.CharField(max_length=255, blank=True)
    archived = models.BooleanField(default=False)

    # Champs supplémentaires utilisés dans les signaux
    auteur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="auteur_logs")
    agent_cible = models.CharField(max_length=100, blank=True)
    reponse = models.TextField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='info')
    priorite = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    confidentiel = models.BooleanField(default=False)
    suivi = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Message entre utilisateur et agent"
        verbose_name_plural = "Journal des Conversations IA"

    def __str__(self):
        return f"💬 [{self.timestamp.strftime('%Y-%m-%d %H:%M')}] {self.agent.name} - {self.scope}"


# === 5. Rapports d'impact automatiques (réaction à un message partagé) ===

class AgentImpactReport(models.Model):
    IMPACT_LEVEL_CHOICES = [
        ('none', 'Aucun'),
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('high', 'Fort'),
        ('critical', 'Bloquant'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    agent = models.ForeignKey(AgentProfile, on_delete=models.CASCADE)
    message = models.ForeignKey(AgentMessageLog, on_delete=models.CASCADE)
    impact_level = models.CharField(max_length=20, choices=IMPACT_LEVEL_CHOICES, default='none')
    summary = models.TextField()
    alert_jared = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Rapport d'Impact Automatique"
        verbose_name_plural = "Rapports d'Impact IA"

    def __str__(self):
        return f"📊 {self.agent.name} → impact `{self.impact_level}` sur message {self.message.id}"
