import urllib.request
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT_DIR / "local_data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("=== CHECKING HUGGINGFACE REPO (`diatribe00/italian-schools-opendata`) COMPLETE TREE ===")

base_api_url = "https://huggingface.co/api/datasets/diatribe00/italian-schools-opendata/tree/main/data"

folders = [
    "adozioni_libri_di_testo",
    "edifici",
    "edilizia_scolastica",
    "mur",
    "personale",
    "personale_scuola",
    "scuola_in_chiaro",
    "scuole",
    "sistema_nazionale_di_valutazione",
    "studenti",
    "valutazione"
]

all_hf_files = []

for f in folders:
    url = f"{base_api_url}/{f}"
    print(f"Querying HF API for `data/{f}`...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Italienation-OpenScience-Client/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            items = json.loads(resp.read().decode("utf-8"))
            for item in items:
                all_hf_files.append({
                    "folder": f,
                    "path": item.get("path"),
                    "type": item.get("type"),
                    "size_bytes": item.get("size", 0)
                })
    except Exception as e:
        print(f"  [ERROR querying `data/{f}`]: {e}")

print(f"\nDiscovered `{len(all_hf_files)}` total files/items across all 11 directories on HuggingFace.")

# Save inventory to JSON
out_json = PROCESSED_DIR / "HF_DATASET_COMPLETE_INVENTORY.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(all_hf_files, f, indent=2, ensure_ascii=False)

# Print summary table
from collections import defaultdict
folder_counts = defaultdict(int)
folder_sizes = defaultdict(int)
for item in all_hf_files:
    if item["type"] == "file":
        folder_counts[item["folder"]] += 1
        folder_sizes[item["folder"]] += item["size_bytes"]

print("\n--- HUGGINGFACE DIRECTORY SUMMARY ---")
for f in folders:
    cnt = folder_counts[f]
    size_mb = round(folder_sizes[f] / (1024 * 1024), 2)
    print(f"* `data/{f}`: {cnt} files ({size_mb} MB)")

# List top files inside high-value folders: studenti, personale, valutazione, adozioni_libri_di_testo
print("\n--- KEY HIGH-VALUE FILES IN `studenti`, `personale_scuola`, `valutazione`, `adozioni_libri_di_testo` ---")
for item in all_hf_files:
    if item["folder"] in ["studenti", "personale_scuola", "valutazione", "adozioni_libri_di_testo", "sistema_nazionale_di_valutazione"]:
        print(f"  [{item['folder']}] -> {item['path']} ({round(item['size_bytes']/1024, 1)} KB)")

print("=== HF TREE CHECK COMPLETE ===")
