#!/usr/bin/env python3
"""
Fetch missing Eurostat ALMP (Active Labour Market Policy) data to fill ANPAL gap.
These two flows show labour-market intervention spending and participant counts by type.
"""

import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass
import requests
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "local_data" / "eurostat"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
HEADERS = {
    "Accept": "text/csv, */*",
    "User-Agent": "Italienation-Research/1.0",
}

# ALMP flows: expenditure and participant counts by intervention type
ALMP_FLOWS = [
    {
        "id": "lmp_ind_exp",
        "label": "almp_expenditure_by_type",
        "params": "startPeriod=2010&endPeriod=2023&geo=IT",
        "desc": "ALMP expenditure by type of action (training, wage subsidy, etc.)"
    },
    {
        "id": "lmp_ind_actp",
        "label": "almp_participants_by_type",
        "params": "startPeriod=2010&endPeriod=2023&geo=IT",
        "desc": "ALMP participant stock by type of action"
    },
]

def fetch_flow(flow_id, label, params, desc):
    out_path = OUTPUT_DIR / f"estat_{label}.csv"
    if out_path.exists():
        print(f"✓ {label} (already downloaded)")
        return True
    
    url = f"{BASE_URL}/{flow_id}"
    params_full = {"format": "SDMX-CSV"}
    params_full.update(dict(p.split("=") for p in params.split("&")))
    
    try:
        print(f"⤳ {label}... ", end="", flush=True)
        r = requests.get(url, params=params_full, headers=HEADERS, timeout=60)
        if r.status_code != 200:
            print(f"HTTP {r.status_code}")
            return False
        
        content = r.text
        if len(content) < 100:
            print(f"empty response")
            return False
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        rows = len([l for l in content.strip().split("\n") if l]) - 1
        print(f"✓ {rows} rows")
        return True
    except Exception as e:
        print(f"✗ {e}")
        return False

if __name__ == "__main__":
    print("Fetching Eurostat ALMP data (substitute for ANPAL)\n")
    ok = fail = 0
    for flow in ALMP_FLOWS:
        if fetch_flow(flow["id"], flow["label"], flow["params"], flow["desc"]):
            ok += 1
        else:
            fail += 1
    print(f"\nDone: {ok} fetched, {fail} failed")
