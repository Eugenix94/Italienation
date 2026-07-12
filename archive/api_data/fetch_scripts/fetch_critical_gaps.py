"""
Critical remaining gaps for Italy NEET analysis.

Targets datasets that failed in wave 5/6 scripts by trying:
  • Eurostat Statistics JSON API instead of SDMX  (different endpoint, broader coverage)
  • OECD.Stat legacy JSON API for PIAAC           (old endpoint, still served)
  • Alternative OECD SDMX dataflow IDs for PIAAC

Outputs
───────
local_data/eurostat/
  eurostat_almp_spending_by_type.csv          (lmp_ind_exp  → JSON API)
  eurostat_almp_participants_stock.csv        (lmp_ind_actp → JSON API)
  eurostat_homeownership_by_age.csv           (ilc_lvho02   → JSON API)
  eurostat_fertility_by_education.csv         (demo_fordeduc → JSON API)
  eurostat_wellbeing_by_age.csv               (ilc_pw05     → JSON API)

local_data/oecd/
  oecd_piaac_adult_skills.csv                 (OECD.Stat PIAAC_LIT + PIAAC_NUM)

Not fetchable via public API (must download manually):
  INVALSI regional scores  → https://invalsi-open.net/data/
  ANPAL Youth Guarantee    → https://www.anpal.gov.it/statistiche
  INPS CIG youth usage     → https://www.inps.it/dati

Run from workspace root:
    .venv\\Scripts\\python.exe api_data/fetch_scripts/fetch_critical_gaps.py
"""

import itertools
import time
from datetime import datetime
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

print(f"Critical gaps fetch  —  {datetime.now():%Y-%m-%d %H:%M}\n")

ROOT      = Path(__file__).resolve().parent.parent.parent
ESTAT_DIR = ROOT / "local_data" / "eurostat"
OECD_DIR  = ROOT / "local_data" / "oecd"
for d in [ESTAT_DIR, OECD_DIR]:
    d.mkdir(parents=True, exist_ok=True)

PAUSE      = 3
SKIP_BYTES = 500
TIMEOUT    = 180
MAX_TRIES  = 4

ESTAT_SDMX  = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"
ESTAT_STATS = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
OECD_SDMX   = "https://sdmx.oecd.org/public/rest/data"
OECD_STAT   = "https://stats.oecd.org/SDMX-JSON/data"   # legacy OECD.Stat endpoint


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def skip(path: Path) -> bool:
    return path.exists() and path.stat().st_size > SKIP_BYTES


def save(df: pd.DataFrame, path: Path, label: str):
    df.to_csv(path, index=False)
    print(f"  SAVED {len(df):,} rows → {path.relative_to(ROOT)}  [{label}]")


def get_retry(url: str, headers: dict | None = None) -> requests.Response | None:
    for attempt in range(1, MAX_TRIES + 1):
        try:
            return requests.get(url, headers=headers or {}, timeout=TIMEOUT)
        except Exception as exc:
            wait = 2 ** (attempt - 1)
            print(f"    [retry {attempt}/{MAX_TRIES}] {exc}; waiting {wait}s")
            time.sleep(wait)
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Eurostat SDMX-CSV  (fast path — already known for some datasets)
# ─────────────────────────────────────────────────────────────────────────────

def estat_sdmx(code: str, params: str, label: str, out: Path, min_rows: int = 5) -> bool:
    url = f"{ESTAT_SDMX}/{code}?format=SDMX-CSV&{params}"
    print(f"  [SDMX] GET {url[:120]}")
    r = get_retry(url)
    if r is None:
        return False
    print(f"  HTTP {r.status_code}  {len(r.content):,} b")
    if r.status_code != 200:
        print(f"  {r.text[:120]}")
        return False
    try:
        df = pd.read_csv(StringIO(r.text), low_memory=False)
    except Exception as e:
        print(f"  [PARSE] {e}")
        return False
    if len(df) < min_rows:
        print(f"  [EMPTY] {len(df)} rows")
        return False
    save(df, out, label)
    return True


# ─────────────────────────────────────────────────────────────────────────────
# Eurostat Statistics JSON API  (broader dataset coverage than SDMX endpoint)
# ─────────────────────────────────────────────────────────────────────────────

