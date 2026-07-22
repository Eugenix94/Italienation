import pandas as pd
import json
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parent.parent / 'processed_data' / 'teacher_precarity.json'

def build_teacher_precarity():
    print("--- Loading Teacher Personnel Data ---")
    df_tit = pd.read_parquet('https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/personale/DOCTIT.parquet')
    df_sup = pd.read_parquet('https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/personale/DOCSUPXXV.parquet')
    
    tenured = len(df_tit)
    substitutes = len(df_sup)
    total = tenured + substitutes
    
    data = {
        "tenured_count": tenured,
        "substitute_count": substitutes,
        "total_count": total,
        "precarity_pct": round((substitutes / total) * 100, 1)
    }
    
    print(json.dumps(data, indent=2))
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved teacher precarity to {OUT_PATH}")

if __name__ == '__main__':
    build_teacher_precarity()
