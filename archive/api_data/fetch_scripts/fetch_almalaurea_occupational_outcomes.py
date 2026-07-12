"""Fetch AlmaLaurea occupational outcome sources for higher-education analysis.

This script downloads the latest official AlmaLaurea occupational reports and
parses public graduate-outcome detail pages into machine-readable CSVs. The
focus is the transition from graduation into work at 1, 3, and 5 years after
graduation, with disaggregation by course type and disciplinary area.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "local_data" / "AlmaLaurea" / "occupational_outcomes"
RAW_DIR = OUTPUT_DIR / "raw"

HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
}

REPORT_FILES = [
    {
        "name": "almalaurea_occupazione_2025_summary.pdf",
        "url": "https://www.almalaurea.it/document-download/29073",
        "description": "Summary report XXVII Indagine (2025) - Condizione occupazionale dei laureati",
    },
    {
        "name": "almalaurea_occupazione_2025_full_report.pdf",
        "url": "https://www.almalaurea.it/document-download/29057",
        "description": "Full report XXVII Indagine (2025) - Condizione occupazionale dei laureati",
    },
]

QUERY_SPECS = [
    {
        "slug": "almalaurea_occupazione_1yr_by_course_type",
        "survey_year": 2024,
        "years_after_graduation": 1,
        "disaggregation": "course_type",
        "url": "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno=2024&corstipo=TUTTI&ateneo=tutti&facolta=tutti&gruppo=tutti&pa=tutti&classe=tutti&postcorso=tutti&isstella=0&annolau=1&condocc=tutti&iscrls=tutti&disaggregazione=corstipo&LANG=it&CONFIG=occupazione",
    },
    {
        "slug": "almalaurea_occupazione_3yr_by_course_type",
        "survey_year": 2024,
        "years_after_graduation": 3,
        "disaggregation": "course_type",
        "url": "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno=2024&corstipo=TUTTI&ateneo=tutti&facolta=tutti&gruppo=tutti&pa=tutti&classe=tutti&postcorso=tutti&isstella=0&annolau=3&condocc=tutti&iscrls=tutti&disaggregazione=corstipo&LANG=it&CONFIG=occupazione",
    },
    {
        "slug": "almalaurea_occupazione_5yr_by_course_type",
        "survey_year": 2024,
        "years_after_graduation": 5,
        "disaggregation": "course_type",
        "url": "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno=2024&corstipo=TUTTI&ateneo=tutti&facolta=tutti&gruppo=tutti&pa=tutti&classe=tutti&postcorso=tutti&isstella=0&annolau=5&condocc=tutti&iscrls=tutti&disaggregazione=corstipo&LANG=it&CONFIG=occupazione",
    },
    {
        "slug": "almalaurea_occupazione_1yr_by_disciplinary_area",
        "survey_year": 2024,
        "years_after_graduation": 1,
        "disaggregation": "disciplinary_area",
        "url": "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno=2024&corstipo=tutti&ateneo=tutti&facolta=tutti&gruppo=tutti&livello=tutti&area4=tutti&pa=tutti&classe=tutti&postcorso=tutti&isstella=0&annolau=1&condocc=tutti&iscrls=tutti&macroareageo=tutti&areageografica=tutti&regione=tutti&dimensione=tutti&aggregacodicione=0&disaggregazione=area4&LANG=it&CONFIG=occupazione",
    },
    {
        "slug": "almalaurea_occupazione_3yr_by_disciplinary_area",
        "survey_year": 2024,
        "years_after_graduation": 3,
        "disaggregation": "disciplinary_area",
        "url": "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno=2024&corstipo=tutti&ateneo=tutti&facolta=tutti&gruppo=tutti&livello=tutti&area4=tutti&pa=tutti&classe=tutti&postcorso=tutti&isstella=0&annolau=3&condocc=tutti&iscrls=tutti&macroareageo=tutti&areageografica=tutti&regione=tutti&dimensione=tutti&aggregacodicione=0&disaggregazione=area4&LANG=it&CONFIG=occupazione",
    },
    {
        "slug": "almalaurea_occupazione_5yr_by_disciplinary_area",
        "survey_year": 2024,
        "years_after_graduation": 5,
        "disaggregation": "disciplinary_area",
        "url": "https://www2.almalaurea.it/cgi-php/universita/statistiche/visualizza.php?anno=2024&corstipo=tutti&ateneo=tutti&facolta=tutti&gruppo=tutti&livello=tutti&area4=tutti&pa=tutti&classe=tutti&postcorso=tutti&isstella=0&annolau=5&condocc=tutti&iscrls=tutti&macroareageo=tutti&areageografica=tutti&regione=tutti&dimensione=tutti&aggregacodicione=0&disaggregazione=area4&LANG=it&CONFIG=occupazione",
    },
]


def ensure_dirs() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_response(url: str, binary: bool = False) -> tuple[bytes | str, str | None]:
    response = requests.get(url, timeout=120, headers=HEADERS)
    response.raise_for_status()
    payload: bytes | str = response.content if binary else response.text
    return payload, response.headers.get("content-type")


def clean_text(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split()).strip()


def parse_numeric(value: str) -> float | None:
    value = clean_text(value)
    if value in {"", "-", "–"}:
        return None
    normalized = value.replace(".", "").replace(",", ".")
    try:
        return float(normalized)
    except ValueError:
        return None


def extract_group_labels(row) -> list[str]:
    labels = []
    for span in row.find_all("span"):
        label = clean_text(span.get_text(" ", strip=True))
        if label and label not in labels:
            labels.append(label)
    if labels:
        return labels

    cells = row.find_all(["th", "td"], recursive=False)
    return [clean_text(cell.get_text(" ", strip=True)) for cell in cells if clean_text(cell.get_text(" ", strip=True))]


def extract_table_rows(table) -> list[list[str]]:
    rows = []
    for row in table.find_all("tr"):
        cells = row.find_all(["th", "td"], recursive=False)
        if not cells:
            continue
        values = [clean_text(cell.get_text(" ", strip=True)) for cell in cells]
        if any(values):
            rows.append(values)
    return rows


def build_raw_csv_rows(table_rows: list[list[str]], group_labels: list[str]) -> list[list[str]]:
    if len(table_rows) < 4:
        return []

    section_title = table_rows[0][0]
    first_data_row = table_rows[2]
    value_count = max(len(first_data_row) - 1, 0)

    column_labels = list(group_labels)
    if value_count == len(group_labels) + 1:
        column_labels = ["Collettivo selezionato"] + column_labels
    elif value_count > len(group_labels):
        extras = value_count - len(group_labels)
        column_labels = ["Collettivo selezionato"]
        while len(column_labels) < extras:
            column_labels.append(f"Colonna {len(column_labels) + 1}")
        column_labels.extend(group_labels)

    rows = [[section_title], [""] + column_labels]
    for row in table_rows[2:]:
        if len(row) == 1:
            continue
        rows.append(row)
    return rows


def build_long_rows(spec: dict[str, object], table_rows: list[list[str]], group_labels: list[str], table_index: int) -> list[dict[str, object]]:
    if len(table_rows) < 4:
        return []

    section_title = table_rows[0][0]
    first_data_row = table_rows[2]
    value_count = max(len(first_data_row) - 1, 0)

    column_labels = list(group_labels)
    if value_count == len(group_labels) + 1:
        column_labels = ["Collettivo selezionato"] + column_labels
    elif value_count > len(group_labels):
        extras = value_count - len(group_labels)
        column_labels = ["Collettivo selezionato"]
        while len(column_labels) < extras:
            column_labels.append(f"Colonna {len(column_labels) + 1}")
        column_labels.extend(group_labels)

    long_rows: list[dict[str, object]] = []
    for row in table_rows[2:]:
        if len(row) < 2:
            continue
        measure = row[0]
        values = row[1:]
        for column_label, value_raw in zip(column_labels, values):
            long_rows.append(
                {
                    "query_slug": spec["slug"],
                    "survey_year": spec["survey_year"],
                    "years_after_graduation": spec["years_after_graduation"],
                    "disaggregation": spec["disaggregation"],
                    "table_index": table_index,
                    "section_title": section_title,
                    "measure": measure,
                    "group_label": column_label,
                    "value_raw": value_raw,
                    "value_numeric": parse_numeric(value_raw),
                    "source_url": spec["url"],
                }
            )
    return long_rows


def write_csv(path: Path, rows: list[list[str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def write_long_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def fetch_report(spec: dict[str, str]) -> dict[str, object]:
    out_path = OUTPUT_DIR / spec["name"]
    if out_path.exists():
        return {
            "source": "AlmaLaurea",
            "type": "report",
            "description": spec["description"],
            "status": "skipped",
            "path": str(out_path),
        }

    payload, content_type = fetch_response(spec["url"], binary=True)
    out_path.write_bytes(payload)
    return {
        "source": "AlmaLaurea",
        "type": "report",
        "description": spec["description"],
        "status": "ok",
        "path": str(out_path),
        "content_type": content_type,
        "bytes": out_path.stat().st_size,
    }


def fetch_query(spec: dict[str, object]) -> tuple[dict[str, object], list[dict[str, object]]]:
    raw_html_path = RAW_DIR / f"{spec['slug']}.html"
    raw_csv_path = OUTPUT_DIR / f"{spec['slug']}.csv"

    html_text, content_type = fetch_response(spec["url"], binary=False)
    raw_html_path.write_text(html_text, encoding="utf-8")

    soup = BeautifulSoup(html_text, "html.parser")
    tables = [
        table
        for table in soup.find_all("table")
        if any(css_class.startswith("dati") for css_class in table.get("class", []))
    ]
    if not tables:
        raise RuntimeError(f"No AlmaLaurea data tables found for {spec['slug']}")

    raw_rows: list[list[str]] = []
    long_rows: list[dict[str, object]] = []
    for table_index, table in enumerate(tables, start=1):
        row_elements = table.find_all("tr")
        if len(row_elements) < 4:
            continue
        group_labels = extract_group_labels(row_elements[2])
        table_rows = extract_table_rows(table)
        raw_rows.extend(build_raw_csv_rows(table_rows, group_labels))
        raw_rows.append([])
        long_rows.extend(build_long_rows(spec, table_rows, group_labels, table_index))

    write_csv(raw_csv_path, raw_rows)
    long_csv_path = OUTPUT_DIR / f"{spec['slug']}_long.csv"
    write_long_csv(long_csv_path, long_rows)

    manifest_entry = {
        "source": "AlmaLaurea",
        "type": "query",
        "status": "ok",
        "slug": spec["slug"],
        "survey_year": spec["survey_year"],
        "years_after_graduation": spec["years_after_graduation"],
        "disaggregation": spec["disaggregation"],
        "path": str(raw_csv_path),
        "long_path": str(long_csv_path),
        "raw_html_path": str(raw_html_path),
        "content_type": content_type,
        "rows": len(long_rows),
        "tables": len(tables),
        "source_url": spec["url"],
    }
    return manifest_entry, long_rows


def main() -> None:
    ensure_dirs()
    manifest: list[dict[str, object]] = []
    combined_long_rows: list[dict[str, object]] = []

    print(f"Saving AlmaLaurea occupational outcome sources to {OUTPUT_DIR}")
    for report in REPORT_FILES:
        print(f"  [report] {report['name']}")
        manifest.append(fetch_report(report))

    for spec in QUERY_SPECS:
        print(f"  [query] {spec['slug']}")
        entry, long_rows = fetch_query(spec)
        manifest.append(entry)
        combined_long_rows.extend(long_rows)

    combined_path = OUTPUT_DIR / "almalaurea_occupational_outcomes_2024_long.csv"
    write_long_csv(combined_path, combined_long_rows)

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nCombined long CSV written to {combined_path}")
    print(f"Manifest written to {manifest_path}")


if __name__ == "__main__":
    main()