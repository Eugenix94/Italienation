#!/usr/bin/env python3
"""
import_hf_ministerial_infrastructure_demographics.py

Imports and processes official Italian Ministry of Education datasets from HuggingFace (`diatribe00/italian-schools-opendata`)
covering physical infrastructure safety (`EDICONSICUREZZASTA`), disability accessibility (`EDISUPBARARCSTA`),
student demographics/citizenship (`ALUITASTRACITSTA`), and didactic process evaluation (`VALUTAZIONE_PROCESSI_STA`).

Produces clean summary CSV panels in `local_data/processed/`:
1. `ministerial_school_building_safety_by_region.csv`
2. `ministerial_architectural_barriers_by_region.csv`
3. `ministerial_foreign_students_integration.csv`
4. `ministerial_snv_process_evaluation_rubric.csv`
"""

import os
import io
import urllib.request
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

def process_building_safety():
    print("\n--- 1. Processing School Building Safety (`EDICONSICUREZZASTA.parquet`) ---")
    df = fetch_parquet("data/edifici/EDICONSICUREZZASTA.parquet")
    if df is None:
        return
    
    # Map school codes / buildings to region based on prefix or merge (if needed, let's group overall and by macro regions using provincial prefixes if available, or compute national / sample province aggregates)
    # Let's extract first 2 characters of CODICESCUOLA (which are province codes like RM, MI, NA, PA, FI, TO, BO, BA, VE, GE, CT, CA)
    df['PROV_CODE'] = df['CODICESCUOLA'].astype(str).str[:2]
    
    # Map key provinces to names and macro areas
    prov_map = {
        'RM': ('Roma', 'Centro'), 'MI': ('Milano', 'Nord'), 'NA': ('Napoli', 'Sud'),
        'TO': ('Torino', 'Nord'), 'PA': ('Palermo', 'Sud'), 'FI': ('Firenze', 'Centro'),
        'BO': ('Bologna', 'Nord'), 'BA': ('Bari', 'Sud'), 'VE': ('Venezia', 'Nord'),
        'GE': ('Genova', 'Nord'), 'CT': ('Catania', 'Sud'), 'CA': ('Cagliari', 'Sud'),
        'BS': ('Brescia', 'Nord'), 'VR': ('Verona', 'Nord'), 'PD': ('Padova', 'Nord'),
        'SA': ('Salerno', 'Sud'), 'ME': ('Messina', 'Sud'), 'LE': ('Lecce', 'Sud')
    }
    
    df['PROV_INFO'] = df['PROV_CODE'].map(prov_map)
    df_known = df.dropna(subset=['PROV_INFO']).copy()
    df_known['provincia'] = df_known['PROV_INFO'].map(lambda x: x[0])
    df_known['macro_area'] = df_known['PROV_INFO'].map(lambda x: x[1])
    
    # Calculate % of buildings with Agibilità (agibility certificate) and Prevenzione Incendi (fire safety)
    df_known['has_agibilita'] = df_known['CERTIFICATOSEGNALAZIONEAGIBILITA'].astype(str).str.upper().str.strip() == 'SI'
    df_known['has_antincendio'] = df_known['CERTIFICATOPREVENZIONEINCENDI'].astype(str).str.upper().str.strip() == 'SI'
    df_known['has_dvr'] = df_known['DOCUMENTOVALUTAZIONERISCHI'].astype(str).str.upper().str.strip() == 'SI'
    
    summary = df_known.groupby(['provincia', 'macro_area']).agg(
        edifici_totali=('CODICEEDIFICIO', 'count'),
        pct_agibilita=('has_agibilita', lambda x: (x.mean() * 100).round(1)),
        pct_antincendio=('has_antincendio', lambda x: (x.mean() * 100).round(1)),
        pct_dvr=('has_dvr', lambda x: (x.mean() * 100).round(1))
    ).reset_index().sort_values(by='edifici_totali', ascending=False)
    
    out_file = os.path.join(OUTPUT_DIR, "ministerial_school_building_safety_by_region.csv")
    summary.to_csv(out_file, index=False, encoding='utf-8')
    print(f"[OK] Saved School building safety summary: {out_file} ({len(summary)} rows)")

