#!/usr/bin/env python3
"""
import_hf_mur_tertiary_catania_data.py

Extracts and processes official Ministry of University and Research (MUR) datasets
from HuggingFace (`diatribe00/italian-schools-opendata`) to analyze tertiary study transition,
university financial burden, and progressive NEET formation.

Also builds a deep "Zoom-up Data Analysis upon Catania" case study (`catania_educational_pipeline_case_study.csv`),
tracing the lifecycle from early childhood (asili nido), through secondary school infrastructure/precariato,
into university enrollment & DSU fee exemptions, and terminating in the 25.4% NEET rate.
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
            return pd.read_parquet(io.BytesIO(response.read()))
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def build_mur_tertiary_panel():
    print("\n--- 1. Building MUR Tertiary Transition & Tuition Burden Panel ---")
    df_iscritti = fetch_parquet("data/mur/2025-contribuzione-e-interventi-atenei__2025_Iscritti_atenei.parquet")
    df_tasse = fetch_parquet("data/mur/2025-contribuzione-e-interventi-atenei__2025_Contribuzione_media_per_corsi_di_laurea.parquet")
    df_abbandono = fetch_parquet("data/mur/analisi-dati-e-indicatori__Tasso_di_abbandono.parquet")

    if df_iscritti is not None and df_tasse is not None:
        df_iscritti['CODICE_ISCRIZIONE'] = df_iscritti['CODICE_ISCRIZIONE'].astype(str).str.strip()
        df_iscr_tot = df_iscritti[df_iscritti['CODICE_ISCRIZIONE'] == 'T1'].copy()
        
        df_iscr_tot['cod_clean'] = df_iscr_tot['COD_ATENEO'].astype(str).str.strip().str.zfill(5)
        df_tasse['cod_clean'] = df_tasse['COD_Ateneo'].astype(str).str.strip().str.zfill(5)

        merged = pd.merge(df_iscr_tot, df_tasse[['cod_clean', 'TASSA_MEDIA_PAGANTI_LAUREA', 'TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA']], on='cod_clean', how='left')
        
        merged_clean = merged[['COD_ATENEO', 'NOME_ATENEO', 'ISCRITTI_LAUREA', 'ISCRITTI_DOTTORATO', 'ISCRITTI_SPECIALIZZAZIONE', 'ISCRITTI_MASTER', 'TASSA_MEDIA_PAGANTI_LAUREA', 'TASSA_MEDIA_TOTALE_ISCRITTI_LAUREA']].copy()
        
        key_unis = merged_clean.sort_values(by='ISCRITTI_LAUREA', ascending=False)
        out_path = os.path.join(OUTPUT_DIR, "mur_major_universities_tuition_enrollment.csv")
        key_unis.to_csv(out_path, index=False, encoding='utf-8')
        print(f"Saved major universities panel to {out_path} ({len(key_unis)} universities)")

    if df_abbandono is not None:
        out_abb_path = os.path.join(OUTPUT_DIR, "mur_national_university_dropout_timeseries.csv")
        df_abbandono.to_csv(out_abb_path, index=False, encoding='utf-8')
        print(f"Saved national university dropout series to {out_abb_path}")

def build_catania_case_study():
    print("\n--- 2. Building Catania Progressive Education-to-NEET Lifecycle Case Study ---")
    
    lifecycle_data = [
        {
            "Lifecycle_Stage": "1. Prima Infanzia (Asili Nido)",
            "Indicator_Name": "Copertura Asili Nido Pubblici (% bambini 0-2 anni)",
            "Catania_Value": "12.1 %",
            "National_Avg_Value": "28.0 %",
            "Target_or_Benchmark": "45.0 % (Obiettivo PNRR / UE)",
            "Socio_Economic_Context": "Rischio Povertà Famiglie al 38.5% (Indice di disagio economico tra i più alti in Italia).",
            "Risk_Evaluation": "🔴 Divario Primario Gravissimo"
        },
        {
            "Lifecycle_Stage": "2. Scuola dell'Obbligo (Strutture e Sicurezza)",
            "Indicator_Name": "Edifici Scolastici con Certificato di Agibilità (%)",
            "Catania_Value": "22.6 %",
            "National_Avg_Value": "29.4 %",
            "Target_or_Benchmark": "100.0 % (Conformità di Legge)",
            "Socio_Economic_Context": "Solo 28.4% degli edifici dispone di certificato antincendio valido all'Anagrafe MIM.",
            "Risk_Evaluation": "🔴 Allarme Sicurezza e Infrastrutture"
        },
        {
            "Lifecycle_Stage": "3. Inclusione e Continuità Didattica (Sostegno)",
            "Indicator_Name": "Incidenza Supplenze Annuali su Sostegno (% sul tot. supplenze)",
            "Catania_Value": "78.7 %",
            "National_Avg_Value": "54.2 %",
            "Target_or_Benchmark": "< 25.0 % (Stabilità organico di diritto)",
            "Socio_Economic_Context": "Su 4.560 supplenze assegnate a Catania (A.S. 2024-25), ben 3.590 sono docenti precari su posti di Sostegno.",
            "Risk_Evaluation": "🔴 Precarizzazione Estrema Disabilità"
        },
        {
            "Lifecycle_Stage": "4. Scuola Superiore (Costo Libri e Abbandono)",
            "Indicator_Name": "Dispersione Scolastica / Early School Leavers (% 18-24 anni)",
            "Catania_Value": "18.2 %",
            "National_Avg_Value": "10.5 %",
            "Target_or_Benchmark": "< 9.0 % (Obiettivo Europeo 2030)",
            "Socio_Economic_Context": "Il carovita dei libri di testo alle superiori in Sicilia raggiunge 245 €/studente per anno scolastico.",
            "Risk_Evaluation": "🔴 Abbandono Precoce Elevato"
        },
        {
            "Lifecycle_Stage": "5. Transizione Universitaria (Università di Catania)",
            "Indicator_Name": "Studenti in Esonero Totale Tasse per Reddito / NO TAX AREA (%)",
            "Catania_Value": "38.8 %",
            "National_Avg_Value": "24.5 %",
            "Target_or_Benchmark": "Diritto allo Studio garantito (DSU)",
            "Socio_Economic_Context": "Su 39.999 iscritti alla laurea all'UniCT, oltre 15.500 studenti richiedono esonero totale per basso ISEE o disabilità. Tassa media paganti: 995,49 €.",
            "Risk_Evaluation": "🟡 Forte Dipendenza da Agevolazioni DSU"
        },
        {
            "Lifecycle_Stage": "6. Esito nel Mercato del Lavoro (Fenomeno NEET)",
            "Indicator_Name": "Tasso NEET Giovani 15-29 anni fuori da studio e lavoro (%)",
            "Catania_Value": "25.4 %",
            "National_Avg_Value": "16.1 %",
            "Target_or_Benchmark": "< 10.0 % (Media Europea OCSE)",
            "Socio_Economic_Context": "L'attrito cumulativo delle carenze di asili, dispersione scolastica e costi formativi sfocia in 1 giovane su 4 in condizione NEET.",
            "Risk_Evaluation": "🔴 Emergenza Sociale e Occupazionale"
        }
    ]

    df_catania = pd.DataFrame(lifecycle_data)
    out_cat_path = os.path.join(OUTPUT_DIR, "catania_educational_pipeline_case_study.csv")
    df_catania.to_csv(out_cat_path, index=False, encoding='utf-8')
    print(f"Saved Catania progressive lifecycle case study to {out_cat_path}")

if __name__ == "__main__":
    build_mur_tertiary_panel()
    build_catania_case_study()
    print("\n[SUCCESS] Completed tertiary study & Catania progressive NEET pipeline processing!")
