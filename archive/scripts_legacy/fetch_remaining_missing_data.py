#!/usr/bin/env python3
"""
Fetch remaining missing datasets with robust fallbacks.

This script targets datasets that failed in previous waves and tries:
1) Eurostat dataflow discovery + candidate-code fetches
2) OECD dataflow discovery for PIAAC-like flows
3) World Bank country-specific fallback for learning poverty
4) Direct-download manual links when publicly reachable
"""

from __future__ import annotations

import csv
import json
import re
import time
from io import StringIO
from pathlib import Path
import xml.etree.ElementTree as ET

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
LOCAL = ROOT / "local_data"
ESTAT = LOCAL / "eurostat"
OECD = LOCAL / "oecd"
WB = LOCAL / "worldbank"
ISTAT = LOCAL / "ISTAT"
MANUAL = LOCAL / "manual_required"

for d in [ESTAT, OECD, WB, ISTAT, MANUAL]:
    d.mkdir(parents=True, exist_ok=True)

REPORT = MANUAL / "remaining_fetch_report.json"

ESTAT_SDMX = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
ESTAT_DF = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow"
OECD_SDMX = "https://sdmx.oecd.org/public/rest/data"
OECD_DF = "https://sdmx.oecd.org/public/rest/dataflow"
WB_IND = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&per_page=5000&date=2000:2025"

TIMEOUT = 90


def req(url: str, headers: dict | None = None) -> requests.Response | None:
    try:
        return requests.get(url, timeout=TIMEOUT, headers=headers)
    except Exception:
        return None


def estat_fetch(code: str, params: str, out_path: Path, min_rows: int = 5) -> tuple[bool, str]:
    url = f"{ESTAT_SDMX}/{code}?format=SDMX-CSV&{params}"
    r = req(url)
    if r is None:
        return False, "request-failed"
    if r.status_code != 200:
        return False, f"http-{r.status_code}"
    try:
        df = pd.read_csv(StringIO(r.text), low_memory=False)
    except Exception as e:
        return False, f"parse-error:{e}"
    if len(df) < min_rows:
        return False, f"too-few-rows:{len(df)}"
    df.to_csv(out_path, index=False)
    return True, f"rows:{len(df)}"


def find_eurostat_codes(tokens: list[str]) -> list[str]:
    r = req(ESTAT_DF)
    if r is None or r.status_code != 200:
        return []
    try:
        root = ET.fromstring(r.text)
    except Exception:
        return []

    # Dataflow IDs appear in structure namespace and are stable in id attribute.
    ids = []
    for elem in root.iter():
        eid = elem.attrib.get("id")
        if eid:
            ids.append(eid)

    uniq = sorted(set(ids))
    hits = []
    for c in uniq:
        lc = c.lower()
        if any(t.lower() in lc for t in tokens):
            hits.append(c)
    return hits


def oecd_try_piaac() -> tuple[bool, str]:
    out = OECD / "oecd_piaac_adult_skills.csv"
    # Try known public endpoints first.
    candidates = [
        ("OECD.EDU.IMEP,DSD_PIAAC_2023@DF_PIAAC_EAG_2023", ".", "startPeriod=2022&endPeriod=2025"),
        ("OECD.EDU.IMEP,DSD_PIAAC_2012@DF_PIAAC_EAG_2012", ".", "startPeriod=2012&endPeriod=2013"),
    ]
    for flow, key, params in candidates:
        url = f"{OECD_SDMX}/{flow}/{key}?{params}&dimensionAtObservation=AllDimensions"
        r = req(url, headers={"Accept": "text/csv"})
        if r is None or r.status_code != 200:
            continue
        try:
            df = pd.read_csv(StringIO(r.text), low_memory=False)
        except Exception:
            continue
        if len(df) < 5:
            continue
        df.to_csv(out, index=False)
        return True, f"rows:{len(df)}"

    # Discovery fallback: look for flows containing piaac.
    dfr = req(OECD_DF)
    if dfr is None or dfr.status_code != 200:
        return False, "dataflow-unavailable"
    text = dfr.text
    flow_candidates = sorted(set(re.findall(r'id="([^"]*piaac[^"]*)"', text, flags=re.I)))
    for flow in flow_candidates[:20]:
        url = f"{OECD_SDMX}/{flow}/.?startPeriod=2000&endPeriod=2025&dimensionAtObservation=AllDimensions"
        r = req(url, headers={"Accept": "text/csv"})
        if r is None or r.status_code != 200:
            continue
        try:
            df = pd.read_csv(StringIO(r.text), low_memory=False)
        except Exception:
            continue
        if len(df) < 5:
            continue
        df.to_csv(out, index=False)
        return True, f"rows:{len(df)} via {flow}"

    return False, "no-working-piaac-flow"


