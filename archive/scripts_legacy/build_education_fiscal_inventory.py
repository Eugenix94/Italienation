#!/usr/bin/env python3
"""Build a compact fiscal inventory for Italy's education system.

This script consolidates the fiscal surfaces already present in the workspace:

- OECD education expenditure split between state, private/household, and total.
- SIOPE school-level expenditure summaries.
- MUR school budget / final accounts / contracts files.
- University tuition benchmark and student support panels.

It writes a CSV inventory plus a short markdown note under local_data/processed/.
"""

from __future__ import annotations

from collections import defaultdict
from datetime import date
from pathlib import Path

import pandas as pd


ROOT = Path(r"c:/Users/Dell/Documents/VSC Projects/Italienation")
LOCAL = ROOT / "local_data"
PROCESSED = LOCAL / "processed"
MUR_BILANCIO = LOCAL / "MinIstruzione" / "BilancioeFinanze"


def money(value: float | int | None) -> float:
    if value is None:
        return 0.0
    try:
        return float(value)
    except Exception:
        return 0.0


def add_row(rows: list[dict], **kwargs) -> None:
    rows.append(kwargs)


def summarize_oecd(rows: list[dict]) -> None:
    path = PROCESSED / "education_expenditure_state_parents_gdp_latest.csv"
    if not path.exists():
        return

    df = pd.read_csv(path)
    italy = df.loc[df["REF_AREA"].eq("ITA")].sort_values("TIME_PERIOD")
    if italy.empty:
        return

    latest = italy.iloc[-1]
    add_row(
        rows,
        source_group="OECD macro education spending",
        source_file=path.name,
        direction="expenditure",
        coverage="system-wide",
        latest_year=int(latest["TIME_PERIOD"]),
        metric="state_pct_gdp",
        value=money(latest["state_pct_gdp"]),
        unit="pct_gdp",
        note="Government / state education spending share of GDP",
    )
    add_row(
        rows,
        source_group="OECD macro education spending",
        source_file=path.name,
        direction="expenditure",
        coverage="system-wide",
        latest_year=int(latest["TIME_PERIOD"]),
        metric="parents_private_pct_gdp",
        value=money(latest["parents_private_pct_gdp"]),
        unit="pct_gdp",
        note="Household / private education spending share of GDP",
    )
    add_row(
        rows,
        source_group="OECD macro education spending",
        source_file=path.name,
        direction="expenditure",
        coverage="system-wide",
        latest_year=int(latest["TIME_PERIOD"]),
        metric="total_pct_gdp",
        value=money(latest["total_pct_gdp"]),
        unit="pct_gdp",
        note="Total education spending share of GDP",
    )
    add_row(
        rows,
        source_group="OECD macro education spending",
        source_file=path.name,
        direction="expenditure",
        coverage="system-wide",
        latest_year=int(latest["TIME_PERIOD"]),
        metric="state_share_of_total_pct",
        value=money(latest["state_share_of_total_pct"]),
        unit="pct",
        note="Share of total spending funded by the state",
    )
    add_row(
        rows,
        source_group="OECD macro education spending",
        source_file=path.name,
        direction="expenditure",
        coverage="system-wide",
        latest_year=int(latest["TIME_PERIOD"]),
        metric="parents_private_share_of_total_pct",
        value=money(latest["parents_private_share_of_total_pct"]),
        unit="pct",
        note="Share of total spending funded by parents/households",
    )


