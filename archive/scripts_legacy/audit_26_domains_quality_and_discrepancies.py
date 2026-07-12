import os
import json
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT_DIR / "local_data" / "processed"
REGISTRY_PATH = PROCESSED_DIR / "DEFINITIVE_DATA_SOURCE_PROVENANCE_REGISTRY.json"

print("=== EXHAUSTIVE 26-DOMAIN DISCREPANCY, IMPRECISION & QUALITY AUDIT ===")

if not REGISTRY_PATH.exists():
    print("ERROR: Registry JSON not found at", REGISTRY_PATH)
    exit(1)

with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    registry = json.load(f)

print(f"Loaded {len(registry)} domains from registry.\n")

audit_results = []
regional_names_by_domain = {}
years_by_domain = {}

for entry in registry:
    d_id = entry["id"]
    p_file = entry["processed_file"].split(" & ")[0]  # Take primary file
    abs_path = ROOT_DIR / p_file
    
    if not abs_path.exists():
        print(f"[MISSING FILE] Domain {d_id}: File `{p_file}` does not exist on disk!")
        audit_results.append({
            "id": d_id,
            "status": "MISSING_FILE",
            "file": p_file,
            "rows": 0,
            "cols": 0,
            "nan_pct": 100.0,
            "issues": ["File missing from disk"]
        })
        continue
        
    try:
        if p_file.endswith(".csv"):
            df = pd.read_csv(abs_path, sep=None, engine="python", on_bad_lines="skip")
        elif p_file.endswith(".xlsx"):
            df = pd.read_excel(abs_path)
        elif p_file.endswith(".json"):
            df = pd.read_json(abs_path)
        else:
            continue
            
        rows, cols = df.shape
        nan_count = df.isna().sum().sum()
        total_cells = rows * cols
        nan_pct = round((nan_count / total_cells * 100), 2) if total_cells > 0 else 0.0
        
        issues = []
        if rows == 0:
            issues.append("Empty DataFrame (0 rows)")
        if nan_pct > 35.0:
            issues.append(f"High missing values rate ({nan_pct}% NaNs)")
            
        # Check temporal columns
        time_cols = [c for c in df.columns if any(t in c.lower() for t in ["year", "anno", "time", "period", "data"])]
        detected_years = set()
        if time_cols:
            for tc in time_cols:
                # Extract 4-digit years
                yrs = df[tc].astype(str).str.extract(r'(\d{4})')[0].dropna().unique().tolist()
                detected_years.update(yrs)
            if detected_years:
                sorted_yrs = sorted(list(detected_years))
                years_by_domain[d_id] = f"{sorted_yrs[0]}-{sorted_yrs[-1]}" if len(sorted_yrs) > 1 else sorted_yrs[0]
                
        # Check regional columns
        reg_cols = [c for c in df.columns if any(r in c.lower() for r in ["region", "regione", "reg_name", "denominazione_regione", "seder", "residenzar"])]
        if reg_cols:
            rc = reg_cols[0]
            regs = df[rc].astype(str).str.strip().str.upper().unique().tolist()
            # Clean common artifacts
            regs = [r for r in regs if r not in ["NAN", "NONE", "TOTALE", "ITALIA", "_T", "ALL"]]
            regional_names_by_domain[d_id] = set(regs)
            
        audit_results.append({
            "id": d_id,
            "status": "OK" if not issues else "ISSUES_FOUND",
            "file": p_file,
            "rows": rows,
            "cols": cols,
            "nan_pct": nan_pct,
            "time_range": years_by_domain.get(d_id, "Static/Cross-section"),
            "issues": issues
        })
        
    except Exception as e:
        print(f"[ERROR READING] Domain {d_id} (`{p_file}`): {e}")
        audit_results.append({
            "id": d_id,
            "status": "READ_ERROR",
            "file": p_file,
            "rows": 0,
            "cols": 0,
            "nan_pct": 100.0,
            "issues": [str(e)]
        })

# Check Regional Naming Discrepancies across regional panels
print("--- REGIONAL ALIGNMENT CHECK ---")
all_regional_domains = list(regional_names_by_domain.keys())
print(f"Detected {len(all_regional_domains)} regional panels: {all_regional_domains}")

if len(all_regional_domains) > 1:
    # Find canonical regional set (e.g. from INVALSI or SIOPE)
    canonical_set = regional_names_by_domain.get("invalsi_implicit_dropout", set())
    if not canonical_set and all_regional_domains:
        canonical_set = list(regional_names_by_domain.values())[0]
        
    print(f"\nCanonical Regional Reference Count: {len(canonical_set)}")
    for d_id, reg_set in regional_names_by_domain.items():
        diff_extra = reg_set - canonical_set
        diff_missing = canonical_set - reg_set
        if diff_extra or diff_missing:
            print(f"  [DISCREPANCY] `{d_id}` vs Canonical:")
            if diff_missing:
                print(f"    -> Missing standard regions: {sorted(list(diff_missing))[:5]}")
            if diff_extra:
                print(f"    -> Non-standard regional strings: {sorted(list(diff_extra))[:5]}")

print("\n--- AUDIT SUMMARY TABLE ---")
df_summary = pd.DataFrame(audit_results)
print(df_summary[["id", "status", "rows", "cols", "nan_pct", "time_range"]].to_string())

# Save complete quality audit artifact
out_audit_path = PROCESSED_DIR / "EXHAUSTIVE_26_DOMAIN_QUALITY_AUDIT_REPORT.csv"
df_summary.to_csv(out_audit_path, index=False)
print(f"\nSaved complete quality audit report to `{out_audit_path}`.")
print("=== AUDIT COMPLETE ===")
