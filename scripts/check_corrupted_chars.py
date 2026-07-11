#!/usr/bin/env python3
import os
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

suspects = ['\ufffd', 'Ã©', 'Ã¨', 'Ã ', 'Ã¬', 'Ã²', 'Ã¹', 'â€™', 'â€œ', 'â€', 'â€“', 'ï»¿', 'Â°', 'â€-', 'Ã€', 'Ã\x88', 'Ã\x89']

print("Searching every file in the repository for TRUE mojibake or corrupted characters...")
count = 0
for fpath in glob.glob(os.path.join(ROOT_DIR, "**", "*.*"), recursive=True):
    if ".git" in fpath or "__pycache__" in fpath or ".gemini" in fpath or "node_modules" in fpath or fpath.endswith(".png") or fpath.endswith(".jpg"):
        continue
    try:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        found = [s for s in suspects if s in content]
        if found:
            rel = os.path.relpath(fpath, ROOT_DIR)
            print(f"[{rel}] contains true suspicious sequences: {found[:5]}")
            count += 1
            if count >= 40:
                print("... (showing first 40 matches only)")
                break
    except Exception:
        pass

if count == 0:
    print("Zero files found with these specific true corrupted sequences!")
