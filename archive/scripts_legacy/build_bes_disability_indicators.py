from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ISTAT_XLSX = ROOT / "local_data" / "ISTAT" / "istat_disability_schools_2022_2023.xlsx"
ALUNNI_STA = ROOT / "local_data" / "MinIstruzione" / "Alunni" / "ALUCORSOETASTA20242520250831.csv"
ALUNNI_PAR = ROOT / "local_data" / "MinIstruzione" / "Alunni" / "ALUCORSOETAPAR20242520250831.csv"
SCUOLE_STA = ROOT / "local_data" / "MinIstruzione" / "Scuole" / "SCUANAGRAFESTAT20242520250831.csv"
SCUOLE_PAR = ROOT / "local_data" / "MinIstruzione" / "Scuole" / "SCUANAGRAFEPAR20242520250831.csv"
OUT_DIR = ROOT / "local_data" / "processed"


def normalize_order(value: str) -> str:
    v = str(value).strip().upper()
    if "INFANZIA" in v:
        return "SCUOLA INFANZIA"
    if "PRIMARIA" in v:
        return "SCUOLA PRIMARIA"
    if "SECONDARIA II" in v or "SECONDO GRADO" in v:
        return "SCUOLA SECONDARIA II GRADO"
    if "SECONDARIA I" in v or "PRIMO GRADO" in v:
        return "SCUOLA SECONDARIA I GRADO"
    return str(value).strip()


def normalize_region(value: str) -> str:
    return (
        str(value)
        .replace("’", "'")
        .replace("  ", " ")
        .strip()
        .upper()
    )


def read_istat_table(sheet: str) -> pd.DataFrame:
    raw = pd.read_excel(ISTAT_XLSX, sheet_name=sheet, header=None)
    cols = list(raw.iloc[2])
    df = raw.iloc[3:].copy()
    df.columns = cols
    df = df.dropna(how="all")

    first_col = df.columns[0]
    df[first_col] = df[first_col].astype(str).str.strip()
    return df


def build_istat_disability_timeseries() -> pd.DataFrame:
    t1 = read_istat_table("Tavola 1")
    t1 = t1[~t1.iloc[:, 0].str.contains("Fonte|Dato provvisorio", case=False, na=False)].copy()
    t1 = t1.rename(
        columns={
            t1.columns[0]: "school_year",
            "Scuola dell'infanzia": "disability_rate_per_100_infanzia",
            "Scuola primaria": "disability_rate_per_100_primaria",
            "Scuola secondaria di I grado": "disability_rate_per_100_secondaria_i",
            "Scuola secondaria di II grado": "disability_rate_per_100_secondaria_ii",
            "Tutti gli ordini": "disability_rate_per_100_all_orders",
        }
    )

    for c in t1.columns[1:]:
        t1[c] = pd.to_numeric(t1[c], errors="coerce")
    return t1


def build_istat_bes_rates() -> pd.DataFrame:
    t11 = read_istat_table("Tavola 11")
    t11 = t11[~t11.iloc[:, 0].astype(str).str.contains("Fonte", case=False, na=False)].copy()
    t11 = t11.rename(
        columns={
            t11.columns[0]: "region",
            "Scuola dell'infanzia": "bes_rate_per_100_infanzia",
            "Scuola primaria": "bes_rate_per_100_primaria",
            "Scuola secondaria di I grado": "bes_rate_per_100_secondaria_i",
            "Scuola secondaria di II grado": "bes_rate_per_100_secondaria_ii",
            "Totale ordini": "bes_rate_per_100_all_orders",
        }
    )

    t11["region"] = t11["region"].map(normalize_region)
    for c in t11.columns[1:]:
        t11[c] = pd.to_numeric(t11[c], errors="coerce")

    t11["source_school_year"] = "2022/2023"
    return t11


