"""
Fetch current labour-market series for Italy (vacancy vs unemployment context).

Outputs in local_data/eurostat:
- eurostat_it_job_vacancy_rate_quarterly.csv
- eurostat_it_job_vacancy_rate_quarterly_by_nace.csv
- eurostat_it_unemployment_rate_monthly.csv
- eurostat_it_unemployment_rate_quarterly_youth.csv
- eurostat_it_labour_market_current_snapshot.csv
"""

from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "local_data" / "eurostat"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BASE = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (current labour market extraction)",
    "Accept": "text/csv, */*",
}
TIMEOUT = 120


SERIES = [
    {
        "name": "it_job_vacancy_rate_quarterly",
        "flow": "jvs_q_nace2",
        # freq.s_adj.nace_r2.sizeclas.indic_em.geo
        "key": "Q.NSA.B-S.GE10.JVR.IT",
        "out": "eurostat_it_job_vacancy_rate_quarterly.csv",
    },
    {
        "name": "it_job_vacancy_rate_quarterly_by_nace",
        "flow": "jvs_q_nace2",
        # Keep all NACE groups for IT to help identify sector access frictions.
        "key": "Q.NSA..GE10.JVR.IT",
        "out": "eurostat_it_job_vacancy_rate_quarterly_by_nace.csv",
    },
    {
        "name": "it_unemployment_rate_monthly_total",
        "flow": "une_rt_m",
        # freq.s_adj.age.unit.sex.geo
        "key": "M.SA.TOTAL.PC_ACT.T.IT",
        "out": "eurostat_it_unemployment_rate_monthly.csv",
    },
    {
        "name": "it_unemployment_rate_quarterly_youth",
        "flow": "une_rt_q",
        # Youth unemployment rate (15-24)
        "key": "Q.SA.Y15-24.PC_ACT.T.IT",
        "out": "eurostat_it_unemployment_rate_quarterly_youth.csv",
    },
]


def fetch_csv(flow: str, key: str) -> pd.DataFrame:
    url = f"{BASE}/{flow}/{key}"
    response = requests.get(
        url,
        params={"format": "SDMX-CSV"},
        headers=HEADERS,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return pd.read_csv(StringIO(response.text), low_memory=False)


def save_df(df: pd.DataFrame, out_name: str) -> Path:
    out_path = OUT_DIR / out_name
    df.to_csv(out_path, index=False)
    return out_path


def build_snapshot(outputs: list[tuple[str, pd.DataFrame]]) -> pd.DataFrame:
    rows: list[dict] = []

    for series_name, df in outputs:
        if "TIME_PERIOD" not in df.columns:
            continue

        work = df.copy()
        work["TIME_PERIOD"] = work["TIME_PERIOD"].astype(str)
        work["OBS_VALUE"] = pd.to_numeric(work.get("OBS_VALUE"), errors="coerce")

        # Keep latest non-null observation for quick monitoring.
        non_null = work.dropna(subset=["OBS_VALUE"]).sort_values("TIME_PERIOD")
        if non_null.empty:
            rows.append(
                {
                    "series": series_name,
                    "latest_time_period": "",
                    "latest_obs_value": "",
                    "notes": "No non-null observations in extracted slice",
                }
            )
            continue

        latest = non_null.iloc[-1]
        rows.append(
            {
                "series": series_name,
                "latest_time_period": latest["TIME_PERIOD"],
                "latest_obs_value": latest["OBS_VALUE"],
                "notes": "",
            }
        )

    return pd.DataFrame(rows)


def main() -> None:
    print("Fetching current Italy labour-market data (Eurostat SDMX)")
    outputs: list[tuple[str, pd.DataFrame]] = []

    for item in SERIES:
        print(f"\n[fetch] {item['name']}")
        print(f"  flow={item['flow']} key={item['key']}")
        try:
            df = fetch_csv(item["flow"], item["key"])
        except requests.RequestException as exc:
            print(f"  [fail] {exc}")
            continue

        out_path = save_df(df, item["out"])
        tp_min = str(df["TIME_PERIOD"].astype(str).min()) if "TIME_PERIOD" in df.columns and not df.empty else ""
        tp_max = str(df["TIME_PERIOD"].astype(str).max()) if "TIME_PERIOD" in df.columns and not df.empty else ""
        print(f"  [ok] rows={len(df):,} period={tp_min} -> {tp_max} file={out_path.relative_to(ROOT)}")
        outputs.append((item["name"], df))

    if not outputs:
        print("\nNo dataset was fetched successfully.")
        return

    snapshot = build_snapshot(outputs)
    snap_path = OUT_DIR / "eurostat_it_labour_market_current_snapshot.csv"
    snapshot.to_csv(snap_path, index=False)

    print("\nSnapshot written:")
    print(f"  {snap_path.relative_to(ROOT)}")
    print(snapshot.to_string(index=False))


if __name__ == "__main__":
    main()
