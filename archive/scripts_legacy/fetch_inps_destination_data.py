from __future__ import annotations

import csv
import datetime as dt
import html
import json
import pathlib
import re
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
HITS_CSV = ROOT / "local_data" / "processed" / "inps_apprenticeship_informal_hits_2026-05-24.csv"
OUT_DIR = ROOT / "local_data" / "INPS" / "destination"
MANIFEST = OUT_DIR / "manifest.json"


def _safe_file_name(package_id: str, url: str, index: int) -> str:
    id_match = re.search(r"ID-(\d+)\.csv$", url, flags=re.IGNORECASE)
    if id_match:
        return f"ID-{id_match.group(1)}.csv"
    base = re.sub(r"[^a-zA-Z0-9._-]+", "_", package_id).strip("_")
    base = base[:90] if len(base) > 90 else base
    return f"{base}__{index}.csv"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    rows = list(csv.DictReader(HITS_CSV.open(encoding="utf-8")))
    manifest_rows: list[dict[str, object]] = []

    for row in rows:
        package_id = html.unescape(row["package_id"])
        title = html.unescape(row.get("title", ""))
        urls = [
            u.strip()
            for u in (row.get("resource_urls") or "").split("|")
            if u.strip().lower().endswith(".csv")
        ]

        for i, url in enumerate(urls, start=1):
            file_name = _safe_file_name(package_id, url, i)
            local_file = OUT_DIR / file_name
            status = "ok"
            error = ""
            bytes_count = 0

            try:
                with urllib.request.urlopen(url, timeout=60) as resp:
                    payload = resp.read()
                local_file.write_bytes(payload)
                bytes_count = len(payload)
            except Exception as exc:  # noqa: BLE001
                status = "error"
                error = str(exc)[:240]

            manifest_rows.append(
                {
                    "package_id": package_id,
                    "title": title,
                    "url": url,
                    "local_file": str(local_file).replace("\\", "/"),
                    "status": status,
                    "bytes": bytes_count,
                    "error": error,
                }
            )

    MANIFEST.write_text(
        json.dumps(
            {
                "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
                "source_hits_file": str(HITS_CSV).replace("\\", "/"),
                "files": manifest_rows,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    ok = sum(1 for x in manifest_rows if x["status"] == "ok")
    err = len(manifest_rows) - ok
    print(f"Downloads attempted: {len(manifest_rows)}")
    print(f"Downloads ok: {ok}")
    print(f"Downloads error: {err}")
    print(f"Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
