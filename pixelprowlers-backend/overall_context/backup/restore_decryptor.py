import os
import sys
import json
import hashlib
from datetime import datetime, timezone
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pathlib import Path

# === CHEMIN RACINE POUR L'IMPORT DES MODULES DE L'APP DJANGO ===
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, '../../'))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# === IMPORTS INTERNES ===
try:
    from backup_event_logger import log_event
    from overall_context.validators.post_restore_validator import validate_file
except ImportError as e:
    print(f"❌ Erreur d'import : {e}")
    sys.exit(1)

# === CHARGEMENT DE LA CLÉ DE CHIFFREMENT ===
env_path = os.path.join(PROJECT_ROOT, '.env.development')
if not os.path.exists(env_path):
    print("❌ Fichier .env.development introuvable à la racine du projet.")
    sys.exit(1)

load_dotenv(dotenv_path=env_path)
BACKUP_KEY = os.getenv("BACKUP_KEY")

if not BACKUP_KEY:
    print("❌ BACKUP_KEY manquante dans .env.development")
    sys.exit(1)

# === INITIALISATION DE FERNET ===
try:
    FERNET = Fernet(BACKUP_KEY.encode())
except Exception as e:
    print(f"❌ Erreur de clé Fernet : {e}")
    sys.exit(1)

# === RÉCUPÉRATION DU FICHIER BIN ===
if len(sys.argv) != 2:
    print("Usage : python restore_decryptor.py <nom_du_fichier.bin>")
    sys.exit(1)

bin_file = sys.argv[1]
backup_dir = os.path.join(PROJECT_ROOT, '.context_backups')
bin_path = os.path.join(backup_dir, bin_file)

if not os.path.isfile(bin_path):
    print(f"❌ Fichier introuvable : {bin_path}")
    sys.exit(1)

# === LECTURE DU MANIFEST ASSOCIÉ ===
manifest_file = bin_file.replace(".bin", ".json")
manifest_path = os.path.join(backup_dir, manifest_file)

if not os.path.isfile(manifest_path):
    print(f"❌ Manifest introuvable : {manifest_path}")
    sys.exit(1)

with open(bin_path, "rb") as f:
    encrypted_data = f.read()

with open(manifest_path, "r") as f:
    manifest = json.load(f)

expected_hash = manifest.get("hash_sha256")
computed_hash = hashlib.sha256(encrypted_data).hexdigest()
zone_name = manifest.get("zone", "unknown")
timestamp = manifest.get("timestamp_utc", datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))

# === VÉRIFICATION DU HASH ===
if expected_hash != computed_hash:
    print("❌ Le hash ne correspond pas ! Fichier corrompu ou modifié.")
    log_event(
        operation="restore",
        zone=zone_name,
        status="failed",
        timestamp=timestamp,
        details={
            "error": "hash_mismatch",
            "bin_file": bin_file,
            "expected": expected_hash,
            "computed": computed_hash
        }
    )
    sys.exit(1)

# === DÉCHIFFREMENT ===
try:
    decrypted_data = FERNET.decrypt(encrypted_data)
except Exception as e:
    print(f"❌ Erreur de déchiffrement : {e}")
    log_event(
        operation="restore",
        zone=zone_name,
        status="failed",
        timestamp=timestamp,
        details={"error": str(e), "bin_file": bin_file}
    )
    sys.exit(1)

# === ÉCRITURE DU FICHIER RESTAURÉ ===
zone_file = manifest["original_file"]
restored_path = os.path.join(PROJECT_ROOT, 'cdn_zones', zone_file)

try:
    with open(restored_path, "wb") as f:
        f.write(decrypted_data)
except Exception as e:
    print(f"❌ Impossible d’écrire le fichier restauré : {e}")
    sys.exit(1)

log_event(
    operation="restore",
    zone=zone_name,
    status="success",
    timestamp=timestamp,
    details={"restored_file": zone_file, "manifest": manifest_file}
)

print(f"\n✅ Fichier restauré : {zone_file}")
print(f"📁 Localisation : cdn_zones/{zone_file}")

# === VALIDATION POST-RESTAURATION ===
print("\n🔍 Validation post-restauration en cours...")

try:
    schema_path = os.path.join(PROJECT_ROOT, 'overall_context', 'data', 'cdn_schema_operational_v1.json')

    result, messages = validate_file(restored_path, schema_path)

    for msg in messages:
        print("🔹", msg)

    if not result:
        log_event(
            operation="restore_validation",
            zone=zone_name,
            status="warning",
            timestamp=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
            details={
                "file": zone_file,
                "issues": messages
            }
        )
        print("⚠️ Validation terminée avec des avertissements.")
    else:
        print("✅ Validation complète réussie.")

except Exception as e:
    print(f"❌ Erreur pendant la validation post-restauration : {e}")
    log_event(
        operation="restore_validation",
        zone=zone_name,
        status="error",
        timestamp=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"),
        details={"error": str(e), "file": zone_file}
    )
