import pandas as pd
import json
import os
from geopy.geocoders import Nominatim
import time

def build_province_map():
    input_file = os.path.join('processed', 'tripartite_territorial_deserts.csv')
    output_file = os.path.join('..', 'frontend', 'src', 'assets', 'province_school_counts.json')

    print("Loading datasets...")
    df = pd.read_csv(input_file)
    
    # Group by PROVINCIA
    prov_stats = df.groupby('PROVINCIA')[['Liceo', 'Tecnico', 'Professionale', 'Is_Total_Desert']].sum().reset_index()
    
    geolocator = Nominatim(user_agent="italienation_mapper_v2")
    
    results = []
    
    for _, row in prov_stats.iterrows():
        prov = row['PROVINCIA']
        print(f"Geocoding {prov}...")
        try:
            loc = geolocator.geocode(f"{prov}, Italy")
            lat = loc.latitude if loc else 41.8719
            lng = loc.longitude if loc else 12.5674
        except Exception as e:
            print(f"Error geocoding {prov}: {e}")
            lat, lng = 41.8719, 12.5674
            
        results.append({
            'id': prov,
            'name': prov.title(),
            'lat': lat,
            'lng': lng,
            'liceo_count': int(row['Liceo']),
            'tecnico_count': int(row['Tecnico']),
            'professionale_count': int(row['Professionale']),
            'total_deserts': int(row['Is_Total_Desert'])
        })
        time.sleep(0.5)  # respect Nominatim rate limits

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully wrote {len(results)} provinces to {output_file}")

if __name__ == '__main__':
    build_province_map()
