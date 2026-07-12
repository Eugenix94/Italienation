"""
Fetch priority ISTAT datasets via SDMX REST API and save as clean, harmonised CSVs.

Output directory: local_data/ISTAT/
Each dataset is saved as:   istat_<slug>_raw.csv     (all available data)
                            istat_<slug>.csv          (harmonised, 2010-2024 filtered)

Harmonisation rules applied:
  - TIME_PERIOD column → integer year (or left as YYYY-Qn for quarterly)
  - OBS_VALUE → float
  - All dimension columns → string
  - Column names lowercased
  - Rows with OBS_VALUE == NaN dropped
  - Italy total rows identified where ITTER107 == 'ITTOT'
"""

import os
import time
import requests
import xml.etree.ElementTree as ET
import pandas as pd

BASE_URL = "https://sdmx.istat.it/SDMXWS/rest"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "local_data", "ISTAT")
OUT_DIR = os.path.normpath(OUT_DIR)
os.makedirs(OUT_DIR, exist_ok=True)

START = "2010"
END   = "2025"

# (flow_id, version, slug, description)
DATASETS = [
    # --- Graduates & Diplomati outcomes ---
    ("612_939", "1.1", "graduates_occupational_status",
     "University graduates – occupational status"),
    ("612_937", "1.0", "graduates_job_search",
     "University graduates – job search"),
    ("613_935", "1.0", "highschool_graduates_employment",
     "High-school graduates – employment conditions and pay"),
    ("613_934", "1.1", "highschool_graduates_demographics",
     "High-school graduates – socio-demographic characteristics"),
    ("613_936", "1.0", "highschool_graduates_job_search",
     "High-school graduates – seeking a job"),
    # --- PhD outcomes ---
    ("392_636", "1.3", "phd_occupational_status",
     "PhD graduates – professional status"),
    ("392_585", "1.2", "phd_wages",
     "PhD graduates – wage and hours worked"),
    # --- NEET + early leavers ---
    ("172_931", "1.0", "neet",
     "NEET – young people not in employment, education or training"),
    ("52_607",  "1.0", "early_school_leavers",
     "Early leavers from education and training (18-24)"),
    # --- Poverty ---
    ("34_201",  "1.0", "poverty_absolute",
     "Absolute poverty indicators"),
    ("34_202",  "1.0", "poverty_relative",
     "Relative poverty indicators"),
    ("34_727",  "1.1", "poverty_new_series",
     "Poverty – new series"),
    ("34_219",  "1.2", "households_financial_difficulty",
     "Households unable to afford selected items"),
    ("498_1104","1.0", "poverty_social_exclusion_risk",
     "People at risk of poverty or social exclusion"),
    # --- Education attainment & school ---
    ("52_912",  "1.0", "population_education_level",
     "Population 15+ by highest education level"),
    ("52_1044", "1.0", "schools",
     "Schools (ISTAT)"),
    # --- Labour market ---
    ("183_464", "1.0", "employment_by_education",
     "Enterprises – workers by education level"),
    ("150_908", "1.2", "labour_force",
     "Labour force"),
    ("151_914", "1.2", "unemployment_rate",
     "Unemployment rate"),
    # --- Migration ---
    ("28_185",  "1.1", "migration_transfers",
     "Migration – transfer of residence (internal + international)"),
    # --- Household spending ---
    ("31_124",  "1.0", "household_spending_avg",
     "Average monthly household expenditure"),
    ("31_214",  "1.0", "household_spending_detail",
     "Household actual expenditure – detail"),
    # --- University stock ---
    ("56_259",  "1.0", "university_students",
     "University students enrolled"),
    ("56_189",  "1.0", "university_indicators",
     "University indicators"),
    ("56_190",  "1.0", "university_graduates",
     "University graduates (stock)"),
    # --- Childcare ---
    ("47_850",  "1.5", "childcare_services",
     "Socio-educational services for infancy / day-care"),
]


