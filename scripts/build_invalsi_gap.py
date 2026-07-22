import pandas as pd
import json
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parent.parent / 'processed_data' / 'invalsi_gap.json'

def build_invalsi_gap():
    print("--- 1. Loading INVALSI RAV Evaluation Data ---")
    url = 'https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/sistema_nazionale_di_valutazione/VALUTAZIONE_ESITI_STA20161720170831.parquet'
    
    df = pd.read_parquet(url)
    
    # CODICECRITERIO == '22' corresponds to: "Risultati nelle prove standardizzate nazionali (INVALSI)"
    df_invalsi = df[df['CODICECRITERIO'] == '22'].copy()
    
    # Ensure PUNTEGGIOSCUOLA is numeric
    df_invalsi['PUNTEGGIOSCUOLA'] = pd.to_numeric(df_invalsi['PUNTEGGIOSCUOLA'], errors='coerce')
    df_invalsi = df_invalsi.dropna(subset=['PUNTEGGIOSCUOLA'])
    
    # Define school track based on CODICEISTITUTO (characters 2 and 3, 0-indexed)
    # Example: RMPS010004 -> 'PS' -> Liceo Scientifico
    def get_track(code):
        if len(code) < 4:
            return 'Altro'
        char_3 = code[2]
        if char_3 == 'P':
            return 'Licei'
        elif char_3 == 'T':
            return 'Istituti Tecnici'
        elif char_3 == 'R':
            return 'Istituti Professionali'
        elif char_3 == 'M' or char_3 == 'E': # Medie / Elementari
            return 'Scuola di Base'
        else:
            return 'Altro'
            
    df_invalsi['TRACK'] = df_invalsi['CODICEISTITUTO'].apply(get_track)
    
    # Filter only High Schools
    high_schools = ['Licei', 'Istituti Tecnici', 'Istituti Professionali']
    df_hs = df_invalsi[df_invalsi['TRACK'].isin(high_schools)]
    
    # Calculate average score by track
    # The score is 1 (lowest) to 7 (highest)
    agg = df_hs.groupby('TRACK')['PUNTEGGIOSCUOLA'].mean().reset_index()
    agg = agg.sort_values('PUNTEGGIOSCUOLA', ascending=False)
    
    results = []
    for _, row in agg.iterrows():
        results.append({
            'track': row['TRACK'],
            'avg_invalsi_score': round(row['PUNTEGGIOSCUOLA'], 2)
        })
        
    print(json.dumps(results, indent=2))
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved INVALSI gaps to {OUT_PATH}")

if __name__ == '__main__':
    build_invalsi_gap()
