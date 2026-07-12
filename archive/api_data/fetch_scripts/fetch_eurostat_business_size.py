"""
Fetch Eurostat business demography data relevant to company size and firm-size structure.

Dataset:
  - bd_size    : Business demography by size class and NACE Rev. 2 activity

The output is saved under local_data/eurostat. The full bd_size dataset is delivered
as compressed TSV from Eurostat and kept as raw source material for later analysis.
"""

from __future__ import annotations

import gzip
import os
from pathlib import Path
from urllib.parse import urlencode

import requests

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "local_data" / "eurostat"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

BD_SIZE_URL = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/bd_size/"
BD_SIZE_PARAMS = {
    "format": "TSV",
    "compressed": "true",
}

HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
    "Accept": "text/tab-separated-values, */*",
}

TIMEOUT = 120


def download_file(url: str, params: dict, out_path: Path) -> bool:
    if out_path.exists():
        print(f"  [skip] {out_path.name} already exists")
        return True

    request_url = f"{url}?{urlencode(params)}"
    print(f"  [fetch] {out_path.name} — {request_url}")
    response = requests.get(url, params=params, headers=HEADERS, timeout=TIMEOUT, stream=True)
    if response.status_code != 200:
        print(f"  [fail] HTTP {response.status_code} — {response.text[:200]}")
        return False

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=65536):
            if not chunk:
                continue
            handle.write(chunk)

    print(f"  [ok] {out_path.name} ({out_path.stat().st_size // 1024} KB)")
    return True


def main() -> None:
    print("Fetching Eurostat business demography dataset(s)")
    print(f"Output directory: {OUTPUT_DIR}")

    raw_out = OUTPUT_DIR / "eurostat_bd_size.tsv.gz"
    success = download_file(BD_SIZE_URL, BD_SIZE_PARAMS, raw_out)

    if not success:
        print("Failed to download bd_size dataset.")
        return

    print("\nDataset downloaded. The raw TSV is stored compressed under local_data/eurostat.")
    print("If you want a parsed CSV version, convert the TSV file with a dedicated parser.")


if __name__ == "__main__":
    main()
