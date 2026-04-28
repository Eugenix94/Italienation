"""
Helper script for downloading and validating the 3 manual datasets.

This script provides guidance and automated validation for:
  1. PIAAC adult skills data
  2. INVALSI regional test scores
  3. ANPAL Youth Guarantee outcomes

Once you download the files manually, place them in the appropriate directories
and run this script to validate structure and integrate with the main analysis.

Usage:
    .venv\\Scripts\\python.exe api_data/fetch_scripts/validate_manual_downloads.py
"""

import json
from pathlib import Path
from datetime import datetime

import pandas as pd

print(f"Manual downloads validator  —  {datetime.now():%Y-%m-%d %H:%M}\n")

ROOT = Path(__file__).resolve().parent.parent.parent
LOCAL_DATA = ROOT / "local_data"

# ─────────────────────────────────────────────────────────────────────────────
# Configuration: expected file locations and validation rules
# ─────────────────────────────────────────────────────────────────────────────

MANUAL_DATASETS = {
    "piaac": {
        "name": "OECD PIAAC Adult Skills (1st Cycle)",
        "dir": LOCAL_DATA / "oecd",
        "filename": "oecd_piaac_adult_skills.csv",
        "min_rows": 10,
        "source_url": "https://www.oecd.org/skills/piaac/data/",
        "instructions": """
            1. Visit: https://www.oecd.org/skills/piaac/data/
            2. Click: "PIAAC 1st cycle database and materials"
            3. Click: "PIAAC database" → "Public Use Files (PUF)"
            4. Download the Italy file (or extract from the country-level statistics CSV)
            5. Save as: local_data/oecd/oecd_piaac_adult_skills.csv
        """,
        "expected_columns": ["country", "year", "literacy", "numeracy", "problem_solving"],
    },
    "invalsi": {
        "name": "INVALSI Regional Test Scores",
        "dir": LOCAL_DATA / "INVALSI",
        "filename": "invalsi_results.csv",
        "min_rows": 100,
        "source_url": "https://invalsi-open.net/data/",
        "instructions": """
            1. Visit: https://invalsi-open.net/data/
            2. Download: "Base dati" → "Risultati scuola" (by region and grade)
            3. Extract Italian regions (Piemonte, Lombardia, etc.)
            4. Save as: local_data/INVALSI/invalsi_results.csv
        """,
        "expected_columns": ["regione", "anno", "grado", "italiano", "matematica"],
    },
    "anpal": {
        "name": "ANPAL Youth Guarantee Outcomes",
        "dir": LOCAL_DATA / "ANPAL",
        "filename": "anpal_youth_guarantee.csv",
        "min_rows": 50,
        "source_url": "https://www.anpal.gov.it/statistiche/garanzia-giovani",
        "instructions": """
            1. Visit: https://www.anpal.gov.it/statistiche/garanzia-giovani
            2. Download: "Risultati annuali" or "Destinazioni" CSV
            3. Extract outcomes (occupied, in training, etc.) by region/year
            4. Save as: local_data/ANPAL/anpal_youth_guarantee.csv
        """,
        "expected_columns": ["regione", "anno", "occupati", "in_formazione", "neet"],
    },
}


def check_dataset(key: str, config: dict) -> dict:
    """Check if a dataset exists, validate structure, report status."""
    result = {
        "key": key,
        "name": config["name"],
        "exists": False,
        "valid": False,
        "rows": 0,
        "columns": [],
        "errors": [],
    }

    config["dir"].mkdir(parents=True, exist_ok=True)
    filepath = config["dir"] / config["filename"]

    if not filepath.exists():
        result["errors"].append(
            f"File not found: {filepath.relative_to(ROOT)}\n"
            f"Download instructions:\n{config['instructions']}"
        )
        return result

    result["exists"] = True

    try:
        df = pd.read_csv(filepath, low_memory=False)
    except Exception as e:
        result["errors"].append(f"Failed to read CSV: {e}")
        return result

    result["rows"] = len(df)
    result["columns"] = df.columns.tolist()

    if result["rows"] < config["min_rows"]:
        result["errors"].append(
            f"Too few rows: {result['rows']} < {config['min_rows']} (minimum)"
        )
    else:
        result["valid"] = True

    return result


def report_status():
    """Check all 3 datasets and print validation report."""
    print("=" * 80)
    print("MANUAL DATASET VALIDATION")
    print("=" * 80)

    results = {}
    for key, config in MANUAL_DATASETS.items():
        results[key] = check_dataset(key, config)

    # ─────────────────────────────────────────────────────────────────────────
    # Print results
    # ─────────────────────────────────────────────────────────────────────────

    for key, result in results.items():
        status_icon = "✓" if result["valid"] else "✗"
        print(f"\n{status_icon} {result['name']}")
        print(f"   Location: {MANUAL_DATASETS[key]['dir'].relative_to(ROOT)} / {MANUAL_DATASETS[key]['filename']}")

        if result["exists"]:
            print(f"   Status: EXISTS")
            print(f"   Rows: {result['rows']:,}")
            print(f"   Columns: {', '.join(result['columns'][:5])}{'...' if len(result['columns']) > 5 else ''}")
        else:
            print(f"   Status: MISSING")

        if result["errors"]:
            for err in result["errors"]:
                print(f"   ERROR: {err}")

    # ─────────────────────────────────────────────────────────────────────────
    # Summary
    # ─────────────────────────────────────────────────────────────────────────

    valid_count = sum(1 for r in results.values() if r["valid"])
    total_count = len(results)

    print("\n" + "=" * 80)
    print(f"SUMMARY: {valid_count}/{total_count} datasets valid")
    print("=" * 80)

    if valid_count == total_count:
        print("\n✓ All manual datasets are ready for integration!")
        print("  Run: python scripts/integrate_manual_datasets.py")
    elif valid_count > 0:
        print(f"\n⚠ {total_count - valid_count} dataset(s) still needed:")
        for key, result in results.items():
            if not result["valid"]:
                print(f"\n  {result['name']}")
                print(f"  {MANUAL_DATASETS[key]['source_url']}")
    else:
        print("\n✗ No manual datasets found. Please download them first.")

    # ─────────────────────────────────────────────────────────────────────────
    # Save manifest
    # ─────────────────────────────────────────────────────────────────────────

    manifest_path = LOCAL_DATA / "manual_datasets_manifest.json"
    manifest = {
        "checked_at": datetime.now().isoformat(),
        "datasets": results,
    }
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"\nManifest saved: {manifest_path.relative_to(ROOT)}")


if __name__ == "__main__":
    report_status()
