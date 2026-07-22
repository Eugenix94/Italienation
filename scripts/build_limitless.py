import pandas as pd
import json
import ast
from pathlib import Path

def extract_wb(file_path, iso3_codes):
    df = pd.read_csv(file_path)
    res = {}
    for iso in iso3_codes:
        # Find latest non-null value for the iso code
        subset = df[(df['countryiso3code'] == iso) & (df['value'].notna())]
        if not subset.empty:
            subset = subset.sort_values(by='date', ascending=False)
            res[iso] = subset.iloc[0]['value']
    return res

def build_limitless():
    data = {}
    
    print("1. Digital Divide")
    df_dd = pd.read_csv('local_data/processed/digital_divide_broadband_schools_nuts3.csv')
    avg_connected = df_dd['Scuole_Connesse_1Gbps_Perc'].mean()
    data['digital_divide'] = {
        'no_broadband_pct': round(100 - avg_connected, 1)
    }
    
    print("2. Learning Poverty")
    lp = extract_wb('local_data/worldbank/wb_learning_poverty.csv', ['ITA'])
    data['learning_poverty'] = {'ita_pct': round(lp.get('ITA', 0), 1)}
    
    print("3. PISA Trend")
    df_pisa = pd.read_csv('local_data/oecd/oecd_it_pisa_trend.csv')
    pisa_data = []
    for _, row in df_pisa.iterrows():
        pisa_data.append({
            'year': int(row['year']),
            'math': row['italy_math'],
            'reading': row['italy_reading'],
            'science': row['italy_science']
        })
    data['pisa_trend'] = pisa_data
    
    print("4. Suicide Mortality")
    df_suicide = pd.read_csv('local_data/worldbank/wb_suicide_mortality.csv')
    ita_suicide = df_suicide[df_suicide['country_id'] == 'ITA'].sort_values('year', ascending=False).iloc[0]['value']
    eu_suicide = df_suicide[df_suicide['country_id'] == 'EUU'].sort_values('year', ascending=False).iloc[0]['value']
    data['suicide_mortality'] = {
        'ita_rate': round(ita_suicide, 2),
        'eu_rate': round(eu_suicide, 2)
    }
    
    print("5. Urban Rural Gap")
    df_ur = pd.read_csv('local_data/Openpolis/openpolis_neet_urban_rural_gap.csv')
    ur_data = []
    for _, row in df_ur.iterrows():
        ur_data.append({
            'territory': row['territory_type'],
            'neet_pct': row['neet_rate_15_29_pct']
        })
    data['urban_rural'] = ur_data
    
    print("6. Tertiary Illusion")
    enroll = extract_wb('local_data/worldbank/wb_tertiary_enrollment_gross.csv', ['ITA', 'EUU'])
    spend = extract_wb('local_data/worldbank/wb_tertiary_spending_pct_gdp_percapita.csv', ['ITA', 'EUU'])
    data['tertiary'] = {
        'ita_enroll': round(enroll.get('ITA', 0), 1),
        'eu_enroll': round(enroll.get('EUU', 0), 1),
        'ita_spend': round(spend.get('ITA', 0), 1),
        'eu_spend': round(spend.get('EUU', 0), 1)
    }
    
    out_path = Path('processed_data/limitless_expansion.json')
    with open(out_path, 'w') as f:
        json.dump(data, f, indent=2)
    print("Saved limitless_expansion.json")

if __name__ == '__main__':
    build_limitless()
