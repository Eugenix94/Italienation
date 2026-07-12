"""
Fetch SIOPE school spending data (USCITE + ENTRATE) for Italian public schools.

Data source: https://www.siope.it/Siope/documenti/siope2/open/last/
No authentication required — public open data released by Banca d'Italia.

Strategy:
  1. Download ANAGRAFICHE.zip (0.8 MB) to extract school entity codes
     (sottocomparto = ENTI_VOL_FIN_IS, comparto = VCF)
  2. For each requested year, stream USCITE / ENTRATE zip (~70 MB each),
     filter rows matching a school entity code, write filtered CSV.

Output: local_data/SIOPE/
  siope_anagrafiche_scuole.csv  — school entity registry
  siope_uscite_{year}.csv       — filtered expenditure rows per year
  siope_entrate_{year}.csv      — filtered receipts rows per year (optional)

CSV columns (no header in source — added here):
  USCITE / ENTRATE:
    codice_ente, anno, mese, codice_gestionale, importo_centesimi

Run:
  python api_data/fetch_scripts/fetch_siope_school_spending.py
  python api_data/fetch_scripts/fetch_siope_school_spending.py --entrate
  python api_data/fetch_scripts/fetch_siope_school_spending.py --years 2022 2023 2024
"""

import argparse
import io
import csv
import sys
import time
import zipfile
from pathlib import Path

import requests

BASE_URL = "https://www.siope.it/Siope/documenti/siope2/open/last/"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "local_data" / "SIOPE"
HEADERS = {"User-Agent": "Mozilla/5.0 (research/open-data; contact: local)"}
SCHOOL_SOTTOCOMPARTO = "ENTI_VOL_FIN_IS"

USCITE_COLS  = ["codice_ente", "anno", "mese", "codice_gestionale", "importo_centesimi"]
ENTRATE_COLS = ["codice_ente", "anno", "mese", "codice_gestionale", "importo_centesimi"]


def download_zip(session: requests.Session, url: str, label: str) -> bytes:
    """Stream-download a zip file, printing progress."""
    r = session.get(url, headers=HEADERS, stream=True, timeout=120)
    r.raise_for_status()
    total = int(r.headers.get("Content-Length", 0))
    chunks = []
    downloaded = 0
    for chunk in r.iter_content(chunk_size=131072):
        chunks.append(chunk)
        downloaded += len(chunk)
        if total:
            pct = downloaded / total * 100
            print(f"\r  {label}: {downloaded/1024/1024:.1f} MB / {total/1024/1024:.1f} MB ({pct:.0f}%)", end="", flush=True)
    print()
    return b"".join(chunks)


def load_school_codes(session: requests.Session) -> tuple[dict[str, dict], set[str]]:
    """Download ANAGRAFICHE and return (school_info_dict, school_codes_set)."""
    url = BASE_URL + "SIOPE_ANAGRAFICHE.zip"
    print(f"Downloading ANAGRAFICHE.zip ...")
    data = download_zip(session, url, "ANAGRAFICHE")
    zf = zipfile.ZipFile(io.BytesIO(data))

    school_info: dict[str, dict] = {}
    for name in zf.namelist():
        if "ENTI_SIOPE" in name:
            content = zf.open(name).read().decode("utf-8", errors="replace")
            for line in content.strip().split("\n"):
                parts = [p.strip('"') for p in line.strip().split(",")]
                if len(parts) >= 9 and parts[8] == SCHOOL_SOTTOCOMPARTO:
                    school_info[parts[0]] = {
                        "codice_ente": parts[0],
                        "data_inizio": parts[1],
                        "data_fine": parts[2],
                        "codice_fiscale": parts[3],
                        "denominazione": parts[4],
                        "codice_regione": parts[5],
                        "codice_provincia": parts[6],
                        "codice_comune": parts[7],
                        "sottocomparto": parts[8],
                    }
            break

    print(f"  Found {len(school_info):,} school entities (sottocomparto={SCHOOL_SOTTOCOMPARTO})")
    return school_info, set(school_info.keys())


def save_school_registry(school_info: dict[str, dict], out_dir: Path) -> None:
    out_path = out_dir / "siope_anagrafiche_scuole.csv"
    fieldnames = ["codice_ente", "data_inizio", "data_fine", "codice_fiscale",
                  "denominazione", "codice_regione", "codice_provincia",
                  "codice_comune", "sottocomparto"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(school_info.values())
    print(f"  Saved registry → {out_path.relative_to(out_dir.parents[1])}")


def filter_zip(
    session: requests.Session,
    url: str,
    school_codes: set[str],
    col_names: list[str],
    out_path: Path,
    label: str,
) -> int:
    """Download zip, filter for school entity codes, write filtered CSV. Returns row count."""
    print(f"\nDownloading {label} ...")
    data = download_zip(session, url, label)
    zf = zipfile.ZipFile(io.BytesIO(data))
    csv_name = zf.namelist()[0]

    content = zf.open(csv_name).read().decode("utf-8", errors="replace")
    lines = content.strip().split("\n")
    total = len(lines)

    filtered: list[list[str]] = []
    for line in lines:
        parts = [p.strip('"') for p in line.strip().split(",")]
        if len(parts) < 5:
            continue
        ente = parts[0]
        # Entity code is always the first 9 chars (some codes are 9-digit, some 15-digit)
        code9 = ente[:9]
        if code9 in school_codes or ente in school_codes:
            filtered.append(parts[:5])  # only keep defined columns

    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(col_names)
        w.writerows(filtered)

    pct = len(filtered) / total * 100 if total else 0
    print(f"  {total:,} total rows → {len(filtered):,} school rows ({pct:.1f}%)")
    print(f"  Saved → {out_path.relative_to(out_path.parents[2])}")
    return len(filtered)


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch SIOPE school spending data")
    parser.add_argument(
        "--years", nargs="+", type=int,
        default=list(range(2017, 2026)),
        help="Years to download (default: 2017-2025)",
    )
    parser.add_argument(
        "--entrate", action="store_true",
        help="Also download ENTRATE (receipts), not just USCITE (expenditure)",
    )
    parser.add_argument(
        "--skip-existing", action="store_true", default=True,
        help="Skip years where output file already exists (default: on)",
    )
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    session = requests.Session()

    # Step 1: Load school entity codes
    school_info, school_codes = load_school_codes(session)
    save_school_registry(school_info, OUTPUT_DIR)

    # Step 2: Download and filter USCITE
    print("\n=== USCITE (expenditure) ===")
    for year in sorted(args.years):
        out_path = OUTPUT_DIR / f"siope_uscite_{year}.csv"
        if args.skip_existing and out_path.exists():
            print(f"  {year}: already exists, skipping")
            continue
        url = BASE_URL + f"SIOPE_USCITE.{year}.zip"
        filter_zip(session, url, school_codes, USCITE_COLS, out_path, f"USCITE {year}")
        time.sleep(1)  # polite delay

    # Step 3: Optionally download ENTRATE
    if args.entrate:
        print("\n=== ENTRATE (receipts) ===")
        for year in sorted(args.years):
            out_path = OUTPUT_DIR / f"siope_entrate_{year}.csv"
            if args.skip_existing and out_path.exists():
                print(f"  {year}: already exists, skipping")
                continue
            url = BASE_URL + f"SIOPE_ENTRATE.{year}.zip"
            filter_zip(session, url, school_codes, ENTRATE_COLS, out_path, f"ENTRATE {year}")
            time.sleep(1)

    print("\nDone.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
