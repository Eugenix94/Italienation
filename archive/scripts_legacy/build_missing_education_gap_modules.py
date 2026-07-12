#!/usr/bin/env python3
"""Build the remaining Italy education finance gap modules.

Outputs:
- local_data/processed/italy_education_finance_levels_real.csv
- local_data/processed/italy_household_burden_module.csv
- local_data/processed/italy_education_territorial_proxy_panel.csv
- local_data/processed/worldbank_italy_cpi_index.csv
- local_data/processed/education_gap_modules_note.md
- local_data/processed/education_gap_modules_manifest.json
"""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd
import requests


ROOT = Path(r"c:/Users/Dell/Documents/VSC Projects/Italienation")
LOCAL = ROOT / "local_data"
PROCESSED = LOCAL / "processed"

EUROSTAT_FINANCE_PATH = LOCAL / "educ_uoe_fini01$defaultview_linear_2_0.csv"
OECD_TREND_PATH = PROCESSED / "italy_education_expenditure_state_parents_trend.csv"
HOUSEHOLD_SNAPSHOT_PATH = PROCESSED / "italy_school_household_cost_snapshot.csv"
TUITION_BENCHMARK_PATH = PROCESSED / "italy_mur_tuition_benchmark_2024.csv"
DSU_SUPPORT_PATH = PROCESSED / "dsu_ersu_support_panel_2024_2025.csv"
ATENEI_SUPPORT_PATH = PROCESSED / "atenei_payment_support_panel_2023_2024.csv"
SIOPE_SUMMARY_PATH = PROCESSED / "siope_school_expenditure_summary.csv"
MINISTRY_STUDENTS_PATH = PROCESSED / "ministry_students_by_region_order_2024_25.csv"
NEET_REGIONAL_PATH = PROCESSED / "neet_regional_target_panel.csv"
LOWER_SECONDARY_PATH = PROCESSED / "istat_lower_secondary_indicators_latest.csv"
REPEATERS_PATH = PROCESSED / "istat_repeaters_upper_secondary_latest.csv"
DISABLED_PATH = PROCESSED / "estimated_disabled_students_by_region_order_2024_25_using_national_rates.csv"
BES_PATH = PROCESSED / "estimated_bes_students_by_region_order_2024_25_using_istat_rates.csv"

CPI_URL = "https://api.worldbank.org/v2/country/ITA/indicator/FP.CPI.TOTL?format=json&per_page=200"
CPI_OUTPUT_PATH = PROCESSED / "worldbank_italy_cpi_index.csv"
FINANCE_OUTPUT_PATH = PROCESSED / "italy_education_finance_levels_real.csv"
HOUSEHOLD_OUTPUT_PATH = PROCESSED / "italy_household_burden_module.csv"
TERRITORIAL_OUTPUT_PATH = PROCESSED / "italy_education_territorial_proxy_panel.csv"
NOTE_OUTPUT_PATH = PROCESSED / "education_gap_modules_note.md"
MANIFEST_OUTPUT_PATH = PROCESSED / "education_gap_modules_manifest.json"

BASE_REAL_YEAR = 2022

REGION_NAME_MAP = {
    "ABRUZZO": "Abruzzo",
    "BASILICATA": "Basilicata",
    "CALABRIA": "Calabria",
    "CAMPANIA": "Campania",
    "EMILIA ROMAGNA": "Emilia-Romagna",
    "EMILIA-ROMAGNA": "Emilia-Romagna",
    "FRIULI-VENEZIA G.": "Friuli-Venezia Giulia",
    "FRIULI-VENEZIA GIULIA": "Friuli-Venezia Giulia",
    "LAZIO": "Lazio",
    "LIGURIA": "Liguria",
    "LOMBARDIA": "Lombardia",
    "MARCHE": "Marche",
    "MOLISE": "Molise",
    "PIEMONTE": "Piemonte",
    "PUGLIA": "Puglia",
    "SARDEGNA": "Sardegna",
    "SICILIA": "Sicilia",
    "TOSCANA": "Toscana",
    "TRENTINO A.A.": "Trentino Alto Adige / Südtirol",
    "TRENTINO-ALTO ADIGE": "Trentino Alto Adige / Südtirol",
    "TRENTINO ALTO ADIGE": "Trentino Alto Adige / Südtirol",
    "UMBRIA": "Umbria",
    "VALLE D'AOSTA": "Valle d'Aosta / Vallée d'Aoste",
    "VALLE D\"AOSTA": "Valle d'Aosta / Vallée d'Aoste",
    "VALLE D''AOSTA": "Valle d'Aosta / Vallée d'Aoste",
    "VENETO": "Veneto",
    "BOLZANO": "Provincia Autonoma Bolzano / Bozen",
    "TRENTO": "Provincia Autonoma Trento",
}


