"""Fetch official ISTAT early-childhood and nursery service datasets.

This script targets the ISTAT `DCIS_SERVSOCEDU1` dataflow family, which covers
municipal nursery provision and territorial early-childhood service indicators.

Outputs:
- local_data/ISTAT/early_childhood_services/*.csv
- local_data/ISTAT/early_childhood_services/raw/*.xml
- local_data/ISTAT/early_childhood_services/manifest.json
"""

from __future__ import annotations

import json
import xml.etree.ElementTree as ET
from io import BytesIO
from pathlib import Path

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "local_data" / "ISTAT" / "early_childhood_services"
RAW_DIR = OUT_DIR / "raw"

ISTAT_BASE_URLS = [
    "https://esploradati.istat.it/SDMXWS/rest",
    "https://sdmx.istat.it/SDMXWS/rest",
]

HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
    "Accept": "*/*",
}
HEADERS_CSV = {
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
    "Accept": "application/vnd.sdmx.data+csv;version=1.0.0, text/csv, */*",
}

NS = {
    "m": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
    "g": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
    "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
}

DATASETS = [
    {
        "flow_id": "47_850_DF_DCIS_SERVSOCEDU1_1",
        "filename": "istat_early_childhood_indicators_provinces.csv",
        "description": "Early-childhood service indicators by province",
    },
    {
        "flow_id": "47_850_DF_DCIS_SERVSOCEDU1_2",
        "filename": "istat_early_childhood_services_regions.csv",
        "description": "Services provided by municipalities by region",
    },
    {
        "flow_id": "47_850_DF_DCIS_SERVSOCEDU1_3",
        "filename": "istat_early_childhood_services_provinces_municipalities.csv",
        "description": "Services provided by municipalities by province and municipality",
    },
    {
        "flow_id": "47_850_DF_DCIS_SERVSOCEDU1_5",
        "filename": "istat_early_childhood_territorial_services_regions.csv",
        "description": "Territorial early-childhood services by region",
    },
    {
        "flow_id": "47_850_DF_DCIS_SERVSOCEDU1_6",
        "filename": "istat_early_childhood_territorial_services_provinces_municipalities.csv",
        "description": "Territorial early-childhood services by province and municipality",
    },
]


def ensure_dirs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)


def fetch_bytes(url: str, timeout: int = 240, headers: dict[str, str] | None = None) -> tuple[bytes, str | None]:
    headers = headers or HEADERS
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.content, response.headers.get("content-type")


def fetch_from_istat(path: str, timeout: int = 240, headers: dict[str, str] | None = None) -> tuple[bytes, str | None, str]:
    last_error: Exception | None = None
    for base_url in ISTAT_BASE_URLS:
        try:
            content, content_type = fetch_bytes(f"{base_url}{path}", timeout=timeout, headers=headers)
            return content, content_type, base_url
        except requests.RequestException as exc:
            last_error = exc
    if last_error is None:
        raise RuntimeError(f"Unable to fetch ISTAT resource for path: {path}")
    raise last_error


def parse_codelists(dsd_xml: bytes) -> dict[str, dict[str, str]]:
    root = ET.fromstring(dsd_xml)
    codelists: dict[str, dict[str, str]] = {}
    for codelist in root.findall(".//s:Codelist", NS):
        codelist_id = codelist.attrib.get("id", "")
        if not codelist_id:
            continue
        mapping: dict[str, str] = {}
        for code in codelist.findall("s:Code", NS):
            code_id = code.attrib.get("id", "")
            if not code_id:
                continue
            label = ""
            for name in code.findall("c:Name", NS):
                lang = name.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
                text = (name.text or "").strip()
                if lang == "en" and text:
                    label = text
                    break
                if not label and text:
                    label = text
            mapping[code_id] = label or code_id
        codelists[codelist_id] = mapping
    return codelists


def parse_sdmx_csv(data_bytes: bytes) -> pd.DataFrame:
    df = pd.read_csv(BytesIO(data_bytes), dtype=str)
    if df.empty:
        raise RuntimeError("ISTAT SDMX CSV response is empty")
    df.columns = [column.lower() for column in df.columns]
    if "obs_value" in df.columns:
        df["obs_value"] = pd.to_numeric(df["obs_value"], errors="coerce")
        df = df.dropna(subset=["obs_value"])
    if "time_period" in df.columns:
        df["year"] = pd.to_numeric(df["time_period"].astype(str).str[:4], errors="coerce")
    return df


def build_code_label_lookup(codelists: dict[str, dict[str, str]]) -> dict[str, str]:
    lookup: dict[str, str] = {}
    for mapping in codelists.values():
        for code, label in mapping.items():
            lookup.setdefault(code, label)
    return lookup


