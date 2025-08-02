import os
import json
from pathlib import Path
from datetime import datetime

# === RÉPERTOIRE DU PROJET ===
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOG_DIR = PROJECT_ROOT / "overall_context" / "logs"
LOG_FILE = LOG_DIR / "backup_restore_events.jsonl"

def log_event(operation: str, zone: str, status: str, details: dict, timestamp: str = None):
    from datetime import datetime

    if timestamp is None:
        timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    event = {
        "operation": operation,
        "zone": zone,
        "status": status,
        "timestamp": timestamp,
        "details": details
    }

    log_dir = os.path.join(os.path.dirname(__file__), '../../.context_logs')
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"{zone}_log.json")

    try:
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(event)

        with open(log_file, "w") as f:
            json.dump(data, f, indent=4)

    except Exception as e:
        print(f"❌ Erreur lors de l'enregistrement du log : {e}")