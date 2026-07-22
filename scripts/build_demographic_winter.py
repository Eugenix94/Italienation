import pandas as pd
import json
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parent.parent / 'processed_data' / 'demographic_winter.json'

def build_demographic_winter():
    print("--- Loading Demographic Winter Data ---")
    df = pd.read_csv('local_data/processed/demographic_winter_school_closures_projection.csv')
    
    # Aggregate National Projections
    total_pop_2024 = df['Pop_Scolastica_6_18_Anno_2024'].sum()
    total_pop_2035 = df['Stima_Pop_6_18_Anno_2035'].sum()
    total_closures = df['Stima_Istituti_Accorpati_o_Chiusi'].sum()
    
    pop_drop_pct = ((total_pop_2024 - total_pop_2035) / total_pop_2024) * 100
    
    data = {
        "pop_6_18_2024": int(total_pop_2024),
        "pop_6_18_2035": int(total_pop_2035),
        "pop_drop_pct": round(pop_drop_pct, 1),
        "projected_school_closures": int(total_closures)
    }
    
    print(json.dumps(data, indent=2))
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved demographic winter to {OUT_PATH}")

if __name__ == '__main__':
    build_demographic_winter()
