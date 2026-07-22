import urllib.request
import json

endpoints = [
    'https://huggingface.co/api/datasets/diatribe00/italian-schools-opendata/tree/main/data/edilizia_scolastica',
    'https://huggingface.co/api/datasets/diatribe00/italian-schools-opendata/tree/main/data/personale'
]

output = []
for url in endpoints:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            output.append(f"--- Folder: {url.split('/')[-1]} ---")
            for item in data:
                output.append(f"{item['path']} ({item.get('size', 'N/A')} bytes)")
    except Exception as e:
        output.append(f"Error fetching {url}: {e}")

with open('scratch/hf_blindspots_audit.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('Saved HF audit to scratch/hf_blindspots_audit.txt')
