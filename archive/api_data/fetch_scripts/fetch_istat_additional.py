"""
Fetch additional ISTAT datasets discovered via catalogue search.

Targets:
- Updated household spending series (31_739)
- More poverty indicators (incidence, intensity, thresholds, affordability)
- School data by level (158_149-260)
- New NEET series (172_1198)
- University financial statements (124_1156, 124_1157)
"""

import os
import time
import requests
import xml.etree.ElementTree as ET
import pandas as pd

BASE_URL = "https://sdmx.istat.it/SDMXWS/rest"
OUT_DIR = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "local_data", "ISTAT")
)
os.makedirs(OUT_DIR, exist_ok=True)

START = "2010"
END   = "2025"

# (flow_id, version, slug, description, use_date_filter)
NEW_DATASETS = [
    # --- Household spending — newer series ---
    ("31_739",   "1.6", "household_spending_new",
     "Household consumer spending (new series)", True),
    # --- Poverty — additional indicators ---
    ("34_178",   "1.0", "poverty_absolute_incidence",
     "Absolute poverty incidence by household type", True),
    ("34_198",   "1.0", "poverty_relative_incidence",
     "Relative poverty incidence by household type", True),
    ("34_204",   "1.0", "poverty_absolute_intensity",
     "Absolute poverty intensity", True),
    ("34_205",   "1.0", "poverty_relative_intensity",
     "Relative poverty intensity", True),
    ("34_211",   "1.0", "poverty_absolute_threshold",
     "Absolute poverty threshold", True),
    ("34_212",   "1.0", "poverty_relative_threshold",
     "Relative poverty threshold", True),
    # --- Household affordability / burden ---
    ("34_280",   "1.1", "households_cannot_afford",
     "Households cannot afford selected expenditures", True),
    ("34_216",   "1.2", "households_no_savings",
     "Households unable to save or face unexpected expenses", True),
    ("34_217",   "1.2", "households_heavy_burden",
     "Households considering some expenses a heavy burden", True),
    # --- Schools by level ---
    ("158_149",  "1.0", "schools_infanzia",
     "Pre-primary schools (scuola dell'infanzia)", True),
    ("158_150",  "1.0", "schools_primaria",
     "Primary schools (scuola primaria)", True),
    ("158_151",  "1.0", "schools_sec1",
     "Lower secondary schools (scuola sec. I grado)", True),
    ("158_260",  "1.0", "schools_sec2",
     "Upper secondary schools (scuola sec. II grado)", True),
    # --- New NEET series ---
    ("172_1198", "1.0", "neet_new",
     "NEET – updated series (172_1198)", True),
    # --- University financial statements ---
    ("124_1156", "1.0", "university_balance_sheet",
     "Universities – balance sheet (stato patrimoniale)", True),
    ("124_1157", "1.0", "university_income_statement",
     "Universities – income statement (conto economico)", True),
]


def fetch_sdmx_data(flow_id: str, version: str, use_date_filter: bool = True) -> str | None:
    if use_date_filter:
        url = (
            f"{BASE_URL}/data/IT1,{flow_id},{version}/all"
            f"?startPeriod={START}&endPeriod={END}"
        )
    else:
        url = f"{BASE_URL}/data/IT1,{flow_id},{version}/all"
    headers = {"Accept": "application/vnd.sdmx.structurespecificdata+xml;version=2.1"}
    try:
        r = requests.get(url, timeout=180, headers=headers)
        if r.status_code == 200:
            return r.text
        print(f"  [WARN] {flow_id} HTTP {r.status_code}: {r.text[:200]}")
        return None
    except requests.exceptions.Timeout:
        print(f"  [ERROR] {flow_id}: timed out after 180s")
        return None
    except Exception as e:
        print(f"  [ERROR] {flow_id}: {e}")
        return None


def xml_to_dataframe(xml_text: str) -> pd.DataFrame:
    root = ET.fromstring(xml_text)
    rows = []
    for series in root.iter():
        if not (series.tag.endswith("}Series") or series.tag == "Series"):
            continue
        dims = dict(series.attrib)
        for obs in series:
            row = dict(dims)
            row.update(obs.attrib)
            rows.append(row)
    return pd.DataFrame(rows) if rows else pd.DataFrame()


def harmonise(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df.columns = [c.lower() for c in df.columns]
    if "obs_value" in df.columns:
        df["obs_value"] = pd.to_numeric(df["obs_value"], errors="coerce")
        df = df.dropna(subset=["obs_value"])
    if "time_period" in df.columns:
        df["year"] = df["time_period"].str[:4].astype(int, errors="ignore")
        try:
            df = df[df["year"].between(int(START), int(END))]
        except Exception:
            pass
    drop_cols = [c for c in df.columns if c.startswith("{") or c in ("obs_status", "obs_conf")]
    df = df.drop(columns=drop_cols, errors="ignore")
    return df.reset_index(drop=True)


def main():
    for flow_id, version, slug, description, use_date in NEW_DATASETS:
        out_path = os.path.join(OUT_DIR, f"istat_{slug}.csv")
        if os.path.exists(out_path):
            sz = os.path.getsize(out_path)
            print(f"→ {flow_id}  [{slug}]  ALREADY EXISTS ({round(sz/1024,1)} KB) — skipping")
            continue

        tag = f"[{START}-{END}]" if use_date else "[no date filter]"
        print(f"\n→ {flow_id} v{version}  [{slug}]  {tag}")
        xml_text = fetch_sdmx_data(flow_id, version, use_date_filter=use_date)
        if xml_text is None:
            print(f"  SKIP (fetch failed)")
            continue

        df = xml_to_dataframe(xml_text)
        if df.empty:
            print(f"  SKIP (empty parse)")
            continue

        df = harmonise(df)
        df.to_csv(out_path, index=False)
        sz = os.path.getsize(out_path)
        print(f"  OK  {df.shape[0]:,} rows × {df.shape[1]} cols  ({round(sz/1024,1)} KB)")
        time.sleep(0.5)

    # Regenerate manifest
    print("\n\n=== Updating manifest ===")
    all_files = sorted(f for f in os.listdir(OUT_DIR) if f.endswith(".csv") and "manifest" not in f)
    rows = []
    for fname in all_files:
        fpath = os.path.join(OUT_DIR, fname)
        try:
            df_tmp = pd.read_csv(fpath, nrows=0)
            n_rows = sum(1 for _ in open(fpath, encoding="utf-8")) - 1
            rows.append({
                "file": fname,
                "slug": fname.replace("istat_", "").replace(".csv", ""),
                "rows": n_rows,
                "cols": len(df_tmp.columns),
                "size_kb": round(os.path.getsize(fpath) / 1024, 1),
            })
        except Exception as e:
            rows.append({"file": fname, "slug": "?", "rows": "?", "cols": "?",
                         "size_kb": "?", "error": str(e)})

    mdf = pd.DataFrame(rows)
    manifest_path = os.path.join(OUT_DIR, "istat_manifest.csv")
    mdf.to_csv(manifest_path, index=False)
    print(f"Manifest updated → {manifest_path}")
    print(mdf[["slug", "rows", "cols", "size_kb"]].to_string(index=False))


if __name__ == "__main__":
    main()