def summarize_siope(rows: list[dict]) -> None:
    path = PROCESSED / "siope_school_expenditure_summary.csv"
    if not path.exists():
        return

    df = pd.read_csv(path)
    df["importo_euro"] = pd.to_numeric(df["importo_euro"], errors="coerce")
    df["anno"] = pd.to_numeric(df["anno"], errors="coerce")
    total_by_year = df.groupby("anno", dropna=True)["importo_euro"].sum().sort_index()

    add_row(
        rows,
        source_group="SIOPE school ledgers",
        source_file=path.name,
        direction="expenditure",
        coverage="school-level",
        latest_year=int(total_by_year.index.max()),
        metric="total_school_expenditure",
        value=money(df["importo_euro"].sum()),
        unit="eur",
        note=f"School expenditure aggregated from {len(df):,} school-year rows",
    )
    add_row(
        rows,
        source_group="SIOPE school ledgers",
        source_file=path.name,
        direction="expenditure",
        coverage="school-level",
        latest_year=int(total_by_year.index.max()),
        metric="unique_schools",
        value=int(df["codice_ente"].nunique()),
        unit="count",
        note="Unique schools appearing in the summary table",
    )
    add_row(
        rows,
        source_group="SIOPE school ledgers",
        source_file=path.name,
        direction="expenditure",
        coverage="school-level",
        latest_year=int(total_by_year.index.max()),
        metric="years_covered",
        value=int(df["anno"].nunique()),
        unit="count",
        note="Number of years present in the summary table",
    )
    current_year = date.today().year
    for year, value in total_by_year.tail(3).items():
        partial_note = "in-year / partial" if int(year) == current_year else "annual total"
        add_row(
            rows,
            source_group="SIOPE school ledgers",
            source_file=path.name,
            direction="expenditure",
            coverage="school-level",
            latest_year=int(year),
            metric="annual_school_expenditure",
            value=money(value),
            unit="eur",
            note=f"{partial_note} school expenditure in the summary table",
        )


def load_mur_budget(path: Path, mode: str) -> dict:
    metrics: dict[str, float] = defaultdict(float)
    rows = 0
    schools: set[str] = set()
    regions: set[str] = set()
    years: set[int] = set()
    top_level1: dict[tuple[str, str], float] = defaultdict(float)
    top_level2: dict[tuple[str, str, str], float] = defaultdict(float)

    usecols_common = ["ANNOSCOLASTICO", "ANNOFINANZIARIO", "REGIONE", "CODICESCUOLA", "TIPOLOGIAVOCE", "CODICELIVELLO1", "CODICELIVELLO2", "IMPORTO"]
    if mode == "consuntivo":
        usecols_common.extend(["IMPORTOACCERTATOIMPEGNATO", "IMPORTORISCOSSOPAGATO", "IMPORTODARISCUOTEREDAPAGARE"])
    elif mode == "contratti":
        usecols_common.extend(["CODICECIG", "OGGETTOBANDO", "PROCEDURASCELTA", "IMPORTOGARA", "IMPORTOAGGIUDICAZIONE"])

    for chunk in pd.read_csv(path, sep=",", usecols=lambda c: c in usecols_common, chunksize=100_000, low_memory=False):
        rows += len(chunk)
        if "CODICESCUOLA" in chunk.columns:
            schools.update(chunk["CODICESCUOLA"].dropna().astype(str))
        if "REGIONE" in chunk.columns:
            regions.update(chunk["REGIONE"].dropna().astype(str))
        if "ANNOFINANZIARIO" in chunk.columns:
            years.update(pd.to_numeric(chunk["ANNOFINANZIARIO"], errors="coerce").dropna().astype(int).tolist())

        if mode in {"progno", "consuntivo"}:
            chunk["IMPORTO"] = pd.to_numeric(chunk.get("IMPORTO"), errors="coerce").fillna(0)
            by_tipologia = chunk.groupby("TIPOLOGIAVOCE")["IMPORTO"].sum()
            for key, value in by_tipologia.items():
                metrics[f"tipologia::{key}"] += float(value)

            by_level1 = chunk.groupby(["TIPOLOGIAVOCE", "CODICELIVELLO1"])["IMPORTO"].sum()
            for (tipologia, level1), value in by_level1.items():
                top_level1[(tipologia, str(level1))] += float(value)

            by_level2 = chunk.groupby(["TIPOLOGIAVOCE", "CODICELIVELLO1", "CODICELIVELLO2"])["IMPORTO"].sum()
            for (tipologia, level1, level2), value in by_level2.items():
                top_level2[(tipologia, str(level1), str(level2))] += float(value)

            if mode == "consuntivo":
                for col in ["IMPORTOACCERTATOIMPEGNATO", "IMPORTORISCOSSOPAGATO", "IMPORTODARISCUOTEREDAPAGARE"]:
                    chunk[col] = pd.to_numeric(chunk.get(col), errors="coerce").fillna(0)
                    metrics[col.lower()] += float(chunk[col].sum())

        elif mode == "contratti":
            for col in ["IMPORTOGARA", "IMPORTOAGGIUDICAZIONE"]:
                chunk[col] = pd.to_numeric(chunk.get(col), errors="coerce").fillna(0)
                metrics[col.lower()] += float(chunk[col].sum())

    return {
        "rows": rows,
        "schools": len(schools),
        "regions": len(regions),
        "years": len(years),
        "latest_year": max(years) if years else None,
        "metrics": metrics,
        "top_level1": top_level1,
        "top_level2": top_level2,
    }


