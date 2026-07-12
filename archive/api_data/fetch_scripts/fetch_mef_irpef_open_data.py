"""
Fetch selected MEF Dipartimento delle Finanze IRPEF open data files.

The public catalog exposes stable direct download URLs for the current annual
release. This script downloads a compact set of files that are useful for
income-distribution, regional, sex, and municipality-level analysis.

Output directory: local_data/MEF/irpef_open_data/
  - raw CSV / ZIP downloads are saved as-is
  - ZIP archives are extracted into a same-named subfolder for convenience
  - a small manifest.json records the files that were fetched
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import requests


BASE_URL = "https://www1.finanze.gov.it/finanze/analisi_stat/public/v_4_0_0/contenuti"
OUTPUT_DIR = Path(__file__).resolve().parents[2] / "local_data" / "MEF" / "irpef_open_data"


FILES = [
    {
        "name": "mef_reg_tipo_reddito_2025.csv",
        "url": f"{BASE_URL}/REG_tipo_reddito_2025.csv?d=1615465800",
        "kind": "csv",
        "description": "IRPEF by regional income class",
    },
    {
        "name": "mef_reg_calcolo_irpef_2025.csv",
        "url": f"{BASE_URL}/REG_calcolo_irpef_2025.csv?d=1615465800",
        "kind": "csv",
        "description": "IRPEF calculation components by regional income class",
    },
    {
        "name": "mef_sesso_tipo_reddito_2025.csv",
        "url": f"{BASE_URL}/sesso_tipo_reddito_2025.csv?d=1615465800",
        "kind": "csv",
        "description": "IRPEF by sex and income type",
    },
    {
        "name": "mef_sesso_calcolo_irpef_2025.csv",
        "url": f"{BASE_URL}/sesso_calcolo_irpef_2025.csv?d=1615465800",
        "kind": "csv",
        "description": "IRPEF calculation components by sex",
    },
    {
        "name": "mef_comunale_irpef_2024.zip",
        "url": f"{BASE_URL}/Redditi_e_principali_variabili_IRPEF_su_base_comunale_CSV_2024.zip?d=1615465800",
        "kind": "zip",
        "description": "Municipality-level IRPEF distribution and tax variables",
    },
    {
        "name": "mef_subcomunale_irpef_2024.zip",
        "url": f"{BASE_URL}/Redditi_e_principali_variabili_IRPEF_su_base_subcomunale_CSV_2024.zip?d=1615465800",
        "kind": "zip",
        "description": "Sub-municipality (CAP) IRPEF distribution and tax variables",
    },
]


HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
    "Accept": "text/csv, application/zip, */*",
}


def download_file(url: str, out_path: Path) -> tuple[int, str | None]:
    response = requests.get(url, headers=HEADERS, timeout=60, stream=True)
    response.raise_for_status()

    out_path.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with out_path.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=65536):
            if not chunk:
                continue
            handle.write(chunk)
            total += len(chunk)

    return total, response.headers.get("content-type")


def extract_zip(zip_path: Path) -> list[str]:
    extract_dir = zip_path.with_suffix("")
    extract_dir.mkdir(parents=True, exist_ok=True)
    extracted = []
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.namelist():
            archive.extract(member, extract_dir)
            extracted.append(str(extract_dir / member))
    return extracted


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []

    print(f"Saving MEF IRPEF downloads to {OUTPUT_DIR}")
    for item in FILES:
        out_path = OUTPUT_DIR / item["name"]
        if out_path.exists():
            print(f"  [skip] {item['name']} already exists")
            manifest.append({**item, "status": "skipped", "path": str(out_path)})
            continue

        print(f"  [fetch] {item['name']} — {item['description']}")
        size, content_type = download_file(item["url"], out_path)
        extracted = []
        if item["kind"] == "zip":
            extracted = extract_zip(out_path)

        print(f"    [ok] {size:,} bytes, content-type={content_type}")
        if extracted:
            print(f"    [extract] {len(extracted)} file(s)")

        manifest.append(
            {
                **item,
                "status": "ok",
                "path": str(out_path),
                "bytes": size,
                "content_type": content_type,
                "extracted_files": extracted,
            }
        )

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nManifest written to {manifest_path}")


if __name__ == "__main__":
    main()