def safe_float(value: object) -> float | None:
    try:
        if pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def safe_div(numerator: float | int | None, denominator: float | int | None) -> float | None:
    numerator_value = safe_float(numerator)
    denominator_value = safe_float(denominator)
    if numerator_value is None or denominator_value in {None, 0}:
        return None
    return numerator_value / denominator_value


def normalize_region_name(value: object) -> str | None:
    if value is None or pd.isna(value):
        return None
    text = str(value).strip().replace("'", "").replace('"', "")
    text = " ".join(text.split())
    key = text.upper()
    return REGION_NAME_MAP.get(key, text)


def fetch_cpi_series() -> pd.DataFrame:
    response = requests.get(CPI_URL, timeout=120)
    response.raise_for_status()
    payload = response.json()
    rows = payload[1] if isinstance(payload, list) and len(payload) > 1 else []
    frame = pd.DataFrame(rows)
    if frame.empty:
        raise RuntimeError("World Bank CPI response was empty")
    frame = frame.loc[:, ["date", "value"]].copy()
    frame = frame.rename(columns={"date": "year", "value": "cpi_index"})
    frame["year"] = pd.to_numeric(frame["year"], errors="coerce")
    frame["cpi_index"] = pd.to_numeric(frame["cpi_index"], errors="coerce")
    frame = frame.loc[frame["year"].notna() & frame["cpi_index"].notna()].copy()
    frame["year"] = frame["year"].astype(int)
    frame = frame.sort_values("year").reset_index(drop=True)
    frame.to_csv(CPI_OUTPUT_PATH, index=False)
    return frame


