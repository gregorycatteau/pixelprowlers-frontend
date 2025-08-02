# ai_assistants/admin.py

from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.timezone import now
from datetime import timedelta

from .models import (
    Manifesto,
    AgentProfile,
    AgentSystemContext,
    JaredLog,
    AgentMessageLog,
    AgentImpactReport,
)

# 👇 Ajout pour action de génération de contexte
from .utils.db_loader import build_context_for_agent


# === Admin pour AgentProfile ===

@admin.register(AgentProfile)
class AgentProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'is_active', 'has_context', 'preview_context')
    list_filter = ('model', 'is_active')
    search_fields = ('name', 'description', 'instructions')
    readonly_fields = ('updated_at',)
    actions = ['regenerate_context']

    # ✅ Action admin : régénérer le contexte système
    def regenerate_context(self, request, queryset):
        """
        Action admin pour regénérer le contexte système des agents sélectionnés.
        """
        count = 0
        for agent in queryset:
            context = build_context_for_agent(agent.name)
            obj, created = AgentSystemContext.objects.update_or_create(
                agent=agent,
                defaults={'context_text': context}
            )
            count += 1
        self.message_user(
            request,
            f"Contexte système régénéré pour {count} agent(s).",
            messages.SUCCESS
        )
    regenerate_context.short_description = "🔁 Régénérer le contexte système"

    # ✅ Affichage : le contexte existe-t-il ?
    def has_context(self, obj):
        return bool(getattr(obj, 'system_context', None))
    has_context.boolean = True
    has_context.short_description = "Contexte ?"

    # ✅ Aperçu : premier bout de texte du contexte
    def preview_context(self, obj):
        if hasattr(obj, 'system_context'):
            context = obj.system_context.context_text
            short = context[:60].replace('\n', ' ') + '...' if len(context) > 60 else context
            return format_html('<span style="color:#777;">{}</span>', short)
        return "-"
    preview_context.short_description = "Aperçu du contexte"


# === Admin pour AgentSystemContext (contexte système par agent) ===

@admin.register(AgentSystemContext)
class AgentSystemContextAdmin(admin.ModelAdmin):
    list_display = ('agent', 'short_context', 'created_at')
    search_fields = ('context_text',)
    readonly_fields = ('created_at',)

    def short_context(self, obj):
        return obj.context_text[:80] + '...' if len(obj.context_text) > 80 else obj.context_text
    short_context.short_description = "Contexte système"


# === Admin pour Manifesto (manifeste global partagé) ===

@admin.register(Manifesto)
class ManifestoAdmin(admin.ModelAdmin):
    list_display = ('version', 'current', 'updated_at')
    search_fields = ('content',)
    list_filter = ('current',)
    readonly_fields = ('created_at', 'updated_at')



# === Admin pour JaredLog (journal stratégique) ===

@admin.register(JaredLog)
class JaredLogAdmin(admin.ModelAdmin):
    list_display = (
        'short_message', 'auteur', 'agent_cible',
        'statut_colored', 'priorite_colored', 'deadline_display',
        'suivi', 'confidentiel', 'horodatage'
    )
    list_filter = (
        'statut', 'priorite', 'suivi', 'confidentiel',
        'agent_cible', 'auteur'
    )
    search_fields = ('message', 'reponse', 'tags')
    readonly_fields = ('horodatage',)

    def short_message(self, obj):
        return obj.message[:60] + ('...' if len(obj.message) > 60 else '')
    short_message.short_description = "Message"

    def statut_colored(self, obj):
        colors = {
            'todo': '#ffb703',
            'done': '#8ecae6',
            'waiting': '#ffd60a',
            'alert': '#ef233c',
            'note': '#adb5bd',
            'info': '#00b4d8',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            colors.get(obj.statut, "#ccc"),
            obj.get_statut_display()
        )
    statut_colored.short_description = "Statut"

    def priorite_colored(self, obj):
        styles = {
            'low': '#9dbf9e',
            'medium': '#f4a261',
            'high': '#e76f51',
            'critical': '#d90429',
        }
        return format_html(
            '<strong style="color: {};">{}</strong>',
            styles.get(obj.priorite, "#ccc"),
            obj.get_priorite_display()
        )
    priorite_colored.short_description = "Priorité"

    def deadline_display(self, obj):
        if not obj.deadline:
            return "-"
        delta = obj.deadline - now()
        if delta < timedelta(0):
            color = "red"
        elif delta < timedelta(days=1):
            color = "orange"
        else:
            color = "green"
        return format_html(
            '<span style="color: {};">{}</span>',
            color,
            obj.deadline.strftime("%Y-%m-%d %H:%M")
        )
    deadline_display.short_description = "Échéance"


# === Admin pour AgentMessageLog (conversations agents/humains) ===

@admin.register(AgentMessageLog)
class AgentMessageLogAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp', 'user', 'agent', 'short_message',
        'scope_colored', 'archived'
    )
    list_filter = ('agent', 'scope', 'archived')
    search_fields = ('message', 'response', 'tags')
    readonly_fields = ('timestamp',)

    def short_message(self, obj):
        return obj.message[:60] + ('...' if len(obj.message) > 60 else '')
    short_message.short_description = "Message"

    def scope_colored(self, obj):
        icons = {
            'private': '🔒',
            'personal': '👤',
            'shared': '🌍',
        }
        colors = {
            'private': '#6c757d',
            'personal': '#17a2b8',
            'shared': '#28a745',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            colors.get(obj.scope, "#000"),
            icons.get(obj.scope, "📄"),
            obj.get_scope_display()
        )
    scope_colored.short_description = "Visibilité"


# === Admin pour AgentImpactReport (analyse d’impact automatique) ===

@admin.register(AgentImpactReport)
class AgentImpactReportAdmin(admin.ModelAdmin):
    list_display = (
        'created_at', 'agent', 'message',
        'impact_level_colored', 'alert_jared'
    )
    list_filter = ('agent', 'impact_level', 'alert_jared')
    search_fields = ('summary',)
    readonly_fields = ('created_at',)

    def impact_level_colored(self, obj):
        palette = {
            'none': '#adb5bd',
            'low': '#6c757d',
            'medium': '#f4a261',
            'high': '#e76f51',
            'critical': '#d90429',
        }
        labels = {
            'none': 'Aucun',
            'low': 'Faible',
            'medium': 'Moyen',
            'high': 'Fort',
            'critical': 'Bloquant',
        }
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            palette.get(obj.impact_level, "#000"),
            labels.get(obj.impact_level, obj.impact_level)
        )
    impact_level_colored.short_description = "Niveau d'impact"
