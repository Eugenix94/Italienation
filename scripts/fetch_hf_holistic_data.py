import os
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET_DIR_PERSONALE = ROOT / "local_data" / "huggingface" / "personale"
TARGET_DIR_EDILIZIA = ROOT / "local_data" / "huggingface" / "edilizia_scolastica"

TARGET_DIR_PERSONALE.mkdir(parents=True, exist_ok=True)
TARGET_DIR_EDILIZIA.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data"

FILES = {
    "personale/DOCSUPXXV.parquet": TARGET_DIR_PERSONALE / "DOCSUPXXV.parquet",
    "personale/DOCTIT.parquet": TARGET_DIR_PERSONALE / "DOCTIT.parquet",
    "edilizia_scolastica/EDICONSICUREZZASTA202120242520250806.parquet": TARGET_DIR_EDILIZIA / "EDICONSICUREZZASTA202120242520250806.parquet",
    "edilizia_scolastica/EDIAMBIENTESTA202120242520250806.parquet": TARGET_DIR_EDILIZIA / "EDIAMBIENTESTA202120242520250806.parquet",
    "edilizia_scolastica/EDIANAGRAFESTA202120242520250806.parquet": TARGET_DIR_EDILIZIA / "EDIANAGRAFESTA202120242520250806.parquet"
}

print("=== Fetching Holistic Data from HuggingFace Mirror ===")
for url_path, dest_path in FILES.items():
    if not dest_path.exists():
        url = f"{BASE_URL}/{url_path}"
        print(f"Downloading {url} ...")
        try:
            urllib.request.urlretrieve(url, dest_path)
            print(f"  -> Saved to {dest_path}")
        except Exception as e:
            print(f"  -> Failed: {e}")
    else:
        print(f"File already exists: {dest_path}")
print("Done.")
