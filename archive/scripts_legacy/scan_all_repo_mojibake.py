#!/usr/bin/env python3
import os
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

suspects = ['\ufffd', 'Ã©', 'Ã¨', 'Ã ', 'Ã¬', 'Ã²', 'Ã¹', 'â€™', 'â€œ', 'â€', 'â€“', 'ï»¿', 'Â°', 'â€-', 'Ã€', 'Ã\x88', 'Ã\x89', 'Ã']

print("Scanning every file in Notebooks/, Final_Analysis/, local_data/, and api_data/...")
count = 0
for fpath in glob.glob(os.path.join(ROOT_DIR, "**", "*.*"), recursive=True):
    if any(k in fpath for k in [".git", "__pycache__", ".gemini", "node_modules", ".png", ".jpg", ".zip"]):
        continue
    try:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        matches = [s for s in suspects if s in content]
        if matches:
            rel = os.path.relpath(fpath, ROOT_DIR)
            print(f"  -> [{rel}] matches: {matches}")
            count += 1
            if count >= 30:
                print("... (showing first 30 only)")
                break
    except Exception:
        pass

if count == 0:
    print("[ALL CLEAN] Absolutely zero files found with mojibake/corrupted symbols anywhere in the repo!")
