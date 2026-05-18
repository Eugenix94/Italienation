"""Fetch official higher-education labour-transition sources for notebook analysis.

This script targets a compact set of datasets that are directly useful for
analysing the transition from higher education into employment and for
contrasting NEET vs EET dynamics after completion of studies.

Outputs:
- local_data/ISTAT/graduate_transitions/*.csv
- local_data/ISTAT/graduate_transitions/raw/*.xml
- local_data/eurostat/estat_young_not_in_edu_employment_by_education_years_since_completion.csv
- local_data/ISTAT/graduate_transitions/manifest.json
"""

from __future__ import annotations

import json
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[2]
ISTAT_OUT = ROOT / "local_data" / "ISTAT" / "graduate_transitions"
ISTAT_RAW_OUT = ISTAT_OUT / "raw"
EUROSTAT_OUT = ROOT / "local_data" / "eurostat"

HEADERS = {
    "User-Agent": "Italienation-Research/1.0 (academic data collection)",
    "Accept": "*/*",
}

NS = {
    "m": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
    "g": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
    "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
}

ISTAT_DATASETS = [
    {
        "flow_id": "612_937_DF_DCCV_LAU_RIC_1",
        "dsd_id": "DCCV_LAU_RIC",
        "dsd_version": "1.0",
        "filename": "istat_university_graduates_job_search.csv",
        "description": "Job search in Italy or abroad (employed or not)",
    },
    {
        "flow_id": "612_939_DF_DCCV_LAU_OCCUP_RED_1",
        "dsd_id": "DCCV_LAU_OCCUP_RED",
        "dsd_version": "1.0",
        "filename": "istat_university_graduates_occupational_condition.csv",
        "description": "Degree group and occupational condition",
    },
    {
        "flow_id": "612_939_DF_DCCV_LAU_OCCUP_RED_2",
        "dsd_id": "DCCV_LAU_OCCUP_RED",
        "dsd_version": "1.0",
        "filename": "istat_university_graduates_profession_group.csv",
        "description": "Degree group and profession group",
    },
    {
        "flow_id": "612_939_DF_DCCV_LAU_OCCUP_RED_3",
        "dsd_id": "DCCV_LAU_OCCUP_RED",
        "dsd_version": "1.0",
        "filename": "istat_university_graduates_monthly_income.csv",
        "description": "Degree group and monthly income",
    },
    {
        "flow_id": "6_471_DF_DCSP_LACIS_13",
        "dsd_id": "DCSP_LACIS",
        "dsd_version": "1.0",
        "filename": "istat_tertiary_degree_employees_by_nace2.csv",
        "description": "Employees with a tertiary degree and economic activities (Nace 2 digit)",
    },
]

EUROSTAT_DATASETS = [
    {
        "flow_id": "EDAT_LFSE_24",
        "filename": "estat_young_not_in_edu_employment_by_education_years_since_completion.csv",
        "description": "Employment rates of young persons not in education and training by educational attainment and years since completion",
        "params": {
            "format": "SDMX-CSV",
            "startPeriod": "2005",
            "geo": "IT",
        },
    }
]


def ensure_dirs() -> None:
    ISTAT_OUT.mkdir(parents=True, exist_ok=True)
    ISTAT_RAW_OUT.mkdir(parents=True, exist_ok=True)
    EUROSTAT_OUT.mkdir(parents=True, exist_ok=True)


def fetch_bytes(url: str, timeout: int = 180) -> tuple[bytes, str | None]:
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.content, response.headers.get("content-type")


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


def fetch_istat_dataset(spec: dict[str, str]) -> dict[str, object]:
    out_path = ISTAT_OUT / spec["filename"]
    raw_path = ISTAT_RAW_OUT / spec["filename"].replace(".csv", ".xml")

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

    data_url = f"https://esploradati.istat.it/SDMXWS/rest/data/IT1,{spec['flow_id']},1.0/all"
    dsd_url = (
        "https://esploradati.istat.it/SDMXWS/rest/datastructure/"
        f"IT1/{spec['dsd_id']}/{spec['dsd_version']}?references=all"
    )

    data_xml, content_type = fetch_bytes(data_url, timeout=240)
    dsd_xml, _ = fetch_bytes(dsd_url, timeout=240)
    raw_path.write_bytes(data_xml)

    codelists = parse_codelists(dsd_xml)
    lookup = build_code_label_lookup(codelists)
    df = parse_generic_data(data_xml)
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
        "rows": int(len(df)),
        "columns": list(df.columns),
    }


def fetch_eurostat_dataset(spec: dict[str, object]) -> dict[str, object]:
    out_path = EUROSTAT_OUT / spec["filename"]
    if out_path.exists():
        df = pd.read_csv(out_path)
        return {
            "source": "Eurostat",
            "flow_id": spec["flow_id"],
            "description": spec["description"],
            "status": "skipped",
            "path": str(out_path),
            "rows": int(len(df)),
            "columns": list(df.columns),
        }

    response = requests.get(
        f"https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{spec['flow_id']}",
        params=spec["params"],
        headers=HEADERS,
        timeout=180,
    )
    response.raise_for_status()
    out_path.write_text(response.text, encoding="utf-8")
    df = pd.read_csv(out_path)
    return {
        "source": "Eurostat",
        "flow_id": spec["flow_id"],
        "description": spec["description"],
        "status": "ok",
        "path": str(out_path),
        "content_type": response.headers.get("content-type"),
        "rows": int(len(df)),
        "columns": list(df.columns),
    }


def main() -> None:
    ensure_dirs()
    manifest: list[dict[str, object]] = []

    print(f"Saving graduate transition sources to {ISTAT_OUT}")
    for spec in ISTAT_DATASETS:
        print(f"  [istat] {spec['flow_id']} — {spec['description']}")
        manifest.append(fetch_istat_dataset(spec))
        time.sleep(1.0)

    for spec in EUROSTAT_DATASETS:
        print(f"  [eurostat] {spec['flow_id']} — {spec['description']}")
        manifest.append(fetch_eurostat_dataset(spec))
        time.sleep(1.0)

    manifest_path = ISTAT_OUT / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nManifest written to {manifest_path}")
    print(f"Datasets saved: {sum(1 for item in manifest if item['status'] in {'ok', 'skipped'})}")


if __name__ == "__main__":
    main()