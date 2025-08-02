from django.contrib import admin
from .models import (
    JaredLog, JaredTask, JaredMessage, JaredConversation,
    JaredStrategicAlert, JaredDecisionLog, JaredRoadmapUpdate,
    JaredDelegatedTask, JaredPrivateNote, JaredKPIReport, JaredHistoryReview,
    Manifesto, ManifestoVersion, ManifestoUpdateSuggestion 
)

# === ADMIN EXISTANT ===

@admin.register(JaredLog)
class JaredLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "event_type", "agent", "summary")
    list_filter = ("event_type", "agent")
    search_fields = ("summary", "details")
    ordering = ("-timestamp",)


@admin.register(JaredTask)
class JaredTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "priority", "assigned_to", "due_date", "created_at")
    list_filter = ("status", "priority", "assigned_to")
    search_fields = ("title", "description")
    ordering = ("-priority", "due_date")
    fieldsets = (
        (None, {
            "fields": ("title", "description", "assigned_to", "created_by")
        }),
        ("Suivi", {
            "fields": ("status", "priority", "due_date")
        }),
    )


@admin.register(JaredMessage)
class JaredMessageAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "sender", "recipient", "context", "content_short")
    search_fields = ("content", "sender", "recipient", "context")
    list_filter = ("sender", "recipient", "context")
    ordering = ("-timestamp",)

    def content_short(self, obj):
        return (obj.content[:50] + "...") if len(obj.content) > 50 else obj.content
    content_short.short_description = "Message"


@admin.register(JaredConversation)
class JaredConversationAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "sender", "recipient", "tag", "preview")
    search_fields = ("sender", "recipient", "content", "tag")
    list_filter = ("sender", "recipient", "tag")
    ordering = ("-timestamp",)

    def preview(self, obj):
        return (obj.content[:60] + "...") if len(obj.content) > 60 else obj.content
    preview.short_description = "Message"

# === BLOCS STRATÉGIQUES ===

@admin.register(JaredStrategicAlert)
class JaredStrategicAlertAdmin(admin.ModelAdmin):
    list_display = ("created_at", "short_reason", "resolved")
    list_filter = ("resolved",)
    search_fields = ("reason", "recommendation")
    ordering = ("-created_at",)

    def short_reason(self, obj):
        return (obj.reason[:70] + "...") if len(obj.reason) > 70 else obj.reason
    short_reason.short_description = "Raison de l'alerte"


@admin.register(JaredDecisionLog)
class JaredDecisionLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "decision_short", "context_short")
    search_fields = ("context", "decision", "impact")
    ordering = ("-timestamp",)

    def decision_short(self, obj):
        return (obj.decision[:60] + "...") if len(obj.decision) > 60 else obj.decision

    def context_short(self, obj):
        return (obj.context[:40] + "...") if len(obj.context) > 40 else obj.context

    decision_short.short_description = "Décision"
    context_short.short_description = "Contexte"


@admin.register(JaredRoadmapUpdate)
class JaredRoadmapUpdateAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "agent_or_theme", "short_update")
    search_fields = ("agent_or_theme", "update")
    ordering = ("-timestamp",)

    def short_update(self, obj):
        return (obj.update[:60] + "...") if len(obj.update) > 60 else obj.update
    short_update.short_description = "Mise à jour"


@admin.register(JaredDelegatedTask)
class JaredDelegatedTaskAdmin(admin.ModelAdmin):
    list_display = ("created_at", "agent_name", "short_task", "completed")
    list_filter = ("completed",)
    search_fields = ("agent_name", "task")
    ordering = ("-created_at",)

    def short_task(self, obj):
        return (obj.task[:60] + "...") if len(obj.task) > 60 else obj.task
    short_task.short_description = "Tâche"


@admin.register(JaredPrivateNote)
class JaredPrivateNoteAdmin(admin.ModelAdmin):
    list_display = ("created_at", "title", "short_content")
    search_fields = ("title", "content")
    ordering = ("-created_at",)

    def short_content(self, obj):
        return (obj.content[:80] + "...") if len(obj.content) > 80 else obj.content
    short_content.short_description = "Contenu"


@admin.register(JaredKPIReport)
class JaredKPIReportAdmin(admin.ModelAdmin):
    list_display = ("generated_at", "summary_short")
    search_fields = ("summary",)
    ordering = ("-generated_at",)

    def summary_short(self, obj):
        return (obj.summary[:80] + "...") if len(obj.summary) > 80 else obj.summary
    summary_short.short_description = "Résumé KPI"


@admin.register(JaredHistoryReview)
class JaredHistoryReviewAdmin(admin.ModelAdmin):
    list_display = ("reviewed_at", "focus", "short_findings")
    search_fields = ("focus", "findings")
    ordering = ("-reviewed_at",)

    def short_findings(self, obj):
        return (obj.findings[:80] + "...") if len(obj.findings) > 80 else obj.findings
    short_findings.short_description = "Constats"

@admin.register(Manifesto)
class ManifestoAdmin(admin.ModelAdmin):
    list_display = ("version", "is_current", "created_at", "updated_at", "short_content")
    list_filter = ("current",)
    search_fields = ("version", "content")
    ordering = ("-created_at",)

    def is_current(self, obj):
        return "✅ Actif" if obj.current else "❌ Inactif"
    is_current.short_description = "Statut"

    def short_content(self, obj):
        return (obj.content[:80] + "...") if len(obj.content) > 80 else obj.content
    short_content.short_description = "Contenu"


@admin.register(ManifestoVersion)
class ManifestoVersionAdmin(admin.ModelAdmin):
    list_display = ("version", "manifesto", "archived_by", "date_archived", "short_content")
    search_fields = ("version", "archived_by", "content")
    ordering = ("-date_archived",)

    def short_content(self, obj):
        return (obj.content[:80] + "...") if len(obj.content) > 80 else obj.content
    short_content.short_description = "Contenu archivé"


@admin.register(ManifestoUpdateSuggestion)
class ManifestoUpdateSuggestionAdmin(admin.ModelAdmin):
    list_display = ("suggested_by", "target_version", "section_reference", "status", "created_at", "short_change")
    list_filter = ("status",)
    search_fields = ("suggested_by", "target_version", "section_reference", "proposed_change", "justification")
    ordering = ("-created_at",)

    def short_change(self, obj):
        return (obj.proposed_change[:60] + "...") if len(obj.proposed_change) > 60 else obj.proposed_change
    short_change.short_description = "Changement proposé"