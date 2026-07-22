import urllib.request
import os
from pathlib import Path

def download_hf_file(url, local_path):
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    if not os.path.exists(local_path):
        print(f"Downloading {url} to {local_path}...")
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=30) as res, open(local_path, 'wb') as f:
                f.write(res.read())
            print("Download complete.")
        except Exception as e:
            print(f"Failed to download {url}: {e}")
    else:
        print(f"File {local_path} already exists. Skipping download.")

if __name__ == '__main__':
    files_to_download = [
        {
            "url": "https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/scuole/SCUANAGRAFESTAT.parquet",
            "local_path": "local_data/HuggingFace/scuole/SCUANAGRAFESTAT.parquet"
        },
        {
            "url": "https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/data/adozioni_libri_di_testo/ALTLOMBARDIA000020260610.parquet",
            "local_path": "local_data/HuggingFace/adozioni_libri_di_testo/ALTLOMBARDIA000020260610.parquet"
        }
    ]
    
    for item in files_to_download:
        download_hf_file(item["url"], item["local_path"])
