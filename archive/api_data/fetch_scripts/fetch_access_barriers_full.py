"""
Fetch a full access-barriers expansion pack for Italy.

This script adds the remaining high-impact signals discussed in planning:
- contract quality / precariousness proxies
- long-term unemployment barrier
- mobility and territorial access proxies
- digital-access proxy
- housing tenure burden proxy

It also records ANPAL/CPI endpoint availability checks into manual_required,
so unresolved official endpoints are documented in a reproducible way.
"""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
EUROSTAT_DIR = ROOT / "local_data" / "eurostat"
MANUAL_DIR = ROOT / "local_data" / "manual_required"
EUROSTAT_DIR.mkdir(parents=True, exist_ok=True)
MANUAL_DIR.mkdir(parents=True, exist_ok=True)

BASE = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (access-barriers expansion)",
    "Accept": "text/csv, */*",
}
TIMEOUT = 120

# These are broad extracts for IT to avoid missing critical dimensions.
SERIES = [
    {
        "name": "it_contract_quality_part_time",
        "flow": "lfsi_pt_a",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_contract_quality_part_time.csv",
        "description": "Part-time employment composition (incl. involuntary part-time dimensions)",
    },
    {
        "name": "it_long_term_unemployment",
        "flow": "une_ltu_a",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_long_term_unemployment.csv",
        "description": "Long-term unemployment rates/levels",
    },
    {
        "name": "it_transport_vehicle_stock_regional",
        "flow": "tran_r_vehst",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_transport_vehicle_stock_regional.csv",
        "description": "Regional vehicle stock proxy for mobility access",
    },
    {
        "name": "it_broadband_access_regional",
        "flow": "isoc_r_broad_h",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_broadband_access_regional.csv",
        "description": "Regional household broadband access proxy for digital job access",
    },
    {
        "name": "it_home_ownership_housing_cost_proxy",
        "flow": "ilc_lvho02",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_home_ownership_housing_cost_proxy.csv",
        "description": "Housing tenure and burden proxies linked to job access",
    },
]

ANPAL_CANDIDATE_ENDPOINTS = [
    "https://dati.anpal.gov.it/api/3/action/package_list",
    "https://dati-anpal.opendatasoft.com/api/explore/v2.1/catalog/datasets?limit=10",
    "https://servizi.anpal.gov.it/",
]


def fetch_series(flow: str, params: dict) -> pd.DataFrame:
    response = requests.get(f"{BASE}/{flow}", params=params, headers=HEADERS, timeout=TIMEOUT)
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text), low_memory=False)


def save_csv(df: pd.DataFrame, file_name: str) -> Path:
    out_path = EUROSTAT_DIR / file_name
    df.to_csv(out_path, index=False)
    return out_path


def build_snapshot(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows)


def check_anpal_endpoints() -> list[dict]:
    checks: list[dict] = []
    for url in ANPAL_CANDIDATE_ENDPOINTS:
        try:
            response = requests.get(url, timeout=30)
            checks.append(
                {
                    "url": url,
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type", ""),
                    "ok": response.status_code == 200,
                    "sample": (response.text or "")[:160].replace("\n", " "),
                }
            )
        except Exception as exc:
            checks.append(
                {
                    "url": url,
                    "status_code": None,
                    "content_type": "",
                    "ok": False,
                    "sample": str(exc),
                }
            )
    return checks


def main() -> None:
    print("Fetching full access-barriers expansion pack for Italy")

    snapshot_rows: list[dict] = []

    for item in SERIES:
        print(f"\n[fetch] {item['name']}")
        print(f"  flow={item['flow']}")
        try:
            df = fetch_series(item["flow"], item["params"])
            out_path = save_csv(df, item["out"])
            period_min = ""
            period_max = ""
            if "TIME_PERIOD" in df.columns and not df.empty:
                periods = df["TIME_PERIOD"].astype(str)
                period_min = periods.min()
                period_max = periods.max()
            print(
                f"  [ok] rows={len(df):,} period={period_min} -> {period_max} "
                f"file={out_path.relative_to(ROOT)}"
            )
            snapshot_rows.append(
                {
                    "series": item["name"],
                    "flow": item["flow"],
                    "status": "ok",
                    "rows": len(df),
                    "time_period_min": period_min,
                    "time_period_max": period_max,
                    "file": str(out_path.relative_to(ROOT)),
                    "description": item["description"],
                }
            )
        except requests.RequestException as exc:
            print(f"  [fail] {exc}")
            snapshot_rows.append(
                {
                    "series": item["name"],
                    "flow": item["flow"],
                    "status": "failed",
                    "rows": 0,
                    "time_period_min": "",
                    "time_period_max": "",
                    "file": "",
                    "description": item["description"],
                    "error": str(exc),
                }
            )

    snapshot_df = build_snapshot(snapshot_rows)
    snapshot_path = EUROSTAT_DIR / "eurostat_it_access_barriers_snapshot.csv"
    snapshot_df.to_csv(snapshot_path, index=False)
    print(f"\nSnapshot written: {snapshot_path.relative_to(ROOT)}")

    anpal_checks = check_anpal_endpoints()
    anpal_json_path = MANUAL_DIR / "anpal_cpi_endpoint_checks_2026-05-20.json"
    anpal_json_path.write_text(json.dumps(anpal_checks, indent=2, ensure_ascii=False), encoding="utf-8")

    anpal_md_path = MANUAL_DIR / "anpal_cpi_data_manual_followup.md"
    lines = [
        "# ANPAL/CPI Data Manual Follow-up",
        "",
        "Auto-generated endpoint checks:",
        "",
    ]
    for item in anpal_checks:
        lines.append(f"- URL: {item['url']}")
        lines.append(f"  - status_code: {item['status_code']}")
        lines.append(f"  - ok: {item['ok']}")
        lines.append(f"  - content_type: {item['content_type']}")
        lines.append(f"  - sample/error: {item['sample']}")
        lines.append("")

    lines.extend(
        [
            "Manual next actions:",
            "",
            "- Verify official ANPAL open-data endpoint/domain currently in use.",
            "- If ANPAL remains unavailable, use national labour administration alternatives and document source substitutions.",
            "- Add CPI performance indicators (registrations, placements, placement time, ALMP participation) once endpoint is confirmed.",
        ]
    )
    anpal_md_path.write_text("\n".join(lines), encoding="utf-8")

    print(f"ANPAL checks written: {anpal_json_path.relative_to(ROOT)}")
    print(f"ANPAL manual follow-up note: {anpal_md_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
