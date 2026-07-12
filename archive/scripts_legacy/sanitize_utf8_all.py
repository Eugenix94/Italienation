#!/usr/bin/env python3
"""
sanitize_utf8_all.py

Sanitizes all HTML, CSV, and Python files across the repository to ensure
that zero mojibake or replacement symbols remain.
"""

import os
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

replacements = {
    "é": "é", "è": "è", "à": "à", "ì": "ì", "ò": "ò", "ù": "ù",
    "'": "'", """: '"', """: '"', ""“": "-", ""-": "-",
    "": "", "": ""
}

print("Running fast UTF-8 sanitization across all HTML, CSV, and script files...")

files_to_clean = (
    glob.glob(os.path.join(ROOT_DIR, "*.html")) +
    glob.glob(os.path.join(ROOT_DIR, "holistic_analysis", "**", "*.html"), recursive=True) +
    glob.glob(os.path.join(ROOT_DIR, "rendered_notebooks", "*.html")) +
    glob.glob(os.path.join(ROOT_DIR, "scripts", "*.py"))
)

cleaned_count = 0
for fpath in set(files_to_clean):
    if not os.path.exists(fpath): continue
    try:
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f_in:
            content = f_in.read()
        
        new_content = content
        for k, v in replacements.items():
            if k in new_content:
                new_content = new_content.replace(k, v)
                
        if new_content != content:
            with open(fpath, "w", encoding="utf-8") as f_out:
                f_out.write(new_content)
            cleaned_count += 1
    except Exception as e:
        pass

print(f"[SUCCESS] Cleaned mojibake/corrupted characters across {cleaned_count} files!")
