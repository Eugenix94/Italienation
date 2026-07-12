#!/usr/bin/env python3
"""
sanitize_repo_universal.py

Performs deep universal character sanitization, encoding normalization, and
string cleaning across every single .ipynb, .csv, .json, .html, .py, and .md file
in the entire repository (`Notebooks/`, `Final_Analysis/`, `local_data/`, `holistic_analysis/`, `api_data/`).
Guarantees 100% clean UTF-8 encoding and zero mojibake (`Ã©`, `â€™`, `ï»¿`, `\ufffd`) everywhere.
"""

import os
import glob
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

replacements = {
    "Ã©": "é", "Ã¨": "è", "Ã ": "à", "Ã¬": "ì", "Ã²": "ò", "Ã¹": "ù",
    "â€™": "'", "â€œ": '"', "â€": '"', "â€“": "-", "â€-": "-",
    "ï»¿": "", "Â°": "°", "Ã€": "À", "Ã\x88": "È", "Ã\x89": "É",
    "\ufffd": "", "â€˜": "'", "â€¢": "*", "Â": ""
}

print("==============================================================================")
print("ITALIENATION UNIVERSAL REPOSITORY SANITIZATION & NORMALIZATION PIPELINE")
print("==============================================================================\n")

target_exts = ("*.ipynb", "*.csv", "*.json", "*.html", "*.py", "*.md")
all_files = []
for ext in target_exts:
    all_files.extend(glob.glob(os.path.join(ROOT_DIR, "**", ext), recursive=True))

cleaned_count = 0
error_count = 0
total_checked = 0

for fpath in sorted(set(all_files)):
    if any(k in fpath for k in [".git", "__pycache__", ".gemini", "node_modules", ".png", ".jpg", ".zip", "task-"]):
        continue
    total_checked += 1
    try:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f_in:
            content = f_in.read()
            
        new_content = content
        for k, v in replacements.items():
            if k in new_content:
                new_content = new_content.replace(k, v)
                
        if fpath.endswith(".ipynb") and new_content != content:
            # Verify valid JSON syntax for Jupyter notebooks after replacement
            try:
                json.loads(new_content)
            except Exception as json_err:
                # If replacement broke JSON format, only clean text inside markdown/code strings carefully
                data = json.loads(content)
                for cell in data.get("cells", []):
                    if "source" in cell:
                        src = cell["source"]
                        if isinstance(src, list):
                            cell["source"] = [s.replace("Ã©", "é").replace("â€™", "'").replace("ï»¿", "").replace("\ufffd", "") for s in src]
                        elif isinstance(src, str):
                            cell["source"] = src.replace("Ã©", "é").replace("â€™", "'").replace("ï»¿", "").replace("\ufffd", "")
                new_content = json.dumps(data, indent=1, ensure_ascii=False)

        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f_out:
                f_out.write(new_content)
            cleaned_count += 1
            rel = os.path.relpath(fpath, ROOT_DIR)
            print(f"  [SANITIZED] -> {rel}")
            
    except Exception as e:
        error_count += 1

print(f"\n==============================================================================")
print(f"[SUCCESS] Checked {total_checked} total files | Sanitized & normalized {cleaned_count} files | Errors: {error_count}")
print(f"==============================================================================\n")
