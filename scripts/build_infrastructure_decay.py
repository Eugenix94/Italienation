import pandas as pd
import json
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parent.parent / 'processed_data' / 'infrastructure_decay.json'

def build_infrastructure_decay():
    print("--- Loading Infrastructure Data ---")
    df = pd.read_csv('local_data/processed/school_infrastructure_seismic_safety_panel.csv')
    
    # We will compute the national average
    avg_agibilita = df['Perc_Certificato_Agibilita'].mean()
    avg_antisismica = df['Perc_Verifica_Antisismica'].mean()
    
    data = {
        "habitability_cert_pct": round(avg_agibilita, 1),
        "no_habitability_cert_pct": round(100 - avg_agibilita, 1),
        "seismic_safety_cert_pct": round(avg_antisismica, 1),
        "no_seismic_safety_cert_pct": round(100 - avg_antisismica, 1)
    }
    
    print(json.dumps(data, indent=2))
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved infrastructure decay to {OUT_PATH}")

if __name__ == '__main__':
    build_infrastructure_decay()
