import urllib.request
import json
import os

base_url = "https://huggingface.co/api/datasets/diatribe00/italian-schools-opendata/tree/main/data"
req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    data = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    print("Top-level dirs:", [d['path'] for d in data])
    for d in data:
        path = d['path']
        sub_url = f"https://huggingface.co/api/datasets/diatribe00/italian-schools-opendata/tree/main/{path}"
        sub_req = urllib.request.Request(sub_url, headers={'User-Agent': 'Mozilla/5.0'})
        sub_data = json.loads(urllib.request.urlopen(sub_req).read().decode('utf-8'))
        print(f"\n--- {path} ---")
        for item in sub_data:
            print(f"  {item['path']} ({item.get('size', 0):,} bytes)")
except Exception as e:
    print("Error:", e)
