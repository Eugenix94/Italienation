import os
import json

MASTER_JSON_PATH = r"C:\Users\Dell\Documents\Antigravity\Italienation\frontend\src\assets\master_data_observatory.json"
API_DIR = r"C:\Users\Dell\Documents\Antigravity\Italienation\frontend\public\api\v1"

if not os.path.exists(API_DIR):
    os.makedirs(API_DIR)

print(f"Reading master data from {MASTER_JSON_PATH}...")
with open(MASTER_JSON_PATH, 'r', encoding='utf-8') as f:
    master_data = json.load(f)

# Dump master catalogue index
catalogue = []
for category, datasets in master_data.items():
    cat_dir = os.path.join(API_DIR, category.lower())
    if not os.path.exists(cat_dir):
        os.makedirs(cat_dir)
        
    for ds in datasets:
        ds_id = ds['id']
        catalogue.append({
            "id": ds_id,
            "category": category,
            "endpoint": f"/api/v1/{category.lower()}/{ds_id}.json",
            "rows": len(ds['data'])
        })
        
        # Dump individual endpoint
        ds_path = os.path.join(cat_dir, f"{ds_id}.json")
        with open(ds_path, 'w', encoding='utf-8') as ds_out:
            json.dump(ds, ds_out, ensure_ascii=False)
        print(f"Created endpoint: {ds_path}")

# Dump the index file
index_path = os.path.join(API_DIR, "index.json")
with open(index_path, 'w', encoding='utf-8') as idx_out:
    json.dump({"version": "1.0", "datasets": catalogue}, idx_out, ensure_ascii=False)

print(f"API Generation complete. Built index with {len(catalogue)} datasets.")