def _jsonstat_to_df(j: dict) -> pd.DataFrame:
    """Parse a Eurostat JSON-stat 2.0 payload into a flat DataFrame."""
    dims   = j.get("dimension", {})
    values = j.get("value", {})

    dim_names  = list(dims.keys())
    dim_maps   = []                    # list of {position: code} per dimension
    dim_labels = []                    # list of {code: label} per dimension

    for name in dim_names:
        cat = dims[name]["category"]
        pos_to_code = {v: k for k, v in cat["index"].items()}
        code_to_lbl = cat.get("label", {})
        dim_maps.append(pos_to_code)
        dim_labels.append(code_to_lbl)

    dim_sizes = [len(m) for m in dim_maps]

    rows = []
    for flat_idx_str, val in values.items():
        if val is None:
            continue
        flat_idx = int(flat_idx_str)
        codes = []
        for size in reversed(dim_sizes):
            codes.append(flat_idx % size)
            flat_idx //= size
        codes.reverse()

        row = {}
        for i, (name, code_pos) in enumerate(zip(dim_names, codes)):
            code = dim_maps[i].get(code_pos, code_pos)
            row[name]              = code
            row[name + "_label"]   = dim_labels[i].get(code, "")
        row["OBS_VALUE"] = val
        rows.append(row)

    return pd.DataFrame(rows)


def estat_json(code: str, params: str, label: str, out: Path, min_rows: int = 5) -> bool:
    url = f"{ESTAT_STATS}/{code}?{params}&format=JSON&lang=en"
    print(f"  [JSON] GET {url[:120]}")
    r = get_retry(url)
    if r is None:
        return False
    print(f"  HTTP {r.status_code}  {len(r.content):,} b")
    if r.status_code != 200:
        print(f"  {r.text[:160]}")
        return False
    try:
        j = r.json()
    except Exception as e:
        print(f"  [JSON PARSE] {e}")
        return False
    try:
        df = _jsonstat_to_df(j)
    except Exception as e:
        print(f"  [DF BUILD] {e}")
        return False
    if len(df) < min_rows:
        print(f"  [EMPTY] {len(df)} rows")
        return False
    save(df, out, label)
    return True


def estat_try(code: str, sdmx_params: str, json_params: str,
              label: str, out: Path) -> bool:
    """Try SDMX first, then fall back to JSON API."""
    if skip(out):
        print(f"  [SKIP] {out.name}  ({out.stat().st_size // 1024} KB)")
        return True
    ok = estat_sdmx(code, sdmx_params, label, out)
    if ok:
        return True
    time.sleep(PAUSE)
    print(f"  SDMX failed → trying JSON API")
    ok = estat_json(code, json_params, label, out)
    return ok


# ─────────────────────────────────────────────────────────────────────────────
# OECD SDMX (new API)
# ─────────────────────────────────────────────────────────────────────────────

def oecd_sdmx(flow: str, key: str, params: str, label: str, out: Path,
              min_rows: int = 5) -> bool:
    url = f"{OECD_SDMX}/{flow}/{key}?{params}&dimensionAtObservation=AllDimensions"
    print(f"  [OECD SDMX] GET {url[:120]}")
    r = get_retry(url, {"Accept": "text/csv"})
    if r is None:
        return False
    print(f"  HTTP {r.status_code}  {len(r.content):,} b")
    if r.status_code != 200:
        print(f"  {r.text[:120]}")
        return False
    try:
        df = pd.read_csv(StringIO(r.text), low_memory=False)
    except Exception as e:
        print(f"  [PARSE] {e}")
        return False
    if len(df) < min_rows:
        print(f"  [EMPTY] {len(df)} rows")
        return False
    save(df, out, label)
    return True


# ─────────────────────────────────────────────────────────────────────────────
# OECD.Stat legacy JSON API  (still serves PIAAC micro-aggregates)
# ─────────────────────────────────────────────────────────────────────────────

def _oecdstat_to_df(j: dict) -> pd.DataFrame:
    """Parse OECD.Stat SDMX-JSON payload."""
    ds     = j.get("dataSets", [{}])[0]
    struct = j.get("structure", {})
    dims   = struct.get("dimensions", {}).get("observation", [])

    dim_values = [d.get("values", []) for d in dims]
    dim_sizes  = [len(v) for v in dim_values]
    dim_names  = [d.get("id", f"dim{i}") for i, d in enumerate(dims)]

    obs_dict = ds.get("observations", {})

    rows = []
    for key_str, obs in obs_dict.items():
        indices = list(map(int, key_str.split(":")))
        row = {}
        for i, (name, idx) in enumerate(zip(dim_names, indices)):
            vals = dim_values[i]
            row[name] = vals[idx].get("id", idx) if idx < len(vals) else idx
        row["OBS_VALUE"] = obs[0] if obs else None
        rows.append(row)

    return pd.DataFrame(rows)


