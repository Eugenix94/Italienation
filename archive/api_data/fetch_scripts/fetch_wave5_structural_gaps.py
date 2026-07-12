"""
Wave 5 — Structural & social-determinant gap datasets for Italy assessment.

New files produced
──────────────────
local_data/eurostat/
  eurostat_life_satisfaction.csv          (ilc_pw01)
  eurostat_self_reported_health.csv       (hlth_silc_10)
  eurostat_neet_by_migration.csv          (edat_lfse_20)
  eurostat_esl_by_migration.csv           (edat_lfse_26)
  eurostat_adult_learning_part_rate.csv   (trng_aes_135)
  eurostat_unmet_healthcare_needs.csv     (hlth_ehis_un5)

local_data/worldbank/
  wb_learning_poverty.csv                 (HD.HCI.LPRV)
  wb_teachers_trained_primary.csv         (SE.PRM.TCAQ.ZS)
  wb_teachers_trained_secondary.csv       (SE.SEC.TCAQ.ZS)
  wb_suicide_mortality.csv                (SH.STA.SUIC.P5)

local_data/oecd/
  oecd_piaac_adult_skills.csv             (PIAAC 2023 cycle EAG view)
  oecd_piaac_adult_skills_2012.csv        (PIAAC 2012 cycle EAG view — fallback)
  oecd_teacher_experience.csv             (EAG UOE non-fin personnel experience)

local_data/ISTAT/
  istat_disability_schools.csv            (158_261 / 158_262 / 52_569)
  istat_mental_wellbeing.csv              (AVQ survey — 163_44 / 34_293)

Not covered here (no clean public API):
  INVALSI results          → invalsi-open.net (manual download, Excel/CSV)
  INPS Osservatorio        → inps.it/dati (portal download)
  ANPAL Youth Guarantee    → anpal.gov.it (portal download)
  AIRE emigrant register   → MAECI (aggregate reports only)
  CIG youth usage          → INPS (portal download)

Run from workspace root:
    .venv\\Scripts\\python.exe api_data/fetch_scripts/fetch_wave5_structural_gaps.py
"""

import time
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from io import StringIO
from pathlib import Path
from datetime import datetime

print(f"Wave 5 structural gaps  —  {datetime.now():%Y-%m-%d %H:%M}\n")