def summarize_mur(rows: list[dict]) -> None:
    file_map = [
        (MUR_BILANCIO / "BISPROGANNO202520260320.csv", "progno"),
        (MUR_BILANCIO / "BISCONSUNTIVO202520251220.csv", "consuntivo"),
        (MUR_BILANCIO / "BISCONTRATTI202420250921.csv", "contratti"),
    ]

    for path, mode in file_map:
        if not path.exists():
            continue
        summary = load_mur_budget(path, mode)
        add_row(
            rows,
            source_group="MUR school finance and procurement",
            source_file=path.name,
            direction="entries+expenditures" if mode != "contratti" else "contracts",
            coverage="school-level",
            latest_year=summary["latest_year"],
            metric="rows",
            value=summary["rows"],
            unit="count",
            note="Raw school finance/procurement rows",
        )
        add_row(
            rows,
            source_group="MUR school finance and procurement",
            source_file=path.name,
            direction="entries+expenditures" if mode != "contratti" else "contracts",
            coverage="school-level",
            latest_year=summary["latest_year"],
            metric="unique_schools",
            value=summary["schools"],
            unit="count",
            note="Unique school codes in the file",
        )
        add_row(
            rows,
            source_group="MUR school finance and procurement",
            source_file=path.name,
            direction="entries+expenditures" if mode != "contratti" else "contracts",
            coverage="school-level",
            latest_year=summary["latest_year"],
            metric="unique_regions",
            value=summary["regions"],
            unit="count",
            note="Unique regions in the file",
        )
        if mode == "progno":
            add_row(rows, source_group="MUR school finance and procurement", source_file=path.name, direction="entries", coverage="school-level", latest_year=summary["latest_year"], metric="total_entries", value=money(summary["metrics"].get("tipologia::ENTRATA")), unit="eur", note="Planned budget entries")
            add_row(rows, source_group="MUR school finance and procurement", source_file=path.name, direction="expenditure", coverage="school-level", latest_year=summary["latest_year"], metric="total_expenditures", value=money(summary["metrics"].get("tipologia::SPESA")), unit="eur", note="Planned budget expenditures")
        elif mode == "consuntivo":
            add_row(rows, source_group="MUR school finance and procurement", source_file=path.name, direction="entries", coverage="school-level", latest_year=summary["latest_year"], metric="total_entries", value=money(summary["metrics"].get("tipologia::ENTRATA")), unit="eur", note="Final-account entries")
            add_row(rows, source_group="MUR school finance and procurement", source_file=path.name, direction="expenditure", coverage="school-level", latest_year=summary["latest_year"], metric="total_expenditures", value=money(summary["metrics"].get("tipologia::SPESA")), unit="eur", note="Final-account expenditures")
            add_row(rows, source_group="MUR school finance and procurement", source_file=path.name, direction="entries+expenditures", coverage="school-level", latest_year=summary["latest_year"], metric="importo_accertato_impegnato", value=money(summary["metrics"].get("importoaccertatoimpegnato")), unit="eur", note="Committed/assessed amount")
            add_row(rows, source_group="MUR school finance and procurement", source_file=path.name, direction="entries+expenditures", coverage="school-level", latest_year=summary["latest_year"], metric="importo_riscosso_pagato", value=money(summary["metrics"].get("importoriscossopagato")), unit="eur", note="Collected/paid amount")
            add_row(rows, source_group="MUR school finance and procurement", source_file=path.name, direction="entries+expenditures", coverage="school-level", latest_year=summary["latest_year"], metric="importo_da_riscuotere_da_pagare", value=money(summary["metrics"].get("importodariscuoteredapagare")), unit="eur", note="Receivable / payable amount")
        else:
            add_row(rows, source_group="MUR school finance and procurement", source_file=path.name, direction="contracts", coverage="school-level", latest_year=summary["latest_year"], metric="total_gara_importo", value=money(summary["metrics"].get("importogara")), unit="eur", note="Tendered amount")
            add_row(rows, source_group="MUR school finance and procurement", source_file=path.name, direction="contracts", coverage="school-level", latest_year=summary["latest_year"], metric="total_awarded_importo", value=money(summary["metrics"].get("importoaggiudicazione")), unit="eur", note="Awarded amount")


