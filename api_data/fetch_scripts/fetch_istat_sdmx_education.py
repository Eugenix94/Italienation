"""
Fetch key ISTAT SDMX datasets relevant to NEET, school sector, and employment.

ISTAT SDMX 2.1 REST endpoint: https://sdmx.istat.it/SDMXWS/rest/
Data URL format: /data/IT1,{FLOW_ID},1.0/?startPeriod={year}&format=csv

Target dataflows (confirmed via ISTAT dataflow discovery):
  172_931  — NEET (giovani non occupati e non in istruzione e formazione)
  52_607   — Early school leavers (18-24 anni che abbandonano gli studi)
  158_149  — Scuola dell'infanzia
  158_150  — Scuola primaria
  158_151  — Scuola secondaria di primo grado
  158_260  — Scuola secondaria di secondo grado
  151_914  — Tasso di disoccupazione
  150_915  — Tasso di occupazione
  124_1156 — Stato patrimoniale delle università (euro)
  124_1157 — Conto economico delle università (euro)
  613_934  — Diplomati - caratteristiche socio-demografiche e curriculum
  613_935  — Diplomati - condizione occupazionale e retribuzione
  612_939  — Laureati - condizione occupazionale
  34_198   — Incidenza di povertà relativa familiare
  270_243  — Spesa per consumi finali della PA (pubblica amministrazione)
"""

import os
import time
import requests

BASE_URL = "https://sdmx.istat.it/SDMXWS/rest/data"
OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "local_data", "ISTAT"
)
START_PERIOD = os.environ.get("ISTAT_START_PERIOD", "2010")

DATAFLOWS = [
    # (flow_id, label, version)
    # Versions confirmed via ISTAT SDMX dataflow endpoint
    ("172_931", "neet_giovani",                        "1.0"),
    ("52_1203", "early_school_leavers",                "1.0"),  # 52_607 empty; 52_1203 current
    ("158_149", "scuola_infanzia",                     "1.0"),
    ("158_150", "scuola_primaria",                     "1.0"),
    ("158_151", "scuola_secondaria_1grado",            "1.0"),
    ("158_260", "scuola_secondaria_2grado",            "1.0"),
    ("151_914", "tasso_disoccupazione",                "1.2"),  # v1.2 confirmed
    ("150_915", "tasso_occupazione",                   "1.2"),  # v1.2 confirmed
    ("124_1156","universita_stato_patrimoniale",        "1.0"),
    ("124_1157","universita_conto_economico",           "1.0"),
    ("613_934", "diplomati_caratteristiche",           "1.1"),  # v1.1 confirmed
    ("613_935", "diplomati_occupazione_retribuzione",  "1.0"),
    ("612_939", "laureati_occupazione",                "1.1"),  # v1.1 confirmed
    ("34_198",  "poverta_relativa_incidenza",          "1.0"),
    # 270_243 Spesa PA: dataflow exists v1.1 but data endpoint returns 404 — omitted
]

HEADERS = {
    "Accept": "application/vnd.sdmx.data+csv;version=1.0.0, text/csv, */*",
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
}


def fetch_dataflow(flow_id: str, label: str, version: str = "1.0") -> bool:
    url = f"{BASE_URL}/IT1,{flow_id},{version}/?startPeriod={START_PERIOD}"
    out_path = os.path.join(OUTPUT_DIR, f"istat_{label}.csv")

    if os.path.exists(out_path):
        print(f"  [skip] {label} — already downloaded")
        return True

    try:
        r = requests.get(url, headers=HEADERS, timeout=60)
        if r.status_code == 200 and len(r.text) > 100:
            os.makedirs(OUTPUT_DIR, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(r.text)
            rows = len(r.text.strip().split("\n")) - 1
            print(f"  [ok]   {label} → {rows} rows, {len(r.text)//1024}KB")
            return True
        else:
            print(f"  [fail] {label}: HTTP {r.status_code} — {r.text[:120]}")
            return False
    except requests.RequestException as e:
        print(f"  [err]  {label}: {e}")
        return False


def main():
    print(f"Fetching {len(DATAFLOWS)} ISTAT SDMX dataflows (startPeriod={START_PERIOD})")
    print(f"Output: {os.path.abspath(OUTPUT_DIR)}\n")

    ok = fail = 0
    for flow_id, label, version in DATAFLOWS:
        success = fetch_dataflow(flow_id, label, version)
        if success:
            ok += 1
        else:
            fail += 1
        time.sleep(1.0)   # be polite to ISTAT server

    print(f"\nDone: {ok} downloaded, {fail} failed.")


if __name__ == "__main__":
    main()
