import nbformat as nbf
import os

def create_notebook():
    nb = nbf.v4.new_notebook()

    # Introduction
    nb.cells.append(nbf.v4.new_markdown_cell("""
# 07. Geospatial Analysis of the Education System
This notebook explores the geographical distribution of ALL Italian public AND private schools, from Kindergarten to Upper Secondary.
"""))

    # Imports
    nb.cells.append(nbf.v4.new_code_cell("""
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
import pgeocode
import os
import warnings
warnings.filterwarnings('ignore')
"""))

    # Load School Data
    nb.cells.append(nbf.v4.new_markdown_cell("""
### 1. Merging Public and Private School Registries
We load `SCUANAGRAFESTAT` (Public) and `SCUANAGRAFEPAR` (Private) datasets.
"""))

    nb.cells.append(nbf.v4.new_code_cell("""
# Load Public Schools
pub_path = '../local_data/MinIstruzione/Scuole/SCUANAGRAFESTAT20242520250831.csv'
pub_scuole = pd.read_csv(pub_path, low_memory=False)
pub_scuole['Settore'] = 'Pubblica'

# Load Private Schools
prv_path = '../local_data/MinIstruzione/Scuole/SCUANAGRAFEPAR20242520250831.csv'
prv_scuole = pd.read_csv(prv_path, low_memory=False)
prv_scuole['Settore'] = 'Privata'

# Concatenate
cols = ['ANNOSCOLASTICO', 'REGIONE', 'PROVINCIA', 'CODICESCUOLA', 
        'DENOMINAZIONESCUOLA', 'INDIRIZZOSCUOLA', 'CAPSCUOLA', 
        'CODICECOMUNESCUOLA', 'DESCRIZIONECOMUNE', 
        'DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA', 'Settore']

for c in cols:
    if c not in prv_scuole.columns:
        prv_scuole[c] = np.nan

scuole = pd.concat([pub_scuole[cols], prv_scuole[cols]], ignore_index=True)

# Categorize all school levels
def categorize_track(desc):
    desc_str = str(desc).upper()
    if 'INFANZIA' in desc_str or 'MATERNA' in desc_str: return 'Infanzia'
    if 'PRIMARIA' in desc_str: return 'Primaria'
    if 'PRIMO GRADO' in desc_str or 'MEDIA' in desc_str: return 'Primo Grado'
    if 'LICEO' in desc_str or 'MAGISTRALE' in desc_str: return 'Liceo'
    if 'TECNICO' in desc_str: return 'Tecnico'
    if 'PROFESSIONALE' in desc_str or "D'ARTE" in desc_str or 'ALBERGHIERO' in desc_str: return 'Professionale'
    if 'COMPRENSIVO' in desc_str: return 'Comprensivo (K-8)'
    return 'Altro'

scuole['Track'] = scuole['DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'].apply(categorize_track)

print(f"Loaded {len(scuole)} total School branches (Public & Private).")
scuole['Track'].value_counts()
"""))

    # Geocoding
    nb.cells.append(nbf.v4.new_markdown_cell("""
### 2. High-Precision Offline Geocoding
We use `pgeocode` to map every single school to the precise latitude and longitude of its ZIP code (`CAPSCUOLA`).
"""))

    nb.cells.append(nbf.v4.new_code_cell("""
nomi = pgeocode.Nominatim('it')

# Clean CAP codes
scuole['CAPSCUOLA'] = scuole['CAPSCUOLA'].astype(str).str.extract(r'(\\d+)')[0]
scuole['CAPSCUOLA'] = scuole['CAPSCUOLA'].str.zfill(5)

# Batch geocode
print("Geocoding based on ZIP codes... (This takes a few seconds)")
geo_data = nomi.query_postal_code(scuole['CAPSCUOLA'].tolist())

scuole['lat'] = geo_data['latitude'].values
scuole['lon'] = geo_data['longitude'].values

# Drop any that failed to geocode
spatial_scuole = scuole.dropna(subset=['lat', 'lon']).copy()
print(f"Successfully geocoded {len(spatial_scuole)} out of {len(scuole)} schools.")
"""))

    # Interactive Map
    nb.cells.append(nbf.v4.new_markdown_cell("""
### 3. Interactive Visualization (With Marker Clustering)
We generate a `folium` map showing the exact neighborhood distribution of over 50,000 schools.
We use Marker Clustering to handle the 50,000+ points efficiently.
"""))

    nb.cells.append(nbf.v4.new_code_cell("""
# Create base map centered on Italy
m = folium.Map(location=[41.8719, 12.5674], zoom_start=6, tiles='CartoDB positron')

colors = {
    'Infanzia': 'lightgreen',
    'Primaria': 'lightblue',
    'Primo Grado': 'purple',
    'Comprensivo (K-8)': 'cadetblue',
    'Liceo': 'blue', 
    'Tecnico': 'orange', 
    'Professionale': 'red',
    'Altro': 'gray'
}

np.random.seed(42)
spatial_scuole['lat_jit'] = spatial_scuole['lat'] + np.random.normal(0, 0.001, len(spatial_scuole))
spatial_scuole['lon_jit'] = spatial_scuole['lon'] + np.random.normal(0, 0.001, len(spatial_scuole))

groups = {}
for track in colors.keys():
    cluster = MarkerCluster(name=track)
    groups[track] = cluster
    m.add_child(cluster)

for idx, row in spatial_scuole.iterrows():
    track = row['Track']
    settore = row['Settore']
    
    popup_text = f"<b>{row['DENOMINAZIONESCUOLA']}</b><br>Track: {track}<br>Type: {settore}<br>City: {row['DESCRIZIONECOMUNE']}<br>CAP: {row['CAPSCUOLA']}"
    
    folium.CircleMarker(
        location=[row['lat_jit'], row['lon_jit']],
        radius=4,
        popup=folium.Popup(popup_text, max_width=300),
        color=colors.get(track, 'gray'),
        fill=True,
        fill_color=colors.get(track, 'gray'),
        fill_opacity=0.8,
        weight=1
    ).add_to(groups[track])

folium.LayerControl().add_to(m)

os.makedirs('../local_data/processed', exist_ok=True)
m.save('../local_data/processed/italy_all_schools_map.html')
print("Map generated and saved to local_data/processed/italy_all_schools_map.html")
"""))

    os.makedirs('Notebooks', exist_ok=True)
    with open('Notebooks/07_geospatial_tripartite_distribution.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    
    print("Notebook 07 updated successfully!")

if __name__ == '__main__':
    create_notebook()
