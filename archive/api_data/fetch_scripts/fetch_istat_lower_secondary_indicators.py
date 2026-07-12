"""Fetch ISTAT lower-secondary indicators and derive a middle-school exam-failure proxy.

This script targets official ISTAT SDMX flow:
- 52_1044_DF_DCIS_SCUOLE_10 (Secondaria I grado - indicatori scolastici)

What this source provides:
- Updated yearly territorial indicators for lower secondary school.
- No direct repeaters flow is exposed for lower secondary.
- The closest outcome signal is `EXAM` = licenziati per 100 esaminati.

Derived proxy:
- failure_at_exam_proxy = 100 - exam_pass_rate

Outputs:
- local_data/ISTAT/school_outcomes/istat_lower_secondary_indicators_long.csv
- local_data/processed/istat_lower_secondary_indicators_latest.csv
- local_data/processed/istat_lower_secondary_exam_proxy_latest.csv
- local_data/processed/istat_lower_secondary_sources_manifest.csv
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict

import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[2]
RAW_OUT = ROOT / "local_data" / "ISTAT" / "school_outcomes"
PROCESSED_OUT = ROOT / "local_data" / "processed"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Italienation ISTAT lower-secondary fetcher)"
}

NS = {
    "m": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
    "g": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
    "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
}

DATAFLOW_ID = "52_1044_DF_DCIS_SCUOLE_10"
DATAFLOW_TITLE_IT = "Secondaria I grado - indicatori scolastici"
DSD_ID = "DCIS_SCUOLE"
DSD_VERSION = "1.0"


def ensure_dirs() -> None:
    RAW_OUT.mkdir(parents=True, exist_ok=True)
    PROCESSED_OUT.mkdir(parents=True, exist_ok=True)


def fetch_xml(url: str, timeout: int = 180) -> bytes:
    response = requests.get(url, headers=HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.content


def parse_codelists(dsd_xml: bytes) -> Dict[str, Dict[str, str]]:
    root = ET.fromstring(dsd_xml)
    codelists: Dict[str, Dict[str, str]] = {}
    for codelist in root.findall(".//s:Codelist", NS):
        cl_id = codelist.attrib.get("id", "")
        if not cl_id:
            continue
        code_map: Dict[str, str] = {}
        for code in codelist.findall("s:Code", NS):
            code_id = code.attrib.get("id", "")
            if not code_id:
                continue
            label = ""
            for name in code.findall("c:Name", NS):
                lang = name.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
                if lang == "it" and (name.text or "").strip():
                    label = (name.text or "").strip()
                    break
            code_map[code_id] = label or code_id
        codelists[cl_id] = code_map
    return codelists


def label_for_code(codelists: Dict[str, Dict[str, str]], code: str) -> str:
    for mapping in codelists.values():
        if code in mapping:
            return mapping[code]
    return code


def parse_data(data_xml: bytes) -> pd.DataFrame:
    root = ET.fromstring(data_xml)
    data_set = root.find(".//m:DataSet", NS)
    if data_set is None:
        raise RuntimeError("ISTAT SDMX response does not contain a DataSet")

    rows: list[dict[str, object]] = []
    for series in data_set.findall("g:Series", NS):
        series_key = series.find("g:SeriesKey", NS)
        key_values: dict[str, str] = {}
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

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("No observations parsed from ISTAT lower-secondary indicators flow")
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
    df["TIME_PERIOD"] = pd.to_numeric(df["TIME_PERIOD"], errors="coerce")
    return df


def school_year_proxy_label(year_value: object) -> str:
    text = str(int(year_value)) if pd.notna(year_value) else ""
    if text.isdigit() and len(text) == 4:
        return f"{text}/{int(text) + 1}"
    return str(year_value)


def main() -> None:
    ensure_dirs()

    data_url = (
        "https://esploradati.istat.it/SDMXWS/rest/data/"
        f"IT1,{DATAFLOW_ID},1.0/all"
    )
    dsd_url = (
        "https://esploradati.istat.it/SDMXWS/rest/datastructure/"
        f"IT1/{DSD_ID}/{DSD_VERSION}?references=all"
    )

    data_xml = fetch_xml(data_url, timeout=240)
    dsd_xml = fetch_xml(dsd_url, timeout=240)

    raw_xml_path = RAW_OUT / "istat_lower_secondary_indicators_raw.xml"
    raw_xml_path.write_bytes(data_xml)

    codelists = parse_codelists(dsd_xml)
    ref_area_map = codelists.get("CL_ITTER107", {})
    management_map = codelists.get("CL_ISCO7CC310PISC_03", {})

    df = parse_data(data_xml)
    df["SOURCE"] = "ISTAT SDMX"
    df["FLOW_ID"] = DATAFLOW_ID
    df["FLOW_TITLE_IT"] = DATAFLOW_TITLE_IT
    df["REF_AREA_LABEL"] = df["REF_AREA"].map(ref_area_map).fillna(df["REF_AREA"])
    df["TYPE_SCHOOL_MANAGEMENT_LABEL"] = (
        df["TYPE_SCHOOL_MANAGEMENT"].map(management_map).fillna(df["TYPE_SCHOOL_MANAGEMENT"])
    )
    df["DATA_TYPE_LABEL"] = df["DATA_TYPE"].apply(lambda code: label_for_code(codelists, code))
    df["SCHOOL_LEVEL_LABEL"] = df["SCHOOL_LEVEL"].apply(lambda code: label_for_code(codelists, code))
    df["SCHOOL_YEAR_PROXY"] = df["TIME_PERIOD"].apply(school_year_proxy_label)
    df["failure_at_exam_proxy"] = pd.NA
    exam_mask = df["DATA_TYPE"] == "EXAM"
    df.loc[exam_mask, "failure_at_exam_proxy"] = 100 - df.loc[exam_mask, "OBS_VALUE"]

    long_out = RAW_OUT / "istat_lower_secondary_indicators_long.csv"
    df.to_csv(long_out, index=False, encoding="utf-8")

    latest_year = int(df["TIME_PERIOD"].max())
    latest = df[df["TIME_PERIOD"] == latest_year].copy()
    latest = latest[
        [
            "REF_AREA",
            "REF_AREA_LABEL",
            "DATA_TYPE",
            "DATA_TYPE_LABEL",
            "TYPE_SCHOOL_MANAGEMENT",
            "TYPE_SCHOOL_MANAGEMENT_LABEL",
            "OBS_VALUE",
            "failure_at_exam_proxy",
            "TIME_PERIOD",
            "SCHOOL_YEAR_PROXY",
            "SOURCE",
            "FLOW_ID",
            "FLOW_TITLE_IT",
        ]
    ].sort_values(["DATA_TYPE", "TYPE_SCHOOL_MANAGEMENT", "OBS_VALUE"], ascending=[True, True, False])
    latest_out = PROCESSED_OUT / "istat_lower_secondary_indicators_latest.csv"
    latest.to_csv(latest_out, index=False, encoding="utf-8")

    exam_proxy_latest = latest[
        (latest["DATA_TYPE"] == "EXAM")
        & (latest["TYPE_SCHOOL_MANAGEMENT"] == "ALL")
        & (latest["REF_AREA"] != "IT")
    ].copy()
    exam_proxy_latest = exam_proxy_latest.sort_values("failure_at_exam_proxy", ascending=False)
    exam_proxy_latest["rank_failure_proxy"] = (
        exam_proxy_latest["failure_at_exam_proxy"].rank(method="dense", ascending=False).astype(int)
    )
    exam_proxy_out = PROCESSED_OUT / "istat_lower_secondary_exam_proxy_latest.csv"
    exam_proxy_latest.to_csv(exam_proxy_out, index=False, encoding="utf-8")

    national_latest = latest[
        (latest["REF_AREA"] == "IT")
        & (latest["TYPE_SCHOOL_MANAGEMENT"] == "ALL")
    ].copy()

    manifest = pd.DataFrame(
        [
            {
                "source": "ISTAT SDMX",
                "flow_id": DATAFLOW_ID,
                "flow_title_it": DATAFLOW_TITLE_IT,
                "endpoint": data_url,
                "min_time_period": int(df["TIME_PERIOD"].min()),
                "max_time_period": latest_year,
                "max_school_year_proxy": school_year_proxy_label(latest_year),
                "has_direct_repeaters_flow": False,
                "exam_indicator_code": "EXAM",
                "exam_indicator_label": national_latest.loc[national_latest["DATA_TYPE"] == "EXAM", "DATA_TYPE_LABEL"].iloc[0],
                "derived_failure_proxy": "100 - licenziati per 100 esaminati",
                "indicator_data_types": " | ".join(sorted(df["DATA_TYPE"].dropna().astype(str).unique())),
                "indicator_data_type_labels": " | ".join(sorted(df["DATA_TYPE_LABEL"].dropna().astype(str).unique())),
                "note": "ISTAT does not expose a direct lower-secondary repeaters flow here; exam-failure proxy derived from EXAM indicator.",
            }
        ]
    )
    manifest_out = PROCESSED_OUT / "istat_lower_secondary_sources_manifest.csv"
    manifest.to_csv(manifest_out, index=False, encoding="utf-8")

    print(f"Saved raw XML: {raw_xml_path}")
    print(f"Saved long table: {long_out}")
    print(f"Saved latest indicators: {latest_out}")
    print(f"Saved exam proxy latest: {exam_proxy_out}")
    print(f"Saved source manifest: {manifest_out}")
    print(f"Latest TIME_PERIOD: {latest_year} -> proxy school year {school_year_proxy_label(latest_year)}")


if __name__ == "__main__":
    main()