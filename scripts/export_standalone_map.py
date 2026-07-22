#!/usr/bin/env python3
"""
export_standalone_map.py — Generates a pure HTML map of Italian Schools and Catania Case Study.
This map is meant to be embedded directly into index.html via an iframe.
"""
import os
import sys
import pandas as pd
import folium
from folium.plugins import MarkerCluster

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_DATA = os.path.join(ROOT, "local_data", "processed")
OUT_FILE = os.path.join(ROOT, "web", "interactive_map.html")

print("Loading datasets...")
try:
    catania_df = pd.read_csv(os.path.join(LOCAL_DATA, "catania_geospatial_schools_case_study.csv"))
    nat_sample = pd.read_csv(os.path.join(LOCAL_DATA, "italy_national_schools_geospatial_sample.csv"))
except Exception as e:
    print(f"Error loading datasets: {e}")
    sys.exit(1)

# Filter valid coordinates
superiori = ['Liceo (Accademico)', 'Istituto Tecnico', 'Istituto Professionale']
ct_sup = catania_df[catania_df['TRACK_TRIPARTITO'].isin(superiori)].dropna(subset=['LATITUDINE', 'LONGITUDINE'])
nat_sample = nat_sample.dropna(subset=['LATITUDINE', 'LONGITUDINE'])

print(f"Plotting {len(ct_sup)} Catania upper secondary schools and {len(nat_sample)} national sample schools...")

color_map = {
    'Liceo (Accademico)': '#3b82f6', # Blue
    'Istituto Tecnico': '#10b981',   # Green
    'Istituto Professionale': '#ef4444' # Red
}

# Create a map centered on Italy but biased slightly towards South to show Catania too
m = folium.Map(location=[41.8719, 12.5674], zoom_start=6, tiles="CartoDB dark_matter", control_scale=True)

# 1. National Sample Cluster
marker_cluster = MarkerCluster(name="Campione Nazionale").add_to(m)
for idx, row in nat_sample.iterrows():
    track = row['TRACK_TRIPARTITO']
    folium.CircleMarker(
        location=[row['LATITUDINE'], row['LONGITUDINE']],
        radius=4,
        color=color_map.get(track, '#ffffff'),
        fill=True,
        fill_opacity=0.6,
        tooltip=track
    ).add_to(marker_cluster)

# 2. Catania Focus Feature Group (always visible at zoom levels)
catania_group = folium.FeatureGroup(name="Catania Case Study (Dettaglio)").add_to(m)
for idx, row in ct_sup.iterrows():
    track = row['TRACK_TRIPARTITO']
    nome = row.get('DENOMINAZIONESCUOLA', track)
    # Ensure escaping single quotes for HTML
    nome = str(nome).replace("'", "&#39;")
    
    popup_html = f"<div style='font-family:sans-serif;width:200px;'><b>{nome}</b><br><span style='color:{color_map.get(track, '#000')};font-weight:bold;'>{track}</span></div>"
    
    folium.CircleMarker(
        location=[row['LATITUDINE'], row['LONGITUDINE']],
        radius=7,
        color=color_map.get(track, 'gray'),
        fill=True,
        fill_color=color_map.get(track, 'gray'),
        fill_opacity=0.9,
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=nome
    ).add_to(catania_group)

# Add Layer Control to toggle views
folium.LayerControl().add_to(m)

# To ensure the map fits the iframe perfectly, we don't need much customization here, Folium defaults to 100% width/height.
print(f"Saving map to {OUT_FILE}...")
m.save(OUT_FILE)
print("Done!")
