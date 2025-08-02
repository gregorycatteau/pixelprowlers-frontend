import os
import sys
import json
import hashlib
from datetime import datetime, timezone
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# === IMPORT LOGGER ===
from backup_event_logger import log_event

# === RÉPERTOIRE RACINE DU PROJET ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../../'))

# === CHARGEMENT .env.development ===
env_path = os.path.join(PROJECT_ROOT, '.env.development')
if not os.path.exists(env_path):
    print("❌ Fichier .env.development introuvable à la racine du projet.")
    sys.exit(1)

load_dotenv(dotenv_path=env_path)
BACKUP_KEY = os.getenv("BACKUP_KEY")

if not BACKUP_KEY:
    print("❌ BACKUP_KEY manquante dans .env.development")
    sys.exit(1)

# === INITIALISATION DU CRYPTAGE ===
try:
    FERNET = Fernet(BACKUP_KEY.encode())
except Exception as e:
    print(f"❌ Erreur de clé Fernet : {e}")
    sys.exit(1)

# === PARAMÈTRES DU SCRIPT ===
if len(sys.argv) != 2:
    print("Usage : python backup_encryptor.py <nom_du_fichier.json>")
    sys.exit(1)

zone_file = sys.argv[1]
zone_path = os.path.join(PROJECT_ROOT, 'cdn_zones', zone_file)

if not os.path.isfile(zone_path):
    print(f"❌ Fichier {zone_file} introuvable dans cdn_zones/")
    sys.exit(1)

# === LECTURE + CHIFFREMENT ===
with open(zone_path, "rb") as f:
    data = f.read()

encrypted_data = FERNET.encrypt(data)
file_hash = hashlib.sha256(encrypted_data).hexdigest()
timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

zone_name = zone_file.split(".")[0]
output_filename = f"{zone_name}__{timestamp}.bin"
manifest_filename = f"{zone_name}__{timestamp}.json"

# === ÉCRITURE DES FICHIERS ===
backup_dir = os.path.join(PROJECT_ROOT, '.context_backups')
os.makedirs(backup_dir, exist_ok=True)

output_path = os.path.join(backup_dir, output_filename)
manifest_path = os.path.join(backup_dir, manifest_filename)

with open(output_path, "wb") as f:
    f.write(encrypted_data)

manifest = {
    "zone": zone_name,
    "original_file": zone_file,
    "timestamp_utc": timestamp,
    "encrypted_file": output_filename,
    "hash_sha256": file_hash,
    "backup_agent": "backup_encryptor.py",
    "context_source": "cdn_zones/"
}

with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)

# === ENREGISTREMENT DANS LE LOGGER ===
log_event(
    operation="backup",
    zone=zone_name,
    status="success",
    timestamp=timestamp,
    details={
        "manifest_file": manifest_filename,
        "encrypted_file": output_filename,
        "hash": file_hash
    }
)

print(f"\n✅ Sauvegarde réussie : {output_filename}")
print(f"📄 Manifest associé : {manifest_filename}")
