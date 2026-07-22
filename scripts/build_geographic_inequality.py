import pandas as pd
import json
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parent.parent / 'processed_data' / 'geographic_inequality.json'

def build_geographic_inequality():
    print("--- 1. Loading School Anagraphics Data ---")
    url = 'https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/scuole/SCUANAGRAFESTAT20252620250901.parquet'
    df = pd.read_parquet(url)
    
    # Base/Middle schools to exclude when looking for High Schools
    base_schools = ['SCUOLA INFANZIA', 'SCUOLA PRIMARIA', 'SCUOLA PRIMO GRADO', 'ISTITUTO COMPRENSIVO', 'CENTRO TERRITORIALE', 'CONVITTO ANNESSO', 'CONVITTO NAZIONALE', 'EDUCANDATO']
    
    # We define keywords for Lyceums
    lyceum_keywords = ['LICEO', 'MAGISTRALE']
    
    results_by_town = {}
    
    for _, row in df.iterrows():
        town = row['DESCRIZIONECOMUNE']
        school_type = str(row['DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA']).upper()
        
        if town not in results_by_town:
            results_by_town[town] = {
                'has_high_school': False,
                'has_lyceum': False,
                'has_ist_superiore': False
            }
            
        if school_type not in base_schools:
            results_by_town[town]['has_high_school'] = True
            
            if 'ISTITUTO SUPERIORE' in school_type:
                results_by_town[town]['has_ist_superiore'] = True
                results_by_town[town]['has_lyceum'] = True # Usually composite schools contain lyceums
                
            for k in lyceum_keywords:
                if k in school_type:
                    results_by_town[town]['has_lyceum'] = True
                    
    total_towns = len(results_by_town)
    towns_no_hs = sum(1 for t in results_by_town.values() if not t['has_high_school'])
    towns_only_voc_tech = sum(1 for t in results_by_town.values() if t['has_high_school'] and not t['has_lyceum'])
    
    # Percentages
    pct_no_hs = (towns_no_hs / total_towns) * 100
    pct_only_voc = (towns_only_voc_tech / total_towns) * 100
    pct_with_lyceum = 100 - pct_no_hs - pct_only_voc
    
    data = {
        "total_municipalities": total_towns,
        "no_high_school_pct": round(pct_no_hs, 1),
        "only_vocational_pct": round(pct_only_voc, 1),
        "full_access_pct": round(pct_with_lyceum, 1)
    }
    
    print(json.dumps(data, indent=2))
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved geographic inequality to {OUT_PATH}")

if __name__ == '__main__':
    build_geographic_inequality()
