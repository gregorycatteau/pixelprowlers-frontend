#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_zone.py
Validateur de blocs de zone (Zx.json) contre le schéma canonique cdn_schema_v1.1.json.

Usage:
  python validate_zone.py cdn_zones/Z3.json
  python validate_zone.py cdn_zones/ --strict --pretty

Sécurité:
- Ne charge que du JSON.
- Ne fait aucun appel réseau.
- Fournit un code retour non-zero en cas d'échec (utile en CI/CD).
"""

import argparse
import json
import sys
import hashlib
import os
from datetime import datetime
from typing import Any, Dict, List, Tuple, Union

# === Constantes ===
DEFAULT_SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "cdn_schema_v1.1.json")
ALLOWED_VISIBILITY_LEVELS = [
    "public",
    "clients",
    "project_member",
    "external_admin",
    "internal_admin",
    "ngner_only",
    "striker_only",
    "redteam_only",
    "hidden",
]

# === Utilitaires ===

def load_json(path: str) -> Dict[str, Any]:
    """Charge un fichier JSON et retourne un dict Python."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def sha256_file(path: str) -> str:
    """Retourne le SHA256 d'un fichier (hex)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def find_zone_files(target: str) -> List[str]:
    """Retourne la liste des fichiers zones (.json) à valider (fichier ou répertoire)."""
    if os.path.isdir(target):
        return sorted(
            [os.path.join(target, f) for f in os.listdir(target) if f.endswith(".json")]
        )
    if os.path.isfile(target) and target.endswith(".json"):
        return [target]
    return []

# === Validation de structure ===

def required_keys(schema: Dict[str, Any]) -> List[str]:
    """
    Détermine les clés obligatoires à partir du schéma.
    On se base sur le bloc 'structure' du schéma v1.1.
    """
    struct = schema.get("structure", {})
    keys = list(struct.keys())
    # Le schéma ne liste pas 'schema_version' mais on l'exige côté CDN (bonnes pratiques)
    keys.append("schema_version")
    # On exige 'notes' si le schéma l'a
    if "notes" in struct.keys():
        pass
    return keys

def validate_types(zone: Dict[str, Any]) -> List[str]:
    """Valide des types évidents pour éviter les erreurs grossières."""
    errors = []
    if not isinstance(zone.get("id"), str):
        errors.append("Le champ 'id' doit être une chaîne.")
    if not isinstance(zone.get("label"), str):
        errors.append("Le champ 'label' doit être une chaîne.")
    if not isinstance(zone.get("intent_scope"), list):
        errors.append("Le champ 'intent_scope' doit être une liste.")
    if not isinstance(zone.get("access_policy"), dict):
        errors.append("Le champ 'access_policy' doit être un objet.")
    if not isinstance(zone.get("structure_schema"), dict):
        errors.append("Le champ 'structure_schema' doit être un objet.")
    if not isinstance(zone.get("recommended_tags"), list):
        errors.append("Le champ 'recommended_tags' doit être une liste.")
    if not isinstance(zone.get("versioning_policy"), dict):
        errors.append("Le champ 'versioning_policy' doit être un objet.")
    if not isinstance(zone.get("security_controls"), dict):
        errors.append("Le champ 'security_controls' doit être un objet.")
    if not isinstance(zone.get("metrics_template"), dict):
        errors.append("Le champ 'metrics_template' doit être un objet.")
    return errors

def validate_access_policy(zone: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Valide la politique d'accès (erreurs + warnings)."""
    errors, warnings = [], []
    ap = zone.get("access_policy", {})
    vis_levels = ap.get("visibility_levels", [])
    if not isinstance(vis_levels, list):
        errors.append("'access_policy.visibility_levels' doit être une liste.")
        return errors, warnings

    unknown = [v for v in vis_levels if v not in ALLOWED_VISIBILITY_LEVELS]
    if unknown:
        errors.append(f"Niveaux de visibilité inconnus: {unknown}")

    if "auth_required" not in ap:
        warnings.append("Champ 'access_policy.auth_required' manquant (recommandé).")
    if "queryable_by_default" not in ap:
        warnings.append("Champ 'access_policy.queryable_by_default' manquant (recommandé).")
    if "default_sensitivity" not in ap:
        warnings.append("Champ 'access_policy.default_sensitivity' manquant (recommandé).")
    return errors, warnings

