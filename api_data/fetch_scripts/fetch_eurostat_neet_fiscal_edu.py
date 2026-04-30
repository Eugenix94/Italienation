"""
Fetch Eurostat SDMX datasets relevant to NEET, youth unemployment, education
expenditure, early school leavers, and training participation for Italy.

Eurostat SDMX 2.1 REST endpoint:
  https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{FLOW}
  Parameters: format=SDMX-CSV, startPeriod, geo=IT (where applicable)

Target dataflows (confirmed via Eurostat dataflow discovery):
  EDAT_LFSE_20   — Early leavers from education and training (all countries)
  EDAT_LFSE_22   — NEET by sex/age/training/labour status
  SDG_08_20      — NEET rate (SDG indicator, all countries)
  SDG_08_20A     — NEET rate by nationality
  TESEM150       — NEET by sex (summary indicator)
  TIPSLM80       — Youth unemployment rate 15-24
  TIPSLM90       — NEET 15-24 (TIPS indicator)
  TPS00066       — Unemployment rates by educational attainment
  EDUC_UOE_FINE06— Education expenditure as % of GDP by ISCED level
  EDUC_UOE_FINE01— Education expenditure by source and ISCED level
  SPR_EXP_FEX    — Social protection expenditure (social exclusion function)
  TRNG_LFS_19    — Participation in education/training by labour status
  TRNG_LFS_20    — Participation in education/training by citizenship
  UNE_EDUC_A     — Unemployment by sex, age and educational attainment (annual)
  YTH_EDUC_020   — Population 30-34 with tertiary education (by sex)
  YTH_EDUC_030   — Young people 20-24 with at least upper secondary education
"""

import os
import time
import requests

BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "local_data", "eurostat"
)
START_PERIOD = os.environ.get("ESTAT_START_PERIOD", "2005")

# (flow_id, label, extra_params)
# extra_params: additional query params to filter size (None = no extra filter)
DATAFLOWS = [
    ("EDAT_LFSE_20",  "early_school_leavers_detail",  {"geo": "IT"}),
    ("EDAT_LFSE_22",  "neet_detail",                  {"geo": "IT", "unit": "PC_POP"}),
    ("SDG_08_20",     "neet_sdg_all_countries",        {}),
    ("SDG_08_20A",    "neet_by_nationality",           {}),
    ("TESEM150",      "neet_by_sex_summary",           {}),
    ("TIPSLM80",      "youth_unemployment_rate",       {}),
    ("TIPSLM90",      "neet_tips_indicator",           {}),
    ("TPS00066",      "unemployment_by_education",     {}),
    ("EDUC_UOE_FINE06","educ_expenditure_pct_gdp",    {"geo": "IT"}),
    ("EDUC_UOE_FINE01","educ_expenditure_by_source",  {"geo": "IT"}),
    ("SPR_EXP_FEX",   "social_exclusion_expenditure", {"geo": "IT"}),
    ("TRNG_LFS_19",   "training_by_labour_status",    {"geo": "IT"}),
    ("TRNG_LFS_20",   "training_by_citizenship",      {"geo": "IT"}),
    ("UNE_EDUC_A",    "unemployment_by_education_age",{"geo": "IT"}),
    ("YTH_EDUC_020",  "tertiary_attainment_30_34",    {}),
    ("YTH_EDUC_030",  "upper_secondary_attainment",   {}),
]

HEADERS = {
    "Accept": "text/csv, */*",
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
}

MAX_SIZE_BYTES = 15 * 1024 * 1024   # skip files > 15MB (too broad)


def fetch_dataflow(flow_id: str, label: str, extra_params: dict) -> bool:
    out_path = os.path.join(OUTPUT_DIR, f"estat_{label}.csv")
    if os.path.exists(out_path):
        print(f"  [skip] {label} — already downloaded")
        return True

    params = {"format": "SDMX-CSV", "startPeriod": START_PERIOD}
    params.update(extra_params)

    try:
        r = requests.get(f"{BASE_URL}/{flow_id}", params=params,
                         headers=HEADERS, timeout=90, stream=True)
        if r.status_code != 200:
            print(f"  [fail] {label}: HTTP {r.status_code} — {r.text[:120]}")
            return False

        chunks = []
        total = 0
        for chunk in r.iter_content(chunk_size=65536):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_SIZE_BYTES:
                print(f"  [skip] {label}: response > {MAX_SIZE_BYTES//1024//1024}MB, skipping (add geo filter)")
                return False
            chunks.append(chunk)

        content = b"".join(chunks).decode("utf-8", errors="replace")
        if len(content) < 100:
            print(f"  [fail] {label}: empty response")
            return False

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        rows = len(content.strip().split("\n")) - 1
        print(f"  [ok]   {label} → {rows} rows, {len(content)//1024}KB")
        return True

    except requests.RequestException as e:
        print(f"  [err]  {label}: {e}")
        return False


def main():
    print(f"Fetching {len(DATAFLOWS)} Eurostat SDMX dataflows (startPeriod={START_PERIOD})")
    print(f"Output: {os.path.abspath(OUTPUT_DIR)}\n")

    ok = fail = 0
    for flow_id, label, extra in DATAFLOWS:
        success = fetch_dataflow(flow_id, label, extra)
        if success:
            ok += 1
        else:
            fail += 1
        time.sleep(1.5)

    print(f"\nDone: {ok} downloaded, {fail} failed.")


if __name__ == "__main__":
    main()
