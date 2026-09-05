import requests
import json
import os

def fetch_world_bank_gdp_growth(country_code):
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.MKTP.KD.ZG?format=json&date=2000:2024&per_page=100'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()[1]
    
    extracted = []
    for entry in data:
        if entry['value'] is not None:
            extracted.append({
                'year': int(entry['date']),
                'growth': float(entry['value'])
            })
    return sorted(extracted, key=lambda x: x['year'])

def calculate_cumulative_index(growth_data, base_year=2000):
    filtered = [d for d in growth_data if d['year'] >= base_year]
    
    index_data = {}
    current_index = 100.0
    
    index_data[base_year] = 100.0
    
    for i in range(1, len(filtered)):
        year = filtered[i]['year']
        growth = filtered[i]['growth']
        current_index = current_index * (1 + (growth / 100.0))
        index_data[year] = round(current_index, 1)
        
    return index_data

def main():
    print('Fetching World Bank Data...')
    italy_growth = fetch_world_bank_gdp_growth('IT')
    eu_growth = fetch_world_bank_gdp_growth('EUU')
    
    italy_index = calculate_cumulative_index(italy_growth)
    eu_index = calculate_cumulative_index(eu_growth)
    
    target_years = [2000, 2005, 2010, 2015, 2020, 2023]
    
    new_real_gdp_growth = []
    for year in target_years:
        if year in italy_index and year in eu_index:
            new_real_gdp_growth.append({
                'year': year,
                'italy': italy_index[year],
                'eu_avg': eu_index[year]
            })
            
    if not new_real_gdp_growth:
        print('Failed to compute new indices.')
        return
        
    json_path = os.path.join('frontend', 'src', 'assets', 'macro_metrics.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    data['real_gdp_growth'] = new_real_gdp_growth
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print('macro_metrics.json successfully updated with live World Bank data!')

if __name__ == '__main__':
    main()