def process_architectural_barriers():
    print("\n--- 2. Processing Architectural Barriers (`EDISUPBARARCSTA.parquet`) ---")
    df = fetch_parquet("data/edifici/EDISUPBARARCSTA.parquet")
    if df is None:
        return
    
    df['PROV_CODE'] = df['CODICESCUOLA'].astype(str).str[:2]
    prov_map = {
        'RM': ('Roma', 'Centro'), 'MI': ('Milano', 'Nord'), 'NA': ('Napoli', 'Sud'),
        'TO': ('Torino', 'Nord'), 'PA': ('Palermo', 'Sud'), 'FI': ('Firenze', 'Centro'),
        'BO': ('Bologna', 'Nord'), 'BA': ('Bari', 'Sud'), 'VE': ('Venezia', 'Nord'),
        'GE': ('Genova', 'Nord'), 'CT': ('Catania', 'Sud'), 'CA': ('Cagliari', 'Sud'),
        'BS': ('Brescia', 'Nord'), 'VR': ('Verona', 'Nord'), 'PD': ('Padova', 'Nord')
    }
    df['PROV_INFO'] = df['PROV_CODE'].map(prov_map)
    df_known = df.dropna(subset=['PROV_INFO']).copy()
    df_known['provincia'] = df_known['PROV_INFO'].map(lambda x: x[0])
    df_known['macro_area'] = df_known['PROV_INFO'].map(lambda x: x[1])
    
    df_known['superato_barriere'] = df_known['ACCORGIMENTISUPERAMENTOBARRIEREARCHITETTONICHE'].astype(str).str.upper().str.strip() == 'SI'
    df_known['has_rampe'] = df_known['ACCESSODAESTERNOCONRAMPE'].astype(str).str.upper().str.strip() == 'SI'
    df_known['has_ascensore'] = df_known['ASCENSORETRASPORTODISABILI'].astype(str).str.upper().str.strip() == 'SI'
    df_known['has_bagni_disabili'] = df_known['SERVIZIIGIENICISPECIFICINORMADISABILI'].astype(str).str.upper().str.strip() == 'SI'
    
    summary = df_known.groupby(['provincia', 'macro_area']).agg(
        edifici_totali=('CODICEEDIFICIO', 'count'),
        pct_superamento_barriere=('superato_barriere', lambda x: (x.mean() * 100).round(1)),
        pct_rampe_esterne=('has_rampe', lambda x: (x.mean() * 100).round(1)),
        pct_ascensori_disabili=('has_ascensore', lambda x: (x.mean() * 100).round(1)),
        pct_bagni_disabili=('has_bagni_disabili', lambda x: (x.mean() * 100).round(1))
    ).reset_index().sort_values(by='edifici_totali', ascending=False)
    
    out_file = os.path.join(OUTPUT_DIR, "ministerial_architectural_barriers_by_region.csv")
    summary.to_csv(out_file, index=False, encoding='utf-8')
    print(f"[OK] Saved Architectural barriers summary: {out_file} ({len(summary)} rows)")

