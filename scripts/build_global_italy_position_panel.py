"""Build OECD + World Bank international position tables for Italy.

Outputs:
- local_data/processed/global_italy_position_oecd_wb_latest.csv
- local_data/processed/italy_position_summary_oecd_wb.csv
- local_data/processed/global_italy_position_method_notes.md

The goal is to show Italy's latest observed position among countries with
comparable data for key cost/access/mobility-proxy indicators.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "local_data" / "processed"
OECD = ROOT / "local_data" / "oecd"


def latest_by_iso(df: pd.DataFrame, value_col: str, year_col: str = "year") -> pd.DataFrame:
    part = df[["iso3", year_col, value_col]].dropna().copy()
    part[year_col] = pd.to_numeric(part[year_col], errors="coerce")
    part = part.dropna(subset=[year_col])
    part[year_col] = part[year_col].astype(int)
    out = part.sort_values(year_col).groupby("iso3", as_index=False).last()
    out = out.rename(columns={year_col: f"{value_col}_year"})
    return out


def rank_block(df: pd.DataFrame, metric: str, better: str) -> pd.DataFrame:
    tmp = df[["iso3", metric]].dropna().copy()
    if tmp.empty:
        return pd.DataFrame(columns=["iso3", f"{metric}_rank", f"{metric}_n", f"{metric}_pct_better"])

    ascending = better == "lower"
    tmp[f"{metric}_rank"] = tmp[metric].rank(method="min", ascending=ascending).astype(int)
    n = len(tmp)
    tmp[f"{metric}_n"] = n

    # percentile where higher is better for interpretation (0-100)
    if n == 1:
        tmp[f"{metric}_pct_better"] = 100.0
    else:
        tmp[f"{metric}_pct_better"] = (1.0 - (tmp[f"{metric}_rank"] - 1) / (n - 1)) * 100.0

    return tmp[["iso3", f"{metric}_rank", f"{metric}_n", f"{metric}_pct_better"]]


def main() -> None:
    panel = pd.read_csv(PROC / "global_he_cost_access_panel.csv", low_memory=False)

    # Core WB latest metrics
    wb_metrics = [
        "education_spending_pct_gdp",
        "tertiary_enrollment_gross_pct",
        "learning_poverty_pct",
        "access_minus_learning_gap",
        "cost_intensity_x_access",
    ]

    wb_latest = panel[["iso3", "country", "year"] + wb_metrics].copy()
    wb_latest["year"] = pd.to_numeric(wb_latest["year"], errors="coerce")

    wb_blocks = []
    for m in wb_metrics:
        b = latest_by_iso(wb_latest[["iso3", "year", m]].copy(), m, "year")
        wb_blocks.append(b)

    world = wb_blocks[0]
    for b in wb_blocks[1:]:
        world = world.merge(b, on="iso3", how="outer")

    # Country name from latest available row in WB panel
    country_name = (
        wb_latest[["iso3", "country", "year"]]
        .dropna(subset=["country", "year"])
        .sort_values("year")
        .groupby("iso3", as_index=False)
        .last()[["iso3", "country"]]
    )
    world = world.merge(country_name, on="iso3", how="left")

    # OECD funding-source latest metrics
    fund = pd.read_csv(OECD / "oecd_education_funding_sources.csv", low_memory=False)
    fund = fund[
        (fund["MEASURE"] == "EXP")
        & (fund["EDUCATION_LEV"] == "ISCED11_1T8")
        & (fund["EXP_DESTINATION"] == "INST_EDU")
        & (fund["EXPENDITURE_TYPE"] == "DIR_EXP")
        & (fund["UNIT_MEASURE"].isin(["PT_B1GQ", "USD_PPP"]))
        & (fund["EXP_SOURCE"].isin(["S13", "S1D_NON_EDU", "_T"]))
    ].copy()

    fund["TIME_PERIOD"] = pd.to_numeric(fund["TIME_PERIOD"], errors="coerce")
    fund["OBS_VALUE"] = pd.to_numeric(fund["OBS_VALUE"], errors="coerce")
    fund = fund.dropna(subset=["TIME_PERIOD", "OBS_VALUE"]).copy()
    fund["TIME_PERIOD"] = fund["TIME_PERIOD"].astype(int)
    fund["iso3"] = fund["REF_AREA"]

    # latest year by iso3 for funding sources
    fund = fund.sort_values("TIME_PERIOD")
    latest_year = fund.groupby("iso3")["TIME_PERIOD"].transform("max")
    fund_latest = fund[fund["TIME_PERIOD"] == latest_year].copy()

    pct = fund_latest[fund_latest["UNIT_MEASURE"] == "PT_B1GQ"]
    usd = fund_latest[fund_latest["UNIT_MEASURE"] == "USD_PPP"]

    pct_wide = (
        pct.pivot_table(index=["iso3", "TIME_PERIOD"], columns="EXP_SOURCE", values="OBS_VALUE", aggfunc="first")
        .rename(columns={"S13": "state_pct_gdp_oecd", "S1D_NON_EDU": "private_pct_gdp_oecd", "_T": "total_pct_gdp_oecd"})
        .reset_index()
        .rename(columns={"TIME_PERIOD": "oecd_funding_year"})
    )
    usd_wide = (
        usd.pivot_table(index=["iso3", "TIME_PERIOD"], columns="EXP_SOURCE", values="OBS_VALUE", aggfunc="first")
        .rename(columns={"S13": "state_usd_ppp_oecd", "S1D_NON_EDU": "private_usd_ppp_oecd", "_T": "total_usd_ppp_oecd"})
        .reset_index()
        .rename(columns={"TIME_PERIOD": "oecd_funding_year_usd"})
    )

    oecd_funding = pct_wide.merge(usd_wide, on="iso3", how="outer")

    oecd_funding["state_share_pct_oecd"] = (oecd_funding["state_usd_ppp_oecd"] / oecd_funding["total_usd_ppp_oecd"]) * 100.0
    oecd_funding["private_share_pct_oecd"] = (oecd_funding["private_usd_ppp_oecd"] / oecd_funding["total_usd_ppp_oecd"]) * 100.0

    # OECD per-student latest (2022 in current dataset)
    perstud = pd.read_csv(OECD / "oecd_education_fin_perstud.csv", low_memory=False)
    perstud = perstud[
        (perstud["MEASURE"] == "FIN_PERSTUD")
        & (perstud["EDUCATION_LEV"] == "ISCED11_1T8")
        & (perstud["UNIT_MEASURE"] == "USD_PPP_ST")
        & (perstud["EXP_SOURCE"] == "_T")
    ].copy()
    perstud["TIME_PERIOD"] = pd.to_numeric(perstud["TIME_PERIOD"], errors="coerce")
    perstud["OBS_VALUE"] = pd.to_numeric(perstud["OBS_VALUE"], errors="coerce")
    perstud = perstud.dropna(subset=["TIME_PERIOD", "OBS_VALUE"]).copy()
    perstud["TIME_PERIOD"] = perstud["TIME_PERIOD"].astype(int)
    perstud["iso3"] = perstud["REF_AREA"]
    perstud_latest = latest_by_iso(perstud[["iso3", "TIME_PERIOD", "OBS_VALUE"]].rename(columns={"TIME_PERIOD": "year", "OBS_VALUE": "per_student_usd_ppp_oecd"}), "per_student_usd_ppp_oecd", "year")

    # Join all
    combined = world.merge(oecd_funding, on="iso3", how="left")
    combined = combined.merge(perstud_latest, on="iso3", how="left")

    # Rank direction config
    rank_config = {
        "education_spending_pct_gdp": "higher",
        "tertiary_enrollment_gross_pct": "higher",
        "learning_poverty_pct": "lower",
        "access_minus_learning_gap": "higher",
        "cost_intensity_x_access": "higher",
        "state_pct_gdp_oecd": "higher",
        "private_pct_gdp_oecd": "lower",
        "state_share_pct_oecd": "higher",
        "private_share_pct_oecd": "lower",
        "per_student_usd_ppp_oecd": "higher",
    }

    for metric, better in rank_config.items():
        rb = rank_block(combined, metric, better)
        combined = combined.merge(rb, on="iso3", how="left")

    combined = combined.sort_values("iso3").reset_index(drop=True)

    # Italy summary long table
    italy = combined[combined["iso3"] == "ITA"].copy()
    if italy.empty:
        raise RuntimeError("Italy (ITA) not found in combined panel.")

    metric_rows = []
    row = italy.iloc[0]
    for metric, better in rank_config.items():
        metric_rows.append(
            {
                "metric": metric,
                "better_direction": better,
                "italy_value": row.get(metric, np.nan),
                "italy_rank": row.get(f"{metric}_rank", np.nan),
                "countries_with_metric": row.get(f"{metric}_n", np.nan),
                "italy_pct_better": row.get(f"{metric}_pct_better", np.nan),
            }
        )
    italy_summary = pd.DataFrame(metric_rows)

    # Output files
    out_global = PROC / "global_italy_position_oecd_wb_latest.csv"
    out_italy = PROC / "italy_position_summary_oecd_wb.csv"
    out_notes = PROC / "global_italy_position_method_notes.md"

    combined.to_csv(out_global, index=False)
    italy_summary.to_csv(out_italy, index=False)

    notes = "\n".join(
        [
            "# Global Italy Position Notes",
            "",
            "Data sources combined:",
            "- World Bank-derived global panel: local_data/processed/global_he_cost_access_panel.csv",
            "- OECD funding sources: local_data/oecd/oecd_education_funding_sources.csv",
            "- OECD per-student finance: local_data/oecd/oecd_education_fin_perstud.csv",
            "",
            "Ranking methodology:",
            "- For each metric, Italy is ranked among countries with non-missing data for that metric.",
            "- Rank direction is metric-specific (e.g., lower learning poverty is better; higher tertiary enrollment is better).",
            "- italy_pct_better is converted to 0-100 scale where 100 indicates top rank for that metric.",
            "",
            "Caveats:",
            "- OECD and World Bank years can differ by metric; this table is a latest-available cross-sectional benchmark.",
            "- Some variables are proxies, not direct causal policy measures.",
        ]
    )
    out_notes.write_text(notes, encoding="utf-8")

    print(f"Wrote {out_global.relative_to(ROOT)} rows={len(combined):,}")
    print(f"Wrote {out_italy.relative_to(ROOT)} rows={len(italy_summary):,}")
    print(f"Wrote {out_notes.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