def build_finance_panel(cpi: pd.DataFrame) -> pd.DataFrame:
    eurostat = pd.read_csv(EUROSTAT_FINANCE_PATH, low_memory=False)
    eurostat = eurostat.loc[
        eurostat["geo"].eq("IT")
        & eurostat["unit"].eq("MIO_EUR")
        & eurostat["expend"].eq("TOTAL")
        & eurostat["sector"].isin(["PUBL", "PRIV", "TOT_SEC"]),
        [
            "TIME_PERIOD",
            "sector",
            "Sector",
            "isced11",
            "International Standard Classification of Education (ISCED 2011)",
            "OBS_VALUE",
        ],
    ].copy()
    eurostat = eurostat.rename(
        columns={
            "TIME_PERIOD": "year",
            "Sector": "sector_label",
            "International Standard Classification of Education (ISCED 2011)": "level_label",
            "OBS_VALUE": "nominal_million_eur",
        }
    )
    eurostat["year"] = pd.to_numeric(eurostat["year"], errors="coerce")
    eurostat["nominal_million_eur"] = pd.to_numeric(eurostat["nominal_million_eur"], errors="coerce")
    eurostat = eurostat.loc[eurostat["year"].notna() & eurostat["nominal_million_eur"].notna()].copy()
    eurostat["year"] = eurostat["year"].astype(int)
    eurostat["nominal_eur"] = eurostat["nominal_million_eur"] * 1_000_000
    eurostat["series_group"] = "eurostat_level_history"
    eurostat = eurostat.merge(cpi, on="year", how="left")

    base_cpi = cpi.loc[cpi["year"].eq(BASE_REAL_YEAR), "cpi_index"]
    if base_cpi.empty:
        raise RuntimeError(f"Missing CPI base year {BASE_REAL_YEAR}")
    base_cpi_value = float(base_cpi.iloc[0])
    eurostat["real_base_year_eur"] = eurostat["nominal_eur"] * base_cpi_value / eurostat["cpi_index"]
    eurostat["real_base_year"] = BASE_REAL_YEAR
    eurostat["per_student_eur"] = pd.NA
    eurostat["population_reference"] = pd.NA
    eurostat["source_file"] = EUROSTAT_FINANCE_PATH.name
    eurostat["note"] = "Historical institution expenditure by level and sector from Eurostat UOE"

    students = pd.read_csv(MINISTRY_STUDENTS_PATH)
    students["students_total"] = pd.to_numeric(students["students_total"], errors="coerce")
    school_students_total = float(students["students_total"].sum())

    siope = pd.read_csv(SIOPE_SUMMARY_PATH)
    siope["anno"] = pd.to_numeric(siope["anno"], errors="coerce")
    siope["importo_euro"] = pd.to_numeric(siope["importo_euro"], errors="coerce")
    siope_annual = (
        siope.groupby("anno", dropna=True)
        .agg(nominal_eur=("importo_euro", "sum"))
        .reset_index()
        .rename(columns={"anno": "year"})
    )
    siope_annual = siope_annual.loc[siope_annual["year"].notna()].copy()
    siope_annual["year"] = siope_annual["year"].astype(int)
    siope_annual = siope_annual.merge(cpi, on="year", how="left")
    siope_annual["nominal_million_eur"] = siope_annual["nominal_eur"] / 1_000_000
    siope_annual["sector"] = "PUBL_LEDGER_PROXY"
    siope_annual["sector_label"] = "School ledger proxy"
    siope_annual["isced11"] = "SCHOOL_ALL"
    siope_annual["level_label"] = "School system all levels"
    siope_annual["series_group"] = "siope_school_proxy"
    siope_annual["real_base_year_eur"] = siope_annual["nominal_eur"] * base_cpi_value / siope_annual["cpi_index"]
    siope_annual["real_base_year"] = BASE_REAL_YEAR
    siope_annual["per_student_eur"] = siope_annual["nominal_eur"] / school_students_total
    siope_annual["population_reference"] = f"School students total from {MINISTRY_STUDENTS_PATH.name} (2024/25 stock)"
    siope_annual["source_file"] = SIOPE_SUMMARY_PATH.name
    siope_annual["note"] = "School-ledger expenditure proxy; comparable within SIOPE but not directly additive to Eurostat institutional totals"

    tuition = pd.read_csv(TUITION_BENCHMARK_PATH)
    tuition = tuition.loc[:, ["academic_year", "aggregation_name", "avg_tuition_all_students_eur", "avg_tuition_payers_eur"]].copy()
    tuition["avg_tuition_all_students_eur"] = pd.to_numeric(tuition["avg_tuition_all_students_eur"], errors="coerce")
    tuition["avg_tuition_payers_eur"] = pd.to_numeric(tuition["avg_tuition_payers_eur"], errors="coerce")
    tuition["year"] = tuition["academic_year"].astype(str).str.extract(r"(\d{4})").astype(float)
    tuition = tuition.loc[tuition["year"].notna()].copy()
    tuition["year"] = tuition["year"].astype(int)
    tuition = tuition.merge(cpi, on="year", how="left")
    tuition["nominal_eur"] = tuition["avg_tuition_all_students_eur"]
    tuition["nominal_million_eur"] = tuition["nominal_eur"] / 1_000_000
    tuition["sector"] = "HOUSEHOLD_TUITION_PROXY"
    tuition["sector_label"] = "Household tuition proxy"
    tuition["isced11"] = "ED6-8"
    tuition["level_label"] = "Tertiary education"
    tuition["series_group"] = "university_tuition_proxy"
    tuition["real_base_year_eur"] = tuition["nominal_eur"] * base_cpi_value / tuition["cpi_index"]
    tuition["real_base_year"] = BASE_REAL_YEAR
    tuition["per_student_eur"] = tuition["avg_tuition_all_students_eur"]
    tuition["population_reference"] = "Average tuition per enrolled student from national MUR benchmark"
    tuition["source_file"] = TUITION_BENCHMARK_PATH.name
    tuition["note"] = "Micro-cost proxy rather than full tertiary expenditure"
    tuition = tuition.rename(columns={"aggregation_name": "aggregation_label"})

    finance = pd.concat(
        [
            eurostat,
            siope_annual,
            tuition,
        ],
        ignore_index=True,
        sort=False,
    )
    finance = finance.sort_values(["series_group", "year", "sector", "isced11"]).reset_index(drop=True)
    finance.to_csv(FINANCE_OUTPUT_PATH, index=False)
    return finance


