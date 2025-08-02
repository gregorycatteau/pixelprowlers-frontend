# ai_assistants/apps.py

from django.apps import AppConfig

class AiAssistantsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_assistants'

    def ready(self):
        # 📡 Chargement des signaux à l'initialisation de l'application
        import ai_assistants.signals  # noqa