def build_students_by_region_order() -> pd.DataFrame:
    students = pd.concat(
        [
            pd.read_csv(ALUNNI_STA, dtype=str),
            pd.read_csv(ALUNNI_PAR, dtype=str),
        ],
        ignore_index=True,
    )

    schools = pd.concat(
        [
            pd.read_csv(SCUOLE_STA, dtype=str)[["CODICESCUOLA", "REGIONE"]],
            pd.read_csv(SCUOLE_PAR, dtype=str)[["CODICESCUOLA", "REGIONE"]],
        ],
        ignore_index=True,
    ).drop_duplicates(subset=["CODICESCUOLA"])

    students["ALUNNI"] = pd.to_numeric(students["ALUNNI"], errors="coerce").fillna(0)
    students["ORDINESCUOLA_NORM"] = students["ORDINESCUOLA"].map(normalize_order)

    merged = students.merge(schools, how="left", on="CODICESCUOLA")
    merged["REGIONE"] = merged["REGIONE"].map(normalize_region)

    grouped = (
        merged.groupby(["ANNOSCOLASTICO", "REGIONE", "ORDINESCUOLA_NORM"], as_index=False)["ALUNNI"]
        .sum()
        .rename(
            columns={
                "ANNOSCOLASTICO": "school_year_code",
                "REGIONE": "region",
                "ORDINESCUOLA_NORM": "order",
                "ALUNNI": "students_total",
            }
        )
    )

    grouped["school_year"] = grouped["school_year_code"].map(
        lambda x: f"{str(x)[:4]}/{str(x)[4:]}" if pd.notna(x) and len(str(x)) == 6 else str(x)
    )
    return grouped[["school_year_code", "school_year", "region", "order", "students_total"]]


def build_bes_estimates(students: pd.DataFrame, bes_rates: pd.DataFrame) -> pd.DataFrame:
    long_rates = bes_rates.melt(
        id_vars=["region", "source_school_year", "bes_rate_per_100_all_orders"],
        value_vars=[
            "bes_rate_per_100_infanzia",
            "bes_rate_per_100_primaria",
            "bes_rate_per_100_secondaria_i",
            "bes_rate_per_100_secondaria_ii",
        ],
        var_name="rate_key",
        value_name="bes_rate_per_100",
    )

    order_map = {
        "bes_rate_per_100_infanzia": "SCUOLA INFANZIA",
        "bes_rate_per_100_primaria": "SCUOLA PRIMARIA",
        "bes_rate_per_100_secondaria_i": "SCUOLA SECONDARIA I GRADO",
        "bes_rate_per_100_secondaria_ii": "SCUOLA SECONDARIA II GRADO",
    }
    long_rates["order"] = long_rates["rate_key"].map(order_map)

    out = students.merge(
        long_rates[["region", "order", "source_school_year", "bes_rate_per_100"]],
        how="left",
        on=["region", "order"],
    )

    out["estimated_bes_students"] = (out["students_total"] * out["bes_rate_per_100"] / 100.0).round(0)
    return out


def build_disabled_estimates(students: pd.DataFrame, dis_ts: pd.DataFrame) -> pd.DataFrame:
    # Use latest national order-specific disability rates as approximation.
    latest = dis_ts[dis_ts["school_year"].astype(str).str.contains("2022/2023")].copy()
    if latest.empty:
        latest = dis_ts.tail(1).copy()

    row = latest.iloc[0]
    rate_map = {
        "SCUOLA INFANZIA": row.get("disability_rate_per_100_infanzia"),
        "SCUOLA PRIMARIA": row.get("disability_rate_per_100_primaria"),
        "SCUOLA SECONDARIA I GRADO": row.get("disability_rate_per_100_secondaria_i"),
        "SCUOLA SECONDARIA II GRADO": row.get("disability_rate_per_100_secondaria_ii"),
    }

    out = students.copy()
    out["disability_rate_per_100_national"] = out["order"].map(rate_map)
    out["estimated_disabled_students"] = (
        out["students_total"] * out["disability_rate_per_100_national"] / 100.0
    ).round(0)
    out["source_school_year"] = str(row.get("school_year"))
    return out


