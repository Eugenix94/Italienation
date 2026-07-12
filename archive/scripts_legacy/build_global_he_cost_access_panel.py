#!/usr/bin/env python3
"""Build a global higher-education cost/access comparison panel.

Outputs:
- local_data/processed/global_he_cost_access_panel.csv
- local_data/processed/global_he_cost_access_latest_year.csv
- local_data/processed/italy_mur_tuition_benchmark_2024.csv
"""

from pathlib import Path
import pandas as pd
import ast
import json
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
WB_DIR = ROOT / "local_data" / "worldbank"
MUR_FILE = ROOT / "local_data" / "MUR" / "2024-contribuzione-e-interventi-atenei" / "2024_atenei_contribuzione_media.csv"
OUT_DIR = ROOT / "local_data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INDICATOR_FILES = {
    "learning_poverty_pct": "wb_learning_poverty.csv",
    "education_spending_pct_gdp": "wb_education_spending_pct_gdp.csv",
    "tertiary_spending_pct_gdp_percap": "wb_tertiary_spending_pct_gdp_percapita.csv",
    "tertiary_enrollment_gross_pct": "wb_tertiary_enrollment_gross.csv",
}

WB_INDICATOR_META = {
    "learning_poverty_pct": {
        "file": "wb_learning_poverty.csv",
        "indicator_code": "SE.LPV.PRIM",
        "indicator_name": "Learning poverty: share below minimum reading proficiency",
        "api_template": "https://api.worldbank.org/v2/country/all/indicator/SE.LPV.PRIM?format=json&per_page=20000",
    },
    "education_spending_pct_gdp": {
        "file": "wb_education_spending_pct_gdp.csv",
        "indicator_code": "SE.XPD.TOTL.GD.ZS",
        "indicator_name": "Government expenditure on education, total (% of GDP)",
        "api_template": "https://api.worldbank.org/v2/country/all/indicator/SE.XPD.TOTL.GD.ZS?format=json&per_page=20000",
    },
    "tertiary_spending_pct_gdp_percap": {
        "file": "wb_tertiary_spending_pct_gdp_percapita.csv",
        "indicator_code": "SE.XPD.TERT.PC.ZS",
        "indicator_name": "Expenditure per tertiary student (% of GDP per capita)",
        "api_template": "https://api.worldbank.org/v2/country/all/indicator/SE.XPD.TERT.PC.ZS?format=json&per_page=20000",
    },
    "tertiary_enrollment_gross_pct": {
        "file": "wb_tertiary_enrollment_gross.csv",
        "indicator_code": "SE.TER.ENRR",
        "indicator_name": "School enrollment, tertiary (% gross)",
        "api_template": "https://api.worldbank.org/v2/country/all/indicator/SE.TER.ENRR?format=json&per_page=20000",
    },
}


