import json

with open('local_data/HuggingFace/manifest_summary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in data.items():
    print(f"=== {k} ({v['rows']} rows) ===")
    print("Columns:", v['columns'])
    if v['head']:
        print("Sample row:")
        for col, val in v['head'][0].items():
            print(f"  {col}: {val}")
    print()
