#!/usr/bin/env python3
"""
Build ANPAL replacement panel from available NEET, employment, and transition data.

ANPAL's missing Garanzia Giovani data would have shown:
  - Youth participation in active labour market programs
  - Outcomes: employment, training, inactivity by region/year
  
This script builds the closest available substitute from:
  - NEET rates (unavailability proxy)
  - Youth unemployment
  - Employment by education
  - School-to-work transitions
  - Early school leavers (risk indicator)
"""

import pandas as pd
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
LOCAL_DATA = ROOT / "local_data"
OUTPUT_DIR = ROOT / "local_data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("Building ANPAL replacement panel from available datasets...\n")

# Core datasets to merge
datasets_to_load = {
    "neet_istat": LOCAL_DATA / "ISTAT" / "istat_neet_giovani.csv",
    "youth_unemp": LOCAL_DATA / "eurostat" / "estat_youth_unemployment_rate.csv",
    "neet_detail": LOCAL_DATA / "eurostat" / "estat_neet_detail.csv",
    "neet_migration": LOCAL_DATA / "eurostat" / "eurostat_neet_by_migration.csv",
    "esl_detail": LOCAL_DATA / "eurostat" / "estat_early_school_leavers_detail.csv",
    "emp_by_edu": LOCAL_DATA / "ISTAT" / "istat_employment_by_education.csv",
}

loaded = {}
missing = []

for key, path in datasets_to_load.items():
    try:
        if path.exists():
            df = pd.read_csv(path, low_memory=False)
            loaded[key] = df
            print(f"✓ {key:20s} → {len(df):6,d} rows")
        else:
            missing.append(key)
            print(f"✗ {key:20s} → not found")
    except Exception as e:
        missing.append(key)
        print(f"✗ {key:20s} → error: {e}")

print(f"\nLoaded {len(loaded)}/{len(datasets_to_load)} datasets\n")

# Build summary: annual NEET rate by main breakdowns (substitute for ANPAL annual outcomes)
if "neet_istat" in loaded:
    df_neet = loaded["neet_istat"].copy()
    
    # Identify numeric columns and year column
    potential_year_cols = [c for c in df_neet.columns if any(x in c.lower() for x in ['anno', 'year', 'time'])]
    potential_value_cols = [c for c in df_neet.columns if any(x in c.lower() for x in ['neet', 'value', 'tasso', 'rate', 'pct'])]
    
    if potential_year_cols and potential_value_cols:
        year_col = potential_year_cols[0]
        value_col = potential_value_cols[0]
        
        # Aggregate to annual NEET rate
        annual_neet = df_neet.groupby(year_col)[value_col].mean().reset_index()
        annual_neet.columns = ["anno", "neet_rate_pct"]
        
        out_path = OUTPUT_DIR / "anpal_replacement_neet_annual.csv"
        annual_neet.to_csv(out_path, index=False)
        print(f"✓ Annual NEET proxy saved: {out_path.name}")
    else:
        print("⚠ Could not identify year/value columns in NEET data")

# Build breakdowns: NEET by migration status (proxy for program participation equity)
if "neet_migration" in loaded:
    df_mig = loaded["neet_migration"].copy()
    out_path = OUTPUT_DIR / "anpal_replacement_neet_by_migration.csv"
    
    # Keep as-is (already stratified by citizenship/migration)
    df_mig.to_csv(out_path, index=False)
    print(f"✓ NEET by migration status saved: {out_path.name}")

# Build transition proxy: youth unemployment as job-placement proxy
if "youth_unemp" in loaded:
    df_yunemp = loaded["youth_unemp"].copy()
    out_path = OUTPUT_DIR / "anpal_replacement_youth_unemployment.csv"
    
    df_yunemp.to_csv(out_path, index=False)
    print(f"✓ Youth unemployment (placement inverse): {out_path.name}")

# Build risk indicator: early school leavers
if "esl_detail" in loaded:
    df_esl = loaded["esl_detail"].copy()
    out_path = OUTPUT_DIR / "anpal_replacement_early_school_leavers.csv"
    
    df_esl.to_csv(out_path, index=False)
    print(f"✓ Early school leavers (pre-program risk): {out_path.name}")

# Create a manifest explaining the replacement datasets
manifest = {
    "title": "ANPAL Replacement Dataset Package (May 2026)",
    "context": "ANPAL Garanzia Giovani data not available from official sources; using public Eurostat/ISTAT substitutes.",
    "datasets": {
        "anpal_replacement_neet_annual.csv": {
            "description": "Annual NEET rate (proxy for Youth Guarantee population)",
            "source": "ISTAT",
            "columns": ["anno (year)", "neet_rate_pct (% not in employment/education/training)"],
            "use_case": "Track aggregate youth exclusion trend"
        },
        "anpal_replacement_neet_by_migration.csv": {
            "description": "NEET by citizenship/migration status (equity breakdown)",
            "source": "Eurostat",
            "use_case": "Assess program effectiveness across migrant vs. native youth"
        },
        "anpal_replacement_youth_unemployment.csv": {
            "description": "Youth (15-24) unemployment rate (job-placement proxy)",
            "source": "Eurostat",
            "use_case": "Inverse of employment outcomes; shows non-placement rate"
        },
        "anpal_replacement_early_school_leavers.csv": {
            "description": "Early school leavers (18-24) by education status (pre-program risk indicator)",
            "source": "Eurostat",
            "use_case": "Identify target population for intervention"
        }
    },
    "limitations": [
        "Eurostat/ISTAT data are observed outcomes, not program participation/placement counts",
        "No regional breakdown by Garanzia Giovani jurisdiction",
        "No intervention-type splits (training vs. job subsidy vs. direct employment)",
        "Annual or quarterly granularity; ANPAL may report monthly"
    ],
    "how_to_use": [
        "Merge these files by year to create a multi-indicator NEET/unemployment dashboard",
        "Use NEET annual as the baseline population metric",
        "Use migration breakdown to assess equity of unmet need",
        "Use youth unemployment to estimate placement gap (100% - employment rate = NEET proxy)",
        "Use early school leavers to understand the pre-program risk population"
    ]
}

manifest_path = OUTPUT_DIR / "anpal_replacement_manifest.json"
with open(manifest_path, "w") as f:
    json.dump(manifest, f, indent=2)
print(f"\n✓ Manifest saved: {manifest_path.name}\n")

print("ANPAL replacement panel complete.")
print("\nNext: Import these files into the transition notebook to replace missing ANPAL data.")