def summarize_support(rows: list[dict]) -> None:
    tuition_path = PROCESSED / "italy_mur_tuition_benchmark_2024.csv"
    if tuition_path.exists():
        df = pd.read_csv(tuition_path)
        for _, item in df.iterrows():
            add_row(
                rows,
                source_group="MUR tuition and cost sharing",
                source_file=tuition_path.name,
                direction="household cost",
                coverage=str(item["aggregation_name"]),
                latest_year=str(item["academic_year"]),
                metric="avg_tuition_payers_eur",
                value=money(item["avg_tuition_payers_eur"]),
                unit="eur",
                note=str(item["source"]),
            )
            add_row(
                rows,
                source_group="MUR tuition and cost sharing",
                source_file=tuition_path.name,
                direction="household cost",
                coverage=str(item["aggregation_name"]),
                latest_year=str(item["academic_year"]),
                metric="avg_tuition_all_students_eur",
                value=money(item["avg_tuition_all_students_eur"]),
                unit="eur",
                note=str(item["source"]),
            )

    dsu_path = PROCESSED / "dsu_ersu_support_panel_2024_2025.csv"
    if dsu_path.exists():
        df = pd.read_csv(dsu_path)
        for col in ["spesa_dsu_total", "spesa_borse_total", "spesa_alloggi_total", "spesa_ristorazione_total", "applications_total", "beneficiaries_borse_total"]:
            add_row(
                rows,
                source_group="University student support",
                source_file=dsu_path.name,
                direction="support expenditure",
                coverage="regional support bodies",
                latest_year=str(df["academic_year"].max()),
                metric=col,
                value=money(pd.to_numeric(df[col], errors="coerce").sum()),
                unit="eur" if col.startswith("spesa_") else "count",
                note="Aggregated across regional support entities",
            )


def build_inventory() -> pd.DataFrame:
    rows: list[dict] = []
    summarize_oecd(rows)
    summarize_siope(rows)
    summarize_mur(rows)
    summarize_support(rows)
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(["source_group", "source_file", "metric"], kind="stable").reset_index(drop=True)
    return df


def write_report(df: pd.DataFrame) -> None:
    inventory_path = PROCESSED / "education_fiscal_inventory.csv"
    report_path = PROCESSED / "education_fiscal_sources_map.md"
    manifest_path = PROCESSED / "education_fiscal_source_manifest.json"

    df.to_csv(inventory_path, index=False)

    source_lines = [
        "# Education Fiscal Sources Map",
        "",
        "This map consolidates the education-system fiscal evidence already present in the workspace.",
        "",
        "## Coverage",
        "- OECD macro split: state vs household/private vs total education spending as share of GDP and USD PPP.",
        "- SIOPE school ledgers: school-level expenditure summaries by year, region, and school code.",
        "- MUR school finance: school budget plans, final accounts, and contracts.",
        "- MUR higher education costs: tuition benchmark and student-support expenditure.",
        "",
        "## Main blind spots",
        "- No single file yet spans the whole system from preschool through university on the same accounting basis.",
        "- School-ledger data and macro OECD data are complementary, not identical, and should not be merged without level-aware adjustments.",
        "- University tuition/support data cover higher education only; they do not proxy mandatory school-level household costs.",
        "",
        "## Snapshot rows",
        "",
    ]
    for _, row in df.head(30).iterrows():
        source_lines.append(
            f"- {row['source_group']} | {row['source_file']} | {row['metric']} = {row['value']:.3f} {row['unit']} ({row['direction']}, {row['coverage']}, latest {row['latest_year']})"
        )

    report_path.write_text("\n".join(source_lines), encoding="utf-8")

    manifest = {
        "inventory_csv": inventory_path.name,
        "report_md": report_path.name,
        "source_files": sorted(df["source_file"].dropna().unique().tolist()),
        "row_count": int(len(df)),
    }
    manifest_path.write_text(pd.Series(manifest).to_json(indent=2), encoding="utf-8")


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df = build_inventory()
    if df.empty:
        raise SystemExit("No fiscal rows were built")
    write_report(df)
    print(f"inventory_rows={len(df)}")
    print(f"inventory_csv={(PROCESSED / 'education_fiscal_inventory.csv')}")
    print(f"report_md={(PROCESSED / 'education_fiscal_sources_map.md')}")


if __name__ == "__main__":
    main()