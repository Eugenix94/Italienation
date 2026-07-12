"""Build national education expenditure panel: state vs parents/private vs total.

Source file:
- local_data/oecd/oecd_education_funding_sources.csv

Outputs:
- local_data/processed/education_expenditure_state_parents_gdp.csv
- local_data/processed/education_expenditure_state_parents_gdp_latest.csv
- local_data/processed/italy_education_expenditure_state_parents_trend.csv

The panel uses OECD finance dimensions:
- S13          -> public/state funding source
- S1D_NON_EDU  -> non-education-sector private source (parents/private entities proxy)
- _T           -> total funding source

Units used:
- PT_B1GQ  (% of GDP)
- USD_PPP  (absolute amount, PPP-adjusted USD)
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "local_data" / "oecd" / "oecd_education_funding_sources.csv"
OUT_DIR = ROOT / "local_data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TARGET_COUNTRIES = ["ITA", "GBR", "DEU", "ESP", "GRC"]
COUNTRY_NAME = {
    "ITA": "Italy",
    "GBR": "UK",
    "DEU": "Germany",
    "ESP": "Spain",
    "GRC": "Greece",
}


def _pivot_metric(df: pd.DataFrame, unit: str, suffix: str) -> pd.DataFrame:
    part = df[df["UNIT_MEASURE"] == unit].copy()
    wide = (
        part.pivot_table(
            index=["REF_AREA", "TIME_PERIOD"],
            columns="EXP_SOURCE",
            values="OBS_VALUE",
            aggfunc="first",
        )
        .rename(
            columns={
                "S13": f"state_{suffix}",
                "S1D_NON_EDU": f"parents_private_{suffix}",
                "_T": f"total_{suffix}",
                "S2": f"rest_world_{suffix}",
            }
        )
        .reset_index()
    )
    return wide


def main() -> None:
    print("Loading OECD funding sources...")
    raw = pd.read_csv(SRC, low_memory=False)

    data = raw[
        raw["REF_AREA"].isin(TARGET_COUNTRIES)
        & (raw["MEASURE"] == "EXP")
        & (raw["EDUCATION_LEV"] == "ISCED11_1T8")
        & (raw["EXP_DESTINATION"] == "INST_EDU")
        & (raw["EXPENDITURE_TYPE"] == "DIR_EXP")
        & raw["UNIT_MEASURE"].isin(["PT_B1GQ", "USD_PPP"])
        & raw["EXP_SOURCE"].isin(["S13", "S1D_NON_EDU", "_T", "S2"])
    ].copy()

    data["TIME_PERIOD"] = pd.to_numeric(data["TIME_PERIOD"], errors="coerce")
    data["OBS_VALUE"] = pd.to_numeric(data["OBS_VALUE"], errors="coerce")
    data = data.dropna(subset=["TIME_PERIOD", "OBS_VALUE"]).copy()
    data["TIME_PERIOD"] = data["TIME_PERIOD"].astype(int)

    pct = _pivot_metric(data, "PT_B1GQ", "pct_gdp")
    usd = _pivot_metric(data, "USD_PPP", "usd_ppp")

    panel = pct.merge(usd, on=["REF_AREA", "TIME_PERIOD"], how="outer")
    panel["Country"] = panel["REF_AREA"].map(COUNTRY_NAME)

    panel["state_share_of_total_pct"] = (panel["state_usd_ppp"] / panel["total_usd_ppp"]) * 100.0
    panel["parents_private_share_of_total_pct"] = (
        panel["parents_private_usd_ppp"] / panel["total_usd_ppp"]
    ) * 100.0
    panel["rest_world_share_of_total_pct"] = (panel["rest_world_usd_ppp"] / panel["total_usd_ppp"]) * 100.0

    # Optional implied GDP from education total and share in GDP (consistency check metric).
    panel["implied_gdp_usd_ppp"] = panel["total_usd_ppp"] / (panel["total_pct_gdp"] / 100.0)

    cols = [
        "REF_AREA",
        "Country",
        "TIME_PERIOD",
        "state_pct_gdp",
        "parents_private_pct_gdp",
        "rest_world_pct_gdp",
        "total_pct_gdp",
        "state_usd_ppp",
        "parents_private_usd_ppp",
        "rest_world_usd_ppp",
        "total_usd_ppp",
        "state_share_of_total_pct",
        "parents_private_share_of_total_pct",
        "rest_world_share_of_total_pct",
        "implied_gdp_usd_ppp",
    ]
    panel = panel[cols].sort_values(["TIME_PERIOD", "REF_AREA"]).reset_index(drop=True)

    panel_path = OUT_DIR / "education_expenditure_state_parents_gdp.csv"
    panel.to_csv(panel_path, index=False)

    latest_year = int(panel["TIME_PERIOD"].max())
    latest = panel[panel["TIME_PERIOD"] == latest_year].copy()
    latest_path = OUT_DIR / "education_expenditure_state_parents_gdp_latest.csv"
    latest.to_csv(latest_path, index=False)

    italy = panel[panel["REF_AREA"] == "ITA"].copy()
    italy_path = OUT_DIR / "italy_education_expenditure_state_parents_trend.csv"
    italy.to_csv(italy_path, index=False)

    print(f"Rows in full panel: {len(panel):,}")
    print(f"Years covered: {panel['TIME_PERIOD'].min()} -> {panel['TIME_PERIOD'].max()}")
    print(f"Latest year snapshot: {latest_year}, rows={len(latest)}")
    print(f"Wrote: {panel_path.relative_to(ROOT)}")
    print(f"Wrote: {latest_path.relative_to(ROOT)}")
    print(f"Wrote: {italy_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
