import pandas as pd
import json
from pathlib import Path

OUT_PATH = Path(__file__).resolve().parent.parent / 'processed_data' / 'textbook_costs.json'

def build_textbook_costs():
    print("--- 1. Loading Textbooks Data (Campania & Lombardia) ---")
    urls = [
        'https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/adozioni_libri_di_testo/ALTCAMPANIA000020260610.parquet',
        'https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/adozioni_libri_di_testo/ALTLOMBARDIA000020260610.parquet'
    ]
    
    dfs = []
    for url in urls:
        print(f"Downloading {url}...")
        df = pd.read_parquet(url)
        dfs.append(df)
        
    df = pd.concat(dfs, ignore_index=True)
    
    # Filter for first year (high school typically has classes 1 to 5)
    df_1 = df[df['ANNOCORSO'] == '1']
    
    # Filter only books that MUST be purchased
    df_buy = df_1[df_1['DAACQUIST'] == 'Si'].copy()
    
    # Convert PREZZO to numeric (it might be a string with commas)
    if df_buy['PREZZO'].dtype == 'object':
        df_buy = df_buy[df_buy['PREZZO'] != 'ND']
        df_buy['PREZZO'] = df_buy['PREZZO'].astype(str).str.replace(',', '.').astype(float)
        
    # Group by School and Section to find the total cost of books per student
    costs_per_class = df_buy.groupby(['CODICESCUOLA', 'SEZIONEANNO'])['PREZZO'].sum().reset_index()
    
    # Calculate average cost for a 1st year student
    avg_cost = costs_per_class['PREZZO'].mean()
    median_cost = costs_per_class['PREZZO'].median()
    max_cost = costs_per_class['PREZZO'].max()
    
    # For narrative impact, let's also find what % of schools exceed the state subsidy (e.g., 250 EUR)
    pct_over_250 = (costs_per_class['PREZZO'] > 250).mean() * 100
    pct_over_350 = (costs_per_class['PREZZO'] > 350).mean() * 100
    
    results = {
        'avg_cost_1st_year': round(avg_cost, 2),
        'median_cost_1st_year': round(median_cost, 2),
        'max_cost_1st_year': round(max_cost, 2),
        'pct_classes_over_250_eur': round(pct_over_250, 1),
        'pct_classes_over_350_eur': round(pct_over_350, 1)
    }
    
    print(json.dumps(results, indent=2))
    
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved textbook costs to {OUT_PATH}")

if __name__ == '__main__':
    build_textbook_costs()
