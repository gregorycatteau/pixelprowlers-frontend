from django.db import models
from django.utils import timezone

# === Modèles existants ===

class JaredLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=100)
    agent = models.CharField(max_length=100)
    summary = models.CharField(max_length=255)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"[{self.timestamp}] {self.event_type} - {self.agent}"


class JaredTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminée'),
        ('blocked', 'Bloquée'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('critical', 'Critique'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assigned_to = models.CharField(max_length=100)
    created_by = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.status})"


class JaredMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=100)
    recipient = models.CharField(max_length=100)
    content = models.TextField()
    context = models.CharField(max_length=255)

    def __str__(self):
        return f"[{self.timestamp}] {self.sender} ➝ {self.recipient} ({self.context})"


class JaredConversation(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=50)
    recipient = models.CharField(max_length=50)
    content = models.TextField()
    tag = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.timestamp}] {self.sender} ➝ {self.recipient}: {self.content[:40]}..."


# === Modèles spécialisés Jared ===

class JaredStrategicAlert(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    reason = models.TextField()
    recommendation = models.TextField(blank=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"⚠️ Alerte stratégique ({'Résolue' if self.resolved else 'Active'})"


class JaredDecisionLog(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    context = models.TextField()
    decision = models.TextField()
    impact = models.TextField(blank=True)

    def __str__(self):
        return f"📌 Décision : {self.decision[:50]}..."


class JaredRoadmapUpdate(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    agent_or_theme = models.CharField(max_length=100)
    update = models.TextField()

    def __str__(self):
        return f"📍 Roadmap {self.agent_or_theme} ({self.timestamp.date()})"


class JaredDelegatedTask(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    agent_name = models.CharField(max_length=100)
    task = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"🧾 Tâche pour {self.agent_name} ({'OK' if self.completed else 'En attente'})"


class JaredPrivateNote(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self):
        return f"🔐 Note : {self.title}"


class JaredKPIReport(models.Model):
    generated_at = models.DateTimeField(default=timezone.now)
    metrics = models.JSONField()
    summary = models.TextField()

    def __str__(self):
        return f"📊 Rapport KPI ({self.generated_at.date()})"


class JaredHistoryReview(models.Model):
    reviewed_at = models.DateTimeField(default=timezone.now)
    focus = models.CharField(max_length=100, blank=True)
    findings = models.TextField()

    def __str__(self):
        return f"📖 Revue historique ({self.focus or 'Global'})"


# === Modèles liés au manifeste de PixelProwlers ===

class Manifesto(models.Model):
    version = models.CharField(max_length=10, default="1.0")
    content = models.TextField(help_text="Contenu intégral du manifeste (Markdown ou format structuré)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    current = models.BooleanField(default=True, help_text="Un seul manifeste actif à la fois")

    def __str__(self):
        return f"📜 Manifeste v{self.version} {'(actif)' if self.current else ''}"


class ManifestoVersion(models.Model):
    manifesto = models.ForeignKey(Manifesto, on_delete=models.CASCADE, related_name="versions")
    version = models.CharField(max_length=10)
    content = models.TextField()
    date_archived = models.DateTimeField(auto_now_add=True)
    archived_by = models.CharField(max_length=100)

    def __str__(self):
        return f"📚 Archive v{self.version} par {self.archived_by}"


class ManifestoUpdateSuggestion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
    ]

    suggested_by = models.CharField(max_length=100, help_text="Nom de l’agent ou personne proposant la mise à jour")
    target_version = models.CharField(max_length=10, help_text="Version cible (ex: 1.1)")
    section_reference = models.CharField(max_length=255, help_text="Référence ou extrait de la section ciblée")
    proposed_change = models.TextField(help_text="Texte proposé pour remplacement ou ajout")
    justification = models.TextField(help_text="Pourquoi cette modification ?")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"✏️ Proposition par {self.suggested_by} ➝ v{self.target_version} ({self.status})"
