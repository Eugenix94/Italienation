import os
import csv
import json
import shutil
from collections import defaultdict

manifest_path = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\FILE_BY_FILE_PROVENANCE_MANIFEST.csv"
base_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data"
public_raw_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\frontend\public\raw_data"
frontend_catalog_json = r"C:\Users\Dell\Documents\Antigravity\Italienation\frontend\src\assets\catalog.json"

os.makedirs(public_raw_dir, exist_ok=True)

catalog = defaultdict(list)

# Define robust categories mapping
def get_category(directory):
    directory = directory.lower()
    if 'istat' in directory: return 'ISTAT - Statistiche Nazionali e Demografia'
    elif 'mur' in directory: return 'MUR - USTAT Anagrafe Universitaria'
    elif 'invalsi' in directory: return 'INVALSI - Esiti e Abbandono Implicito'
    elif 'almalaurea' in directory or 'anpal' in directory or 'inps' in directory: return 'Lavoro e Occupazione (INPS / AlmaLaurea / ANPAL)'
    elif 'mef' in directory or 'siope' in directory: return 'MEF / SIOPE - Bilanci Pubblici e IRPEF'
    elif 'eurydice' in directory or 'international' in directory or 'eurostat' in directory or 'oecd' in directory: return 'International Comparisons (Eurydice / OECD / Eurostat)'
    elif 'opencoesione' in directory: return 'OpenCoesione - PNRR'
    elif 'processed' in directory: return 'Processed & Derivative Models'
    else: return 'Altri Datasets e Fonti Specializzate'

if os.path.exists(manifest_path):
    with open(manifest_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            directory = row.get("Directory", "")
            filename = row.get("File Name", "")
            url = row.get("Direct Source URL", "")
            
            source_file = os.path.join(base_dir, directory, filename)
            dest_file = os.path.join(public_raw_dir, filename)
            
            # Copy file to public/raw_data for download (skip if > 50MB to avoid GitHub limits)
            if os.path.exists(source_file):
                try:
                    size_mb = os.path.getsize(source_file) / (1024 * 1024)
                    if size_mb <= 50:
                        shutil.copy2(source_file, dest_file)
                    else:
                        print(f"Skipping copy of {filename} (Too large: {size_mb:.2f} MB)")
                except Exception as e:
                    print(f"Error copying {filename}: {e}")
            
            # Extract institution origin
            origin = directory.split('\\')[0] if '\\' in directory else directory
            if not origin or origin == '.':
                origin = "ISTAT/WorldBank"
                
            cat_name = get_category(directory)
            
            catalog[cat_name].append({
                "title": filename,
                "url": url,
                "origin": origin,
                "raw_link": f"/raw_data/{filename}"
            })
else:
    print("Manifest not found!")

# Convert to list of categories
final_catalog = []
for cat, links in catalog.items():
    final_catalog.append({
        "category": cat,
        "links": links
    })

with open(frontend_catalog_json, 'w', encoding='utf-8') as f:
    json.dump(final_catalog, f, ensure_ascii=False, indent=2)

print(f"Catalog JSON successfully generated with {sum(len(c['links']) for c in final_catalog)} datasets across {len(final_catalog)} categories.")