def load_wb_indicator(path: Path, value_name: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    cols = ["countryiso3code", "country", "date", "value"]
    df = df[cols].copy()
    df = df.rename(columns={"countryiso3code": "iso3", "date": "year", "value": value_name})
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df[value_name] = pd.to_numeric(df[value_name], errors="coerce")
    return df


def normalize_country_name(series: pd.Series) -> pd.Series:
    def _parse(v):
        if pd.isna(v):
            return v
        if isinstance(v, str) and v.startswith("{") and "'value'" in v:
            try:
                obj = ast.literal_eval(v)
                if isinstance(obj, dict) and "value" in obj:
                    return obj["value"]
            except Exception:
                return v
        return v

    return series.apply(_parse)


def write_sources_manifest(panel_rows: int, latest_rows: int) -> tuple[Path, Path]:
    manifest_path = OUT_DIR / "global_he_cost_access_sources_manifest.json"
    sources_md_path = OUT_DIR / "global_he_cost_access_sources.md"

    manifest = {
        "title": "Global HE Cost/Access Panel Sources Manifest",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "outputs": [
            "local_data/processed/global_he_cost_access_panel.csv",
            "local_data/processed/global_he_cost_access_latest_year.csv",
            "local_data/processed/italy_mur_tuition_benchmark_2024.csv",
        ],
        "row_counts": {
            "global_he_cost_access_panel": panel_rows,
            "global_he_cost_access_latest_year": latest_rows,
        },
        "input_sources": {
            "world_bank_indicators": WB_INDICATOR_META,
            "mur_italy_tuition": {
                "file": "local_data/MUR/2024-contribuzione-e-interventi-atenei/2024_atenei_contribuzione_media.csv",
                "dataset_name": "2024 Contribuzione e interventi atenei",
                "catalog_url": "https://dati-ustat.mur.gov.it/dataset/2024-contribuzione-e-interventi-atenei",
                "fields_used": [
                    "ANNO_ACCADEMICO",
                    "COD_Ateneo",
                    "NOME_ATENEO",
                    "TASSA_MEDIA_PAGANTI_LAUREA",
                    "TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA",
                ],
            },
        },
        "notes": [
            "OECD tuition-fee web pages were blocked by Cloudflare/HTTP 403 in this environment; not included in automated panel.",
            "Eurostat legacy ALMP codes lmp_ind_exp and lmp_ind_actp are not present in the current SDMX 2.1 dataflow catalog.",
        ],
    }

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    md_lines = [
        "# Global HE Cost/Access Sources",
        "",
        f"Generated (UTC): {manifest['generated_at_utc']}",
        "",
        "## Output files",
        "- local_data/processed/global_he_cost_access_panel.csv",
        "- local_data/processed/global_he_cost_access_latest_year.csv",
        "- local_data/processed/italy_mur_tuition_benchmark_2024.csv",
        "",
        "## World Bank indicators",
    ]
    for key, meta in WB_INDICATOR_META.items():
        md_lines.extend(
            [
                f"- {key}",
                f"  - code: {meta['indicator_code']}",
                f"  - name: {meta['indicator_name']}",
                f"  - source file: local_data/worldbank/{meta['file']}",
                f"  - API: {meta['api_template']}",
            ]
        )

    md_lines.extend(
        [
            "",
            "## Italy tuition benchmark source (MUR)",
            "- Dataset: 2024 Contribuzione e interventi atenei",
            "- Catalog: https://dati-ustat.mur.gov.it/dataset/2024-contribuzione-e-interventi-atenei",
            "- Source file: local_data/MUR/2024-contribuzione-e-interventi-atenei/2024_atenei_contribuzione_media.csv",
            "",
            "## Caveats",
            "- OECD tuition-fee pages were blocked in this execution environment and are not part of the automated pull.",
            "- Eurostat legacy ALMP dataset codes lmp_ind_exp and lmp_ind_actp are invalid in current SDMX 2.1 catalog.",
        ]
    )
    sources_md_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    return manifest_path, sources_md_path


def main() -> None:
    merged = None
    for value_name, filename in INDICATOR_FILES.items():
        df = load_wb_indicator(WB_DIR / filename, value_name)
        if merged is None:
            merged = df
        else:
            merged = merged.merge(df[["iso3", "year", value_name]], on=["iso3", "year"], how="outer")

    if merged is None:
        raise RuntimeError("No World Bank indicators loaded")

    # Keep canonical country name per ISO code.
    merged["country"] = normalize_country_name(merged["country"])
    name_map = merged[["iso3", "country"]].dropna().drop_duplicates(subset=["iso3"])  # first seen
    merged = merged.drop(columns=["country"]).merge(name_map, on="iso3", how="left")

    # Useful composite metrics for quick ranking.
    merged["access_minus_learning_gap"] = merged["tertiary_enrollment_gross_pct"] - merged["learning_poverty_pct"]
    merged["cost_intensity_x_access"] = merged["tertiary_spending_pct_gdp_percap"] * merged["tertiary_enrollment_gross_pct"]

    panel_path = OUT_DIR / "global_he_cost_access_panel.csv"
    merged.to_csv(panel_path, index=False)

    # Latest year snapshot per country where at least one core indicator exists.
    core_cols = [
        "learning_poverty_pct",
        "education_spending_pct_gdp",
        "tertiary_spending_pct_gdp_percap",
        "tertiary_enrollment_gross_pct",
    ]
    work = merged.copy()
    work["available_core_metrics"] = work[core_cols].notna().sum(axis=1)
    work = work[work["available_core_metrics"] > 0].copy()
    latest = (
        work.sort_values(["iso3", "year"])
        .groupby("iso3", as_index=False)
        .tail(1)
        .sort_values(["available_core_metrics", "tertiary_enrollment_gross_pct"], ascending=[False, False])
    )
    latest_path = OUT_DIR / "global_he_cost_access_latest_year.csv"
    latest.to_csv(latest_path, index=False)

    # Italy tuition benchmark from MUR.
    mur = pd.read_csv(MUR_FILE, encoding="latin1", sep=";")
    for col in ["TASSA_MEDIA_PAGANTI_LAUREA", "TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA"]:
        mur[col] = (
            mur[col]
            .astype(str)
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
        )
        mur[col] = pd.to_numeric(mur[col], errors="coerce")

    italy = mur[mur["COD_Ateneo"].isin(["TTTTT", "SSSSS"])].copy()
    italy = italy.rename(
        columns={
            "ANNO_ACCADEMICO": "academic_year",
            "COD_Ateneo": "aggregation_code",
            "NOME_ATENEO": "aggregation_name",
            "TASSA_MEDIA_PAGANTI_LAUREA": "avg_tuition_payers_eur",
            "TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA": "avg_tuition_all_students_eur",
        }
    )
    italy["source"] = "MUR 2024 contribuzione e interventi atenei"
    italy_path = OUT_DIR / "italy_mur_tuition_benchmark_2024.csv"
    italy.to_csv(italy_path, index=False)

    manifest_path, sources_md_path = write_sources_manifest(len(merged), len(latest))

    print(f"Saved: {panel_path}")
    print(f"Saved: {latest_path}")
    print(f"Saved: {italy_path}")
    print(f"Saved: {manifest_path}")
    print(f"Saved: {sources_md_path}")
    print(f"Panel rows: {len(merged):,}; latest snapshot rows: {len(latest):,}")


if __name__ == "__main__":
    main()