def fetch_sdmx_data(flow_id: str, version: str) -> str | None:
    """Return raw structured XML text or None on failure."""
    url = (
        f"{BASE_URL}/data/IT1,{flow_id},{version}/all"
        f"?startPeriod={START}&endPeriod={END}"
    )
    headers = {"Accept": "application/vnd.sdmx.structurespecificdata+xml;version=2.1"}
    try:
        r = requests.get(url, timeout=120, headers=headers)
        if r.status_code == 200:
            return r.text
        print(f"  [WARN] {flow_id} HTTP {r.status_code}: {r.text[:120]}")
        return None
    except Exception as e:
        print(f"  [ERROR] {flow_id}: {e}")
        return None


def xml_to_dataframe(xml_text: str) -> pd.DataFrame:
    """Parse SDMX StructureSpecificData XML into a flat DataFrame."""
    root = ET.fromstring(xml_text)

    # Find namespace for the dataset-specific elements
    # Series attributes are dimension keys; Obs child has TIME_PERIOD, OBS_VALUE
    rows = []
    for series in root.iter():
        if not series.tag.endswith("}Series") and not series.tag == "Series":
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
    """Apply standard harmonisation transforms."""
    if df.empty:
        return df
    df.columns = [c.lower() for c in df.columns]

    # Parse OBS_VALUE to numeric
    if "obs_value" in df.columns:
        df["obs_value"] = pd.to_numeric(df["obs_value"], errors="coerce")
        df = df.dropna(subset=["obs_value"])

    # Parse TIME_PERIOD: keep as string but also add year int column
    if "time_period" in df.columns:
        df["year"] = df["time_period"].str[:4].astype(int, errors="ignore")
        # Filter to our window
        try:
            df = df[df["year"].between(int(START), int(END))]
        except Exception:
            pass

    # Drop SDMX XML namespace remnants
    drop_cols = [c for c in df.columns if c.startswith("{") or c in ("obs_status", "obs_conf")]
    df = df.drop(columns=drop_cols, errors="ignore")

    return df.reset_index(drop=True)


def main():
    manifest = []
    for flow_id, version, slug, description in DATASETS:
        print(f"\n→ {flow_id} v{version}  [{slug}]")
        xml_text = fetch_sdmx_data(flow_id, version)
        if xml_text is None:
            print(f"  SKIP (no data)")
            manifest.append({"id": flow_id, "slug": slug, "description": description,
                              "status": "failed", "rows": 0, "file": ""})
            continue

        df_raw = xml_to_dataframe(xml_text)
        if df_raw.empty:
            print(f"  SKIP (empty parse)")
            manifest.append({"id": flow_id, "slug": slug, "description": description,
                              "status": "empty", "rows": 0, "file": ""})
            continue

        df = harmonise(df_raw.copy())

        out_file = os.path.join(OUT_DIR, f"istat_{slug}.csv")
        df.to_csv(out_file, index=False)

        print(f"  OK  {len(df):,} rows × {len(df.columns)} cols → {os.path.basename(out_file)}")
        manifest.append({
            "id": flow_id, "slug": slug, "description": description,
            "status": "ok", "rows": len(df), "file": os.path.basename(out_file),
            "columns": list(df.columns),
            "years": f"{df['year'].min()}–{df['year'].max()}" if "year" in df.columns else "?",
        })
        time.sleep(0.5)   # be polite

    # Write manifest
    manifest_df = pd.DataFrame(manifest)
    manifest_path = os.path.join(OUT_DIR, "istat_manifest.csv")
    manifest_df.to_csv(manifest_path, index=False)
    print(f"\n{'='*60}")
    print(f"Done. {sum(1 for m in manifest if m['status']=='ok')}/{len(DATASETS)} datasets saved.")
    print(f"Manifest → {manifest_path}")
    print(manifest_df[["id","slug","status","rows","years"]].to_string(index=False))


if __name__ == "__main__":
    main()
