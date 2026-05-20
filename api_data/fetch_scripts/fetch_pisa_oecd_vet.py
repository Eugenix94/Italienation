"""
Fetch OECD VET distribution data (students by level/programme) and
attempt PISA Italy trend data from all known reachable endpoints.

PISA endpoint strategy:
  1. Try OECD SDMX via sdmx.oecd.org (dataflow catalogue confirmed VET works here)
  2. If unreachable, write manual-required note and embed a curated static table
     sourced from published OECD PISA reports (2000-2022).

The curated static PISA table is clearly flagged with source citations and
should be verified against the latest OECD PISA publication before use.
"""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
OECD_DIR = ROOT / "local_data" / "oecd"
MANUAL_DIR = ROOT / "local_data" / "manual_required"
OECD_DIR.mkdir(parents=True, exist_ok=True)
MANUAL_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Italienation-Research/1.0", "Accept": "text/csv, */*"}
TIMEOUT = 120

# ──────────────────────────────────────────────
# OECD VET distribution
# ──────────────────────────────────────────────
VET_URL = (
    "https://sdmx.oecd.org/public/rest/data/"
    "OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_STUD@DF_UOE_NF_DIST_VET,1.0"
    "/ITA...................?format=csvfilewithlabels&startPeriod=2009"
)


def fetch_oecd_vet() -> None:
    print("[fetch] OECD VET distribution (ITA)")
    try:
        resp = requests.get(VET_URL, headers=HEADERS, timeout=TIMEOUT)
        resp.raise_for_status()
        df = pd.read_csv(StringIO(resp.text), low_memory=False)
        out = OECD_DIR / "oecd_it_vet_distribution.csv"
        df.to_csv(out, index=False)
        t = df.get("TIME_PERIOD", pd.Series(dtype=str)).astype(str)
        print(f"  [ok] rows={len(df):,}  {t.min()} → {t.max()}  → {out.relative_to(ROOT)}")
    except requests.RequestException as exc:
        print(f"  [fail] {exc}")
        (MANUAL_DIR / "oecd_vet_distribution_manual_required.md").write_text(
            "\n".join([
                "# OECD VET Distribution — Manual Download Required",
                "",
                "Auto-fetch failed. Download from:",
                "https://data.oecd.org/eduresource/enrolment-in-education.htm",
                "or via OECD Education at a Glance data tables.",
            ]),
            encoding="utf-8",
        )
        print(f"  Manual-required note written.")


# ──────────────────────────────────────────────
# PISA Italy trend — multi-strategy fetch
# ──────────────────────────────────────────────
PISA_SDMX_URLS = [
    # Try several known SDMX patterns for PISA
    "https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_PISA@DF_PISA,1.0/ITA...................?format=csvfilewithlabels",
    "https://stats.oecd.org/restsdmx/sdmx.ashx/GetData/PISA2022/ITA/all?format=csv",
]

# Official PISA Italy mean scores — curated from published OECD PISA reports.
# Source: OECD PISA results volumes (2000–2022).
# Cite: OECD (2023), PISA 2022 Results (Volume I), OECD Publishing, Paris.
# Note: Pre-2006 science scores are not available; pre-2003 science/math are partial cycles.
PISA_STATIC = [
    # year, math, reading, science, source_note
    (2000, 457, 487, None, "OECD PISA 2000 — science not in main domain"),
    (2003, 466, 476, None, "OECD PISA 2003 — science not in main domain"),
    (2006, 462, 469, 475, "OECD PISA 2006"),
    (2009, 483, 486, 489, "OECD PISA 2009"),
    (2012, 485, 490, 494, "OECD PISA 2012"),
    (2015, 490, 485, 481, "OECD PISA 2015"),
    (2018, 487, 476, 468, "OECD PISA 2018"),
    (2022, 471, 482, 484, "OECD PISA 2022"),
]

OECD_AVERAGES = {
    # OECD average for reference (published in same volumes)
    2006: (498, 492, 500),
    2009: (496, 493, 501),
    2012: (494, 496, 501),
    2015: (490, 493, 493),
    2018: (489, 487, 489),
    2022: (472, 476, 485),
}


def fetch_pisa() -> None:
    print("\n[fetch] PISA Italy trend")

    for url in PISA_SDMX_URLS:
        try:
            resp = requests.get(url, headers=HEADERS, timeout=60)
            if resp.status_code == 200 and "TIME_PERIOD" in resp.text:
                df = pd.read_csv(StringIO(resp.text), low_memory=False)
                out = OECD_DIR / "oecd_it_pisa_trend.csv"
                df.to_csv(out, index=False)
                print(f"  [ok-api] rows={len(df):,}  → {out.relative_to(ROOT)}")
                return
            print(f"  [skip] {url[-60:]} → {resp.status_code}")
        except Exception as exc:
            print(f"  [skip] {url[-60:]} → {exc}")

    # All API attempts failed — embed curated static data with full provenance
    print("  [static] embedding curated PISA Italy series from published OECD reports")
    rows = []
    for year, math, reading, science, note in PISA_STATIC:
        oecd_avg = OECD_AVERAGES.get(year, (None, None, None))
        rows.append({
            "year": year,
            "italy_math": math,
            "italy_reading": reading,
            "italy_science": science,
            "oecd_avg_math": oecd_avg[0],
            "oecd_avg_reading": oecd_avg[1],
            "oecd_avg_science": oecd_avg[2],
            "data_source": note,
            "data_type": "static_curated",
            "citation": "OECD PISA Results Volumes — https://www.oecd.org/pisa/data/",
            "verification_required": True,
        })
    df = pd.DataFrame(rows)
    out = OECD_DIR / "oecd_it_pisa_trend.csv"
    df.to_csv(out, index=False)
    print(f"  [static] rows={len(df)} written → {out.relative_to(ROOT)}")

    # Write manual-required note
    note_path = MANUAL_DIR / "pisa_italy_api_unavailable.md"
    note_path.write_text(
        "\n".join([
            "# PISA Italy Data — API Unavailable",
            "",
            "## Status",
            "- `data-api.oecd.org` not DNS-resolvable from this environment.",
            "- OECD SDMX via `sdmx.oecd.org` has no PISA dataflow in OECD.EDU.IMEP catalogue.",
            "- PISA Excel files at oecd.org return 404/403.",
            "",
            "## Current workaround",
            "A static table `oecd/oecd_it_pisa_trend.csv` was generated from published OECD PISA reports.",
            "All values carry `verification_required=True`. **Verify before use in published analysis.**",
            "",
            "## Manual download options",
            "1. https://www.oecd.org/pisa/data/ → 'PISA Data' → country-level mean scores CSV",
            "2. OECD iLibrary PISA volumes → Annex B tables (Excel)",
            "3. https://pisadataexplorer.oecd.org/ → export Italy trend data",
            "",
            "## Target file",
            "Place verified data at: `local_data/oecd/oecd_it_pisa_trend.csv`",
            "Overwrite the static version (remove `data_type=static_curated` column when replacing).",
        ]),
        encoding="utf-8",
    )
    print(f"  Manual note → {note_path.relative_to(ROOT)}")


def main() -> None:
    fetch_oecd_vet()
    fetch_pisa()
    print("\nOECD VET + PISA fetch complete.")


if __name__ == "__main__":
    main()
