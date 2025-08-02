from django.apps import AppConfig


class JaredDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jared_dashboard'

    from django.apps import AppConfig

    def ready(self):
        import jared_dashboard.signals  # Assure le chargement des signaux
