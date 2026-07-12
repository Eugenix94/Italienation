import os
import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
LOCAL_DATA = ROOT_DIR / "local_data"
PROCESSED_DIR = LOCAL_DATA / "processed"

print("=== STARTING PRECISION & DISCREPANCY RESOLUTION BRIDGE ===")

# 1. Fix OpenCoesione School Digital Projects Summary (`DEN_REGIONE`)
print("1. Fixing OpenCoesione School Digital Projects Summary...")
oc_path = LOCAL_DATA / "OpenCoesione" / "structural_projects" / "opencoesione_digital_projects_all_cycles" / "progetti_esteso_RETI_SERVIZI_DIGITALI_20251231.csv"
oc_out = PROCESSED_DIR / "opencoesione_school_digital_projects_summary.csv"

if oc_path.exists():
    try:
        df_oc = pd.read_csv(oc_path, sep=None, engine="python", on_bad_lines="skip")
        if "DEN_REGIONE" in df_oc.columns:
            # Group by region and sum public financing
            df_oc["FINANZ_TOTALE_PUBBLICO"] = pd.to_numeric(df_oc["FINANZ_TOTALE_PUBBLICO"].astype(str).str.replace(",", "."), errors="coerce").fillna(0)
            df_sum = df_oc.groupby(["COD_REGIONE", "DEN_REGIONE"]).agg(
                total_projects=("COD_LOCALE_PROGETTO", "count"),
                total_public_funding=("FINANZ_TOTALE_PUBBLICO", "sum")
            ).reset_index()
            # Clean regional strings
            df_sum["DEN_REGIONE"] = df_sum["DEN_REGIONE"].astype(str).str.strip().str.upper()
            df_sum.to_csv(oc_out, index=False, encoding="utf-8")
            print(f"  -> Successfully fixed `{oc_out}` (`{len(df_sum)}` regions mapped using `DEN_REGIONE`)")
        else:
            print("  [WARNING] `DEN_REGIONE` column not found in OpenCoesione CSV.")
    except Exception as e:
        print(f"  [ERROR] OpenCoesione fix failed: {e}")

# 2. Fix SIOPE Expenditure Regional Mapping (`Codice Regione ISTAT to Name`)
print("2. Mapping SIOPE Expenditure by Region to Canonical Regional Names...")
siope_path = PROCESSED_DIR / "siope_expenditure_by_region_year.csv"
siope_clean_path = PROCESSED_DIR / "siope_expenditure_by_region_clean.csv"

istat_reg_map = {
    "1.0": "PIEMONTE", "2.0": "VALLE D'AOSTA", "3.0": "LOMBARDIA", "4.0": "TRENTINO-ALTO ADIGE",
    "5.0": "VENETO", "6.0": "FRIULI VENEZIA GIULIA", "7.0": "LIGURIA", "8.0": "EMILIA ROMAGNA",
    "9.0": "TOSCANA", "10.0": "UMBRIA", "11.0": "MARCHE", "12.0": "LAZIO", "13.0": "ABRUZZO",
    "14.0": "MOLISE", "15.0": "CAMPANIA", "16.0": "PUGLIA", "17.0": "BASILICATA", "18.0": "CALABRIA",
    "19.0": "SICILIA", "20.0": "SARDEGNA"
}

if siope_path.exists():
    try:
        df_siope = pd.read_csv(siope_path)
        # Melt from wide to long or create mapped columns
        long_rows = []
        for _, row in df_siope.iterrows():
            anno = row["anno"]
            for col, reg_name in istat_reg_map.items():
                if col in df_siope.columns:
                    long_rows.append({
                        "anno": anno,
                        "codice_regione": col,
                        "denominazione_regione": reg_name,
                        "spesa_siope_cassa": row[col]
                    })
        df_long = pd.DataFrame(long_rows)
        df_long.to_csv(siope_clean_path, index=False, encoding="utf-8")
        print(f"  -> Successfully created clean SIOPE regional panel `{siope_clean_path}` (`{len(df_long)}` regional-year observations)")
    except Exception as e:
        print(f"  [ERROR] SIOPE fix failed: {e}")

print("=== PRECISION & DISCREPANCY RESOLUTION COMPLETE ===")
