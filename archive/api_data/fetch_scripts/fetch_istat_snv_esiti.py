"""Fetch the MIM SNV 'Esiti' datasets and build a bocciatura proxy summary.

The official portal does not expose a single numeric 'bocciatura' field.
Instead, this script downloads the school self-evaluation outcomes datasets
(sezione Esiti) and derives a conservative proxy using the rubric scores and
keyword hits in the motivation text.

Outputs:
- local_data/MinIstruzione/SNV/esiti_raw/*.csv
- local_data/processed/snv_esiti_school_long.csv
- local_data/processed/snv_esiti_school_year_proxy.csv
- local_data/processed/snv_esiti_manifest.csv
"""

from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[2]
RAW_OUT = ROOT / "local_data" / "MinIstruzione" / "SNV" / "esiti_raw"
PROCESSED_OUT = ROOT / "local_data" / "processed"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Italienation SNV fetch script)"
}

DATASETS = {
    "statale": {
        "page": (
            "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf"
            "?area=Sistema%20Nazionale%20di%20Valutazione&datasetId=DS0500VALUTAZIONE_ESITI_STA"
        ),
    },
    "paritaria": {
        "page": (
            "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf"
            "?area=Sistema%20Nazionale%20di%20Valutazione&datasetId=DS0510VALUTAZIONE_ESITI_PAR"
        ),
    },
}

KEYWORDS = [
    "ammissione alla classe successiva",
    "non sono ammessi",
    "non e' ammesso",
    "non è ammesso",
    "insuccesso",
    "abbandon",
    "ripeten",
    "bocciat",
    "debiti formativi",
    "successo scolastico",
    "fallimento",
]


def ensure_dirs() -> None:
    RAW_OUT.mkdir(parents=True, exist_ok=True)
    PROCESSED_OUT.mkdir(parents=True, exist_ok=True)


def discover_csv_urls(page_url: str) -> list[str]:
    """Extract downloadable CSV URLs from the dataset page HTML."""
    response = requests.get(page_url, headers=HEADERS, timeout=60)
    response.raise_for_status()
    html = response.text
    hrefs = re.findall(r'href="(?P<href>VALUTAZIONE_ESITI_[^"]+\.csv)"', html)
    urls = [urljoin(page_url.rstrip("/") + "/", href) for href in hrefs]
    # Preserve order while removing duplicates.
    return list(dict.fromkeys(urls))


def download_file(url: str, dest: Path) -> Path:
    response = requests.get(url, headers=HEADERS, stream=True, timeout=120)
    response.raise_for_status()
    with dest.open("wb") as handle:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                handle.write(chunk)
    return dest


def read_csv_flexible(path: Path) -> pd.DataFrame:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        for sep in (";", ","):
            try:
                df = pd.read_csv(path, sep=sep, encoding=encoding, low_memory=False)
                if df.shape[1] > 1:
                    return df
            except Exception:
                continue
    raise ValueError(f"Could not read CSV file: {path}")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned.columns = [str(col).strip().upper() for col in cleaned.columns]
    rename_map = {
        "ANNOSCOLASTICO": "annoscolastico",
        "CODICEISTITUTO": "codice_istituto",
        "SEZIONE": "sezione",
        "CODICECRITERIO": "codice_criterio",
        "PUNTEGGIOSCUOLA": "punteggio_scuola",
        "MOTIVAZIONEPUNTEGGIOSCUOLA": "motivazione_punteggio_scuola",
    }
    cleaned = cleaned.rename(columns={k: v for k, v in rename_map.items() if k in cleaned.columns})
    return cleaned


def keyword_hits(text: str) -> list[str]:
    lowered = (text or "").lower()
    hits = [keyword for keyword in KEYWORDS if keyword in lowered]
    return hits


def academic_year_label(value: object) -> str:
    text = str(value).strip()
    digits = re.sub(r"\D", "", text)
    if len(digits) == 6 and digits.isdigit():
        return f"{digits[:4]}/{digits[4:]}"
    return text


