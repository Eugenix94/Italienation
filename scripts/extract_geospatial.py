import pandas as pd
import json
from pathlib import Path

def extract_geospatial():
    df = pd.read_csv('local_data/processed/italy_national_schools_geospatial_sample.csv')
    
    # We want a clean array of [lat, lon, type] for Leaflet
    geo_data = []
    
    for _, row in df.iterrows():
        # Ensure we have valid coordinates
        if pd.notna(row['LATITUDINE']) and pd.notna(row['LONGITUDINE']):
            # Color code: Liceo = blue, Professionale/Tecnico = orange
            school_type = str(row['TRACK_TRIPARTITO'])
            color = 'blue' if 'Liceo' in school_type else 'orange'
            
            geo_data.append({
                "lat": float(row['LATITUDINE']),
                "lon": float(row['LONGITUDINE']),
                "type": school_type,
                "color": color,
                "prov": str(row['PROVINCIA_NOME'])
            })
            
    out_path = Path('processed_data/geospatial_map.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(geo_data, f)
        
    print(f"Successfully extracted {len(geo_data)} geospatial coordinates.")

if __name__ == '__main__':
    extract_geospatial()
