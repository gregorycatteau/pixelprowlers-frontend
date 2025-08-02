from .models import JaredStrategicAlert

def jared_alert_banner(request):
    """
    Renvoie True + message si au moins une alerte critique non résolue existe.
    Accessible dans tous les templates admin via {{ jared_alert }}
    """
    alerts = JaredStrategicAlert.objects.filter(resolved=False)
    return {
        "jared_alert": alerts.first() if alerts.exists() else None
    }
