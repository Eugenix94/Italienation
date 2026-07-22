import pandas as pd
import json
from pathlib import Path

# Paths
ROOT = Path(__file__).resolve().parent.parent
WB_PATH = ROOT / 'local_data' / 'worldbank' / 'wb_education_spending_pct_gdp.csv'
OUT_PATH = ROOT / 'processed_data' / 'global_benchmarks.json'

def build_global_benchmarks():
    print("--- 1. Loading World Bank Spending Data ---")
    df = pd.read_csv(WB_PATH)
    
    # Filter for the year 2020 or 2021 where data is most complete globally
    df_recent = df[df['date'].isin([2020, 2021, 2022])]
    
    # We want a list of comparative countries: ITA, DEU, FRA, ESP, GBR, EUU (European Union)
    target_countries = ['ITA', 'DEU', 'FRA', 'ESP', 'GBR', 'EUU']
    
    df_target = df_recent[df_recent['countryiso3code'].isin(target_countries)].copy()
    
    # Drop NaNs
    df_target = df_target.dropna(subset=['value'])
    
    # Sort by date descending and get the first (most recent) value for each country
    df_target = df_target.sort_values('date', ascending=False)
    df_final = df_target.groupby('countryiso3code').first().reset_index()
    
    results = []
    for _, row in df_final.iterrows():
        try:
            # The country name is a stringified dict: "{'id': 'IT', 'value': 'Italy'}"
            # Let's extract just the value string using eval or regex
            c_str = row['country']
            c_name = eval(c_str)['value']
        except:
            c_name = row['country']
            
        results.append({
            'iso3': row['countryiso3code'],
            'country_name': c_name,
            'year': row['date'],
            'spending_pct_gdp': round(row['value'], 2)
        })
        
    # Sort by spending descending
    results = sorted(results, key=lambda x: x['spending_pct_gdp'], reverse=True)
    
    print(json.dumps(results, indent=2))
    
    # Save
    with open(OUT_PATH, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved global benchmarks to {OUT_PATH}")

if __name__ == '__main__':
    build_global_benchmarks()
