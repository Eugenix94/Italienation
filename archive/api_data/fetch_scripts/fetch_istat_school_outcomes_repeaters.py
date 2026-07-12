"""Fetch ISTAT upper-secondary repeaters and build bocciatura proxy outputs.

This script targets official ISTAT SDMX flow:
- 52_1044_DF_DCIS_SCUOLE_15 (Secondaria II grado - ripetenti per anno di corso)

Why this source:
- It is updated to TIME_PERIOD 2024 at run time.
- It contains territorial detail (REF_AREA) and school-track detail.
- ISTAT does not expose a direct "promossi/bocciati" variable in this flow,
  so repeaters are used as an official proxy for school failure pressure.

Outputs:
- local_data/ISTAT/school_outcomes/istat_repeaters_upper_secondary_long.csv
- local_data/processed/istat_repeaters_upper_secondary_latest.csv
- local_data/processed/istat_repeaters_upper_secondary_ranking.csv
- local_data/processed/istat_school_outcomes_sources_manifest.csv
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
    "User-Agent": "Mozilla/5.0 (Italienation ISTAT school outcomes fetcher)"
}

NS = {
    "m": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
    "g": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/data/generic",
    "s": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
    "c": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
}

DATAFLOW_ID = "52_1044_DF_DCIS_SCUOLE_15"
DATAFLOW_TITLE_IT = "Secondaria II grado - ripetenti per anno di corso"
INDICATORS_FLOW_ID = "52_1044_DF_DCIS_SCUOLE_13"
INDICATORS_FLOW_TITLE_IT = "Secondaria II grado - indicatori scolastici"
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
    """Return mapping: codelist_id -> {code -> italian_label}.

    Falls back to code itself if Italian label is unavailable.
    """
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


def parse_repeaters_data(data_xml: bytes) -> pd.DataFrame:
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

    if not rows:
        raise RuntimeError("No observations parsed from ISTAT repeaters flow")

    df = pd.DataFrame(rows)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")
    return df


def parse_series_key_rows(data_xml: bytes) -> pd.DataFrame:
    """Parse only series keys (no observations), useful for metadata checks."""
    root = ET.fromstring(data_xml)
    data_set = root.find(".//m:DataSet", NS)
    if data_set is None:
        raise RuntimeError("ISTAT SDMX response does not contain a DataSet")

    rows: list[dict[str, str]] = []
    for series in data_set.findall("g:Series", NS):
        series_key = series.find("g:SeriesKey", NS)
        if series_key is None:
            continue
        row: dict[str, str] = {}
        for value in series_key.findall("g:Value", NS):
            dim_id = value.attrib.get("id")
            dim_val = value.attrib.get("value")
            if dim_id:
                row[dim_id] = dim_val or ""
        if row:
            rows.append(row)
    return pd.DataFrame(rows)


def label_for_code(codelists: Dict[str, Dict[str, str]], code: str) -> str:
    for mapping in codelists.values():
        if code in mapping:
            return mapping[code]
    return code


def school_year_proxy_label(year_value: object) -> str:
    text = str(year_value).strip()
    if text.isdigit() and len(text) == 4:
        return f"{text}/{int(text) + 1}"
    return text


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
    indicators_data_url = (
        "https://esploradati.istat.it/SDMXWS/rest/data/"
        f"IT1,{INDICATORS_FLOW_ID},1.0/all"
    )
    indicators_xml = fetch_xml(indicators_data_url, timeout=240)
    dsd_xml = fetch_xml(dsd_url, timeout=240)

    raw_xml_path = RAW_OUT / "istat_repeaters_upper_secondary_raw.xml"
    raw_xml_path.write_bytes(data_xml)

    codelists = parse_codelists(dsd_xml)
    ref_area_map = codelists.get("CL_ITTER107", {})
    type_school_map = codelists.get("CL_ISCO7NOC92PISC_07", {})
    school_year_map = codelists.get("CL_ISCO7CC913PISC_03", {})
    management_map = codelists.get("CL_ISCO7CC310PISC_03", {})

    indicator_keys = parse_series_key_rows(indicators_xml)
    indicator_codes = sorted(
        code
        for code in indicator_keys.get("DATA_TYPE", pd.Series(dtype=str)).dropna().astype(str).unique()
    )
    indicator_labels = [label_for_code(codelists, code) for code in indicator_codes]
    has_direct_promossi_or_bocciati = any(
        token in " | ".join(indicator_labels).lower()
        for token in ("promoss", "ammess", "bocci", "ripeten", "respint", "insuccess")
    )

    df = parse_repeaters_data(data_xml)
    df["SOURCE"] = "ISTAT SDMX"
    df["FLOW_ID"] = DATAFLOW_ID
    df["FLOW_TITLE_IT"] = DATAFLOW_TITLE_IT
    df["REF_AREA_LABEL"] = df["REF_AREA"].map(ref_area_map).fillna(df["REF_AREA"])
    df["TYPE_SCHOOL_LABEL"] = df["TYPE_SCHOOL"].map(type_school_map).fillna(df["TYPE_SCHOOL"])
    df["SCHOOL_YEAR_LABEL"] = df["SCHOOL_YEAR"].map(school_year_map).fillna(df["SCHOOL_YEAR"])
    df["TYPE_SCHOOL_MANAGEMENT_LABEL"] = (
        df["TYPE_SCHOOL_MANAGEMENT"].map(management_map).fillna(df["TYPE_SCHOOL_MANAGEMENT"])
    )
    df["SCHOOL_YEAR_PROXY"] = df["TIME_PERIOD"].apply(school_year_proxy_label)

    long_out = RAW_OUT / "istat_repeaters_upper_secondary_long.csv"
    df.to_csv(long_out, index=False, encoding="utf-8")

    totals = df[
        (df["SEX"] == "T")
        & (df["CITIZENSHIP"] == "TOTAL")
        & (df["TYPE_SCHOOL_MANAGEMENT"] == "ALL")
        & (df["SCHOOL_YEAR"] == "ALL")
    ].copy()

    totals["TIME_PERIOD_INT"] = pd.to_numeric(totals["TIME_PERIOD"], errors="coerce")
    latest_year = int(totals["TIME_PERIOD_INT"].max())

    latest = totals[totals["TIME_PERIOD_INT"] == latest_year].copy()
    latest = latest[
        [
            "REF_AREA",
            "REF_AREA_LABEL",
            "TYPE_SCHOOL",
            "TYPE_SCHOOL_LABEL",
            "OBS_VALUE",
            "TIME_PERIOD",
            "SCHOOL_YEAR_PROXY",
            "SOURCE",
            "FLOW_ID",
            "FLOW_TITLE_IT",
        ]
    ].rename(columns={"OBS_VALUE": "repeaters"})
    latest = latest.sort_values(["TYPE_SCHOOL", "repeaters"], ascending=[True, False])

    latest_out = PROCESSED_OUT / "istat_repeaters_upper_secondary_latest.csv"
    latest.to_csv(latest_out, index=False, encoding="utf-8")

    ranking = latest[latest["TYPE_SCHOOL"] == "ALL"].copy()
    ranking = ranking[ranking["REF_AREA"] != "IT"]
    ranking["rank_repeaters"] = ranking["repeaters"].rank(method="dense", ascending=False).astype(int)
    ranking = ranking.sort_values("rank_repeaters")
    ranking_out = PROCESSED_OUT / "istat_repeaters_upper_secondary_ranking.csv"
    ranking.to_csv(ranking_out, index=False, encoding="utf-8")

    manifest = pd.DataFrame(
        [
            {
                "source": "ISTAT SDMX",
                "flow_id": DATAFLOW_ID,
                "flow_title_it": DATAFLOW_TITLE_IT,
                "endpoint": data_url,
                "min_time_period": int(totals["TIME_PERIOD_INT"].min()),
                "max_time_period": latest_year,
                "max_school_year_proxy": school_year_proxy_label(latest_year),
                "has_time_period_2025": bool((totals["TIME_PERIOD_INT"] == 2025).any()),
                "checked_indicator_flow_id": INDICATORS_FLOW_ID,
                "checked_indicator_flow_title_it": INDICATORS_FLOW_TITLE_IT,
                "indicator_data_types": " | ".join(indicator_codes),
                "indicator_data_type_labels": " | ".join(indicator_labels),
                "has_direct_promossi_or_bocciati": has_direct_promossi_or_bocciati,
                "note": "No direct promossi/bocciati variable found in checked ISTAT upper-secondary flows; repeaters used as proxy.",
            }
        ]
    )
    manifest_out = PROCESSED_OUT / "istat_school_outcomes_sources_manifest.csv"
    manifest.to_csv(manifest_out, index=False, encoding="utf-8")

    print(f"Saved raw XML: {raw_xml_path}")
    print(f"Saved long table: {long_out}")
    print(f"Saved latest table: {latest_out}")
    print(f"Saved ranking table: {ranking_out}")
    print(f"Saved source manifest: {manifest_out}")
    print(f"Latest TIME_PERIOD: {latest_year} -> proxy school year {school_year_proxy_label(latest_year)}")


if __name__ == "__main__":
    main()