def oecd_stat(flow: str, key: str, params: str, label: str, out: Path,
              min_rows: int = 5) -> bool:
    url = f"{OECD_STAT}/{flow}/{key}/OECD?{params}&dimensionAtObservation=AllDimensions"
    print(f"  [OECD.Stat] GET {url[:120]}")
    r = get_retry(url, {"Accept": "application/vnd.sdmx.data+json;version=1.0"})
    if r is None:
        return False
    print(f"  HTTP {r.status_code}  {len(r.content):,} b")
    if r.status_code != 200:
        print(f"  {r.text[:160]}")
        return False
    try:
        j = r.json()
    except Exception as e:
        print(f"  [JSON PARSE] {e}")
        return False
    try:
        df = _oecdstat_to_df(j)
    except Exception as e:
        print(f"  [DF BUILD] {e}")
        return False
    if len(df) < min_rows:
        print(f"  [EMPTY] {len(df)} rows")
        return False
    save(df, out, label)
    return True


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — EUROSTAT  (JSON API fallback for previously 404'd datasets)
# ═════════════════════════════════════════════════════════════════════════════

print("\n══════ EUROSTAT ══════")

# 1.1  ALMP expenditure by type of action  (lmp_ind_exp)
# Italy's low/misallocated ALMP spend is central to the policy diagnosis.
# Expenditure split by category (training vs. wage subsidy vs. direct job
# creation) is the key lever indicator.
print("\n── 1.1  ALMP expenditure by type  (lmp_ind_exp)")
estat_try(
    "lmp_ind_exp",
    "startPeriod=2010&endPeriod=2023&geo=IT",
    "sinceTimePeriod=2010&geo=IT",
    "ALMP expenditure by type",
    ESTAT_DIR / "eurostat_almp_spending_by_type.csv",
)
time.sleep(PAUSE)

# 1.2  ALMP participants by type of action  (lmp_ind_actp)
# Participant stock by intervention category — training, employment
# incentives, direct job creation, supported employment, rehabilitation.
print("\n── 1.2  ALMP participants by type  (lmp_ind_actp)")
estat_try(
    "lmp_ind_actp",
    "startPeriod=2010&endPeriod=2023&geo=IT",
    "sinceTimePeriod=2010&geo=IT",
    "ALMP participants by type",
    ESTAT_DIR / "eurostat_almp_participants_stock.csv",
)
time.sleep(PAUSE)

# 1.3  Homeownership / tenure by age  (ilc_lvho02)
# Youth in Italy overwhelmingly live with parents partly because renting is
# prohibitively expensive. Tenure-by-age shows the housing-NEET link.
print("\n── 1.3  Homeownership by age  (ilc_lvho02)")
estat_try(
    "ilc_lvho02",
    "startPeriod=2010&endPeriod=2024&geo=IT",
    "sinceTimePeriod=2010&geo=IT",
    "homeownership/tenure by age",
    ESTAT_DIR / "eurostat_homeownership_by_age.csv",
)
time.sleep(PAUSE)

# 1.4  Fertility rate by educational attainment  (demo_fordeduc)
# Italy TFR 1.24 (2023). Childbearing strongly concentrated among lower-
# educated women, driving NEET via early parenthood channel.
print("\n── 1.4  Fertility by education  (demo_fordeduc)")
estat_try(
    "demo_fordeduc",
    "startPeriod=2010&endPeriod=2024&geo=IT",
    "sinceTimePeriod=2010&geo=IT",
    "fertility by education",
    ESTAT_DIR / "eurostat_fertility_by_education.csv",
)
time.sleep(PAUSE)

# 1.5  Subjective wellbeing by age group  (ilc_pw05)
# Mean life satisfaction broken down by 5-year age bands — allows direct
# comparison of 15-24 vs. 25-34 wellbeing deficit in Italy vs. EU.
print("\n── 1.5  Wellbeing by age  (ilc_pw05)")
estat_try(
    "ilc_pw05",
    "startPeriod=2013&endPeriod=2024&geo=IT",
    "sinceTimePeriod=2013&geo=IT",
    "wellbeing by age",
    ESTAT_DIR / "eurostat_wellbeing_by_age.csv",
)
time.sleep(PAUSE)


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — OECD  PIAAC adult skills
# ═════════════════════════════════════════════════════════════════════════════

print("\n══════ OECD — PIAAC adult skills ══════")

PIAAC_OUT = OECD_DIR / "oecd_piaac_adult_skills.csv"

if skip(PIAAC_OUT):
    print(f"  [SKIP] {PIAAC_OUT.name}  ({PIAAC_OUT.stat().st_size // 1024} KB)")
else:
    # --- Attempt A: OECD.Stat legacy API  (PIAAC_LIT = literacy proficiency) ---
    print("\n── 2.A  OECD.Stat: PIAAC_LIT (literacy)")
    ok = oecd_stat(
        "PIAAC_LIT",
        "ITA+OECD",
        "startTime=2012&endTime=2015",
        "PIAAC literacy",
        PIAAC_OUT,
    )
    time.sleep(PAUSE)

    if not ok:
        # --- Attempt B: OECD.Stat: PIAAC_NUM (numeracy) ---
        print("\n── 2.B  OECD.Stat: PIAAC_NUM (numeracy)")
        ok = oecd_stat(
            "PIAAC_NUM",
            "ITA+OECD",
            "startTime=2012&endTime=2015",
            "PIAAC numeracy",
            PIAAC_OUT,
        )
        time.sleep(PAUSE)

    if not ok:
        # --- Attempt C: new OECD SDMX 2023-cycle (DF_PIAAC) ---
        print("\n── 2.C  OECD SDMX: DSD_PIAAC@DF_PIAAC,1.0")
        ok = oecd_sdmx(
            "OECD.EDU.IMEP,DSD_PIAAC@DF_PIAAC,1.0",
            "ITA",
            "startPeriod=2012&endPeriod=2024",
            "PIAAC (new SDMX)",
            PIAAC_OUT,
        )
        time.sleep(PAUSE)

    if not ok:
        # --- Attempt D: OECD SDMX 1st-cycle explicit ID ---
        print("\n── 2.D  OECD SDMX: DSD_PIAAC@DF_PIAAC_2012,1.0")
        ok = oecd_sdmx(
            "OECD.EDU.IMEP,DSD_PIAAC@DF_PIAAC_2012,1.0",
            "ITA",
            "startPeriod=2012&endPeriod=2014",
            "PIAAC 2012 cycle",
            PIAAC_OUT,
        )
        time.sleep(PAUSE)

    if not ok:
        # --- Attempt E: broader OECD SDMX EAG PIAAC view ---
        print("\n── 2.E  OECD SDMX: DSD_EAG_LSO_EA@DF_LSO_PIAAC,1.0")
        ok = oecd_sdmx(
            "OECD.EDU.IMEP,DSD_EAG_LSO_EA@DF_LSO_PIAAC,1.0",
            "ITA",
            "startPeriod=2012&endPeriod=2024",
            "PIAAC EAG view",
            PIAAC_OUT,
        )
        time.sleep(PAUSE)

    if not ok:
        print(
            "\n  [MANUAL] All PIAAC API attempts failed.\n"
            "  Download manually from:\n"
            "    https://www.oecd.org/skills/piaac/data/\n"
            "  Choose 'PIAAC 1st Cycle' → 'Country-level statistics' → CSV\n"
            f"  Save to: {PIAAC_OUT.relative_to(ROOT)}"
        )

# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Manual-only notice
# ═════════════════════════════════════════════════════════════════════════════

print("""
══════ MANUAL DOWNLOADS NEEDED ══════

INVALSI regional test scores (annual, by region/grade):
  → https://invalsi-open.net/data/
  → Download "Base dati" → "Risultati scuola" CSV
  → Save to: local_data/INVALSI/

ANPAL Youth Guarantee outcomes:
  → https://www.anpal.gov.it/statistiche/garanzia-giovani
  → Save to: local_data/ANPAL/

INPS CIG (cassa integrazione guadagni) youth usage:
  → https://www.inps.it/dati/tabelle-statistiche/cassa-integrazione-guadagni
  → Save to: local_data/INPS/
""")

print("\nDone.")
