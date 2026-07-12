"""
Document manual-required data sources that cannot be fetched automatically:
  - INPS apprenticeship contracts by region/sector/year
  - OECD TALIS Italy (teacher working conditions)
  - Parental education intergenerational series

Creates machine-readable manifests and human-readable guides for each,
so the gap is tracked and pipeline consumers know what is missing and why.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANUAL_DIR = ROOT / "local_data" / "manual_required"
MANUAL_DIR.mkdir(parents=True, exist_ok=True)

MANUAL_SOURCES = [
    {
        "name": "inps_apprenticeship_contracts",
        "title": "INPS Apprenticeship Contracts by Region/Sector/Year",
        "priority": "high",
        "why_needed": (
            "Apprenticeship (contratto di apprendistato) is the main institutionalised "
            "school-to-work bridge in Italy. Data on contracts activated/terminated by "
            "region, sector, and school type directly measures the VET pathway's "
            "employment-creation capacity."
        ),
        "api_status": "blocked — INPS open data portal (inps.it/opendata) returns 404; "
                       "odapi/wrapper.php endpoint not found; no SDMX feed identified.",
        "manual_steps": [
            "1. Go to https://www.inps.it/it/it/dati-e-bilanci/opendata.html",
            "2. Search for 'apprendistato' in the dataset catalogue.",
            "3. Download annual CSV files for apprenticeship activations by region.",
            "Alternative: https://www.cliclavoro.gov.it/Barometro-Del-Lavoro/ → "
            "Apprendistato section → export tables.",
            "Alternative 2: https://www.lavoro.gov.it/temi-e-priorita/lavoro/focus-on/"
            "contratti-di-lavoro/Pagine/apprendistato.aspx → Dati statistici PDF/Excel.",
        ],
        "target_file": "local_data/ISTAT/apprenticeship_contracts.csv",
        "expected_columns": ["year", "region", "sector_nace2", "contracts_activated", "contracts_terminated"],
    },
    {
        "name": "oecd_talis_italy",
        "title": "OECD TALIS Italy — Teacher Working Conditions and Professional Development",
        "priority": "medium",
        "why_needed": (
            "TALIS 2018 and 2024 provide teacher professional development participation, "
            "job satisfaction, classroom management practices, and share with permanent "
            "contracts. Relevant for hypothesis that teacher precariousness affects "
            "educational quality (bocciatura rates, INVALSI scores)."
        ),
        "api_status": "blocked — OECD SDMX (sdmx.oecd.org) has no TALIS dataflow in "
                       "OECD.EDU.IMEP catalogue; data-api.oecd.org DNS unresolvable from "
                       "this environment; TALIS microdata requires registration.",
        "manual_steps": [
            "1. Go to https://www.oecd.org/education/talis/talisproducts.htm",
            "2. Download 'TALIS 2018 Country Notes — Italy' PDF for key indicators.",
            "3. For structured data: https://stats.oecd.org/Index.aspx?DataSetCode=TALIS_2018 "
            "→ export Italy data as CSV.",
            "4. Alternatively use the TALIS 2018 Technical Report Annex tables.",
        ],
        "target_file": "local_data/oecd/oecd_it_talis_teacher_conditions.csv",
        "expected_columns": ["year", "indicator", "italy_value", "oecd_avg"],
    },
    {
        "name": "istat_parental_education_by_region",
        "title": "ISTAT Parental Education Attainment by Region (Intergenerational)",
        "priority": "medium",
        "why_needed": (
            "Direct parental education attainment distribution by region is needed for "
            "the OED/Goldthorpe mobility analysis (origin dimension). ISTAT's RCFL survey "
            "and census data track this. Enables direct computation of intergenerational "
            "educational transmission rates by territory."
        ),
        "api_status": "blocked — ISTAT SDMX catalogue search did not surface a "
                       "RCFL/parental-education-by-region flow with the keywords tested. "
                       "ISTAT esploradati timeout/500 errors persist for some flows.",
        "manual_steps": [
            "1. Go to https://esploradati.istat.it/ → search 'titolo di studio genitore'",
            "2. Or use https://www.istat.it/it/archivio/istruzione → "
            "'Indagine sulle forze di lavoro' → download by educational attainment + parent",
            "3. Alternative: ISTAT BES dataset 'Istruzione' includes parental background indicators "
            "at regional level.",
        ],
        "target_file": "local_data/ISTAT/istat_parental_education_by_region.csv",
        "expected_columns": ["year", "region", "parent_edu_level", "share_population"],
    },
    {
        "name": "inapp_internship_stage_data",
        "title": "INAPP/Isfol Internship (Tirocinio) Prevalence Data",
        "priority": "low",
        "why_needed": (
            "Italy has a well-documented problem of unpaid or low-paid internships "
            "('stage') as a barrier to youth labour market entry. Structured data on "
            "internship prevalence, duration, and compensation by sector and region would "
            "contextualise the post-secondary employment gap in AlmaLaurea and ANPAL data."
        ),
        "api_status": "no known machine-readable endpoint — INAPP (formerly Isfol) "
                       "publishes annual reports as PDF; no open data SDMX or CSV feed found.",
        "manual_steps": [
            "1. Go to https://www.inapp.gov.it/ → Publications → Tirocini",
            "2. Download annual tirocini monitoring report tables.",
            "3. Relevant report: 'Quarto rapporto di monitoraggio dei tirocini' (latest year).",
        ],
        "target_file": "local_data/manual_required/inapp_tirocini_summary.csv",
        "expected_columns": ["year", "region", "sector", "internship_count", "avg_duration_months", "avg_compensation_eur"],
    },
]


def main() -> None:
    print("Generating manual-required source manifests\n")

    for source in MANUAL_SOURCES:
        json_path = MANUAL_DIR / f"{source['name']}_manual_required.json"
        json_path.write_text(json.dumps(source, indent=2, ensure_ascii=False), encoding="utf-8")

        md_lines = [
            f"# {source['title']}",
            "",
            f"**Priority:** {source['priority']}",
            "",
            "## Why this is needed",
            source["why_needed"],
            "",
            "## API/automation status",
            source["api_status"],
            "",
            "## Manual steps to obtain data",
            *[f"- {step}" for step in source["manual_steps"]],
            "",
            "## Target output file",
            f"`{source['target_file']}`",
            "",
            "## Expected columns",
            ", ".join(f"`{c}`" for c in source["expected_columns"]),
        ]
        md_path = MANUAL_DIR / f"{source['name']}_manual_required.md"
        md_path.write_text("\n".join(md_lines), encoding="utf-8")
        print(f"  [ok] {source['name']}")

    # Consolidated manifest
    manifest = {
        "generated": "2026-05-21",
        "sources": MANUAL_SOURCES,
        "note": (
            "These sources could not be fetched automatically. "
            "Follow the manual steps to obtain and place data in target files."
        ),
    }
    master_path = MANUAL_DIR / "manual_required_master_manifest.json"
    master_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nMaster manifest → {master_path.relative_to(ROOT)}")
    print("Done.")


if __name__ == "__main__":
    main()
