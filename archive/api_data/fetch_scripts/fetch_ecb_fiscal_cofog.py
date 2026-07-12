"""
Fetch ECB SDMX datasets relevant to Italy government finance, COFOG education
spending, and tax receipts.

ECB SDMX 2.1 REST endpoint: https://data-api.ecb.europa.eu/service/data/{flow}/{key}
  format=csvdata  (ECB uses 'csvdata' not 'SDMX-CSV')

Available fiscal dataflows (confirmed from ECB dataflow list):
  E11     — COFOG: Classification Functions of Government (Eurostat ESA2010 TP table 11)
             Dimensions: FREQ.REF_AREA.SECTOR.COFOG99.UNIT
  E09     — Government Tax and Social Contributions Receipts (Eurostat ESA2010 TP table 9)
  GFS_PUB — Government Finance Statistics - Published series (ECB/Eurostat joint)
  GST     — Government Statistics (broad)

NOTE on Banca d'Italia (BdI):
  The BdI SDMX REST web service (infostat.bancaditalia.it) does not expose a
  publicly accessible SDMX 2.1 REST API — all standard paths return 404.
  BdI fiscal/banking data for Italy is accessible via:
    - ECB datasets (E09, E11, GFS_PUB) which include Italy (REF_AREA=IT)
    - Eurostat GOV_10A series (requires MEF/Istat reporting)
    - BdI annual statistical bulletin (PDF) — not programmatically accessible
  This script fetches the ECB routes that cover BdI-equivalent fiscal data.
"""

import os
import time
import requests

BASE_URL = "https://data-api.ecb.europa.eu/service/data"
OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "local_data", "ecb"
)
START_PERIOD = os.environ.get("ECB_START_PERIOD", "2005")

# ECB key format: dimension values joined by dots, wildcards are empty or omitted
# For E11 (COFOG): FREQ.REF_AREA.SECTOR.COFOG99.UNIT
# GF09 = Education (COFOG), S13 = General Government
DATAFLOWS = [
    # (flow_id, key, label, description)
    (
        "E11",
        "A.IT.S13.GF09.XDC",
        "cofog_education_expenditure_IT",
        "COFOG: Italy general govt education expenditure (annual, EUR)"
    ),
    (
        "E11",
        "A.IT.S13.GF10.XDC",
        "cofog_social_protection_expenditure_IT",
        "COFOG: Italy general govt social protection expenditure (annual, EUR)"
    ),
    (
        "E11",
        "A.IT.S13.GF08.XDC",
        "cofog_recreation_culture_expenditure_IT",
        "COFOG: Italy general govt recreation & culture expenditure (annual, EUR)"
    ),
    (
        "E11",
        "A.IT.S13.GF_TOTAL.XDC",
        "cofog_total_govt_expenditure_IT",
        "COFOG: Italy general govt total expenditure (annual, EUR)"
    ),
    (
        "E09",
        "A.IT.S13.S1._Z.D5._Z._Z.XDC._T.S._Z.A",
        "tax_income_profits_IT",
        "Tax receipts: Italy income & profit taxes (annual)"
    ),
    (
        "E09",
        "A.IT.S13.S1._Z.D21._Z._Z.XDC._T.S._Z.A",
        "tax_VAT_and_production_IT",
        "Tax receipts: Italy VAT and production taxes (annual)"
    ),
    (
        "GFS_PUB",
        "A.IT.S13..,XDC,V,N",
        "govt_finance_stats_IT_annual",
        "Government Finance Statistics: Italy all accounts (annual)"
    ),
]

HEADERS = {
    "Accept": "text/csv, */*",
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
}

TIMEOUT_DATA = 60   # seconds; ECB can be slow for Italy-filtered data


def fetch_dataflow(flow_id: str, key: str, label: str, description: str) -> bool:
    out_path = os.path.join(OUTPUT_DIR, f"ecb_{label}.csv")
    if os.path.exists(out_path):
        print(f"  [skip] {label} — already downloaded")
        return True

    url = f"{BASE_URL}/{flow_id}/{key}"
    params = {"format": "csvdata", "startPeriod": START_PERIOD}
    print(f"  Fetching {label}…")
    print(f"    {description}")

    try:
        r = requests.get(url, params=params, headers=HEADERS,
                         timeout=TIMEOUT_DATA, stream=True)

        if r.status_code != 200:
            print(f"  [warn] {label}: HTTP {r.status_code} for key, trying fallback with flow-level filters…")
            # Retry without key and request Italy-only rows when possible.
            r2 = requests.get(
                f"{BASE_URL}/{flow_id}",
                params={**params, "REF_AREA": "IT", "refArea": "IT", "geo": "IT"},
                headers=HEADERS, timeout=TIMEOUT_DATA, stream=True,
            )
            if r2.status_code == 200:
                r = r2
            else:
                print(f"  [fail] {label}: key HTTP {r.status_code}, fallback HTTP {r2.status_code}")
                return False

        chunks = []
        total = 0
        MAX_BYTES = 20 * 1024 * 1024  # 20MB cap
        for chunk in r.iter_content(chunk_size=65536):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_BYTES:
                print(f"  [warn] {label}: > 20MB, truncating at first {MAX_BYTES//1024//1024}MB")
                break
            chunks.append(chunk)

        content = b"".join(chunks).decode("utf-8", errors="replace")
        if len(content) < 50:
            print(f"  [fail] {label}: empty or near-empty response")
            return False

        os.makedirs(OUTPUT_DIR, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        rows = len(content.strip().split("\n")) - 1
        print(f"  [ok]   {label} → {rows} rows, {len(content)//1024}KB")
        return True

    except requests.Timeout:
        print(f"  [timeout] {label}: server took > {TIMEOUT_DATA}s — skip")
        return False
    except requests.RequestException as e:
        print(f"  [err]  {label}: {e}")
        return False


def main():
    print("Fetching ECB SDMX fiscal / government finance datasets for Italy")
    print(f"Output: {os.path.abspath(OUTPUT_DIR)}\n")
    print("Note: Banca d'Italia SDMX REST API is not publicly accessible at")
    print("      standard paths; ECB E11/E09/GFS_PUB carry equivalent BdI-sourced data.\n")

    ok = fail = 0
    for flow_id, key, label, desc in DATAFLOWS:
        success = fetch_dataflow(flow_id, key, label, desc)
        if success:
            ok += 1
        else:
            fail += 1
        time.sleep(2.0)

    print(f"\nDone: {ok} downloaded, {fail} failed/skipped.")
    if fail > 0:
        print("Tip: ECB GFS_PUB with broad key may timeout; run again or")
        print("     check https://data-api.ecb.europa.eu/service/data/E11 manually.")


if __name__ == "__main__":
    main()
