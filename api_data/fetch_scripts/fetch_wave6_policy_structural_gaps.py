"""
Wave 6 — Policy, labour-structure, and social-capital gaps.

Goal
----
Fetch the remaining high-value comparative indicators suggested for the
Italy assessment, with robust retry logic and compact query filters.

Outputs (local_data/eurostat)
-----------------------------
- eurostat_almp_spending_by_type.csv          (lmp_ind_actp)
- eurostat_almp_participants_stock.csv        (lmp_par_summ)
- eurostat_poverty_single_household.csv       (ilc_li03)
- eurostat_broadband_access_nuts2.csv         (isoc_r_broad_h)
- eurostat_social_support_gap.csv             (ilc_scp18)
- eurostat_institutional_trust.csv            (ilc_pw07)
- eurostat_grade_retention.csv                (educ_uoe_enra10)
- eurostat_tertiary_field_distribution.csv    (educ_uoe_enrt01)
- eurostat_job_vacancy_rate.csv               (jvs_a_nace2)
- eurostat_homeownership_by_age.csv           (ilc_lvho02)
- eurostat_fertility_by_education.csv         (demo_fordeduc)
- eurostat_wellbeing_by_age.csv               (ilc_pw05)

Run from workspace root:
    .venv\\Scripts\\python.exe api_data/fetch_scripts/fetch_wave6_policy_structural_gaps.py
"""

import time
from io import StringIO
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent.parent
ESTAT_DIR = ROOT / "local_data" / "eurostat"
ESTAT_DIR.mkdir(parents=True, exist_ok=True)

ESTAT_SDMX = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data"

SKIP_BYTES = 500
PAUSE = 2
MAX_TRIES = 4
TIMEOUT = 90


def skip(path: Path) -> bool:
    return path.exists() and path.stat().st_size > SKIP_BYTES


def save(df: pd.DataFrame, out: Path, label: str):
    df.to_csv(out, index=False)
    print(f"  SAVED {len(df):,} rows -> {out.relative_to(ROOT)} [{label}]")


def get_with_retry(url: str) -> requests.Response | None:
    last_error = None
    for attempt in range(1, MAX_TRIES + 1):
        try:
            return requests.get(url, timeout=TIMEOUT)
        except Exception as exc:
            last_error = exc
            wait = 2 ** (attempt - 1)
            print(f"    [RETRY {attempt}/{MAX_TRIES}] {exc} ; waiting {wait}s")
            time.sleep(wait)
    print(f"    [ERROR] {last_error}")
    return None


def estat_fetch(code: str, params: str, label: str, out_name: str, min_rows: int = 5) -> bool:
    out = ESTAT_DIR / out_name
    if skip(out):
        print(f"  [SKIP] {out.name} ({out.stat().st_size // 1024} KB)")
        return True

    url = f"{ESTAT_SDMX}/{code}?format=SDMX-CSV&{params}"
    print(f"  GET {url[:125]}")
    response = get_with_retry(url)
    if response is None:
        return False

    print(f"  HTTP {response.status_code} {len(response.content):,} b")
    if response.status_code != 200:
        print(f"  {response.text[:160]}")
        return False

    try:
        df = pd.read_csv(StringIO(response.text), low_memory=False)
    except Exception as exc:
        print(f"  [PARSE ERROR] {exc}")
        return False

    if len(df) < min_rows:
        print(f"  [EMPTY] only {len(df)} rows")
        return False

    save(df, out, label)
    return True


def run_task(title: str, *fetch_attempts) -> bool:
    print(f"\n-- {title}")
    for args in fetch_attempts:
        if estat_fetch(*args):
            time.sleep(PAUSE)
            return True
    time.sleep(PAUSE)
    return False


print("Wave 6 policy + structural gaps\n")

# 1) Active labour market policy spending by intervention category.
run_task(
    "ALMP spending by type",
    (
        "lmp_ind_actp",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "ALMP spending by type",
        "eurostat_almp_spending_by_type.csv",
    ),
    (
        "lmp_ind_exp",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "ALMP spending by type (fallback)",
        "eurostat_almp_spending_by_type.csv",
    ),
)

