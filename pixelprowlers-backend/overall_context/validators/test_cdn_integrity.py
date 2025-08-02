#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_cdn_integrity.py
Audit global: cohérence entre cdn_zones, schéma, et registre.

Usage:
  python test_cdn_integrity.py --zones ./cdn_zones \
    --schema overall_context/data/cdn_schema_v1.1.json \
    --registry overall_context/data/cdn_registry.json \
    --pretty
"""

import argparse
import json
import os
from datetime import datetime
from typing import Dict, Any, List, Tuple

ALLOWED_VISIBILITY_LEVELS = [
    "public","clients","project_member","external_admin","internal_admin",
    "ngner_only","striker_only","redteam_only","hidden"
]

def load_json(p: str) -> Dict[str, Any]:
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def list_zone_files(zones_dir: str) -> List[str]:
    return sorted([
        os.path.join(zones_dir, f)
        for f in os.listdir(zones_dir)
        if f.endswith(".json")
    ])

def validate_zone(zone: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    """Validation légère (réutilise la logique clé du validateur sans l'importer)."""
    errors, warnings = [], []
    required = ["id","code","label","description","intent_scope","access_policy","structure_schema",
                "recommended_tags","versioning_policy","security_controls","metrics_template","schema_version"]
    for k in required:
        if k not in zone:
            errors.append(f"Champ manquant: {k}")

    # access policy
    ap = zone.get("access_policy", {})
    if "visibility_levels" not in ap or not isinstance(ap["visibility_levels"], list):
        errors.append("access_policy.visibility_levels absent/incorrect.")
    else:
        bad = [v for v in ap["visibility_levels"] if v not in ALLOWED_VISIBILITY_LEVELS]
        if bad:
            errors.append(f"Niveaux de visibilité inconnus: {bad}")

    # schema version
    sv = str(zone.get("schema_version"))
    expected = str(schema.get("schema_version","1.1.0"))
    if sv != expected:
        warnings.append(f"schema_version={sv}, attendu={expected} (peut nécessiter migration).")

    ok = len(errors) == 0
    return ok, errors, warnings

def main():
    parser = argparse.ArgumentParser(description="Audit d'intégrité du CDN zones/schéma/registre.")
    parser.add_argument("--zones", required=True, help="Répertoire cdn_zones/")
    parser.add_argument("--schema", required=True, help="Chemin schéma v1.1")
    parser.add_argument("--registry", required=True, help="Chemin cdn_registry.json")
    parser.add_argument("--pretty", action="store_true", help="Affichage humain.")
    args = parser.parse_args()

    schema = load_json(args.schema)
    registry = load_json(args.registry)
    files = list_zone_files(args.zones)

    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "zones_dir": args.zones,
        "checked": len(files),
        "results": [],
        "registry_sync": {
            "missing_in_registry": [],
            "ghost_in_registry": []
        }
    }

    ids_seen = set()
    for fp in files:
        try:
            zone = load_json(fp)
            ok, errs, warns = validate_zone(zone, schema)
            zid = zone.get("id", os.path.basename(fp))
            ids_seen.add(zid)
            report["results"].append({
                "file": fp,
                "zone_id": zid,
                "ok": ok,
                "errors": errs,
                "warnings": warns
            })
        except Exception as e:
            report["results"].append({
                "file": fp,
                "zone_id": None,
                "ok": False,
                "errors": [f"Exception: {repr(e)}"],
                "warnings": []
            })

    # Comparaison avec le registre
    reg_ids = {e.get("id") for e in registry.get("entries", [])}
    report["registry_sync"]["missing_in_registry"] = sorted(list(ids_seen - reg_ids))
    report["registry_sync"]["ghost_in_registry"] = sorted(list(reg_ids - ids_seen))

    if args.pretty:
        print(f"\n=== CDN INTEGRITY REPORT @ {report['timestamp']} ===")
        for r in report["results"]:
            status = "OK " if r["ok"] else "ERR"
            print(f"[{status}] {r['zone_id'] or '??'} :: {r['file']}")
            for e in r["errors"]:
                print(f"   - ERR: {e}")
            for w in r["warnings"]:
                print(f"   - WRN: {w}")
        print("\n--- Registry sync ---")
        print("  Missing in registry:", report["registry_sync"]["missing_in_registry"])
        print("  Ghost in registry  :", report["registry_sync"]["ghost_in_registry"])
        print("")
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))

    # Code retour: fail si au moins une zone invalide
    exit_code = 0 if all(r["ok"] for r in report["results"]) else 1
    raise SystemExit(exit_code)

if __name__ == "__main__":
    main()
