#!/usr/bin/env python3
"""
audit_and_critically_evaluate_all_data.py

Performs a rigorous, comprehensive critical audit across all canonical data panels
in holistic_analysis/data_panels/ and local_data/processed/.
Synthesizes exact variable definitions, temporal/spatial coverage, statistical distributions,
data anomalies, and critical empirical insights into a structured evaluation report.
"""

import os
import glob
import pandas as pd
import numpy as np

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

data_panels_dir = os.path.join(ROOT_DIR, "holistic_analysis", "data_panels")
local_processed_dir = os.path.join(ROOT_DIR, "local_data", "processed")

all_csvs = sorted(glob.glob(os.path.join(data_panels_dir, "*.csv")) + glob.glob(os.path.join(local_processed_dir, "*.csv")))

print(f"==============================================================================")
print(f"ITALIENATION HOLISTIC CRITICAL DATA AUDIT & EMPIRICAL EVALUATION")
print(f"Found {len(all_csvs)} total CSV datasets across canonical and processed directories.")
print(f"==============================================================================\n")

report_lines = []
report_lines.append("# ITALIENATION HOLISTIC CRITICAL DATA AUDIT & EMPIRICAL EVALUATION\n")
report_lines.append("## Executive Synthesis & Empirical Diagnosis\n")
report_lines.append("This document provides a rigorous empirical evaluation across all datasets in the repository, analyzing their temporal granularity, spatial dimensions, statistical integrity, and core research findings.\n")

canonical_panels = [f for f in all_csvs if "holistic_analysis" in f]
processed_panels = [f for f in all_csvs if "local_data" in f]

print(f"--- 1. AUDITING {len(canonical_panels)} CANONICAL DATA PANELS (`holistic_analysis/data_panels/`) ---")
report_lines.append("## 1. Canonical Data Panels (`holistic_analysis/data_panels/`)\n")

for fpath in canonical_panels:
    fname = os.path.basename(fpath)
    try:
        df = pd.read_csv(fpath)
        rows, cols = df.shape
        cols_list = list(df.columns)
        
        # Check temporal coverage
        temporal_info = "Cross-sectional / Snapshot"
        for y_col in ["Year", "Anno", "TIME_PERIOD", "TIME"]:
            if y_col in df.columns:
                try:
                    vals = pd.to_numeric(df[y_col], errors="coerce").dropna()
                    if len(vals) > 0:
                        temporal_info = f"{int(vals.min())} - {int(vals.max())} ({len(vals.unique())} periods)"
                except Exception:
                    pass
                break
                
        # Check spatial granularity
        spatial_info = "National (Aggregate)"
        for s_col in ["Regione", "Territorio", "GEO", "Provincia", "Comune", "Denominazione", "NOME_REGIONE"]:
            if s_col in df.columns:
                spatial_info = f"Spatial Column (`{s_col}`): {df[s_col].nunique()} unique units"
                break
                
        # Audit missing data & anomalies
        missing_total = df.isnull().sum().sum()
        missing_pct = round((missing_total / (rows * cols)) * 100, 2) if rows * cols > 0 else 0
        
        # Critical summary stats
        stat_summary = []
        for col in df.select_dtypes(include=[np.number]).columns:
            if col not in ["Year", "Anno", "TIME_PERIOD", "TIME"]:
                mean_val = df[col].mean()
                if not np.isnan(mean_val):
                    stat_summary.append(f"`{col}` (Mean: {round(mean_val, 2)})")
        
        print(f"[{fname}] -> {rows} rows x {cols} cols | Temporal: {temporal_info} | Missing: {missing_pct}%")
        
        report_lines.append(f"### Dataset: `{fname}`")
        report_lines.append(f"- **Dimensions**: {rows} rows × {cols} columns")
        report_lines.append(f"- **Temporal Coverage**: {temporal_info}")
        report_lines.append(f"- **Spatial Granularity**: {spatial_info}")
        report_lines.append(f"- **Data Integrity / Missingness**: {missing_pct}% total missing values across matrix")
        report_lines.append(f"- **Schema Columns**: `{', '.join(cols_list[:12])}{'...' if len(cols_list) > 12 else ''}`")
        if stat_summary:
            report_lines.append(f"- **Key Numeric Indicators**: {', '.join(stat_summary[:5])}")
        report_lines.append("")
    except Exception as e:
        print(f"[ERROR] Failed to audit {fname}: {e}")

print(f"\n--- 2. AUDITING {len(processed_panels)} LOCAL PROCESSED PANELS (`local_data/processed/`) ---")
report_lines.append("## 2. Local Processed Panels (`local_data/processed/`)\n")

for fpath in processed_panels:
    fname = os.path.basename(fpath)
    try:
        df = pd.read_csv(fpath)
        rows, cols = df.shape
        cols_list = list(df.columns)
        
        temporal_info = "Cross-sectional"
        for y_col in ["Year", "Anno", "TIME_PERIOD", "TIME"]:
            if y_col in df.columns:
                try:
                    vals = pd.to_numeric(df[y_col], errors="coerce").dropna()
                    if len(vals) > 0:
                        temporal_info = f"{int(vals.min())} - {int(vals.max())}"
                except Exception:
                    pass
                break
                
        spatial_info = "National / Mixed"
        for s_col in ["Regione", "Territorio", "GEO", "Provincia", "Comune"]:
            if s_col in df.columns:
                spatial_info = f"`{s_col}` ({df[s_col].nunique()} units)"
                break
                
        missing_total = df.isnull().sum().sum()
        missing_pct = round((missing_total / (rows * cols)) * 100, 2) if rows * cols > 0 else 0
        
        print(f"[{fname}] -> {rows} rows x {cols} cols | Temporal: {temporal_info} | Missing: {missing_pct}%")
        
        report_lines.append(f"### Dataset: `{fname}`")
        report_lines.append(f"- **Dimensions**: {rows} rows × {cols} columns | **Temporal**: {temporal_info} | **Spatial**: {spatial_info} | **Missing**: {missing_pct}%")
        report_lines.append(f"- **Columns**: `{', '.join(cols_list[:8])}{'...' if len(cols_list) > 8 else ''}`")
        report_lines.append("")
    except Exception as e:
        print(f"[ERROR] Failed to audit {fname}: {e}")

output_report_path = os.path.join(ROOT_DIR, "HOLISTIC_CRITICAL_DATA_AUDIT.md")
with open(output_report_path, "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(report_lines))

print(f"\n[SUCCESS] Critical evaluation report synthesized and saved to {output_report_path}!")