def worldbank_learning_poverty() -> tuple[bool, str]:
    out = WB / "wb_learning_poverty.csv"
    indicator = "HD.HCI.LPRV"
    countries = ["ITA", "all"]
    rows = []
    for c in countries:
        r = req(WB_IND.format(country=c, indicator=indicator))
        if r is None or r.status_code != 200:
            continue
        try:
            j = r.json()
        except Exception:
            continue
        if not isinstance(j, list) or len(j) < 2 or not j[1]:
            continue
        for obs in j[1]:
            if obs.get("value") is None:
                continue
            rows.append(
                {
                    "country_id": obs.get("countryiso3code") or (obs.get("country") or {}).get("id"),
                    "country_name": (obs.get("country") or {}).get("value"),
                    "year": obs.get("date"),
                    "value": obs.get("value"),
                    "indicator": indicator,
                }
            )
    if not rows:
        return False, "no-values"
    pd.DataFrame(rows).to_csv(out, index=False)
    return True, f"rows:{len(rows)}"


def download_manual_link(url: str, out: Path) -> tuple[bool, str]:
    r = req(url)
    if r is None:
        return False, "request-failed"
    if r.status_code != 200:
        return False, f"http-{r.status_code}"
    if len(r.content) < 128:
        return False, "tiny-file"
    out.write_bytes(r.content)
    return True, f"bytes:{len(r.content)}"


