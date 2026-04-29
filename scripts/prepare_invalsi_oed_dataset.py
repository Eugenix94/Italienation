from __future__ import annotations

from pathlib import Path
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INVALSI_DIR = ROOT / "local_data" / "INVALSI"
ISTAT_NEET = ROOT / "local_data" / "ISTAT" / "istat_neet_new.csv"
OUT_DIR = ROOT / "local_data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_MAIN = OUT_DIR / "italy_oed_triangle_dataset.csv"
OUT_COMPONENTS = OUT_DIR / "italy_oed_components_by_file.csv"


def read_csv_robust(path: Path, sep: str = ";", dtype: type | str = str) -> pd.DataFrame:
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            return pd.read_csv(path, sep=sep, dtype=dtype, encoding=enc)
        except UnicodeDecodeError:
            continue
    return pd.read_csv(path, sep=sep, dtype=dtype)


def parse_school_year_to_numeric(year_label: str) -> int | None:
    s = str(year_label)
    m_full = re.search(r"(20\d{2})-(20\d{2})", s)
    if m_full:
        return int(m_full.group(2))

    m_short = re.search(r"(20\d{2})-(\d{2})", s)
    if m_short:
        start_year = int(m_short.group(1))
        end_two = int(m_short.group(2))
        century = (start_year // 100) * 100
        return century + end_two

    return None


def safe_to_float(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.replace(" ", "", regex=False)
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
        .astype(float)
    )


def extract_origin_component() -> pd.DataFrame:
    files = sorted(INVALSI_DIR.glob("*wle_genere_origine_qescs*ms202*.csv"))
    parts: list[pd.DataFrame] = []

    for path in files:
        df = read_csv_robust(path, sep=";", dtype=str)
        required = ["Anno_new", "WLE_ESCS_Q01", "WLE_ESCS_Q04", "MATERIA", "GRADO"]
        if not all(c in df.columns for c in required):
            continue

        tmp = df[required].copy()
        tmp["year"] = tmp["Anno_new"].apply(parse_school_year_to_numeric)
        tmp["q1"] = safe_to_float(tmp["WLE_ESCS_Q01"])
        tmp["q4"] = safe_to_float(tmp["WLE_ESCS_Q04"])
        tmp["origin_qescs_gap"] = tmp["q4"] - tmp["q1"]
        tmp["component"] = "origin"
        tmp["source_file"] = path.name
        parts.append(tmp[["year", "MATERIA", "GRADO", "origin_qescs_gap", "component", "source_file"]])

    if not parts:
        return pd.DataFrame(columns=["year", "origin_qescs_gap"])

    all_df = pd.concat(parts, ignore_index=True)
    grouped = (
        all_df.dropna(subset=["year", "origin_qescs_gap"])
        .groupby("year", as_index=False)["origin_qescs_gap"]
        .mean()
    )
    return grouped


def extract_education_component() -> pd.DataFrame:
    files = sorted(INVALSI_DIR.glob("*livelli*ms202*.csv"))
    parts: list[pd.DataFrame] = []

    for path in files:
        df = read_csv_robust(path, sep=";", dtype=str)
        year_col = None
        if "Anno_scolastico" in df.columns:
            year_col = "Anno_scolastico"
        elif "Anno_new" in df.columns:
            year_col = "Anno_new"

        if year_col is None:
            continue

        level_cols = [c for c in df.columns if c.upper().startswith("LIVELLO")]
        if not level_cols:
            continue

        tmp = df.copy()
        tmp["year"] = tmp[year_col].apply(parse_school_year_to_numeric)
        for c in level_cols:
            tmp[c] = safe_to_float(tmp[c])

        l1 = "LIVELLO_1" if "LIVELLO_1" in tmp.columns else ("LIVELLO1" if "LIVELLO1" in tmp.columns else None)
        l3 = "LIVELLO_3" if "LIVELLO_3" in tmp.columns else ("LIVELLO3" if "LIVELLO3" in tmp.columns else None)
        l4 = "LIVELLO_4" if "LIVELLO_4" in tmp.columns else ("LIVELLO4" if "LIVELLO4" in tmp.columns else None)
        l5 = "LIVELLO_5" if "LIVELLO_5" in tmp.columns else ("LIVELLO5" if "LIVELLO5" in tmp.columns else None)

        if l4 and l5:
            tmp["high_share"] = tmp[[l4, l5]].sum(axis=1, min_count=1)
            tmp["low_share"] = tmp[l1] if l1 else pd.NA
        elif l3:
            tmp["high_share"] = tmp[l3]
            tmp["low_share"] = tmp[l1] if l1 else pd.NA
        else:
            continue

        tmp["education_advantage"] = tmp["high_share"] - tmp["low_share"]
        tmp["source_file"] = path.name
        parts.append(tmp[["year", "education_advantage", "source_file"]])

    if not parts:
        return pd.DataFrame(columns=["year", "education_advantage"])

    all_df = pd.concat(parts, ignore_index=True)
    grouped = (
        all_df.dropna(subset=["year", "education_advantage"])
        .groupby("year", as_index=False)["education_advantage"]
        .mean()
    )
    return grouped


def extract_destination_component() -> pd.DataFrame:
    disp_files = sorted(INVALSI_DIR.glob("*report_generale_unito_dispersione_e_eccellenti*2025.csv"))
    frames: list[pd.DataFrame] = []

    for path in disp_files:
        df = read_csv_robust(path, sep=";", dtype=str)
        required = ["anno", "Pct_dispersione"]
        if not all(c in df.columns for c in required):
            continue

        tmp = df.copy()
        tmp["year"] = tmp["anno"].apply(parse_school_year_to_numeric)
        tmp["destination_dispersion"] = safe_to_float(tmp["Pct_dispersione"])
        frames.append(tmp[["year", "destination_dispersion"]])

    if frames:
        all_df = pd.concat(frames, ignore_index=True)
        grouped = (
            all_df.dropna(subset=["year", "destination_dispersion"])
            .groupby("year", as_index=False)["destination_dispersion"]
            .mean()
        )
        return grouped

    return pd.DataFrame(columns=["year", "destination_dispersion"])


def minmax(s: pd.Series, invert: bool = False) -> pd.Series:
    s = s.astype(float)
    lo = s.min()
    hi = s.max()
    if pd.isna(lo) or pd.isna(hi) or hi == lo:
        norm = pd.Series([0.5] * len(s), index=s.index)
    else:
        norm = (s - lo) / (hi - lo)
    if invert:
        norm = 1 - norm
    return norm


def build_oed_table() -> tuple[pd.DataFrame, pd.DataFrame]:
    origin = extract_origin_component()
    education = extract_education_component()
    destination = extract_destination_component()

    merged = origin.merge(education, on="year", how="outer").merge(destination, on="year", how="outer")
    merged = merged.sort_values("year").dropna(subset=["year"]) 

    # Keep recent years only for current-policy analysis.
    merged = merged[merged["year"] >= 2023].copy()

    merged["O_raw_origin"] = merged["origin_qescs_gap"]
    merged["E_raw_education"] = merged["education_advantage"]
    merged["D_raw_destination"] = merged["destination_dispersion"]

    # O: more origin-based gap -> weaker mobility, so invert
    merged["O"] = minmax(merged["O_raw_origin"], invert=True)
    merged["E"] = minmax(merged["E_raw_education"], invert=False)
    # D: higher dispersion means worse destination inclusion, so invert
    merged["D"] = minmax(merged["D_raw_destination"], invert=True)

    total = merged[["O", "E", "D"]].sum(axis=1)
    merged["O_share"] = merged["O"] / total
    merged["E_share"] = merged["E"] / total
    merged["D_share"] = merged["D"] / total

    components = pd.DataFrame(
        {
            "component": ["O", "E", "D"],
            "proxy": [
                "Inverse ESCS Q4-Q1 WLE gap",
                "High-level minus low-level proficiency share",
                "Inverse implicit school dispersion rate",
            ],
            "note": [
                "Higher means weaker origin penalty",
                "Higher means stronger educational performance",
                "Higher means better destination inclusion",
            ],
        }
    )

    return merged, components


def main() -> None:
    oed, components = build_oed_table()
    oed.to_csv(OUT_MAIN, index=False)
    components.to_csv(OUT_COMPONENTS, index=False)
    print(f"Wrote: {OUT_MAIN}")
    print(f"Rows: {len(oed)}")
    print(f"Wrote: {OUT_COMPONENTS}")


if __name__ == "__main__":
    main()