def validate_versioning_policy(zone: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Valide la politique de version/rétention."""
    errors, warnings = [], []
    vp = zone.get("versioning_policy", {})
    if vp.get("retention_policy") == "contextual":
        rr = vp.get("retention_rules", {})
        # Règles contextuelles recommandées minimales
        expected = ["prod_feature", "internal_doc", "sensitive_logs", "pentest_files"]
        for k in expected:
            if k not in rr:
                warnings.append(f"Règle de rétention '{k}' manquante dans 'retention_rules'.")
    else:
        warnings.append("Il est recommandé d'utiliser 'retention_policy': 'contextual' en v1.1.")
    return errors, warnings

def validate_metrics(zone: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    """Valide le bloc métriques (post-incident ready)."""
    errors, warnings = [], []
    m = zone.get("metrics_template", {})
    must = ["track_usage", "track_last_accessed", "track_modifications", "log_extraction_attempts", "alert_on_unauthorized_access", "anomaly_score", "forensic_hooks"]
    for k in must:
        if k not in m:
            warnings.append(f"Champ 'metrics_template.{k}' manquant (recommandé pour post-incident).")
    return errors, warnings

def validate_zone_against_schema(zone: Dict[str, Any], schema: Dict[str, Any], strict: bool) -> Tuple[bool, List[str], List[str]]:
    """Valide un bloc contre le schéma. Retourne (ok, errors, warnings)."""
    errors: List[str] = []
    warnings: List[str] = []

    # 1) Champs requis
    req = required_keys(schema)
    for k in req:
        if k not in zone:
            (errors if strict else warnings).append(f"Champ manquant: '{k}'")

    # 2) Types
    errors.extend(validate_types(zone))

    # 3) Version de schéma
    sv = zone.get("schema_version")
    if sv is None:
        (errors if strict else warnings).append("Absence de 'schema_version'. Attendu: '1.1.0'.")
    elif str(sv) != str(schema.get("schema_version", "1.1.0")):
        (errors if strict else warnings).append(f"schema_version='{sv}' différent du schéma attendu '{schema.get('schema_version','1.1.0')}'.")

    # 4) Access policy
    e, w = validate_access_policy(zone)
    errors.extend(e); warnings.extend(w)

    # 5) Versioning policy
    e, w = validate_versioning_policy(zone)
    errors.extend(e); warnings.extend(w)

    # 6) Metrics
    e, w = validate_metrics(zone)
    errors.extend(e); warnings.extend(w)

    ok = len(errors) == 0
    return ok, errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Valide un ou plusieurs blocs de zone contre cdn_schema_v1.1.json.")
    parser.add_argument("target", help="Fichier Zx.json ou dossier cdn_zones/")
    parser.add_argument("--schema", default=DEFAULT_SCHEMA_PATH, help="Chemin vers cdn_schema_v1.1.json")
    parser.add_argument("--strict", action="store_true", help="Échec si des champs manquent (sinon warnings).")
    parser.add_argument("--pretty", action="store_true", help="Affichage lisible pour humains.")
    args = parser.parse_args()

    # Charger schéma
    try:
        schema = load_json(os.path.abspath(args.schema))
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"Impossible de charger le schéma: {e}"}))
        sys.exit(2)

    files = find_zone_files(args.target)
    if not files:
        print(json.dumps({"ok": False, "error": "Aucun fichier .json trouvé à valider."}))
        sys.exit(2)

    global_ok = True
    results = []

    for path in files:
        try:
            zone = load_json(path)
            ok, errors, warnings = validate_zone_against_schema(zone, schema, args.strict)
            file_hash = sha256_file(path)
            result = {
                "file": path,
                "sha256": file_hash,
                "ok": ok,
                "errors": errors,
                "warnings": warnings,
                "checked_at": datetime.utcnow().isoformat() + "Z"
            }
            results.append(result)
            if not ok:
                global_ok = False
        except Exception as e:
            results.append({
                "file": path,
                "ok": False,
                "errors": [f"Exception: {repr(e)}"],
                "warnings": [],
                "checked_at": datetime.utcnow().isoformat() + "Z"
            })
            global_ok = False

    if args.pretty:
        # Affichage humain
        for r in results:
            status = "✅ OK" if r["ok"] else "❌ FAIL"
            print(f"\n{status} {r['file']}  (sha256={r['sha256']})")
            if r["errors"]:
                print("  Erreurs:")
                for e in r["errors"]:
                    print(f"   - {e}")
            if r["warnings"]:
                print("  Warnings:")
                for w in r["warnings"]:
                    print(f"   - {w}")
        print("")
    else:
        print(json.dumps({"ok": global_ok, "results": results}, ensure_ascii=False))

    sys.exit(0 if global_ok else 1)

if __name__ == "__main__":
    main()
