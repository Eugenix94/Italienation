#!/usr/bin/env python3
"""
fetch_geospatial_schools.py — Downloads the complete Italian School Registry from HF,
extracts geospatial data (lat/lon), and generates the Catania Case Study + National Sample.
"""
import os
import sys
import pandas as pd
import urllib.request

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')

# Target endpoints
HF_DATASET_URL = "https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/scuola_in_chiaro/SIC_ANAGRAFE_COMPLETA.parquet"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(ROOT, "local_data", "new_frontiers")
PROC_DIR = os.path.join(ROOT, "local_data", "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)

parquet_path = os.path.join(RAW_DIR, "sic_anagrafe_completa_raw.parquet")

print("1. Downloading HuggingFace SIC_ANAGRAFE_COMPLETA dataset...")
try:
    req = urllib.request.Request(HF_DATASET_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response, open(parquet_path, 'wb') as out_file:
        data = response.read()
        out_file.write(data)
        print(f"Downloaded securely: {len(data)} bytes to {parquet_path}")
except Exception as e:
    print(f"Failed to download: {e}")
    sys.exit(1)

print("\n2. Processing Geospatial Data via Pandas...")
try:
    df = pd.read_parquet(parquet_path)
    
    # Let's inspect the columns to find what we need. The file is usually structured with clear names.
    # Typical names in SIC: 'DESCRIZIONE_REGIONE', 'DESCRIZIONE_PROVINCIA', 'DESCRIZIONE_COMUNE', 
    # 'INDIRIZZO_SCUOLA', 'DESCRIZIONE_TIPOLOGIA_GRADO_ISTRUZIONE_SCUOLA', 'LATITUDINE', 'LONGITUDINE'
    
    # Standardizing column names to uppercase for safety
    df.columns = [str(c).upper() for c in df.columns]
    
    # Determine the actual column names present
    prov_col = 'PROVINCIA_NOME'
    lat_col = 'LATITUDINE'
    lon_col = 'LONGITUDINE'
    type_col = 'TIPO_ISTRUZIONE'
    name_col = 'DENOMINAZIONESCUOLA'
    
    # Filter out records missing coordinates
    # Ensure they are numeric
    df[lat_col] = pd.to_numeric(df[lat_col].astype(str).str.replace(',', '.'), errors='coerce')
    df[lon_col] = pd.to_numeric(df[lon_col].astype(str).str.replace(',', '.'), errors='coerce')
    
    df_valid = df.dropna(subset=[lat_col, lon_col]).copy()
    print(f"Valid geocoded schools found: {len(df_valid)}")
    
    # Map the Tripartite Tracking System based on the school type description
    def map_track(desc):
        d = str(desc).upper()
        if 'LICEO' in d or 'CLASSICO' in d or 'SCIENTIFICO' in d or 'LINGUISTICO' in d:
            return 'Liceo (Accademico)'
        if 'TECNICO' in d:
            return 'Istituto Tecnico'
        if 'PROFESSIONALE' in d or 'IEFP' in d:
            return 'Istituto Professionale'
        if 'PRIMARIA' in d or 'INFANZIA' in d:
            return 'Primaria/Infanzia'
        if 'PRIMO GRADO' in d or 'MEDIA' in d:
            return 'Secondaria I Grado (Media)'
        return 'Altro / Comprensivo'

    df_valid['TRACK_TRIPARTITO'] = df_valid[type_col].apply(map_track)

    # Filter only Secondary Schools (Superiori) for the Tripartite map
    superiori = ['Liceo (Accademico)', 'Istituto Tecnico', 'Istituto Professionale']
    df_superiori = df_valid[df_valid['TRACK_TRIPARTITO'].isin(superiori)]
    
    # ---------------------------------------------------------
    # A) Catania Case Study
    # ---------------------------------------------------------
    catania_df = df_valid[df_valid[prov_col].str.upper().str.contains('CATANIA', na=False)]
    catania_file = os.path.join(PROC_DIR, "catania_geospatial_schools_case_study.csv")
    
    # We save specific details for Catania
    cols_to_save_ct = [name_col, prov_col, type_col, 'TRACK_TRIPARTITO', lat_col, lon_col] if name_col else [prov_col, type_col, 'TRACK_TRIPARTITO', lat_col, lon_col]
    cols_to_save_ct = [c for c in cols_to_save_ct if c] # Keep only valid columns
    
    catania_df[cols_to_save_ct].to_csv(catania_file, index=False)
    print(f"Generated Catania Case Study: {catania_file} ({len(catania_df)} schools)")

    # ---------------------------------------------------------
    # B) National Sample (Generalized)
    # ---------------------------------------------------------
    # Subsample to ~15% for the national map to prevent rendering lags and protect precise locational overexposure
    national_sample = df_superiori.sample(frac=0.15, random_state=42)
    
    # Add a tiny bit of random noise (jitter) to the coordinates to generalize them "not precisely" as the user requested
    import numpy as np
    national_sample[lat_col] += np.random.normal(0, 0.005, len(national_sample))
    national_sample[lon_col] += np.random.normal(0, 0.005, len(national_sample))
    
    national_file = os.path.join(PROC_DIR, "italy_national_schools_geospatial_sample.csv")
    national_sample[[prov_col, 'TRACK_TRIPARTITO', lat_col, lon_col]].to_csv(national_file, index=False)
    print(f"Generated National Generalized Sample: {national_file} ({len(national_sample)} upper secondary schools)")

except Exception as e:
    import traceback
    print(f"Error processing data: {e}")
    traceback.print_exc()