def build_household_module() -> pd.DataFrame:
    rows: list[dict] = []

    oecd = pd.read_csv(OECD_TREND_PATH)
    oecd["TIME_PERIOD"] = pd.to_numeric(oecd["TIME_PERIOD"], errors="coerce")
    latest_oecd = oecd.loc[oecd["TIME_PERIOD"].notna()].sort_values("TIME_PERIOD").iloc[-1]
    rows.extend(
        [
            {
                "domain": "macro_household_share",
                "reference_period": int(latest_oecd["TIME_PERIOD"]),
                "segment": "system-wide",
                "indicator": "parents_private_pct_gdp",
                "value": safe_float(latest_oecd.get("parents_private_pct_gdp")),
                "unit": "pct_gdp",
                "min_eur": pd.NA,
                "max_eur": pd.NA,
                "source_file": OECD_TREND_PATH.name,
                "note": "Household/private share of GDP devoted to education",
            },
            {
                "domain": "macro_household_share",
                "reference_period": int(latest_oecd["TIME_PERIOD"]),
                "segment": "system-wide",
                "indicator": "parents_private_share_of_total_pct",
                "value": safe_float(latest_oecd.get("parents_private_share_of_total_pct")),
                "unit": "pct",
                "min_eur": pd.NA,
                "max_eur": pd.NA,
                "source_file": OECD_TREND_PATH.name,
                "note": "Household/private share of total education expenditure",
            },
        ]
    )

    snapshot = pd.read_csv(HOUSEHOLD_SNAPSHOT_PATH)
    for _, row in snapshot.iterrows():
        rows.append(
            {
                "domain": "household_micro_cost",
                "reference_period": row.get("school_year"),
                "segment": row.get("level"),
                "indicator": row.get("indicator"),
                "value": pd.NA,
                "unit": "eur",
                "min_eur": safe_float(row.get("min_eur")),
                "max_eur": safe_float(row.get("max_eur")),
                "source_file": row.get("source_file", HOUSEHOLD_SNAPSHOT_PATH.name),
                "note": row.get("note"),
            }
        )

    atenei = pd.read_csv(ATENEI_SUPPORT_PATH)
    weighted_total = atenei["students_in_contrib_classes_total"].fillna(0).sum()
    no_contrib_weighted = safe_div((atenei["share_no_contrib_class"].fillna(0) * atenei["students_in_contrib_classes_total"].fillna(0)).sum(), weighted_total)
    up_to_500_weighted = safe_div((atenei["share_contrib_up_to_500"].fillna(0) * atenei["students_in_contrib_classes_total"].fillna(0)).sum(), weighted_total)
    rows.extend(
        [
            {
                "domain": "tertiary_access_buffer",
                "reference_period": "2023-2024",
                "segment": "national weighted",
                "indicator": "share_no_contrib_class",
                "value": no_contrib_weighted,
                "unit": "share",
                "min_eur": pd.NA,
                "max_eur": pd.NA,
                "source_file": ATENEI_SUPPORT_PATH.name,
                "note": "Weighted share of university students in no-contribution class",
            },
            {
                "domain": "tertiary_access_buffer",
                "reference_period": "2023-2024",
                "segment": "national weighted",
                "indicator": "share_contrib_up_to_500",
                "value": up_to_500_weighted,
                "unit": "share",
                "min_eur": pd.NA,
                "max_eur": pd.NA,
                "source_file": ATENEI_SUPPORT_PATH.name,
                "note": "Weighted share of university students paying at most 500 EUR",
            },
        ]
    )

    dsu = pd.read_csv(DSU_SUPPORT_PATH)
    dsu_spend = pd.to_numeric(dsu["spesa_dsu_total"], errors="coerce")
    dsu_eligible = pd.to_numeric(dsu["eligible_students_total"], errors="coerce")
    dsu_beneficiaries = pd.to_numeric(dsu["beneficiaries_borse_total"], errors="coerce")
    rows.extend(
        [
            {
                "domain": "tertiary_support",
                "reference_period": "2024-2025",
                "segment": "national total",
                "indicator": "spesa_dsu_total",
                "value": float(dsu_spend.sum()),
                "unit": "eur",
                "min_eur": pd.NA,
                "max_eur": pd.NA,
                "source_file": DSU_SUPPORT_PATH.name,
                "note": "Observed regional DSU/ERSU support expenditure total",
            },
            {
                "domain": "tertiary_support",
                "reference_period": "2024-2025",
                "segment": "national total",
                "indicator": "support_eur_per_eligible_student",
                "value": safe_div(dsu_spend.sum(), dsu_eligible.sum()),
                "unit": "eur_per_student",
                "min_eur": pd.NA,
                "max_eur": pd.NA,
                "source_file": DSU_SUPPORT_PATH.name,
                "note": "Support expenditure divided by eligible students",
            },
            {
                "domain": "tertiary_support",
                "reference_period": "2024-2025",
                "segment": "national total",
                "indicator": "support_eur_per_grant_beneficiary",
                "value": safe_div(dsu_spend.sum(), dsu_beneficiaries.sum()),
                "unit": "eur_per_beneficiary",
                "min_eur": pd.NA,
                "max_eur": pd.NA,
                "source_file": DSU_SUPPORT_PATH.name,
                "note": "Support expenditure divided by observed grant beneficiaries",
            },
        ]
    )

    household = pd.DataFrame(rows)
    household.to_csv(HOUSEHOLD_OUTPUT_PATH, index=False)
    return household