ROOT      = Path(__file__).resolve().parent.parent.parent
ESTAT_DIR = ROOT / "local_data" / "eurostat"
WB_DIR    = ROOT / "local_data" / "worldbank"
OECD_DIR  = ROOT / "local_data" / "oecd"
ISTAT_DIR = ROOT / "local_data" / "ISTAT"
for d in [ESTAT_DIR, WB_DIR, OECD_DIR, ISTAT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PAUSE      = 3   # seconds between requests
SKIP_BYTES = 500
TIMEOUT    = 90

# ─────────────────────────────────────────────────────────────────────────────
# Utility helpers
# ─────────────────────────────────────────────────────────────────────────────

def skip(path: Path, label: str) -> bool:
    if path.exists() and path.stat().st_size > SKIP_BYTES:
        print(f"  [SKIP] {path.name}  ({path.stat().st_size // 1024} KB)")
        return True
    return False


def save(df: pd.DataFrame, path: Path, label: str):
    df.to_csv(path, index=False)
    print(f"  SAVED {len(df):,} rows → {path.relative_to(ROOT)}  [{label}]")


# ─────────────────────────────────────────────────────────────────────────────
# Source A — Eurostat SDMX-CSV
# ─────────────────────────────────────────────────────────────────────────────

ESTAT_SDMX  = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
ESTAT_STATS = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"


def estat_sdmx(code: str, params: str, label: str, out: Path, min_rows: int = 5) -> bool:
    if skip(out, label):
        return True
    url = f"{ESTAT_SDMX}/{code}?format=SDMX-CSV&{params}"
    print(f"  GET {url[:115]}")
    try:
        r = requests.get(url, timeout=TIMEOUT)
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False
    print(f"  HTTP {r.status_code}  {len(r.content):,} b")
    if r.status_code != 200:
        print(f"  {r.text[:120]}")
        return False
    try:
        df = pd.read_csv(StringIO(r.text), low_memory=False)
    except Exception as e:
        print(f"  [PARSE ERROR] {e}")
        return False
    if len(df) < min_rows:
        print(f"  [EMPTY] only {len(df)} rows")
        return False
    save(df, out, label)
    return True


def estat_json(code: str, params: str, label: str, out: Path, min_rows: int = 5) -> bool:
    """Fallback: Eurostat Statistics JSON → flattened DataFrame."""
    if skip(out, label):
        return True
    url = f"{ESTAT_STATS}/{code}?{params}&format=JSON&lang=en"
    print(f"  [JSON] GET {url[:115]}")
    try:
        r = requests.get(url, timeout=TIMEOUT)
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False
    if r.status_code != 200:
        print(f"  HTTP {r.status_code}  {r.text[:120]}")
        return False
    try:
        j = r.json()
    except Exception as e:
        print(f"  [JSON PARSE ERROR] {e}")
        return False
    # Flatten dimension × value map
    dims   = j.get("dimension", {})
    values = j.get("value", {})
    sizes  = [d["category"]["index"] for d in dims.values()]
    labels = list(dims.keys())
    rows   = []
    for flat_idx, val in values.items():
        if val is None:
            continue
        idx  = int(flat_idx)
        cats = {}
        for name, cat_map in zip(reversed(labels), reversed(sizes)):
            cat_idx = idx % len(cat_map)
            idx    //= len(cat_map)
            rev_map = {v: k for k, v in cat_map.items()}
            cats[name] = rev_map.get(cat_idx, cat_idx)
        cats["OBS_VALUE"] = val
        rows.append(cats)
    if len(rows) < min_rows:
        print(f"  [EMPTY] only {len(rows)} rows")
        return False
    df = pd.DataFrame(rows)
    save(df, out, label)
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Source B — World Bank
# ─────────────────────────────────────────────────────────────────────────────

WB_BASE = "https://api.worldbank.org/v2/country/all/indicator"


def wb_fetch(indicator: str, label: str, out: Path,
             start: int = 2004, end: int = 2024) -> bool:
    if skip(out, label):
        return True
    url = f"{WB_BASE}/{indicator}?format=json&per_page=5000&date={start}:{end}"
    print(f"  GET {url[:110]}")
    try:
        r = requests.get(url, timeout=TIMEOUT)
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False
    if r.status_code != 200:
        print(f"  HTTP {r.status_code}")
        return False
    data = r.json()
    if len(data) < 2 or not data[1]:
        print("  [EMPTY] no records returned")
        return False
    rows = []
    for obs in data[1]:
        if obs.get("value") is None:
            continue
        rows.append({
            "country_id":   obs.get("countryiso3code") or (obs.get("country") or {}).get("id"),
            "country_name": (obs.get("country") or {}).get("value"),
            "year":         int(obs["date"]),
            "value":        float(obs["value"]),
            "indicator":    indicator,
        })
    if not rows:
        print("  [EMPTY] all values null")
        return False
    df = pd.DataFrame(rows)
    save(df, out, label)
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Source C — OECD SDMX (Accept: text/csv)
# ─────────────────────────────────────────────────────────────────────────────

OECD_SDMX = "https://sdmx.oecd.org/public/rest/data"


def oecd_fetch(flow: str, key: str, params: str, label: str, out: Path,
               min_rows: int = 5) -> bool:
    if skip(out, label):
        return True
    url = f"{OECD_SDMX}/{flow}/{key}?{params}&dimensionAtObservation=AllDimensions"
    print(f"  GET {url[:115]}")
    try:
        r = requests.get(url, headers={"Accept": "text/csv"}, timeout=TIMEOUT)
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False
    print(f"  HTTP {r.status_code}  {len(r.content):,} b")
    if r.status_code != 200:
        print(f"  {r.text[:120]}")
        return False
    try:
        df = pd.read_csv(StringIO(r.text), low_memory=False)
    except Exception as e:
        print(f"  [PARSE ERROR] {e}")
        return False
    if len(df) < min_rows:
        print(f"  [EMPTY] only {len(df)} rows")
        return False
    save(df, out, label)
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Source D — ISTAT SDMX (structured-specific XML)
# ─────────────────────────────────────────────────────────────────────────────

ISTAT_BASE = "https://sdmx.istat.it/SDMXWS/rest"


def istat_xml_to_df(xml_text: str) -> pd.DataFrame:
    root = ET.fromstring(xml_text)
    rows = []
    for series in root.iter():
        if not (series.tag.endswith("}Series") or series.tag == "Series"):
            continue
        dims = dict(series.attrib)
        for obs in series:
            rows.append({**dims, **obs.attrib})
    return pd.DataFrame(rows)


def istat_fetch(flow_id: str, version: str, label: str, out: Path,
                start: str = "2010", end: str = "2025") -> bool:
    if skip(out, label):
        return True
    url = (f"{ISTAT_BASE}/data/IT1,{flow_id},{version}/all"
           f"?startPeriod={start}&endPeriod={end}")
    headers = {"Accept": "application/vnd.sdmx.structurespecificdata+xml;version=2.1"}
    print(f"  GET {url[:110]}")
    try:
        r = requests.get(url, timeout=TIMEOUT, headers=headers)
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False
    print(f"  HTTP {r.status_code}  {len(r.content):,} b")
    if r.status_code != 200:
        print(f"  {r.text[:120]}")
        return False
    try:
        df = istat_xml_to_df(r.text)
    except Exception as e:
        print(f"  [XML PARSE ERROR] {e}")
        return False
    if len(df) < 5:
        print(f"  [EMPTY] only {len(df)} rows")
        return False
    save(df, out, label)
    return True


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1  —  EUROSTAT
# ═════════════════════════════════════════════════════════════════════════════

print("\n══════ EUROSTAT ══════")

# 1.1  Life satisfaction by age group  (ilc_pw01)
# Mean rating 0-10 for overall life satisfaction; breakdown by age shows
# whether young Italians are systematically less satisfied.
print("\n── 1.1  Life satisfaction  (ilc_pw01)")
estat_sdmx(
    "ilc_pw01",
    "startPeriod=2013&endPeriod=2024&indic_wb=SW_LIFS",
    "life satisfaction",
    ESTAT_DIR / "eurostat_life_satisfaction.csv",
)
time.sleep(PAUSE)

# 1.2  Self-reported health status by educational level  (hlth_silc_10)
# % reporting bad/very bad health by education attainment — key social
# determinant that links education gaps to health outcomes.
print("\n── 1.2  Self-reported health by education  (hlth_silc_10)")
print("  [SKIP] hlth_silc_10 temporarily skipped during bulk restore (endpoint often hangs)")
time.sleep(PAUSE)

# 1.3  NEET rate by citizenship / migration background  (edat_lfse_20)
# Splits NEET by EU/non-EU/national citizenship — critical for diagnosing
# whether immigrant youth drive or trail the national NEET average.
print("\n── 1.3  NEET by migration/citizenship  (edat_lfse_20)")
estat_sdmx(
    "edat_lfse_20",
    "startPeriod=2010&endPeriod=2024",
    "NEET by migration",
    ESTAT_DIR / "eurostat_neet_by_migration.csv",
)
time.sleep(PAUSE)

# 1.4  Early school leaving by country of birth  (edat_lfse_26)
# ESL rate split by native-born vs. foreign-born — reveals the migrant
# education integration gap distinct from overall ESL trend.
print("\n── 1.4  ESL by country of birth  (edat_lfse_26)")
estat_sdmx(
    "edat_lfse_26",
    "startPeriod=2010&endPeriod=2024",
    "ESL by migration",
    ESTAT_DIR / "eurostat_esl_by_migration.csv",
)
time.sleep(PAUSE)

# 1.5  Adult learning participation rate  (trng_aes_135)
# % of 25-64 population who participated in education/training in past 4 weeks
# from the Adult Education Survey. Distinct from enrollment counts — measures
# actual participation. Italy is chronically near bottom of EU rankings.
print("\n── 1.5  Adult learning participation rate  (trng_aes_135)")
ok = estat_sdmx(
    "trng_aes_135",
    "startPeriod=2007&endPeriod=2023",
    "adult learning participation rate",
    ESTAT_DIR / "eurostat_adult_learning_part_rate.csv",
)
if not ok:
    # alternative code for the same series
    estat_sdmx(
        "trng_lfs_03",
        "startPeriod=2010&endPeriod=2024",
        "adult learning participation rate (trng_lfs_03)",
        ESTAT_DIR / "eurostat_adult_learning_part_rate.csv",
    )
time.sleep(PAUSE)

# 1.6  Unmet need for medical examination  (hlth_ehis_un5)
# % reporting unmet healthcare needs by reason (cost, waiting time, too far).
# Italy has notable regional disparities; pairs with poverty data.
print("\n── 1.6  Unmet healthcare needs  (hlth_ehis_un5)")
ok = estat_sdmx(
    "hlth_ehis_un5",
    "startPeriod=2008&endPeriod=2023",
    "unmet healthcare needs",
    ESTAT_DIR / "eurostat_unmet_healthcare_needs.csv",
)
if not ok:
    estat_sdmx(
        "hlth_silc_08",
        "startPeriod=2010&endPeriod=2023",
        "unmet healthcare needs (hlth_silc_08)",
        ESTAT_DIR / "eurostat_unmet_healthcare_needs.csv",
    )
time.sleep(PAUSE)


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2  —  WORLD BANK
# ═════════════════════════════════════════════════════════════════════════════

print("\n══════ WORLD BANK ══════")

# 2.1  Learning poverty  (HD.HCI.LPRV)
# Share of children who cannot read a simple text by age 10 (combined
# enrollment + proficiency). A key WB benchmark for education quality;
# Italy performs poorly vs. Northern Europe.
print("\n── 2.1  Learning poverty  (HD.HCI.LPRV)")
wb_fetch(
    "HD.HCI.LPRV",
    "learning poverty",
    WB_DIR / "wb_learning_poverty.csv",
)
time.sleep(PAUSE)

# 2.2  Primary school teachers who are trained  (SE.PRM.TCAQ.ZS)
# % of primary teachers with minimum pedagogical qualifications.
# Relevant to school quality debate in Mezzogiorno.
print("\n── 2.2  Trained primary teachers  (SE.PRM.TCAQ.ZS)")
wb_fetch(
    "SE.PRM.TCAQ.ZS",
    "trained primary teachers",
    WB_DIR / "wb_teachers_trained_primary.csv",
)
time.sleep(PAUSE)

# 2.3  Secondary school teachers who are trained  (SE.SEC.TCAQ.ZS)
print("\n── 2.3  Trained secondary teachers  (SE.SEC.TCAQ.ZS)")
wb_fetch(
    "SE.SEC.TCAQ.ZS",
    "trained secondary teachers",
    WB_DIR / "wb_teachers_trained_secondary.csv",
)
time.sleep(PAUSE)

# 2.4  Suicide mortality rate  (SH.STA.SUIC.P5)
# Per 100,000 population. Proxy for population-level mental health crisis;
# youth suicide in Italy rose post-2020 alongside NEET spike.
print("\n── 2.4  Suicide mortality rate  (SH.STA.SUIC.P5)")
wb_fetch(
    "SH.STA.SUIC.P5",
    "suicide mortality rate",
    WB_DIR / "wb_suicide_mortality.csv",
)
time.sleep(PAUSE)


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3  —  OECD  (PIAAC adult skills + teacher experience)
# ═════════════════════════════════════════════════════════════════════════════

print("\n══════ OECD ══════")

# 3.1  PIAAC 2023 — adult literacy & numeracy proficiency
# The Programme for the International Assessment of Adult Competencies
# measures real-world skill use in 16-65 year-olds.  Italy scored near the
# bottom in both literacy and numeracy in the 2012 cycle; 2023 cycle data
# show ongoing structural deficit. Essential for linking educational
# attainment gaps to actual labour-market skill supply.
print("\n── 3.1  PIAAC adult skills (2023 cycle)")
piaac_out = OECD_DIR / "oecd_piaac_adult_skills.csv"
ok = oecd_fetch(
    "OECD.EDU.IMEP,DSD_PIAAC_2023@DF_PIAAC_EAG_2023",
    ".",                                  # all dimensions
    "startPeriod=2022&endPeriod=2024",
    "PIAAC adult skills 2023",
    piaac_out,
)
time.sleep(PAUSE)

if not ok:
    # Fallback: 2012 cycle (first round)
    print("  → fallback: PIAAC 2012 cycle")
    oecd_fetch(
        "OECD.EDU.IMEP,DSD_PIAAC_2012@DF_PIAAC_EAG_2012",
        ".",
        "startPeriod=2012&endPeriod=2013",
        "PIAAC adult skills 2012",
        OECD_DIR / "oecd_piaac_adult_skills_2012.csv",
    )
    time.sleep(PAUSE)

# 3.2  Teacher experience distribution  (EAG UOE non-financial personnel)
# Years of teaching experience by ISCED level. Italy has one of the oldest
# teacher workforces in the OECD — average age ~50 vs OECD average ~44.
# This captures the structural renewal challenge.
print("\n── 3.2  Teacher experience distribution")
ok = oecd_fetch(
    "OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_EXP,1.0",
    ".",
    "startPeriod=2015&endPeriod=2023",
    "teacher experience",
    OECD_DIR / "oecd_teacher_experience.csv",
)
time.sleep(PAUSE)

if not ok:
    # Fallback: teacher age class (AGE dimension of personnel dataset)
    print("  → fallback: teacher age classification")
    oecd_fetch(
        "OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_PERS@DF_UOE_NF_PERS_AGE,1.0",
        ".",
        "startPeriod=2015&endPeriod=2023",
        "teacher age",
        OECD_DIR / "oecd_teacher_experience.csv",
    )
    time.sleep(PAUSE)


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4  —  ISTAT (disability integration in schools; mental wellbeing)
# ═════════════════════════════════════════════════════════════════════════════

print("\n══════ ISTAT ══════")

# 4.1  Disability integration in schools
# ISTAT "Integrazione degli alunni con disabilità nelle scuole primarie e
# secondarie" — number of disabled pupils by school level, region, and type
# of support (hours of support teacher, etc.).  Disabled students carry
# disproportionately high NEET risk; this dataset quantifies coverage gaps.
# Flow IDs to try: 158_261 (sec2 disabled), 158_262, 52_569
print("\n── 4.1  Disability integration in schools")
disability_out = ISTAT_DIR / "istat_disability_schools.csv"
found = False
for flow_id, version in [("158_261", "1.0"), ("158_262", "1.0"), ("52_569", "1.0"),
                          ("52_590", "1.0"), ("52_623", "1.0")]:
    if found:
        break
    print(f"  Trying flow {flow_id} v{version} …")
    found = istat_fetch(flow_id, version, f"disability schools ({flow_id})", disability_out)
    if not found:
        time.sleep(PAUSE)
if not found:
    print("  [NOTE] Could not fetch disability-schools data via SDMX.\n"
          "         Manual download: https://www.istat.it/it/istruzione-e-formazione"
          "/integrazione-scolastica-degli-alunni-con-disabilita")

time.sleep(PAUSE)

# 4.2  Mental wellbeing / psychological distress — AVQ survey
# The "Aspetti della vita quotidiana" multipurpose survey collects
# self-reported psychological distress (MHI-5 scale), social isolation,
# and limitations due to health.  Youth (15-34) values are key for
# understanding post-COVID NEET surge beyond pure labour-market explanations.
# Flow IDs to try: 163_44 (multipurpose individual), 34_293, 34_261
print("\n── 4.2  Mental wellbeing  (AVQ survey)")
wellbeing_out = ISTAT_DIR / "istat_mental_wellbeing.csv"
found = False
for flow_id, version in [("163_44", "1.0"), ("34_293", "1.0"), ("34_261", "1.0"),
                          ("163_51", "1.0"), ("163_52", "1.0")]:
    if found:
        break
    print(f"  Trying flow {flow_id} v{version} …")
    found = istat_fetch(flow_id, version, f"mental wellbeing ({flow_id})", wellbeing_out)
    if not found:
        time.sleep(PAUSE)
if not found:
    print("  [NOTE] Could not fetch AVQ mental wellbeing via SDMX.\n"
          "         Manual download: https://www.istat.it/it/files/2024/07/tavole-AVQ-2023.xlsx")

# ═════════════════════════════════════════════════════════════════════════════
# Summary
# ═════════════════════════════════════════════════════════════════════════════

print("\n\n══════ SUMMARY ══════")
targets = [
    ESTAT_DIR / "eurostat_life_satisfaction.csv",
    ESTAT_DIR / "eurostat_self_reported_health.csv",
    ESTAT_DIR / "eurostat_neet_by_migration.csv",
    ESTAT_DIR / "eurostat_esl_by_migration.csv",
    ESTAT_DIR / "eurostat_adult_learning_part_rate.csv",
    ESTAT_DIR / "eurostat_unmet_healthcare_needs.csv",
    WB_DIR    / "wb_learning_poverty.csv",
    WB_DIR    / "wb_teachers_trained_primary.csv",
    WB_DIR    / "wb_teachers_trained_secondary.csv",
    WB_DIR    / "wb_suicide_mortality.csv",
    OECD_DIR  / "oecd_piaac_adult_skills.csv",
    OECD_DIR  / "oecd_piaac_adult_skills_2012.csv",
    OECD_DIR  / "oecd_teacher_experience.csv",
    ISTAT_DIR / "istat_disability_schools.csv",
    ISTAT_DIR / "istat_mental_wellbeing.csv",
]
ok_count = sum(1 for p in targets if p.exists() and p.stat().st_size > SKIP_BYTES)
print(f"\n  {ok_count}/{len(targets)} files present and non-empty.")
for p in targets:
    status = "OK " if (p.exists() and p.stat().st_size > SKIP_BYTES) else "MISS"
    size   = f"{p.stat().st_size // 1024} KB" if p.exists() else "—"
    print(f"  [{status}]  {p.relative_to(ROOT)}  {size}")

print("\nDone.\n")
print("─" * 60)
print("Manual-download reminders (no public API):")
print("  INVALSI results    → https://invalsi-open.net")
print("  INPS precariato    → https://www.inps.it/it/it/dati-e-bilanci/")
print("  ANPAL Garanzia G.  → https://www.anpal.gov.it/documents/")
print("  Youth CIG usage    → https://www.inps.it (Osservatorio CIG)")
print("  AIRE emigrant reg. → https://www.istat.it/migrazioni")
print("  INAPP VET surveys  → https://inapp.org/it/dati")
