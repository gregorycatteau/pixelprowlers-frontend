import os
import time
import json
import openai
from dotenv import load_dotenv
from jared_dashboard.utils.manifesto_loader import get_current_manifesto_dict

# 🔍 Chargement du .env depuis agents/
AGENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "agents"))
dotenv_path = os.path.join(AGENTS_DIR, ".env")

print(f"🔎 Chargement du fichier .env depuis : {dotenv_path}")
load_dotenv(dotenv_path=dotenv_path, override=True)

# 🔐 Récupération des variables
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("JARED_ASSISTANT_ID")  # ✅ Nom corrigé

print("🧪 Clé API OpenAI :", api_key[:10] + "..." if api_key else "❌ Non trouvée")
print("🧠 ID Jared :", assistant_id if assistant_id else "❌ Non trouvé")

# 🧱 Sécurité : erreurs explicites
if not api_key:
    raise ValueError("❌ Clé API OpenAI non trouvée dans .env (clé : OPENAI_API_KEY)")
if not assistant_id:
    raise ValueError("❌ ID de Jared non trouvé dans .env (clé : JARED_ASSISTANT_ID)")

openai.api_key = api_key

def ask_jared(message: str) -> str:
    """
    Envoie un message à Jared et retourne sa réponse.
    Gère le thread, le contexte du manifeste, l'exécution et la récupération.
    """
    print(f"💬 Message envoyé à Jared : {message}")

    try:
        # 🧠 Chargement du manifeste actuel
        try:
            manifesto = get_current_manifesto_dict()
            system_message = (
                "Tu es Jared, coordinateur stratégique de PixelProwlers.\n"
                "Voici le manifeste de référence que tu dois suivre dans toutes tes réponses :\n\n"
                + json.dumps(manifesto, indent=2, ensure_ascii=False)
            )
            print("📘 Manifeste chargé et injecté dans le contexte.")
        except Exception as e:
            system_message = "Tu es Jared, coordinateur stratégique de PixelProwlers. (⚠️ Manifeste non disponible)"
            print("⚠️ Erreur de chargement du manifeste :", e)

        # 🎯 Création du thread de conversation
        print("🧵 Création du thread...")
        thread = openai.beta.threads.create()
        print(f"✅ Thread ID : {thread.id}")

        # 💬 Ajout du message système (contexte initial)
        print("📥 Envoi du message système (manifeste)...")
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="system",
            content=system_message
        )

        # ✉️ Message utilisateur
        print("📤 Envoi du message utilisateur...")
        openai.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # 🚀 Lancement du run
        print("🚀 Lancement du run avec Jared...")
        run = openai.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id
        )

        # ⏳ Attente de la complétion
        print("⏳ Attente de la complétion...")
        while True:
            current = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            print("🔄 Statut actuel :", current.status)
            if current.status in ["completed", "failed", "cancelled"]:
                break
            time.sleep(0.7)

        if current.status != "completed":
            return f"⚠️ Le run a échoué avec le statut : {current.status}"

        # ✅ Récupération de la réponse
        print("📥 Récupération des messages...")
        messages = openai.beta.threads.messages.list(thread_id=thread.id)
        print(f"📨 {len(messages.data)} messages récupérés")

        for m in reversed(messages.data):
            if m.role == "assistant":
                reply = m.content[0].text.value
                print("✅ Réponse de Jared :", reply)
                return reply

        return "⚠️ Aucun message de l'assistant trouvé."

    except Exception as e:
        print("❌ Erreur dans ask_jared :", str(e))
        return f"❌ Erreur lors de la requête à Jared : {str(e)}"
