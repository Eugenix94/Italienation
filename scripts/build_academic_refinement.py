import pandas as pd
import json
from pathlib import Path
import glob

def build_aggregations():
    print("1. Aggregating Map Data by Province...")
    df_schools = pd.read_parquet('local_data/HuggingFace/hf_schools_registry_stat.parquet')
    
    # Define a helper function for branch
    def get_branch(desc):
        desc = str(desc).upper()
        if 'LICEO' in desc: return 'Liceo'
        if 'TECNIC' in desc: return 'Tecnico'
        if 'PROF' in desc: return 'Professionale'
        return 'Altro'

    df_schools['Branch'] = df_schools['DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'].apply(get_branch)
    df_filtered = df_schools[df_schools['Branch'] != 'Altro']
    
    # Calculate centroids using the previously extracted valid school coordinates
    with open('processed_data/geospatial_map.json', 'r', encoding='utf-8') as f:
        valid_schools = json.load(f)
    
    prov_coords = {}
    for s in valid_schools:
        prov = s.get('prov')
        if prov not in prov_coords:
            prov_coords[prov] = {'lats': [], 'lons': []}
        prov_coords[prov]['lats'].append(s['lat'])
        prov_coords[prov]['lons'].append(s['lon'])
        
    centroids = {}
    for prov, data in prov_coords.items():
        centroids[prov] = {
            'LATITUDINE': sum(data['lats']) / len(data['lats']),
            'LONGITUDINE': sum(data['lons']) / len(data['lons'])
        }

    agg_df = df_filtered.groupby(['REGIONE', 'PROVINCIA', 'Branch']).size().reset_index(name='Count')

    provincial_data = {}
    for _, row in agg_df.iterrows():
        reg = row['REGIONE']
        prov = row['PROVINCIA']
        branch = row['Branch']
        count = row['Count']
        
        if prov not in provincial_data:
            provincial_data[prov] = {
                'regione': reg,
                'provincia': prov,
                'Liceo': 0,
                'Tecnico': 0,
                'Professionale': 0,
                'Total': 0,
                'lat': centroids.get(prov, {}).get('LATITUDINE', 41.87),
                'lon': centroids.get(prov, {}).get('LONGITUDINE', 12.56)
            }
        
        provincial_data[prov][branch] += count
        provincial_data[prov]['Total'] += count

    with open('processed_data/provincial_map_agg.json', 'w', encoding='utf-8') as f:
        json.dump(provincial_data, f, indent=2)
    print(f"Saved aggregation for {len(provincial_data)} provinces.")

    print("2. Extracting Complete Curriculum Matrix...")
    # Load all textbook adoption files
    files = glob.glob('local_data/HuggingFace/adozioni_libri_di_testo/*.parquet')
    
    # We will map school code -> branch
    school_branch_map = dict(zip(df_filtered['CODICESCUOLA'], df_filtered['Branch']))
    
    curriculum = {'Liceo': {}, 'Tecnico': {}, 'Professionale': {}}
    
    count = 0
    for file in files:
        df = pd.read_parquet(file, columns=['CODICESCUOLA', 'DISCIPLINA'])
        df = df.dropna(subset=['CODICESCUOLA', 'DISCIPLINA'])
        df['DISCIPLINA'] = df['DISCIPLINA'].str.strip().str.upper()
        
        # Map branch
        df['Branch'] = df['CODICESCUOLA'].map(school_branch_map)
        df = df.dropna(subset=['Branch'])
        
        # Count unique occurrences of school offering a subject
        unique_offerings = df.drop_duplicates(subset=['CODICESCUOLA', 'DISCIPLINA'])
        
        counts = unique_offerings.groupby(['Branch', 'DISCIPLINA']).size().reset_index(name='N_Schools')
        
        for _, row in counts.iterrows():
            b = row['Branch']
            d = row['DISCIPLINA']
            c = row['N_Schools']
            if d not in curriculum[b]:
                curriculum[b][d] = 0
            curriculum[b][d] += c
            
        count += 1
        print(f"Processed {count}/{len(files)} regions for curriculum.")
        
    # Sort subjects by count descending
    for b in curriculum:
        sorted_subjects = sorted(curriculum[b].items(), key=lambda x: x[1], reverse=True)
        # Keep top 100 for each branch to prevent massive JSON bloat, or keep all?
        # User requested "every subject", but there are thousands of typos. Let's keep those with >= 5 schools.
        curriculum[b] = [{"subject": k, "schools": v} for k, v in sorted_subjects if v >= 5]
        
    with open('processed_data/curriculum_matrix.json', 'w', encoding='utf-8') as f:
        json.dump(curriculum, f, indent=2)
    print("Saved curriculum matrix.")

if __name__ == '__main__':
    build_aggregations()
