import os
import json
import csv

PROCESSED_DIR = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\processed"
OUTPUT_FILE = r"C:\Users\Dell\Documents\Antigravity\Italienation\frontend\src\assets\master_data_observatory.json"

categories = {
    "Origin": ["gini", "household", "nido", "demographic", "cost", "textbook"],
    "Education": ["orario", "ptof", "pcto", "bocciati", "invalsi", "tutoring", "diplomifici", "curriculum", "subtrack", "tripartite_territorial"],
    "Destination": ["employment", "almadiploma", "adults_living", "brain_drain", "migration", "financial", "tripartite_vs", "eurydice", "oecd"],
    "Macro-Finance": ["gdp", "macro_cost", "pnrr"]
}

def categorize_file(filename):
    lower_f = filename.lower()
    for cat, keywords in categories.items():
        if any(kw in lower_f for kw in keywords):
            return cat
    return "Other"

master_data = {
    "Origin": [],
    "Education": [],
    "Destination": [],
    "Macro-Finance": [],
    "Other": []
}

for f in os.listdir(PROCESSED_DIR):
    if f.endswith('.csv'):
        filepath = os.path.join(PROCESSED_DIR, f)
        
        # Skip files larger than 1MB to prevent browser memory issues
        size = os.path.getsize(filepath)
        if size > 1000000:
            print(f"Skipping {f} (Too large: {size} bytes)")
            continue
            
        cat = categorize_file(f)
        try:
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
                
                master_data[cat].append({
                    "id": f.replace('.csv', ''),
                    "filename": f,
                    "data": data,
                    "columns": reader.fieldnames if reader.fieldnames else []
                })
        except Exception as e:
            print(f"Error parsing {f}: {e}")

with open(OUTPUT_FILE, 'w', encoding='utf-8') as jfile:
    json.dump(master_data, jfile, ensure_ascii=False)

print(f"Master JSON built successfully with {sum(len(v) for v in master_data.values())} datasets.")
