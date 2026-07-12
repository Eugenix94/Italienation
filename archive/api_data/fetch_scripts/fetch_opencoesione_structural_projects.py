"""Fetch selected OpenCoesione datasets for territorial exclusion analysis.

The OpenCoesione portal exposes stable direct downloads for project-level and
theme-level open data. This script collects the highest-value files for
territorial inequality work without downloading the full 250+ MB all-projects
archive.

Outputs:
- local_data/OpenCoesione/structural_projects/*
- local_data/OpenCoesione/structural_projects/manifest.json
"""

from __future__ import annotations

import json
import zipfile
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "local_data" / "OpenCoesione" / "structural_projects"

HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
    "Accept": "application/zip, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, */*",
}

FILES = [
    {
        "name": "opencoesione_projects_aggregated.zip",
        "url": "https://opencoesione.gov.it/it/opendata/progetti_esteso_aggregati.zip",
        "kind": "zip",
        "description": "Extended aggregated OpenCoesione project dataset across programming cycles",
    },
    {
        "name": "opencoesione_projects_metadata.xlsx",
        "url": "https://opencoesione.gov.it/media/opendata/metadati_progetti_tracciato_esteso.xlsx",
        "kind": "xlsx",
        "description": "Metadata for the extended OpenCoesione project trace",
    },
    {
        "name": "opencoesione_synthetic_theme_mapping.xlsx",
        "url": "https://opencoesione.gov.it/media/uploads/metadati_temi_sintetici.xlsx",
        "kind": "xlsx",
        "description": "Theme mapping between synthetic policy themes and CUP classifications",
    },
    {
        "name": "opencoesione_digital_projects_all_cycles.zip",
        "url": "https://opencoesione.gov.it/it/opendata/temi/progetti_esteso_RETI_SERVIZI_DIGITALI.zip",
        "kind": "zip",
        "description": "All-cycle OpenCoesione projects in the digital networks and services theme",
    },
    {
        "name": "opencoesione_digital_projects_2021_2027.zip",
        "url": "https://opencoesione.gov.it/it/opendata/temi/progetti_esteso_RETI_SERVIZI_DIGITALI_2021-2027.zip",
        "kind": "zip",
        "description": "2021-2027 OpenCoesione projects in the digital networks and services theme",
    },
]


def download_file(url: str, out_path: Path) -> tuple[int, str | None]:
    response = requests.get(url, headers=HEADERS, timeout=120, stream=True)
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

    print(f"Saving OpenCoesione downloads to {OUTPUT_DIR}")
    for item in FILES:
        out_path = OUTPUT_DIR / item["name"]
        if out_path.exists():
            print(f"  [skip] {item['name']} already exists")
            manifest.append({**item, "status": "skipped", "path": str(out_path)})
            continue

        print(f"  [fetch] {item['name']} - {item['description']}")
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