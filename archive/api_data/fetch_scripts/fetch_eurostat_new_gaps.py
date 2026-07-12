"""
Fetch the second-wave gap-filling Eurostat series for Italy.

Covers:
  - Regional GDP at NUTS2 (nama_10r_3gdp)
  - Overqualification proxy: employment by education+occupation (lfsa_egised)
  - VET participation rates (trng_lfse_04)
  - VET enrolment by programme (educ_uoe_enrs04)
  - VET graduates by programme (educ_uoe_grad04)
  - Upper secondary graduation by programme type (educ_uoe_grad02)
  - Tertiary enrolment — parental-education-linked (educ_uoe_enra04)
  - NEETs by education level 15-29 (edat_lfse_03)
  - NEETs by citizenship/sex 15-24 (edat_lfse_01)
  - Crime by category/NUTS2 (crim_off_cat)
  - Youth mental health self-reported (hlth_ehis_pe1e)
"""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "local_data" / "eurostat"
OUT.mkdir(parents=True, exist_ok=True)

BASE = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (gap-filling expansion)",
    "Accept": "text/csv, */*",
}
TIMEOUT = 180

# All flows filtered to Italy and from 2009 onward.
# crim_off_cat and hlth_ehis_pe1e do not have a geo=IT parameter that narrows
# significantly — we pull all EU and filter post-download to keep related context.
SERIES = [
    {
        "name": "it_regional_gdp_nuts2",
        "flow": "nama_10r_3gdp",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_regional_gdp_nuts2.csv",
        "desc": "Regional GDP per capita at NUTS2 level (PPS and EUR) — Italy NUTS2 regions",
    },
    {
        "name": "it_overqualification_proxy",
        "flow": "lfsa_egised",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_overqualification_proxy.csv",
        "desc": "Employment by education attainment (ISCED) and occupation (ISCO-08) — overqualification proxy",
    },
    {
        "name": "it_vet_participation",
        "flow": "trng_lfse_04",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_vet_participation.csv",
        "desc": "Participation in VET by sex and age — Italy",
    },
    {
        "name": "eu_vet_enrolment_by_programme",
        "flow": "educ_uoe_enrs04",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_vet_enrolment_by_programme.csv",
        "desc": "VET enrolment by programme orientation, work-time, sector — Italy",
    },
    {
        "name": "eu_vet_graduates_by_programme",
        "flow": "educ_uoe_grad04",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_vet_graduates_by_programme.csv",
        "desc": "VET graduates by ISCED level and sex — Italy",
    },
    {
        "name": "it_upper_secondary_graduation_by_programme",
        "flow": "educ_uoe_grad02",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_upper_secondary_graduation_by_programme.csv",
        "desc": "Upper secondary graduates by ISCED orientation and field — Italy",
    },
    {
        "name": "eu_tertiary_enrolment_parental_context",
        "flow": "educ_uoe_enra04",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_tertiary_enrolment_parental_context.csv",
        "desc": "Tertiary enrolment rates (parental education intergenerational proxy) — Italy",
    },
    {
        "name": "it_neet_by_education_level",
        "flow": "edat_lfse_03",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_neet_by_education_level.csv",
        "desc": "NEETs aged 15-29 by highest educational attainment level — Italy",
    },
    {
        "name": "it_neet_by_citizenship_sex",
        "flow": "edat_lfse_01",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_neet_by_citizenship_sex.csv",
        "desc": "NEETs by sex, citizenship and work status — Italy",
    },
    {
        "name": "eu_crime_by_category_region",
        "flow": "crim_off_cat",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_crime_by_category.csv",
        "desc": "Recorded offences by category — Italy (territorial crime context for NEET north-south gap)",
    },
    {
        "name": "eu_youth_mental_health",
        "flow": "hlth_ehis_pe1e",
        "params": {"format": "SDMX-CSV", "geo": "IT", "startPeriod": "2009"},
        "out": "eurostat_it_youth_mental_health.csv",
        "desc": "Self-reported mental health by education, age, sex — Italy",
    },
]


def fetch(flow: str, params: dict) -> pd.DataFrame:
    resp = requests.get(f"{BASE}/{flow}", params=params, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return pd.read_csv(StringIO(resp.text), low_memory=False)


def main() -> None:
    print("Fetching Eurostat new-gaps expansion pack (Italy)\n")
    snapshot_rows: list[dict] = []

    for item in SERIES:
        print(f"[fetch] {item['name']}  flow={item['flow']}")
        try:
            df = fetch(item["flow"], item["params"])
            out_path = OUT / item["out"]
            df.to_csv(out_path, index=False)
            t_min = t_max = ""
            if "TIME_PERIOD" in df.columns and not df.empty:
                t = df["TIME_PERIOD"].astype(str)
                t_min, t_max = t.min(), t.max()
            print(f"  [ok] rows={len(df):,}  {t_min} → {t_max}  → {out_path.relative_to(ROOT)}")
            snapshot_rows.append({
                "series": item["name"], "flow": item["flow"], "status": "ok",
                "rows": len(df), "time_min": t_min, "time_max": t_max,
                "file": str(out_path.relative_to(ROOT)), "desc": item["desc"],
            })
        except requests.RequestException as exc:
            print(f"  [fail] {exc}")
            snapshot_rows.append({
                "series": item["name"], "flow": item["flow"], "status": "failed",
                "rows": 0, "time_min": "", "time_max": "", "file": "", "desc": item["desc"],
                "error": str(exc),
            })

    snap = pd.DataFrame(snapshot_rows)
    snap_path = OUT / "eurostat_it_new_gaps_snapshot.csv"
    snap.to_csv(snap_path, index=False)
    print(f"\nSnapshot → {snap_path.relative_to(ROOT)}")
    ok = (snap["status"] == "ok").sum()
    print(f"Done: {ok}/{len(SERIES)} flows fetched successfully.")


if __name__ == "__main__":
    main()