def load_regional_school_stock() -> pd.DataFrame:
    students = pd.read_csv(MINISTRY_STUDENTS_PATH)
    students["region_name"] = students["region"].map(normalize_region_name)
    students["students_total"] = pd.to_numeric(students["students_total"], errors="coerce")
    wide = (
        students.pivot_table(
            index="region_name",
            columns="order",
            values="students_total",
            aggfunc="sum",
        )
        .reset_index()
        .rename_axis(columns=None)
    )
    wide = wide.rename(
        columns={
            "SCUOLA PRIMARIA": "students_primary",
            "SCUOLA SECONDARIA I GRADO": "students_lower_secondary",
            "SCUOLA SECONDARIA II GRADO": "students_upper_secondary",
        }
    )
    stock = students.groupby("region_name", as_index=False).agg(school_students_total=("students_total", "sum"))
    stock = stock.merge(wide, on="region_name", how="left")
    return stock


def load_regional_special_needs(path: Path, value_col: str, output_col: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    frame["region_name"] = frame["region"].map(normalize_region_name)
    frame[value_col] = pd.to_numeric(frame[value_col], errors="coerce")
    return frame.groupby("region_name", as_index=False).agg(**{output_col: (value_col, "sum")})


def load_regional_neet() -> pd.DataFrame:
    frame = pd.read_csv(NEET_REGIONAL_PATH)
    frame["TIME_PERIOD"] = pd.to_numeric(frame["TIME_PERIOD"], errors="coerce")
    frame = frame.loc[frame["TIME_PERIOD"].eq(2024)].copy()
    frame = frame.loc[~frame["Territorio"].isin(["Nord-ovest", "Nord-est", "Isole"])].copy()
    frame = frame.loc[~frame["Territorio"].str.contains("Provincia Autonoma", na=False)].copy()
    frame = frame.rename(columns={"REF_AREA": "neet_region_code", "Territorio": "region_name", "neet_count_15_29": "neet_count_15_29_thousands"})
    return frame.loc[:, ["neet_region_code", "region_name", "neet_count_15_29_thousands", "neet_risk_index", "neet_percentile", "covid_period"]]


def load_regional_lower_secondary() -> pd.DataFrame:
    frame = pd.read_csv(LOWER_SECONDARY_PATH)
    frame["TIME_PERIOD"] = pd.to_numeric(frame["TIME_PERIOD"], errors="coerce")
    frame = frame.loc[
        frame["TIME_PERIOD"].eq(2024)
        & frame["TYPE_SCHOOL_MANAGEMENT"].eq("ALL")
        & frame["DATA_TYPE"].isin(["DISAB", "ENROL"])
    ].copy()
    frame = frame.loc[~frame["REF_AREA_LABEL"].isin(["Nord-ovest", "Nord-est", "Isole"])].copy()
    frame = frame.loc[~frame["REF_AREA_LABEL"].str.contains("Provincia|Metropolitana", na=False)].copy()
    frame["region_name"] = frame["REF_AREA_LABEL"].map(normalize_region_name)
    pivot = (
        frame.pivot_table(index="region_name", columns="DATA_TYPE", values="OBS_VALUE", aggfunc="first")
        .reset_index()
        .rename_axis(columns=None)
        .rename(columns={"DISAB": "lower_secondary_disabled_per_1000", "ENROL": "lower_secondary_students_per_class"})
    )
    return pivot


def load_regional_repeaters() -> pd.DataFrame:
    frame = pd.read_csv(REPEATERS_PATH)
    frame["TIME_PERIOD"] = pd.to_numeric(frame["TIME_PERIOD"], errors="coerce")
    frame = frame.loc[frame["TIME_PERIOD"].eq(2024) & frame["TYPE_SCHOOL"].eq("ALL")].copy()
    frame = frame.loc[~frame["REF_AREA_LABEL"].isin(["Nord-ovest", "Nord-est", "Isole"])].copy()
    frame = frame.loc[~frame["REF_AREA_LABEL"].str.contains("Provincia|Metropolitana", na=False)].copy()
    frame["region_name"] = frame["REF_AREA_LABEL"].map(normalize_region_name)
    frame = frame.rename(columns={"repeaters": "upper_secondary_repeaters_pct"})
    return frame.loc[:, ["region_name", "upper_secondary_repeaters_pct"]]


def load_regional_dsu() -> pd.DataFrame:
    dsu = pd.read_csv(DSU_SUPPORT_PATH)
    dsu["region_name"] = dsu["region"].map(normalize_region_name)
    numeric_cols = [
        "applications_total",
        "eligible_students_total",
        "beneficiaries_borse_total",
        "spesa_borse_total",
        "spesa_dsu_total",
        "pasti_erogati_total",
        "studenti_mensa_total",
    ]
    for col in numeric_cols:
        dsu[col] = pd.to_numeric(dsu[col], errors="coerce")
    regional = dsu.groupby("region_name", as_index=False).agg(
        dsu_applications_total=("applications_total", "sum"),
        dsu_eligible_students_total=("eligible_students_total", "sum"),
        dsu_grant_beneficiaries_total=("beneficiaries_borse_total", "sum"),
        dsu_grant_spend_eur=("spesa_borse_total", "sum"),
        dsu_total_spend_eur=("spesa_dsu_total", "sum"),
        dsu_meals_total=("pasti_erogati_total", "sum"),
        dsu_meal_students_total=("studenti_mensa_total", "sum"),
    )
    regional["dsu_spend_per_eligible_eur"] = regional.apply(
        lambda row: safe_div(row["dsu_total_spend_eur"], row["dsu_eligible_students_total"]),
        axis=1,
    )
    regional["dsu_spend_per_beneficiary_eur"] = regional.apply(
        lambda row: safe_div(row["dsu_total_spend_eur"], row["dsu_grant_beneficiaries_total"]),
        axis=1,
    )
    return regional


def build_territorial_panel() -> pd.DataFrame:
    panel = load_regional_school_stock()
    panel = panel.merge(load_regional_special_needs(DISABLED_PATH, "estimated_disabled_students", "estimated_disabled_students_total"), on="region_name", how="left")
    panel = panel.merge(load_regional_special_needs(BES_PATH, "estimated_bes_students", "estimated_bes_students_total"), on="region_name", how="left")
    panel = panel.merge(load_regional_neet(), on="region_name", how="left")
    panel = panel.merge(load_regional_lower_secondary(), on="region_name", how="left")
    panel = panel.merge(load_regional_repeaters(), on="region_name", how="left")
    panel = panel.merge(load_regional_dsu(), on="region_name", how="left")

    panel["estimated_disabled_share_pct"] = panel.apply(
        lambda row: safe_div(row.get("estimated_disabled_students_total"), row.get("school_students_total")) * 100
        if safe_div(row.get("estimated_disabled_students_total"), row.get("school_students_total")) is not None
        else None,
        axis=1,
    )
    panel["estimated_bes_share_pct"] = panel.apply(
        lambda row: safe_div(row.get("estimated_bes_students_total"), row.get("school_students_total")) * 100
        if safe_div(row.get("estimated_bes_students_total"), row.get("school_students_total")) is not None
        else None,
        axis=1,
    )
    panel["funding_proxy_scope"] = "Regional funding proxy covers tertiary DSU/ERSU support, not whole school-system expenditure"
    panel = panel.sort_values("region_name").reset_index(drop=True)
    panel.to_csv(TERRITORIAL_OUTPUT_PATH, index=False)
    return panel


def write_note(finance: pd.DataFrame, household: pd.DataFrame, territorial: pd.DataFrame) -> None:
    eurostat_max_year = int(finance.loc[finance["series_group"].eq("eurostat_level_history"), "year"].max())
    siope_max_year = int(finance.loc[finance["series_group"].eq("siope_school_proxy"), "year"].max())
    latest_private_share = household.loc[household["indicator"].eq("parents_private_share_of_total_pct"), "value"].dropna()
    top_tertiary_support = territorial.sort_values("dsu_total_spend_eur", ascending=False).head(5)
    lines = [
        "# Education gap modules",
        "",
        f"Generated on {date.today().isoformat()}.",
        "",
        "## What this adds",
        "",
        f"- Eurostat level-aware expenditure history for Italy, inflation-adjusted to {BASE_REAL_YEAR} euros through a World Bank CPI fetch.",
        "- A richer household burden module combining macro private-spending shares, school material costs, tuition buffers, and DSU support totals.",
        "- A territorial proxy panel joining regional school stocks and outcome indicators with named regional tertiary support spending.",
        "",
        "## Caveats",
        "",
        f"- Eurostat education finance currently ends in {eurostat_max_year}; current school-spend proxies come from SIOPE through {siope_max_year}.",
        "- The territorial funding join uses DSU/ERSU regional support spending because available SIOPE region pivots use unstable territorial codes and would be misleading as a direct school-spend join.",
        "- School per-student proxy values use 2024/25 ministry student stocks as the denominator, so they are best read as current operating proxies rather than strict historical rates.",
        "",
        "## Quick reads",
        "",
    ]
    if not latest_private_share.empty:
        lines.append(f"- Latest OECD-based household/private share of total education expenditure in the workspace trend file: {latest_private_share.iloc[0]:.1f}%.")
    for _, row in top_tertiary_support.iterrows():
        spend = safe_float(row.get("dsu_total_spend_eur"))
        if spend is None:
            continue
        lines.append(f"- {row['region_name']}: about EUR {spend:,.0f} in observed regional DSU/ERSU support spending.")
    NOTE_OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest() -> None:
    manifest = {
        "generated_on": date.today().isoformat(),
        "outputs": [
            FINANCE_OUTPUT_PATH.name,
            HOUSEHOLD_OUTPUT_PATH.name,
            TERRITORIAL_OUTPUT_PATH.name,
            CPI_OUTPUT_PATH.name,
            NOTE_OUTPUT_PATH.name,
        ],
        "sources": [
            EUROSTAT_FINANCE_PATH.name,
            OECD_TREND_PATH.name,
            HOUSEHOLD_SNAPSHOT_PATH.name,
            TUITION_BENCHMARK_PATH.name,
            DSU_SUPPORT_PATH.name,
            ATENEI_SUPPORT_PATH.name,
            SIOPE_SUMMARY_PATH.name,
            MINISTRY_STUDENTS_PATH.name,
            NEET_REGIONAL_PATH.name,
            LOWER_SECONDARY_PATH.name,
            REPEATERS_PATH.name,
            DISABLED_PATH.name,
            BES_PATH.name,
            CPI_URL,
        ],
    }
    MANIFEST_OUTPUT_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    cpi = fetch_cpi_series()
    finance = build_finance_panel(cpi)
    household = build_household_module()
    territorial = build_territorial_panel()
    write_note(finance, household, territorial)
    write_manifest()
    print(f"Wrote {FINANCE_OUTPUT_PATH}")
    print(f"Wrote {HOUSEHOLD_OUTPUT_PATH}")
    print(f"Wrote {TERRITORIAL_OUTPUT_PATH}")
    print(f"Wrote {CPI_OUTPUT_PATH}")
    print(f"Wrote {NOTE_OUTPUT_PATH}")
    print(f"Wrote {MANIFEST_OUTPUT_PATH}")


if __name__ == "__main__":
    main()