# 2) ALMP participant stock.
run_task(
    "ALMP participant stock",
    (
        "lmp_par_summ",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "ALMP participant stock",
        "eurostat_almp_participants_stock.csv",
    ),
)

# 3) At-risk-of-poverty by household type (includes single-person households).
run_task(
    "Poverty risk by household type",
    (
        "ilc_li03",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "poverty by household type",
        "eurostat_poverty_single_household.csv",
    ),
)

# 4) Broadband access by region (NUTS).
run_task(
    "Broadband access by region",
    (
        "isoc_r_broad_h",
        "startPeriod=2010&endPeriod=2024",
        "broadband access (regional)",
        "eurostat_broadband_access_nuts2.csv",
    ),
    (
        "isoc_r_iuse_i",
        "startPeriod=2010&endPeriod=2024",
        "internet use (regional fallback)",
        "eurostat_broadband_access_nuts2.csv",
    ),
)

# 5) Social support gap (people lacking support network).
run_task(
    "Social support availability",
    (
        "ilc_scp18",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "social support gap",
        "eurostat_social_support_gap.csv",
    ),
    (
        "ilc_pw06",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "social support gap (fallback)",
        "eurostat_social_support_gap.csv",
    ),
)

# 6) Institutional trust.
run_task(
    "Institutional trust",
    (
        "ilc_pw07",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "trust in institutions",
        "eurostat_institutional_trust.csv",
    ),
)

# 7) Grade retention / repeaters.
run_task(
    "Grade retention",
    (
        "educ_uoe_enra10",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "grade retention",
        "eurostat_grade_retention.csv",
    ),
)

# 8) Tertiary field-of-study distribution.
run_task(
    "Tertiary field distribution",
    (
        "educ_uoe_enrt01",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "tertiary field distribution",
        "eurostat_tertiary_field_distribution.csv",
    ),
)

# 9) Job vacancy rate.
run_task(
    "Job vacancy rate",
    (
        "jvs_a_nace2",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "job vacancy rate",
        "eurostat_job_vacancy_rate.csv",
    ),
    (
        "jvs_q_nace2",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "job vacancy rate (quarterly fallback)",
        "eurostat_job_vacancy_rate.csv",
    ),
)

# 10) Homeownership vs renting by age.
run_task(
    "Homeownership by age",
    (
        "ilc_lvho02",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "homeownership by age",
        "eurostat_homeownership_by_age.csv",
    ),
)

# 11) Fertility by education.
run_task(
    "Fertility by education",
    (
        "demo_fordeduc",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "fertility by education",
        "eurostat_fertility_by_education.csv",
    ),
)

# 12) Subjective wellbeing by age.
run_task(
    "Wellbeing by age",
    (
        "ilc_pw05",
        "startPeriod=2010&endPeriod=2024&geo=IT",
        "wellbeing by age",
        "eurostat_wellbeing_by_age.csv",
    ),
)

print("\nSUMMARY")
targets = [
    "eurostat_almp_spending_by_type.csv",
    "eurostat_almp_participants_stock.csv",
    "eurostat_poverty_single_household.csv",
    "eurostat_broadband_access_nuts2.csv",
    "eurostat_social_support_gap.csv",
    "eurostat_institutional_trust.csv",
    "eurostat_grade_retention.csv",
    "eurostat_tertiary_field_distribution.csv",
    "eurostat_job_vacancy_rate.csv",
    "eurostat_homeownership_by_age.csv",
    "eurostat_fertility_by_education.csv",
    "eurostat_wellbeing_by_age.csv",
]

ok = 0
for name in targets:
    p = ESTAT_DIR / name
    if p.exists() and p.stat().st_size > SKIP_BYTES:
        ok += 1
        print(f"  [OK ] {p.relative_to(ROOT)} ({p.stat().st_size // 1024} KB)")
    else:
        print(f"  [MISS] {p.relative_to(ROOT)}")

print(f"\nCompleted: {ok}/{len(targets)} files present")
