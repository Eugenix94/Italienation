#!/usr/bin/env python3
"""
Build expanded NEET-derived datasets for gender dynamics, COVID shock analysis,
and a region-level predictive panel.

Outputs are written to local_data/processed/ and are derived only from files that
already exist in the repository:
  - local_data/ISTAT/istat_neet_new.csv
  - local_data/NEET ... Dati regionali ...csv
  - local_data/processed/transition_bridge_model_panel.csv

The regional target is a size-normalized proxy: a within-year risk index based on
regional NEET counts for ages 15-29. This keeps the model useful even when the
raw source exposes counts rather than a population share.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
LOCAL_DATA = ROOT / "local_data"
OUTPUT_DIR = LOCAL_DATA / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def read_csv_smart(path: Path) -> pd.DataFrame:
    """Read a CSV with a small set of separator/encoding fallbacks."""

    encodings = ["utf-8", "utf-8-sig", "cp1252", "latin-1"]
    separators = [",", ";", "\t"]
    for encoding in encodings:
        for separator in separators:
            try:
                frame = pd.read_csv(path, encoding=encoding, sep=separator, low_memory=False)
                if frame.shape[1] > 1:
                    return frame
            except Exception:
                continue

    return pd.read_csv(path, encoding="latin-1", sep=None, engine="python", low_memory=False)


def to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def normalize_columns(frame: pd.DataFrame) -> pd.DataFrame:
    frame = frame.copy()
    frame.columns = [str(col).strip() for col in frame.columns]
    return frame


def period_label(year: int) -> str:
    if year <= 2019:
        return "pre_covid"
    if year <= 2021:
        return "covid_shock"
    return "recovery"


def safe_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denominator = denominator.replace(0, np.nan)
    return numerator / denominator


def build_gender_panel() -> dict[str, pd.DataFrame]:
    source_path = LOCAL_DATA / "ISTAT" / "istat_neet_new.csv"
    if not source_path.exists():
        raise FileNotFoundError(f"Missing source file: {source_path}")

    df = normalize_columns(read_csv_smart(source_path))

    filters = {
        "tipo_dato": {"NEET"},
        "cittadinanza": {"TOTAL"},
        "condizione_prof_eu": {"TOT"},
        "ruolo_fam": {"TOT"},
        "titolo_studio": {"99"},
    }
    for column, allowed in filters.items():
        if column in df.columns:
            df = df[df[column].astype(str).isin(allowed)].copy()

    if "obs_value" not in df.columns:
        raise KeyError("The national NEET source does not expose obs_value")

    df["obs_value"] = to_numeric(df["obs_value"])
    df["year"] = to_numeric(df["year"]).astype("Int64")
    if "sesso" in df.columns:
        df["sesso"] = df["sesso"].astype(str)
    if "classe_eta" in df.columns:
        df["classe_eta"] = df["classe_eta"].astype(str)

    sex_map = {"1": "male", "2": "female", "9": "total"}
    df["sex_label"] = df["sesso"].map(sex_map).fillna(df.get("sesso", pd.Series(dtype=str)).astype(str))

    panel = (
        df[df["sex_label"].isin(["male", "female", "total"])].copy()
        .groupby(["year", "classe_eta", "sex_label"], as_index=False)["obs_value"]
        .mean()
        .sort_values(["classe_eta", "year", "sex_label"])
    )

    pivot = panel.pivot_table(index=["year", "classe_eta"], columns="sex_label", values="obs_value")
    pivot["female_minus_male_pp"] = pivot.get("female") - pivot.get("male")
    pivot["female_to_male_ratio"] = safe_ratio(pivot.get("female"), pivot.get("male"))
    pivot = pivot.reset_index().sort_values(["classe_eta", "year"])

    yearly_total = (
        panel[panel["sex_label"] == "total"]
        .groupby("year", as_index=False)["obs_value"]
        .mean()
        .rename(columns={"obs_value": "neet_total_obs_value"})
    )

    panel_path = OUTPUT_DIR / "neet_gender_year_panel.csv"
    pivot_path = OUTPUT_DIR / "neet_gender_gap_by_year.csv"
    yearly_path = OUTPUT_DIR / "neet_gender_total_yearly.csv"
    panel.to_csv(panel_path, index=False)
    pivot.to_csv(pivot_path, index=False)
    yearly_total.to_csv(yearly_path, index=False)

    return {
        "panel": panel,
        "pivot": pivot,
        "yearly_total": yearly_total,
        "source_path": source_path,
    }


def build_covid_summary(gender_panel: pd.DataFrame) -> pd.DataFrame:
    covid = gender_panel.copy()
    covid = covid[covid["sex_label"].isin(["male", "female", "total"])].copy()
    covid["covid_period"] = covid["year"].astype(int).map(period_label)

    summary = (
        covid.groupby(["covid_period", "classe_eta", "sex_label"], as_index=False)["obs_value"]
        .mean()
        .rename(columns={"obs_value": "mean_neet_obs_value"})
    )

    baseline = summary[summary["covid_period"] == "pre_covid"].rename(
        columns={"mean_neet_obs_value": "pre_covid_mean_neet_obs_value"}
    )
    summary = summary.merge(
        baseline[["classe_eta", "sex_label", "pre_covid_mean_neet_obs_value"]],
        on=["classe_eta", "sex_label"],
        how="left",
    )
    summary["delta_vs_pre_covid_pp"] = summary["mean_neet_obs_value"] - summary["pre_covid_mean_neet_obs_value"]
    summary["pct_change_vs_pre_covid"] = safe_ratio(
        summary["delta_vs_pre_covid_pp"], summary["pre_covid_mean_neet_obs_value"]
    ) * 100.0

    summary_path = OUTPUT_DIR / "neet_covid_period_summary.csv"
    summary.sort_values(["classe_eta", "sex_label", "covid_period"]).to_csv(summary_path, index=False)
    return summary


def build_regional_model_panel() -> dict[str, pd.DataFrame | dict[str, float | list | str]]:
    regional_path = next(
        (
            path
            for path in LOCAL_DATA.glob("NEET*Dati regionali*.csv")
            if path.is_file()
        ),
        None,
    )
    bridge_path = OUTPUT_DIR / "transition_bridge_model_panel.csv"

    if regional_path is None:
        raise FileNotFoundError("Could not find the regional NEET source file")
    if not bridge_path.exists():
        raise FileNotFoundError(f"Missing bridge panel: {bridge_path}")

    df_reg = normalize_columns(read_csv_smart(regional_path))
    df_bridge = normalize_columns(read_csv_smart(bridge_path))

    df_reg["TIME_PERIOD"] = to_numeric(df_reg["TIME_PERIOD"]).astype("Int64")
    df_reg["Osservazione"] = to_numeric(df_reg["Osservazione"])
    df_reg["AGE"] = df_reg["AGE"].astype(str)
    df_reg["Territorio"] = df_reg["Territorio"].astype(str)
    df_reg["REF_AREA"] = df_reg["REF_AREA"].astype(str)

    exclusion_terms = {"italia", "nord", "centro", "sud", "isole", "mezzogiorno", "totale"}
    regional_slice = df_reg[
        (df_reg["FREQ"].astype(str) == "A")
        & (df_reg["DATA_TYPE"].astype(str).str.upper() == "NEET")
        & (df_reg["AGE"].astype(str) == "Y15-29")
        & (~df_reg["Territorio"].str.lower().isin(exclusion_terms))
    ].copy()

    regional_target = (
        regional_slice.groupby(["REF_AREA", "Territorio", "TIME_PERIOD"], as_index=False)["Osservazione"]
        .mean()
        .rename(columns={"Osservazione": "neet_count_15_29"})
        .sort_values(["TIME_PERIOD", "neet_count_15_29"], ascending=[True, False])
    )

    regional_target["neet_risk_index"] = regional_target.groupby("TIME_PERIOD")["neet_count_15_29"].transform(
        lambda s: (s - s.mean()) / (s.std(ddof=0) if s.std(ddof=0) not in (0, np.nan) else 1.0)
    )
    regional_target["neet_percentile"] = regional_target.groupby("TIME_PERIOD")["neet_count_15_29"].rank(pct=True)
    regional_target["covid_period"] = regional_target["TIME_PERIOD"].astype(int).map(period_label)

    bridge = df_bridge.copy()
    bridge["TIME_PERIOD"] = to_numeric(bridge["TIME_PERIOD"]).astype("Int64")
    bridge["REF_AREA"] = bridge["REF_AREA"].astype(str)

    panel = bridge.merge(
        regional_target[["REF_AREA", "TIME_PERIOD", "neet_count_15_29", "neet_risk_index", "neet_percentile", "covid_period"]],
        on=["REF_AREA", "TIME_PERIOD"],
        how="left",
    )

    panel_path = OUTPUT_DIR / "neet_regional_model_panel.csv"
    target_path = OUTPUT_DIR / "neet_regional_target_panel.csv"
    regional_target.to_csv(target_path, index=False)
    panel.to_csv(panel_path, index=False)

    model_result = fit_baseline_model(panel)
    return {
        "regional_target": regional_target,
        "panel": panel,
        "model_result": model_result,
        "source_path": regional_path,
    }


def fit_baseline_model(panel: pd.DataFrame) -> dict[str, object]:
    model_df = panel.copy()
    model_df = model_df[model_df["neet_risk_index"].notna()].copy()

    candidate_features = [
        "lower_disability_per_1000_t_minus_1",
        "lower_class_size_t_minus_1",
        "lower_exam_success_t_minus_1",
        "lower_foreign_share_t_minus_1",
        "lower_median_grade_t_minus_1",
        "lower_public_share_t_minus_1",
        "lower_exam_failure_t_minus_1",
        "upper_repeaters_all_t",
        "upper_repeaters_fir_t",
        "upper_lic_t",
        "upper_tec_t",
        "upper_voc_t",
        "upper_voc_minus_lic_t",
        "upper_tec_minus_lic_t",
        "transition_jump_all_t",
        "transition_jump_fir_t",
        "TIME_PERIOD",
    ]
    feature_cols = [column for column in candidate_features if column in model_df.columns]

    covid_dummies = pd.get_dummies(model_df.get("covid_period", pd.Series(index=model_df.index, dtype=str)), prefix="covid", drop_first=True)
    feature_frame = pd.concat([model_df[feature_cols], covid_dummies], axis=1)
    feature_frame = feature_frame.apply(pd.to_numeric, errors="coerce").astype(float)

    train_mask = model_df["TIME_PERIOD"].astype(int) < 2024
    test_mask = model_df["TIME_PERIOD"].astype(int) == 2024
    if train_mask.sum() < 10 or test_mask.sum() == 0:
        raise ValueError("Insufficient rows to train the baseline model")

    train_features = feature_frame.loc[train_mask].copy()
    test_features = feature_frame.loc[test_mask].copy()
    target = model_df["neet_risk_index"].astype(float)

    train_means = train_features.mean()
    train_stds = train_features.std(ddof=0).replace(0, 1).fillna(1)
    train_centered = ((train_features.fillna(train_means) - train_means) / train_stds).to_numpy(dtype=float)
    test_centered = ((test_features.fillna(train_means) - train_means) / train_stds).to_numpy(dtype=float)

    y_train = target.loc[train_mask].to_numpy(dtype=float)
    y_train_mean = float(np.nanmean(y_train))
    y_train_centered = y_train - y_train_mean

    alpha = 1.0
    identity = np.eye(train_centered.shape[1], dtype=float)
    coefficients = np.linalg.solve(train_centered.T @ train_centered + alpha * identity, train_centered.T @ y_train_centered)

    train_pred = y_train_mean + train_centered @ coefficients
    test_pred = y_train_mean + test_centered @ coefficients

    y_test = target.loc[test_mask].to_numpy(dtype=float)
    residuals = y_test - test_pred
    rmse = float(np.sqrt(np.mean(residuals**2)))
    mae = float(np.mean(np.abs(residuals)))
    ss_tot = float(np.sum((y_test - np.mean(y_test)) ** 2))
    r2 = float(1.0 - np.sum(residuals**2) / ss_tot) if ss_tot else float("nan")

    prediction_frame = model_df.loc[test_mask, ["REF_AREA", "REF_AREA_LABEL", "TIME_PERIOD", "neet_count_15_29", "neet_risk_index"]].copy()
    prediction_frame["predicted_neet_risk_index"] = test_pred
    prediction_frame["prediction_error"] = prediction_frame["neet_risk_index"] - prediction_frame["predicted_neet_risk_index"]
    prediction_frame = prediction_frame.sort_values("predicted_neet_risk_index", ascending=False)

    coeff_frame = pd.DataFrame(
        {
            "feature": feature_frame.columns,
            "coefficient": coefficients,
            "absolute_coefficient": np.abs(coefficients),
        }
    ).sort_values("absolute_coefficient", ascending=False)

    metrics = {
        "train_rows": int(train_mask.sum()),
        "test_rows": int(test_mask.sum()),
        "features": feature_frame.columns.tolist(),
        "rmse": rmse,
        "mae": mae,
        "r2": r2,
        "target": "neet_risk_index",
        "holdout_year": 2024,
    }

    prediction_frame.to_csv(OUTPUT_DIR / "neet_regional_risk_model_predictions.csv", index=False)
    coeff_frame.to_csv(OUTPUT_DIR / "neet_regional_risk_model_coefficients.csv", index=False)
    with open(OUTPUT_DIR / "neet_regional_risk_model_metrics.json", "w", encoding="utf-8") as handle:
        json.dump(metrics, handle, indent=2)

    return {
        "metrics": metrics,
        "predictions": prediction_frame,
        "coefficients": coeff_frame,
    }


def write_manifest(gender_result: dict[str, pd.DataFrame], covid_summary: pd.DataFrame, regional_result: dict[str, object]) -> None:
    manifest = {
        "title": "Expanded NEET Derived Dataset Package (May 2026)",
        "inputs": [
            "local_data/ISTAT/istat_neet_new.csv",
            "local_data/NEET  (giovani non occupati e non in istruzione e formazione) - Dati regionali (IT1,172_931_DF_DCCV_NEET1_6,1.0).csv",
            "local_data/processed/transition_bridge_model_panel.csv",
        ],
        "outputs": {
            "neet_gender_year_panel.csv": {
                "description": "National NEET panel by year, age group, and sex",
                "columns": ["year", "classe_eta", "sex_label", "obs_value"],
            },
            "neet_gender_gap_by_year.csv": {
                "description": "Female-minus-male NEET gap and female/male ratio by year and age group",
                "columns": ["year", "classe_eta", "female_minus_male_pp", "female_to_male_ratio"],
            },
            "neet_gender_total_yearly.csv": {
                "description": "Total-sex national NEET trend",
                "columns": ["year", "neet_total_obs_value"],
            },
            "neet_covid_period_summary.csv": {
                "description": "Pre-COVID, shock, and recovery summary by sex and age group",
                "columns": ["covid_period", "classe_eta", "sex_label", "mean_neet_obs_value"],
            },
            "neet_regional_target_panel.csv": {
                "description": "Regional NEET target proxy using within-year normalized counts for ages 15-29",
                "columns": ["REF_AREA", "Territorio", "TIME_PERIOD", "neet_count_15_29", "neet_risk_index"],
            },
            "neet_regional_model_panel.csv": {
                "description": "Regional feature panel merged with the NEET target proxy",
                "columns": ["REF_AREA", "REF_AREA_LABEL", "TIME_PERIOD", "neet_risk_index"],
            },
            "neet_regional_risk_model_predictions.csv": {
                "description": "Holdout-year predictions from the baseline region-level model",
                "columns": ["REF_AREA", "TIME_PERIOD", "neet_risk_index", "predicted_neet_risk_index"],
            },
            "neet_regional_risk_model_coefficients.csv": {
                "description": "Standardized coefficients from the baseline model",
                "columns": ["feature", "coefficient"],
            },
            "neet_regional_risk_model_metrics.json": {
                "description": "Evaluation metrics for the baseline model",
                "columns": ["rmse", "mae", "r2"],
            },
        },
        "notes": [
            "Gender analysis comes directly from the existing ISTAT national NEET micro-aggregation.",
            "COVID impact is summarized as a pre-COVID vs shock vs recovery comparison.",
            "The predictive model uses a within-year risk index because the regional source exposes counts rather than population shares.",
            "The baseline model is intentionally simple and reproducible; it is a starting point rather than a final forecasting system.",
        ],
    }

    manifest_path = OUTPUT_DIR / "neet_expanded_sources_manifest.json"
    manifest_md = OUTPUT_DIR / "neet_expanded_sources.md"

    with open(manifest_path, "w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    md_lines = [
        "# Expanded NEET Sources",
        "",
        "## Inputs",
    ]
    for item in manifest["inputs"]:
        md_lines.append(f"- {item}")
    md_lines.extend(["", "## Outputs"])
    for name, spec in manifest["outputs"].items():
        md_lines.append(f"- {name}: {spec['description']}")
    md_lines.extend(["", "## Notes"])
    for note in manifest["notes"]:
        md_lines.append(f"- {note}")

    with open(manifest_md, "w", encoding="utf-8") as handle:
        handle.write("\n".join(md_lines) + "\n")


def main() -> None:
    print("Building expanded NEET-derived datasets...")
    gender_result = build_gender_panel()
    covid_summary = build_covid_summary(gender_result["panel"])
    regional_result = build_regional_model_panel()
    write_manifest(gender_result, covid_summary, regional_result)

    print("Done.")
    print(f"Gender panel rows: {len(gender_result['panel']):,}")
    print(f"COVID summary rows: {len(covid_summary):,}")
    print(f"Regional target rows: {len(regional_result['regional_target']):,}")
    print("Model metrics:")
    for key, value in regional_result["model_result"]["metrics"].items():
        if key in {"features"}:
            print(f"  {key}: {len(value)} features")
        else:
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()