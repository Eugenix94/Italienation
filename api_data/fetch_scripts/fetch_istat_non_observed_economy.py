"""
Fetch ISTAT non-observed-economy release assets.

The public press release exposes the report PDF and the companion Excel tables
directly. This script downloads both assets and writes a small manifest for
traceability.
"""

from __future__ import annotations

import json
from pathlib import Path

import requests


OUTPUT_DIR = Path(__file__).resolve().parents[2] / "local_data" / "ISTAT" / "non_observed_economy"

FILES = [
    {
        "name": "istat_non_observed_economy_report_2023.pdf",
        "url": "https://www.istat.it/wp-content/uploads/2025/10/Report-ECONOMIA-NON-OSSERVATA-NEI-CONTI-NAZIONALI_ANNO2023.pdf",
        "description": "ISTAT report and methodological note",
    },
    {
        "name": "istat_non_observed_economy_tables_2025.xlsx",
        "url": "https://www.istat.it/wp-content/uploads/2025/10/Tavole-Economia-non-osservata_2025.xlsx",
        "description": "ISTAT companion tables workbook",
    },
]


HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
    "Accept": "application/pdf, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, */*",
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


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = []

    print(f"Saving ISTAT non-observed economy assets to {OUTPUT_DIR}")
    for item in FILES:
        out_path = OUTPUT_DIR / item["name"]
        if out_path.exists():
            print(f"  [skip] {item['name']} already exists")
            manifest.append({**item, "status": "skipped", "path": str(out_path)})
            continue

        print(f"  [fetch] {item['name']} — {item['description']}")
        size, content_type = download_file(item["url"], out_path)
        print(f"    [ok] {size:,} bytes, content-type={content_type}")
        manifest.append(
            {
                **item,
                "status": "ok",
                "path": str(out_path),
                "bytes": size,
                "content_type": content_type,
            }
        )

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nManifest written to {manifest_path}")


if __name__ == "__main__":
    main()