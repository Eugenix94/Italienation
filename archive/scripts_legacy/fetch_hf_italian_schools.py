import urllib.request
import pandas as pd
import io
import os
import json

output_dir = "local_data/HuggingFace"
os.makedirs(output_dir, exist_ok=True)

# List of key files to download and inspect/summarize
files_to_download = [
    ("personale_scuola/DOCSUPXXV20242520250831.parquet", "hf_teachers_suppl_2024_25.parquet"),
    ("personale_scuola/ATASUP20242520250831.parquet", "hf_ata_suppl_2024_25.parquet"),
    ("personale/DOCTIT.parquet", "hf_teachers_titular.parquet"),
    ("studenti/ALUSECGRADOINDSTA.parquet", "hf_students_upper_sec_stat_2024_25.parquet"),
    ("scuole/SCUANAGRAFESTAT.parquet", "hf_schools_registry_stat.parquet"),
    ("valutazione/VALUTAZIONE_ESITI_STA.parquet", "hf_evaluation_outcomes_stat.parquet")
]

base_url = "https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data"

summary_report = {}

for remote_path, local_name in files_to_download:
    url = f"{base_url}/{remote_path}"
    local_path = os.path.join(output_dir, local_name)
    print(f"Downloading {url} to {local_path}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(local_path, 'wb') as out_file:
            out_file.write(response.read())
        
        # Read parquet using pandas
        df = pd.read_parquet(local_path)
        print(f"Successfully loaded {local_name}: {df.shape[0]:,} rows, {df.shape[1]} cols")
        summary_report[local_name] = {
            "rows": df.shape[0],
            "cols": df.shape[1],
            "columns": df.columns.tolist(),
            "head": df.head(3).to_dict(orient="records")
        }
    except Exception as e:
        print(f"Failed {remote_path}: {e}")

with open(os.path.join(output_dir, "manifest_summary.json"), "w", encoding="utf-8") as f:
    json.dump(summary_report, f, indent=2, default=str)

print("Saved summary report to local_data/HuggingFace/manifest_summary.json")
