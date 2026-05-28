#!/usr/bin/env python3
"""Build Italy education expenditure history and supporting source extracts.

Outputs:
- local_data/processed/italy_education_expenditure_history_panel.csv
- local_data/processed/italy_school_household_cost_snapshot.csv
- local_data/processed/save_the_children_italy_school_stats.csv
- local_data/processed/education_expenditure_web_sources_2026-05-27.md
- local_data/processed/education_expenditure_web_sources_manifest.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd
import requests
from pypdf import PdfReader


ROOT = Path(r"c:/Users/Dell/Documents/VSC Projects/Italienation")
LOCAL = ROOT / "local_data"
PROCESSED = LOCAL / "processed"
OWID = LOCAL / "ourWorldData"

SAVE_CHILDREN_PDF_URL = "https://s3-www.savethechildren.it/public/files/Scheda_scuole.pdf"
SAVE_CHILDREN_PDF_PATH = LOCAL / "SaveTheChildren" / "Scheda_scuole.pdf"
SAVE_CHILDREN_TEXT_PATH = PROCESSED / "save_the_children_scheda_scuole_excerpt.txt"


def load_oecd_trend() -> pd.DataFrame:
    path = PROCESSED / "italy_education_expenditure_state_parents_trend.csv"
    df = pd.read_csv(path)
    df = df.rename(columns={"TIME_PERIOD": "year"})
    keep = [
        "year",
        "state_pct_gdp",
        "parents_private_pct_gdp",
        "total_pct_gdp",
        "state_share_of_total_pct",
        "parents_private_share_of_total_pct",
        "state_usd_ppp",
        "parents_private_usd_ppp",
        "total_usd_ppp",
    ]
    return df[keep].copy()


def load_owid_public_pct_gdp() -> pd.DataFrame:
    path = OWID / "total-government-expenditure-on-education-gdp" / "total-government-expenditure-on-education-gdp.csv"
    df = pd.read_csv(path)
    df = df.loc[df["Code"].eq("ITA"), ["Year", "Public spending on education as a share of GDP (historical and recent)"]].copy()
    df = df.rename(columns={
        "Year": "year",
        "Public spending on education as a share of GDP (historical and recent)": "public_pct_gdp_owid",
    })
    return df


def load_owid_public_pct_govexp() -> pd.DataFrame:
    path = OWID / "EdGovSpending" / "share-of-education-in-government-expenditure.csv"
    df = pd.read_csv(path)
    df = df.loc[df["Code"].eq("ITA"), ["Year", "Government expenditure on education, total (% of government expenditure)"]].copy()
    df = df.rename(columns={
        "Year": "year",
        "Government expenditure on education, total (% of government expenditure)": "public_pct_govexp_owid",
    })
    return df


def load_siope_annual() -> pd.DataFrame:
    path = PROCESSED / "siope_school_expenditure_summary.csv"
    df = pd.read_csv(path)
    df["anno"] = pd.to_numeric(df["anno"], errors="coerce")
    df["importo_euro"] = pd.to_numeric(df["importo_euro"], errors="coerce")
    annual = (
        df.groupby("anno", dropna=True)
        .agg(
            siope_school_expenditure_eur=("importo_euro", "sum"),
            siope_school_count=("codice_ente", "nunique"),
        )
        .reset_index()
        .rename(columns={"anno": "year"})
    )
    annual["siope_series_note"] = annual["year"].apply(lambda year: "in-year / partial" if int(year) == 2026 else "annual total")
    return annual


def load_household_cost_snapshot() -> pd.DataFrame:
    rows: list[dict] = []

    primary_path = LOCAL / "ItalyPrimarySchoolBookExpenses.csv"
    primary = pd.read_csv(primary_path, comment="#")
    primary_total = primary.loc[primary["Classe"].astype(str).eq("TOTAL")].iloc[0]
    rows.append(
        {
            "level": "primary",
            "indicator": "textbook_cover_price_total",
            "school_year": "2025-2026",
            "min_eur": float(primary_total["Prezzo (€)"]),
            "max_eur": float(primary_total["Prezzo (€)"]),
            "note": "Official primary textbook total from Ministerial Decree n. 73/2025",
            "source_file": primary_path.name,
        }
    )

    secondary_path = LOCAL / "ItalianMeanSecondarySchoolExpenses.csv"
    secondary = pd.read_csv(secondary_path, comment="#")
    for _, row in secondary.iterrows():
        total = str(row["Total Mean Annual Spending (€)"]).replace("≈", "")
        range_match = re.search(r"(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)", total)
        if range_match:
            min_eur = float(range_match.group(1))
            max_eur = float(range_match.group(2))
        else:
            value_match = re.search(r"(\d+(?:\.\d+)?)", total)
            min_eur = max_eur = float(value_match.group(1)) if value_match else None
        rows.append(
            {
                "level": str(row["School Level"]),
                "indicator": "estimated_mean_annual_household_spending",
                "school_year": "undated-current",
                "min_eur": min_eur,
                "max_eur": max_eur,
                "note": "Estimated textbooks plus other materials",
                "source_file": secondary_path.name,
            }
        )

    tuition_path = PROCESSED / "italy_mur_tuition_benchmark_2024.csv"
    tuition = pd.read_csv(tuition_path)
    for _, row in tuition.iterrows():
        rows.append(
            {
                "level": str(row["aggregation_name"]),
                "indicator": "average_university_tuition_all_students",
                "school_year": str(row["academic_year"]),
                "min_eur": float(row["avg_tuition_all_students_eur"]),
                "max_eur": float(row["avg_tuition_all_students_eur"]),
                "note": "Average university tuition across all enrolled students",
                "source_file": tuition_path.name,
            }
        )
        rows.append(
            {
                "level": str(row["aggregation_name"]),
                "indicator": "average_university_tuition_payers",
                "school_year": str(row["academic_year"]),
                "min_eur": float(row["avg_tuition_payers_eur"]),
                "max_eur": float(row["avg_tuition_payers_eur"]),
                "note": "Average university tuition among payers only",
                "source_file": tuition_path.name,
            }
        )

    return pd.DataFrame(rows)


def fetch_save_children_text() -> str:
    SAVE_CHILDREN_PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(SAVE_CHILDREN_PDF_URL, timeout=120)
    response.raise_for_status()
    SAVE_CHILDREN_PDF_PATH.write_bytes(response.content)
    reader = PdfReader(str(SAVE_CHILDREN_PDF_PATH))
    text = "\n".join((page.extract_text() or "") for page in reader.pages[:6])
    SAVE_CHILDREN_TEXT_PATH.write_text(text, encoding="utf-8")
    return text


def extract_first_float(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None
    value = match.group(1).replace(",", ".")
    return float(value)


def build_save_children_stats() -> pd.DataFrame:
    text = fetch_save_children_text()
    stats = [
        {
            "indicator": "students_below_minimum_italian_lower_secondary_pct",
            "value": extract_first_float(r"il\s+(39)%\s+degli studenti.*?competenze in Italiano", text),
            "unit": "pct",
            "reference_year": "INVALSI 2022",
            "source_url": SAVE_CHILDREN_PDF_URL,
            "note": "Lower secondary students below minimum Italian competency level",
        },
        {
            "indicator": "students_below_minimum_math_lower_secondary_pct",
            "value": extract_first_float(r"(44)% in Matematica", text),
            "unit": "pct",
            "reference_year": "INVALSI 2022",
            "source_url": SAVE_CHILDREN_PDF_URL,
            "note": "Lower secondary students below minimum math competency level",
        },
        {
            "indicator": "early_school_leavers_18_24_pct",
            "value": extract_first_float(r"raggiunge il (12,7)%", text),
            "unit": "pct",
            "reference_year": "Eurostat 2021",
            "source_url": SAVE_CHILDREN_PDF_URL,
            "note": "Early school leavers aged 18-24",
        },
        {
            "indicator": "archipelago_learning_gain_math_months",
            "value": extract_first_float(r"raggiunti in (2) mesi di scuola", text),
            "unit": "months",
            "reference_year": "2022 evaluation",
            "source_url": SAVE_CHILDREN_PDF_URL,
            "note": "Equivalent math learning gain for participants",
        },
        {
            "indicator": "archipelago_learning_gain_italian_months",
            "value": extract_first_float(r"raggiunti in (3\.5) mesi di scuola", text),
            "unit": "months",
            "reference_year": "2022 evaluation",
            "source_url": SAVE_CHILDREN_PDF_URL,
            "note": "Equivalent Italian learning gain for participants",
        },
    ]
    df = pd.DataFrame(stats)
    return df.loc[df["value"].notna()].copy()


def build_history_panel() -> pd.DataFrame:
    panel = load_owid_public_pct_gdp()
    panel = panel.merge(load_owid_public_pct_govexp(), on="year", how="outer")
    panel = panel.merge(load_oecd_trend(), on="year", how="outer")
    panel = panel.merge(load_siope_annual(), on="year", how="outer")
    panel = panel.sort_values("year").reset_index(drop=True)
    return panel


def write_web_note(history: pd.DataFrame, save_children: pd.DataFrame, household: pd.DataFrame) -> None:
    latest_public_pct_gdp = history.loc[history["public_pct_gdp_owid"].notna()].iloc[-1]
    latest_public_pct_govexp = history.loc[history["public_pct_govexp_owid"].notna()].iloc[-1]
    latest_oecd = history.loc[history["total_pct_gdp"].notna()].iloc[-1]
    primary = household.loc[household["level"].eq("primary") & household["indicator"].eq("textbook_cover_price_total")].iloc[0]

    lines = [
        "# Education Expenditure Web Sources",
        "",
        "This note combines browser-verified public URLs with locally processed datasets.",
        "",
        "## Verified public URLs",
        "- World Bank public expenditure as % of GDP: https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS?locations=IT",
        "- World Bank public expenditure as % of government expenditure: https://data.worldbank.org/indicator/SE.XPD.TOTL.GB.ZS?locations=IT",
        "- ISTAT educational poverty hub: https://www.istat.it/statistiche-per-temi/focus/la-poverta-educativa/",
        f"- Save the Children school factsheet PDF: {SAVE_CHILDREN_PDF_URL}",
        "",
        "## Processed summary",
        "- Browser verification from the World Bank page shows Italy at 4.1% of GDP in 2022 and 7.4% of government expenditure in 2022.",
        f"- Latest locally available historical panel point for public education spending as % of GDP: {latest_public_pct_gdp['public_pct_gdp_owid']:.1f}% in {int(latest_public_pct_gdp['year'])}.",
        f"- Latest locally available historical panel point for public education spending as % of government expenditure: {latest_public_pct_govexp['public_pct_govexp_owid']:.1f}% in {int(latest_public_pct_govexp['year'])}.",
        f"- Latest OECD Italy split: state {latest_oecd['state_pct_gdp']:.3f}% GDP, parents/private {latest_oecd['parents_private_pct_gdp']:.3f}% GDP, total {latest_oecd['total_pct_gdp']:.3f}% GDP in {int(latest_oecd['year'])}.",
        f"- Official primary textbook cover-price total: EUR {primary['min_eur']:.2f} for 2025-2026.",
        "",
        "## Save the Children extracted indicators",
    ]
    for _, row in save_children.iterrows():
        lines.append(f"- {row['indicator']}: {row['value']} {row['unit']} ({row['reference_year']})")

    (PROCESSED / "education_expenditure_web_sources_2026-05-27.md").write_text("\n".join(lines), encoding="utf-8")

    manifest = {
        "history_panel": "italy_education_expenditure_history_panel.csv",
        "household_snapshot": "italy_school_household_cost_snapshot.csv",
        "save_children_stats": "save_the_children_italy_school_stats.csv",
        "web_note": "education_expenditure_web_sources_2026-05-27.md",
        "verified_urls": [
            "https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS?locations=IT",
            "https://data.worldbank.org/indicator/SE.XPD.TOTL.GB.ZS?locations=IT",
            "https://www.istat.it/statistiche-per-temi/focus/la-poverta-educativa/",
            SAVE_CHILDREN_PDF_URL,
        ],
    }
    (PROCESSED / "education_expenditure_web_sources_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    history = build_history_panel()
    household = load_household_cost_snapshot()
    save_children = build_save_children_stats()

    history.to_csv(PROCESSED / "italy_education_expenditure_history_panel.csv", index=False)
    household.to_csv(PROCESSED / "italy_school_household_cost_snapshot.csv", index=False)
    save_children.to_csv(PROCESSED / "save_the_children_italy_school_stats.csv", index=False)
    write_web_note(history, save_children, household)

    print(f"history_rows={len(history)}")
    print(f"household_rows={len(household)}")
    print(f"save_children_rows={len(save_children)}")


if __name__ == "__main__":
    main()