def build_sources_manifest() -> dict:
    return {
        "generated_at": pd.Timestamp.now("UTC").isoformat(),
        "outputs": [
            "istat_disability_rate_timeseries_by_order.csv",
            "istat_bes_rate_by_region_order_2022_2023.csv",
            "ministry_students_by_region_order_2024_25.csv",
            "estimated_bes_students_by_region_order_2024_25_using_istat_rates.csv",
            "estimated_disabled_students_by_region_order_2024_25_using_national_rates.csv",
        ],
        "sources": [
            {
                "id": "istat_disability_bes_2022_2023",
                "type": "xlsx",
                "path": "local_data/ISTAT/istat_disability_schools_2022_2023.xlsx",
                "url": "https://www.istat.it/wp-content/uploads/2024/02/tavole-alunni-con-disabilit%C3%A0-as.2022-2023.xlsx",
                "notes": "Tavola 1 (disability rates by order/year) and Tavola 11 (BES rates by region/order).",
            },
            {
                "id": "mim_students_statali_2024_25",
                "type": "csv",
                "path": "local_data/MinIstruzione/Alunni/ALUCORSOETASTA20242520250831.csv",
                "notes": "School-level students by age/course; used for regional enrollment totals.",
            },
            {
                "id": "mim_students_paritarie_2024_25",
                "type": "csv",
                "path": "local_data/MinIstruzione/Alunni/ALUCORSOETAPAR20242520250831.csv",
                "notes": "School-level students by age/course; used for regional enrollment totals.",
            },
            {
                "id": "mim_school_registry_statali_2024_25",
                "type": "csv",
                "path": "local_data/MinIstruzione/Scuole/SCUANAGRAFESTAT20242520250831.csv",
                "notes": "Contains school-region mapping for state schools.",
            },
            {
                "id": "mim_school_registry_paritarie_2024_25",
                "type": "csv",
                "path": "local_data/MinIstruzione/Scuole/SCUANAGRAFEPAR20242520250831.csv",
                "notes": "Contains school-region mapping for non-state schools.",
            },
        ],
        "caveats": [
            "BES and disability student counts are estimated for 2024/25 by applying published ISTAT rates to Ministry enrollment totals.",
            "Estimated disability counts use national order-specific rates (from ISTAT Tavola 1), not region-specific disability rates.",
            "Estimated BES counts use region+order rates from ISTAT Tavola 11 (school year 2022/23).",
            "Current Ministry student extracts used in this pipeline do not include scuola infanzia rows, so estimates cover primary and secondary levels only.",
        ],
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    disability_ts = build_istat_disability_timeseries()
    bes_rates = build_istat_bes_rates()
    students = build_students_by_region_order()
    bes_est = build_bes_estimates(students, bes_rates)
    dis_est = build_disabled_estimates(students, disability_ts)

    disability_ts.to_csv(OUT_DIR / "istat_disability_rate_timeseries_by_order.csv", index=False)
    bes_rates.to_csv(OUT_DIR / "istat_bes_rate_by_region_order_2022_2023.csv", index=False)
    students.to_csv(OUT_DIR / "ministry_students_by_region_order_2024_25.csv", index=False)
    bes_est.to_csv(
        OUT_DIR / "estimated_bes_students_by_region_order_2024_25_using_istat_rates.csv",
        index=False,
    )
    dis_est.to_csv(
        OUT_DIR / "estimated_disabled_students_by_region_order_2024_25_using_national_rates.csv",
        index=False,
    )

    manifest = build_sources_manifest()
    (OUT_DIR / "bes_disability_sources_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    md_lines = [
        "# BES and Disability Sources Manifest",
        "",
        "This manifest documents files used to build BES/disability indicators and student-count estimates.",
        "",
        "## Outputs",
    ]
    md_lines.extend([f"- {x}" for x in manifest["outputs"]])
    md_lines.append("")
    md_lines.append("## Sources")
    for src in manifest["sources"]:
        md_lines.append(f"- {src['id']}: {src['path']}")
        if "url" in src:
            md_lines.append(f"  - url: {src['url']}")
        md_lines.append(f"  - notes: {src['notes']}")
    md_lines.append("")
    md_lines.append("## Caveats")
    md_lines.extend([f"- {x}" for x in manifest["caveats"]])

    (OUT_DIR / "bes_disability_sources.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print("Wrote BES/disability outputs to:", OUT_DIR)
    print("Rows - disability_ts:", len(disability_ts))
    print("Rows - bes_rates:", len(bes_rates))
    print("Rows - students:", len(students))
    print("Rows - bes_est:", len(bes_est))
    print("Rows - dis_est:", len(dis_est))


if __name__ == "__main__":
    main()
