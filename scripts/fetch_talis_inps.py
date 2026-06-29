import os
import requests
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OECD_DIR = ROOT / "local_data" / "oecd"
INPS_DIR = ROOT / "local_data" / "INPS"

OECD_DIR.mkdir(parents=True, exist_ok=True)
INPS_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0"}

def download_file(url, out_path):
    print(f"Downloading {url} to {out_path}...")
    try:
        response = requests.get(url, headers=HEADERS, timeout=60, verify=False)
        response.raise_for_status()
        with open(out_path, "wb") as f:
            f.write(response.content)
        print(f"Success. Size: {out_path.stat().st_size} bytes")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# 1. TALIS
talis_url = "https://www.oecd.org/content/dam/oecd/en/about/programmes/edu/talis/directories-index/TALIS_cycles_participation.xlsx/_jcr_content/renditions/original.media_file.download_attachment.file/TALIS_cycles_participation.xlsx"
download_file(talis_url, OECD_DIR / "TALIS_cycles_participation.xlsx")

# 2. INPS
inps_urls = {
    "ID-5515.csv": "https://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5515.csv",
    "ID-5516.csv": "https://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5516.csv",
    "ID-5139.csv": "https://www.inps.it/docallegati/Mig/OpenData/CSV/ID-5139.csv",
    "ID-2326.csv": "https://www.inps.it/docallegati/Mig/OpenData/ID-2326.csv",
    "ID-2324.csv": "https://www.inps.it/docallegati/Mig/OpenData/ID-2324.csv"
}
for name, url in inps_urls.items():
    download_file(url, INPS_DIR / name)
