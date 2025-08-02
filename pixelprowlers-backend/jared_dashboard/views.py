# jared_dashboard/views.py

from django.shortcuts import render, redirect
from django.utils.timezone import now, timedelta
from .models import (
    JaredLog, JaredTask, JaredMessage, JaredConversation,
    Manifesto, ManifestoUpdateSuggestion
)
from .utils.jared_client import ask_jared


def jared_dashboard_view(request):
    """
    Vue principale du cockpit Jared.
    Permet d’interagir avec l’IA, consulter les logs, tâches, messages, alertes et le manifeste.
    """
    if request.method == "POST":
        user_msg = request.POST.get("message", "").strip()
        if user_msg:
            print("🛠 Message utilisateur reçu :", user_msg)

            # 💾 Enregistrement du message utilisateur
            JaredConversation.objects.create(
                sender="user",
                recipient="jared",
                content=user_msg
            )

            # 🔁 Appel de Jared via l'API OpenAI
            try:
                print("💬 Message envoyé à Jared :", user_msg)
                jared_reply = ask_jared(user_msg)
                print("✅ Réponse de Jared :", jared_reply)
            except Exception as e:
                jared_reply = "⚠️ Une erreur est survenue lors de la réponse de Jared."
                print("❌ Erreur :", e)

            # 💾 Enregistrement de la réponse de Jared
            JaredConversation.objects.create(
                sender="jared",
                recipient="user",
                content=jared_reply
            )

            # 🚫 Protection anti double soumission
            return redirect("jared_dashboard")

    # 📊 Données à afficher dans le cockpit
    logs = JaredLog.objects.order_by("-timestamp")[:10]
    tasks = JaredTask.objects.order_by("-due_date")[:10]
    messages = JaredMessage.objects.order_by("-timestamp")[:10]
    alerts = JaredTask.objects.filter(
        due_date__lte=now() + timedelta(days=3)
    ).exclude(status="done")
    chat_messages = JaredConversation.objects.all().order_by("timestamp")[:30]

    # 📜 Récupère le manifeste actif
    current_manifesto = Manifesto.objects.filter(current=True).first()

    return render(request, "jared_dashboard/dashboard.html", {
        "logs": logs,
        "tasks": tasks,
        "messages": messages,
        "alerts": alerts,
        "chat_messages": chat_messages,
        "conversations": chat_messages,
        "current_manifesto": current_manifesto,
    })


def jared_admin_summary_view(request):
    """
    Vue secondaire affichant un résumé stratégique (par exemple depuis le menu admin).
    Peut être utilisée pour un tableau de bord allégé.
    """
    alerts = JaredTask.objects.filter(
        due_date__lte=now() + timedelta(days=3)
    ).exclude(status="done")

    return render(request, "jared_dashboard/admin_summary.html", {
        "alerts": alerts,
    })


# 🧠 Squelette futur : Suggestion de mise à jour du manifeste
def manifesto_suggestion_view(request):
    """
    (Optionnel) Formulaire de proposition de mise à jour du manifeste.
    À compléter avec un formulaire HTML ou Django Form.
    """
    if request.method == "POST":
        # Exemple : extraire les données du formulaire et créer un objet
        # À sécuriser plus tard avec user/session validation
        ManifestoUpdateSuggestion.objects.create(
            suggested_by=request.POST.get("suggested_by", "Inconnu"),
            target_version=request.POST.get("target_version", "1.1"),
            section_reference=request.POST.get("section_reference", ""),
            proposed_change=request.POST.get("proposed_change", ""),
            justification=request.POST.get("justification", "")
        )
        return redirect("jared_dashboard")  # ou autre page de confirmation

    return render(request, "jared_dashboard/manifesto_suggestion.html", {})
