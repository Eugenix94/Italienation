import pandas as pd
import json
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parent.parent / 'processed_data' / 'sostegno_precarity.json'

def build_sostegno_precarity():
    print("--- Loading Sostegno Personnel Data ---")
    df_tit = pd.read_parquet('https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/personale/DOCTIT.parquet')
    df_sup = pd.read_parquet('https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/personale/DOCSUPXXV.parquet')
    
    tit_sostegno = df_tit[df_tit['TIPOPOSTO'] == 'SOSTEGNO']
    sup_sostegno = df_sup[df_sup['TIPOPOSTO'] == 'SOSTEGNO']
    
    tenured = len(tit_sostegno)
    substitutes = len(sup_sostegno)
    total = tenured + substitutes
    
    data = {
        "tenured_sostegno": tenured,
        "substitute_sostegno": substitutes,
        "total_sostegno": total,
        "sostegno_precarity_pct": round((substitutes / total) * 100, 1)
    }
    
    print(json.dumps(data, indent=2))
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved sostegno precarity to {OUT_PATH}")

if __name__ == '__main__':
    build_sostegno_precarity()