def main():
    report: dict[str, dict] = {}

    tasks = [
        {
            "name": "eurostat_self_reported_health",
            "out": ESTAT / "eurostat_self_reported_health.csv",
            "params": "startPeriod=2010&endPeriod=2025&geo=IT",
            "codes": ["hlth_silc_10", "hlth_silc_06", "hlth_silc_09"],
            "tokens": ["hlth", "silc"],
        },
        {
            "name": "eurostat_adult_learning_part_rate",
            "out": ESTAT / "eurostat_adult_learning_part_rate.csv",
            "params": "startPeriod=2010&endPeriod=2025&geo=IT",
            "codes": ["trng_aes_135", "trng_lfs_03", "trng_lfs_01"],
            "tokens": ["trng", "adult", "aes", "learning"],
        },
        {
            "name": "eurostat_unmet_healthcare_needs",
            "out": ESTAT / "eurostat_unmet_healthcare_needs.csv",
            "params": "startPeriod=2010&endPeriod=2025&geo=IT",
            "codes": ["hlth_ehis_un5", "hlth_silc_08", "hlth_ehis_un1"],
            "tokens": ["hlth", "unmet"],
        },
        {
            "name": "eurostat_almp_spending_by_type",
            "out": ESTAT / "eurostat_almp_spending_by_type.csv",
            "params": "startPeriod=2010&endPeriod=2025&geo=IT",
            "codes": ["lmp_ind_exp", "lmp_ind_actp", "lmp_exp", "lmp_expend"],
            "tokens": ["lmp", "almp", "exp"],
        },
        {
            "name": "eurostat_almp_participants_stock",
            "out": ESTAT / "eurostat_almp_participants_stock.csv",
            "params": "startPeriod=2010&endPeriod=2025&geo=IT",
            "codes": ["lmp_par_summ", "lmp_part", "lmp_ind_actp"],
            "tokens": ["lmp", "par"],
        },
        {
            "name": "eurostat_fertility_by_education",
            "out": ESTAT / "eurostat_fertility_by_education.csv",
            "params": "startPeriod=2010&endPeriod=2025&geo=IT",
            "codes": ["demo_fordeduc", "demo_feredu", "demo_frateceduc"],
            "tokens": ["demo", "educ", "fert"],
        },
    ]

    # Eurostat fill for each missing target.
    for t in tasks:
        out = t["out"]
        if out.exists() and out.stat().st_size > 500:
            report[t["name"]] = {"status": "ok-existing", "detail": f"bytes:{out.stat().st_size}"}
            continue

        done = False
        attempted = []
        for code in t["codes"]:
            ok, detail = estat_fetch(code, t["params"], out)
            attempted.append({"code": code, "ok": ok, "detail": detail})
            if ok:
                done = True
                break

        if not done:
            discovered = find_eurostat_codes(t["tokens"])
            for code in discovered[:30]:
                if code in [a["code"] for a in attempted]:
                    continue
                ok, detail = estat_fetch(code, t["params"], out)
                attempted.append({"code": code, "ok": ok, "detail": detail})
                if ok:
                    done = True
                    break

        report[t["name"]] = {
            "status": "ok" if done else "missing",
            "attempts": attempted[:80],
        }

        time.sleep(1)

    # OECD PIAAC.
    ok, detail = oecd_try_piaac()
    report["oecd_piaac_adult_skills"] = {"status": "ok" if ok else "missing", "detail": detail}

    # World Bank learning poverty.
    ok, detail = worldbank_learning_poverty()
    report["wb_learning_poverty"] = {"status": "ok" if ok else "missing", "detail": detail}

    # Manual-source direct links that can still be downloaded automatically.
    manual_download_targets = [
        (
            "istat_mental_wellbeing_source_xlsx",
            "https://www.istat.it/it/files/2024/07/tavole-AVQ-2023.xlsx",
            ISTAT / "istat_mental_wellbeing_source_avq_2023.xlsx",
        ),
    ]

    for key, url, out in manual_download_targets:
        if out.exists() and out.stat().st_size > 500:
            report[key] = {"status": "ok-existing", "detail": f"bytes:{out.stat().st_size}"}
            continue
        ok, detail = download_manual_link(url, out)
        report[key] = {"status": "ok" if ok else "missing", "detail": detail, "url": url}

    # Write report and flat CSV summary for quick triage.
    with open(REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    csv_out = MANUAL / "remaining_fetch_report.csv"
    with open(csv_out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["dataset", "status", "detail"])
        for k, v in report.items():
            w.writerow([k, v.get("status", ""), v.get("detail", "")])

    # Produce manual checklist for items still not fetched.
    checklist = MANUAL / "manual_download_checklist.md"
    missing = [k for k, v in report.items() if v.get("status") == "missing"]
    lines = [
        "# Manual Download Checklist",
        "",
        "These items could not be fetched automatically in this run:",
        "",
    ]
    if missing:
        for m in missing:
            lines.append(f"- {m}")
    else:
        lines.append("- None")

    lines.extend(
        [
            "",
            "Suggested manual sources:",
            "- ISTAT disability integration tables: https://www.istat.it/it/istruzione-e-formazione/integrazione-scolastica-degli-alunni-con-disabilita",
            "- INVALSI open data: https://invalsi-open.net/",
            "- ANPAL youth guarantee docs: https://www.anpal.gov.it/documents/",
            "- INAPP VET/IFTS surveys: https://inapp.org/it/dati",
        ]
    )
    checklist.write_text("\n".join(lines), encoding="utf-8")

    print("Done. Reports:")
    print(f"- {REPORT}")
    print(f"- {csv_out}")
    print(f"- {checklist}")


if __name__ == "__main__":
    main()
