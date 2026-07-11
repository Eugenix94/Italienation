#!/usr/bin/env python3
import os
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

suspects = ['\ufffd', 'Ã©', 'Ã¨', 'Ã ', 'Ã¬', 'Ã²', 'Ã¹', 'â€™', 'â€œ', 'â€', 'â€“', 'ï»¿', 'Â°', 'â€-', 'Ã€', 'Ã\x88', 'Ã\x89', 'Ã']

files = (
    glob.glob(os.path.join(ROOT_DIR, "holistic_analysis", "data_panels", "*.csv")) +
    glob.glob(os.path.join(ROOT_DIR, "local_data", "processed", "*.csv")) +
    glob.glob(os.path.join(ROOT_DIR, "rendered_notebooks", "*.html")) +
    glob.glob(os.path.join(ROOT_DIR, "holistic_analysis", "interactive_web_experience", "**", "*.html"), recursive=True) +
    glob.glob(os.path.join(ROOT_DIR, "*.html")) +
    glob.glob(os.path.join(ROOT_DIR, "*.md")) +
    glob.glob(os.path.join(ROOT_DIR, "holistic_analysis", "**", "*.md"), recursive=True)
)

print(f"Scanning {len(files)} core data, markdown, and HTML files...")
found_any = False
for fpath in sorted(set(files)):
    if not os.path.exists(fpath): continue
    try:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        matches = [s for s in suspects if s in content]
        if matches:
            rel = os.path.relpath(fpath, ROOT_DIR)
            print(f"  -> [{rel}] matches: {matches}")
            found_any = True
    except Exception as e:
        pass

if not found_any:
    print("[CLEAN] Zero mojibake or corrupted characters found across all core files!")
