import pandas as pd
import json

def build_full_benchmark():
    # Load the macro dataset
    file_path = 'processed_data/global_italy_position_oecd_wb_latest.csv'
    df = pd.read_csv(file_path)
    
    # We want to extract OECD/EU27 nations and a few key globals
    # To keep the UI clean but comprehensive, let's filter to countries that have valid education spending data
    df_clean = df.dropna(subset=['education_spending_pct_gdp'])
    
    # Sort by Education Spending
    df_clean = df_clean.sort_values(by='education_spending_pct_gdp', ascending=False)
    
    # Select key columns
    records = []
    for _, row in df_clean.iterrows():
        # Avoid non-countries or regional blocs except OECD/EU
        iso = str(row['iso3'])
        if iso in ['WLD', 'HIC', 'MIC', 'LIC'] and iso != 'ITA': 
            continue
            
        records.append({
            "iso3": iso,
            "country": row.get('country', iso),
            "education_spending_pct_gdp": round(row['education_spending_pct_gdp'], 1),
            "tertiary_enrollment": round(row['tertiary_enrollment_gross_pct'], 1) if pd.notnull(row.get('tertiary_enrollment_gross_pct')) else None,
            "learning_poverty": round(row['learning_poverty_pct'], 1) if pd.notnull(row.get('learning_poverty_pct')) else None
        })
        
    out_path = 'rendered_outputs/data_oecd_full.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=4)
        
    print(f"Generated {len(records)} country records in {out_path}")

if __name__ == '__main__':
    build_full_benchmark()