def parse_generic_data(data_xml: bytes) -> pd.DataFrame:
    root = ET.fromstring(data_xml)
    data_set = root.find(".//m:DataSet", NS)
    if data_set is None:
        raise RuntimeError("ISTAT SDMX response does not contain a DataSet")

    rows: list[dict[str, object]] = []
    for series in data_set.findall("g:Series", NS):
        key_values: dict[str, str] = {}
        series_key = series.find("g:SeriesKey", NS)
        if series_key is not None:
            for value in series_key.findall("g:Value", NS):
                dim_id = value.attrib.get("id")
                dim_val = value.attrib.get("value")
                if dim_id:
                    key_values[dim_id] = dim_val or ""

        for obs in series.findall("g:Obs", NS):
            obs_dim = obs.find("g:ObsDimension", NS)
            obs_value = obs.find("g:ObsValue", NS)
            if obs_dim is None or obs_value is None:
                continue
            row = dict(key_values)
            row["TIME_PERIOD"] = obs_dim.attrib.get("value", "")
            row["OBS_VALUE"] = obs_value.attrib.get("value", "")
            rows.append(row)

    if not rows:
        raise RuntimeError("No observations parsed from ISTAT response")

    df = pd.DataFrame(rows)
    df.columns = [column.lower() for column in df.columns]
    df["obs_value"] = pd.to_numeric(df["obs_value"], errors="coerce")
    df = df.dropna(subset=["obs_value"]).reset_index(drop=True)
    if "time_period" in df.columns:
        df["year"] = pd.to_numeric(df["time_period"].astype(str).str[:4], errors="coerce")
    return df


def add_label_columns(df: pd.DataFrame, lookup: dict[str, str]) -> pd.DataFrame:
    for column in df.columns:
        if column in {"time_period", "obs_value", "year", "source", "flow_id", "description"}:
            continue
        if not pd.api.types.is_object_dtype(df[column]):
            continue
        labeled = df[column].map(lookup).fillna(df[column])
        if (labeled != df[column]).any():
            df[f"{column}_label"] = labeled
    return df


def fetch_dataset(spec: dict[str, str], lookup: dict[str, str]) -> dict[str, object]:
    out_path = OUT_DIR / spec["filename"]
    raw_path = RAW_DIR / spec["filename"].replace(".csv", ".raw")

    if out_path.exists() and raw_path.exists():
        df = pd.read_csv(out_path)
        return {
            "source": "ISTAT",
            "flow_id": spec["flow_id"],
            "description": spec["description"],
            "status": "skipped",
            "path": str(out_path),
            "rows": int(len(df)),
            "columns": list(df.columns),
        }

    data_path_csv = f"/data/IT1,{spec['flow_id']},1.0/all?format=SDMX-CSV"
    try:
        data_bytes, content_type, base_url = fetch_from_istat(data_path_csv, headers=HEADERS_CSV)
        df = parse_sdmx_csv(data_bytes)
        raw_path.write_bytes(data_bytes)
        print(f"    [api] CSV fetch succeeded for {spec['flow_id']}")
    except Exception as csv_exc:
        print(f"    [warn] CSV API fetch failed for {spec['flow_id']}: {csv_exc}")
        data_path_xml = f"/data/IT1,{spec['flow_id']},1.0/all"
        data_bytes, content_type, base_url = fetch_from_istat(data_path_xml, headers=HEADERS)
        raw_path.write_bytes(data_bytes)
        df = parse_generic_data(data_bytes)

    df["source"] = "ISTAT SDMX"
    df["flow_id"] = spec["flow_id"]
    df["description"] = spec["description"]
    df = add_label_columns(df, lookup)
    df.to_csv(out_path, index=False, encoding="utf-8")

    return {
        "source": "ISTAT",
        "flow_id": spec["flow_id"],
        "description": spec["description"],
        "status": "ok",
        "path": str(out_path),
        "raw_path": str(raw_path),
        "content_type": content_type,
        "base_url": base_url,
        "rows": int(len(df)),
        "columns": list(df.columns),
    }


def main() -> None:
    ensure_dirs()

    dsd_path = RAW_DIR / "DCIS_SERVSOCEDU1_datastructure.xml"
    lookup: dict[str, str] = {}
    if dsd_path.exists():
        dsd_xml = dsd_path.read_bytes()
        codelists = parse_codelists(dsd_xml)
        lookup = build_code_label_lookup(codelists)
    else:
        dsd_path_suffix = "/datastructure/IT1/DCIS_SERVSOCEDU1/1.0?references=all"
        try:
            dsd_xml, _, _ = fetch_from_istat(dsd_path_suffix)
            dsd_path.write_bytes(dsd_xml)
            codelists = parse_codelists(dsd_xml)
            lookup = build_code_label_lookup(codelists)
        except requests.RequestException as exc:
            print(f"[warn] Unable to fetch DSD for DCIS_SERVSOCEDU1; continuing without labels: {exc}")

    manifest = []
    print(f"Saving ISTAT early-childhood service datasets to {OUT_DIR}")
    for spec in DATASETS:
        print(f"  [fetch] {spec['flow_id']} - {spec['description']}")
        try:
            item = fetch_dataset(spec, lookup)
            print(f"    [{item['status']}] {item.get('rows', 0):,} rows")
        except requests.RequestException as exc:
            item = {
                "source": "ISTAT",
                "flow_id": spec["flow_id"],
                "description": spec["description"],
                "status": "error",
                "error": str(exc),
            }
            print(f"    [error] {exc}")
        manifest.append(item)

    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nManifest written to {manifest_path}")


if __name__ == "__main__":
    main()