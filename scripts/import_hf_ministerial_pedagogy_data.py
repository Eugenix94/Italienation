#!/usr/bin/env python3
"""
import_hf_ministerial_pedagogy_data.py

Imports comprehensive Italian Ministry of Education datasets from HuggingFace (diatribe00/italian-schools-opendata)
focusing specifically on Pedagogy, Textbooks (Adozioni & Prezzi), Teacher Formation & Workforce (Precariato & Sostegno),
and National Evaluation Outcomes (SNV RAV Rubric Levels 1-7 across Criteria 21-24).

Produces clean summary CSV panels in `local_data/processed/`:
1. `ministerial_textbook_costs_by_region_level.csv`
2. `ministerial_snv_pedagogy_outcomes_rubric.csv`
3. `ministerial_teacher_workforce_precariato_2024_25.csv`
"""

import os
import io
import urllib.request
import json
import pandas as pd
import numpy as np

OUTPUT_DIR = os.path.join("local_data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

HF_BASE_RESOLVE = "https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main"

def fetch_parquet(rel_path):
    url = f"{HF_BASE_RESOLVE}/{rel_path}"
    print(f"Fetching {url} ...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req) as response:
            content = response.read()
            return pd.read_parquet(io.BytesIO(content))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def process_snv_pedagogy_outcomes():
    print("\n--- 1. Processing SNV Pedagogy Outcomes (`VALUTAZIONE_ESITI_STA.parquet`) ---")
    df = fetch_parquet("data/valutazione/VALUTAZIONE_ESITI_STA.parquet")
    if df is None:
        return
    
    # Map Criteria codes to clear pedagogical labels
    criteria_map = {
        '21': 'Risultati scolastici (Esami e Promozioni)',
        '22': 'Risultati Prove Nazionali (INVALSI)',
        '23': 'Competenze Chiave e di Cittadinanza',
        '24': 'Risultati a Distanza (Università e Lavoro)'
    }
    
    # Clean score column to numeric (1-7)
    df['PUNTEGGIOSCUOLA_NUM'] = pd.to_numeric(df['PUNTEGGIOSCUOLA'], errors='coerce')
    df = df.dropna(subset=['PUNTEGGIOSCUOLA_NUM'])
    
    # Group by criteria and calculate distribution of rubric levels
    summary = df.groupby('CODICECRITERIO')['PUNTEGGIOSCUOLA_NUM'].agg([
        ('numero_scuole', 'count'),
        ('punteggio_medio', 'mean'),
        ('punteggio_mediano', 'median'),
        ('pct_eccellenza_6_7', lambda x: (x >= 6).mean() * 100),
        ('pct_intermedio_4_5', lambda x: ((x >= 4) & (x <= 5)).mean() * 100),
        ('pct_critico_1_3', lambda x: (x <= 3).mean() * 100)
    ]).reset_index()
    
    summary['criterio_nome'] = summary['CODICECRITERIO'].map(lambda c: criteria_map.get(str(c), f"Criterio {c}"))
    summary['punteggio_medio'] = summary['punteggio_medio'].round(2)
    summary['pct_eccellenza_6_7'] = summary['pct_eccellenza_6_7'].round(1)
    summary['pct_intermedio_4_5'] = summary['pct_intermedio_4_5'].round(1)
    summary['pct_critico_1_3'] = summary['pct_critico_1_3'].round(1)
    
    out_file = os.path.join(OUTPUT_DIR, "ministerial_snv_pedagogy_outcomes_rubric.csv")
    summary.to_csv(out_file, index=False, encoding='utf-8')
    print(f"[OK] Saved SNV Pedagogy outcomes summary: {out_file} ({len(summary)} rows)")

def process_teacher_workforce():
    print("\n--- 2. Processing Teacher Formation & Workforce (`DOCSUPXXV20242520250831.parquet`) ---")
    df = fetch_parquet("data/personale_scuola/DOCSUPXXV20242520250831.parquet")
    if df is None:
        return
    
    # Convert numeric counts
    df['maschi'] = pd.to_numeric(df['DOCENTISUPPLENTIMASCHI'], errors='coerce').fillna(0)
    df['femmine'] = pd.to_numeric(df['DOCENTISUPPLENTIFEMMINE'], errors='coerce').fillna(0)
    df['totale_supplenti'] = df['maschi'] + df['femmine']
    
    # Group by province and post type (Sostegno vs Normale/Comune)
    summary = df.groupby(['PROVINCIA', 'TIPOPOSTO'])['totale_supplenti'].sum().unstack(fill_value=0).reset_index()
    if 'SOSTEGNO' in summary.columns and ('NORMALE' in summary.columns or 'COMUNE' in summary.columns):
        norm_col = 'NORMALE' if 'NORMALE' in summary.columns else 'COMUNE'
        summary['totale_supplenze'] = summary['SOSTEGNO'] + summary[norm_col]
        summary['pct_sostegno_su_totale'] = (summary['SOSTEGNO'] / summary['totale_supplenze'] * 100).round(1)
    else:
        # Sum all numeric columns just in case
        cols = [c for c in summary.columns if c != 'PROVINCIA']
        summary['totale_supplenze'] = summary[cols].sum(axis=1)
        summary['pct_sostegno_su_totale'] = 0.0
    
    # Sort by total supplenze descending
    summary = summary.sort_values(by='totale_supplenze', ascending=False)
    
    out_file = os.path.join(OUTPUT_DIR, "ministerial_teacher_workforce_precariato_2024_25.csv")
    summary.to_csv(out_file, index=False, encoding='utf-8')
    print(f"[OK] Saved Teacher workforce & sostegno summary: {out_file} ({len(summary)} rows)")

def process_textbooks_costs():
    print("\n--- 3. Processing Textbooks Financial Burden (`adozioni_libri_di_testo` sample regions) ---")
    regions = [
        ('ALTLOMBARDIA000020260610.parquet', 'Lombardia', 'Nord'),
        ('ALTLIGURIA000020260610.parquet', 'Liguria', 'Nord'),
        ('ALTLAZIO000020260610.parquet', 'Lazio', 'Centro'),
        ('ALTEMILIAROMAGNA000020260610.parquet', 'Emilia-Romagna', 'Nord'),
        ('ALTCAMPANIA000020260610.parquet', 'Campania', 'Sud'),
        ('ALTABRUZZO000020260610.parquet', 'Abruzzo', 'Sud')
    ]
    
    all_data = []
    for file_name, reg_name, macro in regions:
        df = fetch_parquet(f"data/adozioni_libri_di_testo/{file_name}")
        if df is not None:
            df['PREZZO_NUM'] = pd.to_numeric(df['PREZZO'].astype(str).str.replace(',', '.'), errors='coerce')
            df['DAACQUIST'] = df['DAACQUIST'].astype(str).str.upper().str.strip()
            # Filter only textbooks that families must purchase ('SI')
            df_buy = df[df['DAACQUIST'] == 'SI']
            
            # Group by School Code, Course Year, Section to get total price per student basket
            basket = df_buy.groupby(['CODICESCUOLA', 'TIPOGRADOSCUOLA', 'ANNOCORSO', 'SEZIONEANNO'])['PREZZO_NUM'].sum().reset_index()
            
            # Now average across school types in the region
            reg_summary = basket.groupby('TIPOGRADOSCUOLA')['PREZZO_NUM'].agg(['mean', 'median', 'count']).reset_index()
            reg_summary['regione'] = reg_name
            reg_summary['macro_area'] = macro
            reg_summary['costo_medio_basket_eur'] = reg_summary['mean'].round(2)
            reg_summary['costo_mediano_basket_eur'] = reg_summary['median'].round(2)
            reg_summary['combinazioni_classi'] = reg_summary['count']
            
            all_data.append(reg_summary[['regione', 'macro_area', 'TIPOGRADOSCUOLA', 'costo_medio_basket_eur', 'costo_mediano_basket_eur', 'combinazioni_classi']])
    
    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        out_file = os.path.join(OUTPUT_DIR, "ministerial_textbook_costs_by_region_level.csv")
        final_df.to_csv(out_file, index=False, encoding='utf-8')
        print(f"[OK] Saved Textbooks cost summary: {out_file} ({len(final_df)} rows)")

if __name__ == "__main__":
    print("=== STARTING IMPORT OF OFFICIAL MINISTERIAL PEDAGOGY & OUTCOME DATA ===")
    process_snv_pedagogy_outcomes()
    process_teacher_workforce()
    process_textbooks_costs()
    print("=== IMPORT COMPLETED SUCCESSFULLY ===")