def build_proxy_table(df: pd.DataFrame, school_type: str, source_url: str) -> pd.DataFrame:
    table = normalize_columns(df)

    if "punteggio_scuola" in table.columns:
        table["punteggio_scuola"] = pd.to_numeric(table["punteggio_scuola"], errors="coerce")

    table["school_type"] = school_type
    table["source_url"] = source_url
    table["academic_year"] = table["annoscolastico"].apply(academic_year_label)
    table["motivazione_lower"] = table.get("motivazione_punteggio_scuola", "").fillna("").astype(str).str.lower()
    table["keyword_hits"] = table["motivazione_lower"].apply(keyword_hits)
    table["keyword_hit_count"] = table["keyword_hits"].apply(len)
    table["score_is_low"] = table["punteggio_scuola"].le(2) if "punteggio_scuola" in table.columns else False
    table["score_is_weak"] = table["punteggio_scuola"].le(3) if "punteggio_scuola" in table.columns else False
    table["bocciatura_proxy"] = table["score_is_low"] | (table["keyword_hit_count"] > 0)
    table["bocciatura_proxy_reason"] = table["keyword_hits"].apply(lambda hits: ", ".join(hits) if hits else "")
    table["bocciatura_proxy_strength"] = pd.to_numeric(table.get("punteggio_scuola"), errors="coerce")
    return table.drop(columns=["motivazione_lower"], errors="ignore")


def summarize_proxy_table(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["school_type", "academic_year", "codice_istituto"]
    summary = (
        df.groupby(group_cols, dropna=False)
        .agg(
            rows=("codice_criterio", "count"),
            avg_score=("punteggio_scuola", "mean"),
            min_score=("punteggio_scuola", "min"),
            low_score_rows=("score_is_low", "sum"),
            weak_score_rows=("score_is_weak", "sum"),
            proxy_rows=("bocciatura_proxy", "sum"),
            keyword_hits=("keyword_hit_count", "sum"),
        )
        .reset_index()
    )
    summary["proxy_rate"] = summary["proxy_rows"] / summary["rows"].where(summary["rows"] != 0, 1)
    summary["school_proxy_flag"] = summary["proxy_rows"] > 0
    return summary.sort_values(["academic_year", "school_type", "proxy_rate"], ascending=[True, True, False])


def main() -> None:
    ensure_dirs()

    manifest_rows: list[dict[str, object]] = []
    long_tables: list[pd.DataFrame] = []

    for school_type, meta in DATASETS.items():
        page_url = meta["page"]
        csv_urls = discover_csv_urls(page_url)
        if not csv_urls:
            print(f"No CSV URLs discovered for {school_type}")
            manifest_rows.append(
                {
                    "school_type": school_type,
                    "source_page": page_url,
                    "download_url": "",
                    "local_path": "",
                    "status": "NO_URLS",
                    "rows": 0,
                    "error": "No CSV links found on dataset page",
                }
            )
            continue

        for url in csv_urls:
            file_name = url.rsplit("/", 1)[-1]
            local_path = RAW_OUT / school_type / file_name
            local_path.parent.mkdir(parents=True, exist_ok=True)
            try:
                download_file(url, local_path)
                raw_df = read_csv_flexible(local_path)
                proxy_df = build_proxy_table(raw_df, school_type, page_url)
                long_tables.append(proxy_df)
                manifest_rows.append(
                    {
                        "school_type": school_type,
                        "source_page": page_url,
                        "download_url": url,
                        "local_path": str(local_path.relative_to(ROOT)),
                        "status": "OK",
                        "rows": int(len(proxy_df)),
                        "error": "",
                    }
                )
                print(f"Downloaded {school_type}: {file_name} ({len(proxy_df):,} rows)")
            except Exception as exc:
                manifest_rows.append(
                    {
                        "school_type": school_type,
                        "source_page": page_url,
                        "download_url": url,
                        "local_path": str(local_path.relative_to(ROOT)),
                        "status": "ERROR",
                        "rows": 0,
                        "error": str(exc),
                    }
                )
                print(f"ERROR {school_type} {file_name}: {exc}")

    manifest_df = pd.DataFrame(manifest_rows)
    manifest_path = PROCESSED_OUT / "snv_esiti_manifest.csv"
    manifest_df.to_csv(manifest_path, index=False, encoding="utf-8")

    if not long_tables:
        raise RuntimeError("No SNV Esiti tables were downloaded successfully")

    long_df = pd.concat(long_tables, ignore_index=True)
    long_path = PROCESSED_OUT / "snv_esiti_school_long.csv"
    long_df.to_csv(long_path, index=False, encoding="utf-8")

    summary_df = summarize_proxy_table(long_df)
    summary_path = PROCESSED_OUT / "snv_esiti_school_year_proxy.csv"
    summary_df.to_csv(summary_path, index=False, encoding="utf-8")

    print(f"Saved raw files under: {RAW_OUT}")
    print(f"Processed long table: {long_path}")
    print(f"Processed summary: {summary_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()