def process_foreign_students():
    print("\n--- 3. Processing Foreign Students & Citizenship (`ALUITASTRACITSTA.parquet`) ---")
    df = fetch_parquet("data/studenti/ALUITASTRACITSTA.parquet")
    if df is None:
        return
    
    df['PROV_CODE'] = df['CODICESCUOLA'].astype(str).str[:2]
    prov_map = {
        'RM': ('Roma', 'Centro'), 'MI': ('Milano', 'Nord'), 'NA': ('Napoli', 'Sud'),
        'TO': ('Torino', 'Nord'), 'PA': ('Palermo', 'Sud'), 'FI': ('Firenze', 'Centro'),
        'BO': ('Bologna', 'Nord'), 'BA': ('Bari', 'Sud'), 'VE': ('Venezia', 'Nord'),
        'GE': ('Genova', 'Nord'), 'CT': ('Catania', 'Sud'), 'CA': ('Cagliari', 'Sud')
    }
    df['PROV_INFO'] = df['PROV_CODE'].map(prov_map)
    df_known = df.dropna(subset=['PROV_INFO']).copy()
    df_known['provincia'] = df_known['PROV_INFO'].map(lambda x: x[0])
    df_known['macro_area'] = df_known['PROV_INFO'].map(lambda x: x[1])
    
    df_known['alunni_tot'] = pd.to_numeric(df_known['ALUNNI'], errors='coerce').fillna(0)
    df_known['alunni_stranieri'] = pd.to_numeric(df_known['ALUNNICITTADINANZANONITALIANA'], errors='coerce').fillna(0)
    
    # Filter for Upper Secondary vs Primaria/Media
    summary = df_known.groupby(['provincia', 'macro_area', 'ORDINESCUOLA'])[['alunni_tot', 'alunni_stranieri']].sum().reset_index()
    summary['pct_alunni_stranieri'] = (summary['alunni_stranieri'] / summary['alunni_tot'] * 100).round(1)
    
    # Let's pivot or keep top orders
    summary = summary[summary['alunni_tot'] > 100].sort_values(by=['provincia', 'ORDINESCUOLA'])
    
    out_file = os.path.join(OUTPUT_DIR, "ministerial_foreign_students_integration.csv")
    summary.to_csv(out_file, index=False, encoding='utf-8')
    print(f"[OK] Saved Foreign students summary: {out_file} ({len(summary)} rows)")

def process_process_evaluation():
    print("\n--- 4. Processing Process & Didactic Evaluation Rubric (`VALUTAZIONE_PROCESSI_STA.parquet`) ---")
    df = fetch_parquet("data/valutazione/VALUTAZIONE_PROCESSI_STA.parquet")
    if df is None:
        return
    
    # Map Process criteria codes
    criteria_map = {
        '31': 'Curricolo, Progettazione e Valutazione',
        '32': 'Ambiente di Apprendimento e Laboratori',
        '33': 'Inclusione e Differenziazione Didattica',
        '34': 'Continuità e Orientamento Studenti',
        '35': 'Sviluppo e Formazione Continua Docenti'
    }
    
    df['PUNTEGGIOSCUOLA_NUM'] = pd.to_numeric(df['PUNTEGGIOSCUOLA'], errors='coerce')
    df = df.dropna(subset=['PUNTEGGIOSCUOLA_NUM'])
    
    summary = df.groupby('CODICECRITERIO')['PUNTEGGIOSCUOLA_NUM'].agg([
        ('numero_scuole', 'count'),
        ('punteggio_medio', 'mean'),
        ('punteggio_mediano', 'median'),
        ('pct_eccellenza_6_7', lambda x: (x >= 6).mean() * 100),
        ('pct_critico_1_3', lambda x: (x <= 3).mean() * 100)
    ]).reset_index()
    
    summary['criterio_nome'] = summary['CODICECRITERIO'].map(lambda c: criteria_map.get(str(c), f"Processo Criterio {c}"))
    summary['punteggio_medio'] = summary['punteggio_medio'].round(2)
    summary['pct_eccellenza_6_7'] = summary['pct_eccellenza_6_7'].round(1)
    summary['pct_critico_1_3'] = summary['pct_critico_1_3'].round(1)
    
    out_file = os.path.join(OUTPUT_DIR, "ministerial_snv_process_evaluation_rubric.csv")
    summary.to_csv(out_file, index=False, encoding='utf-8')
    print(f"[OK] Saved Process evaluation summary: {out_file} ({len(summary)} rows)")

if __name__ == "__main__":
    print("=== STARTING IMPORT OF MINISTERIAL INFRASTRUCTURE & DEMOGRAPHIC DATA ===")
    process_building_safety()
    process_architectural_barriers()
    process_foreign_students()
    process_process_evaluation()
    print("=== ALL 4 DATASETS IMPORTED SUCCESSFULLY ===")
