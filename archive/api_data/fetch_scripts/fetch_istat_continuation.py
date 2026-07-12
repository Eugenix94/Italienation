"""
Continuation script: fetch remaining ISTAT datasets not yet saved.

Handles:
1. Datasets that weren't reached before the previous script was killed
2. 4 datasets that returned 404 with date filter — retried WITHOUT date filter
3. Manifest CSV generation for all fetched files
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

# Datasets still needed (flow_id, version, slug, description, use_date_filter)
REMAINING = [
    # Was being fetched when previous run was killed
    ("31_214",  "1.0", "household_spending_detail",
     "Household actual expenditure – detail", True),
    # University stock datasets
    ("56_259",  "1.0", "university_students",
     "University students enrolled", True),
    ("56_189",  "1.0", "university_indicators",
     "University indicators", True),
    ("56_190",  "1.0", "university_graduates",
     "University graduates (stock)", True),
    # Childcare
    ("47_850",  "1.5", "childcare_services",
     "Socio-educational services for infancy / day-care", True),
    # --- Retry without date filter (previously 404) ---
    ("52_607",  "1.0", "early_school_leavers",
     "Early leavers from education and training (18-24)", False),
    ("34_727",  "1.1", "poverty_new_series",
     "Poverty – new series (new definition)", False),
    ("52_912",  "1.0", "population_education_level",
     "Population 15+ by highest education level attained", False),
    ("52_1044", "1.0", "schools",
     "Schools – key indicators (ISTAT)", False),
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
        print(f"  [ERROR] {flow_id}: request timed out after 180s")
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
        series_dims = dict(series.attrib)
        for obs in series:
            row = dict(series_dims)
            row.update(obs.attrib)
            rows.append(row)
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


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
    manifest_new = []

    for flow_id, version, slug, description, use_date in REMAINING:
        out_path = os.path.join(OUT_DIR, f"istat_{slug}.csv")
        if os.path.exists(out_path):
            print(f"\n→ {flow_id}  [{slug}]  ALREADY EXISTS — skipping")
            fsize = os.path.getsize(out_path)
            manifest_new.append({
                "id": flow_id, "slug": slug, "description": description,
                "status": "already_saved",
                "rows": "?", "cols": "?",
                "file": f"istat_{slug}.csv",
                "size_kb": round(fsize / 1024, 1),
                "date_filtered": use_date,
            })
            continue

        date_tag = f" [date: {START}-{END}]" if use_date else " [NO date filter]"
        print(f"\n→ {flow_id} v{version}  [{slug}]{date_tag}")
        xml_text = fetch_sdmx_data(flow_id, version, use_date_filter=use_date)
        if xml_text is None:
            print(f"  SKIP (fetch failed)")
            manifest_new.append({
                "id": flow_id, "slug": slug, "description": description,
                "status": "failed", "rows": 0, "cols": 0, "file": "",
                "size_kb": 0, "date_filtered": use_date,
            })
            continue

        df = xml_to_dataframe(xml_text)
        if df.empty:
            print(f"  SKIP (empty parse)")
            manifest_new.append({
                "id": flow_id, "slug": slug, "description": description,
                "status": "empty", "rows": 0, "cols": 0, "file": "",
                "size_kb": 0, "date_filtered": use_date,
            })
            continue

        df = harmonise(df)
        df.to_csv(out_path, index=False)
        fsize = os.path.getsize(out_path)
        print(f"  OK  {df.shape[0]:,} rows × {df.shape[1]} cols → istat_{slug}.csv  "
              f"({round(fsize/1024,1)} KB)")
        manifest_new.append({
            "id": flow_id, "slug": slug, "description": description,
            "status": "ok", "rows": df.shape[0], "cols": df.shape[1],
            "file": f"istat_{slug}.csv",
            "size_kb": round(fsize / 1024, 1),
            "date_filtered": use_date,
        })
        time.sleep(0.5)

    # ----- Build full manifest from all CSV files in OUT_DIR -----
    print("\n\n=== Building manifest ===")
    all_files = sorted(f for f in os.listdir(OUT_DIR) if f.endswith(".csv") and f != "istat_manifest.csv")
    manifest_rows = []
    for fname in all_files:
        fpath = os.path.join(OUT_DIR, fname)
        try:
            df_tmp = pd.read_csv(fpath, nrows=0)
            full_len = sum(1 for _ in open(fpath, encoding="utf-8")) - 1
            manifest_rows.append({
                "file": fname,
                "slug": fname.replace("istat_", "").replace(".csv", ""),
                "rows": full_len,
                "cols": len(df_tmp.columns),
                "size_kb": round(os.path.getsize(fpath) / 1024, 1),
            })
        except Exception as e:
            manifest_rows.append({"file": fname, "slug": "?", "rows": "?", "cols": "?",
                                   "size_kb": "?", "error": str(e)})

    manifest_df = pd.DataFrame(manifest_rows)
    manifest_path = os.path.join(OUT_DIR, "istat_manifest.csv")
    manifest_df.to_csv(manifest_path, index=False)
    print(f"Manifest written → {manifest_path}")
    print(manifest_df.to_string(index=False))


if __name__ == "__main__":
    main()
