#!/usr/bin/env python3
"""
convert_all_notebooks_to_html.py

Converts all 21+ Jupyter notebooks (.ipynb) across `Notebooks/` and `Final_Analysis/`
into standalone HTML files in `rendered_notebooks/` using jupyter nbconvert.
Includes UTF-8 sanitization to ensure no mojibake or replacement characters emerge.
"""

import os
import glob
import subprocess

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")
OUT_DIR_ROOT = os.path.join(ROOT_DIR, "rendered_notebooks")
OUT_DIR_WEB = os.path.join(ROOT_DIR, "holistic_analysis", "interactive_web_experience", "rendered_notebooks")

os.makedirs(OUT_DIR_ROOT, exist_ok=True)
os.makedirs(OUT_DIR_WEB, exist_ok=True)

def clean_html_text(text):
    if not isinstance(text, str):
        return str(text)
    replacements = {
        "é": "é", "è": "è", "à": "à", "ì": "ì", "ò": "ò", "ù": "ù",
        "'": "'", """: '"', """: '"', ""“": "-", ""-": "-",
        "": "", "": ""
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text

print(f"Scanning for all .ipynb notebooks in {ROOT_DIR}...")
notebooks = sorted(glob.glob(os.path.join(ROOT_DIR, "**", "*.ipynb"), recursive=True))

converted_count = 0
for nb_path in notebooks:
    if ".ipynb_checkpoints" in nb_path:
        continue
    fname = os.path.basename(nb_path)
    base_name = os.path.splitext(fname)[0]
    out_html_root = os.path.join(OUT_DIR_ROOT, base_name + ".html")
    out_html_web = os.path.join(OUT_DIR_WEB, base_name + ".html")
    
    print(f"--> Converting {fname} to HTML...")
    try:
        # Run nbconvert
        cmd = [
            "py", "-m", "jupyter", "nbconvert",
            "--to", "html",
            "--theme", "dark",
            "--output", base_name,
            "--output-dir", OUT_DIR_ROOT,
            nb_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Clean and copy from OUT_DIR_ROOT to OUT_DIR_WEB
        if os.path.exists(out_html_root):
            with open(out_html_root, "r", encoding="utf-8", errors="ignore") as f_in:
                html_data = clean_html_text(f_in.read())
            with open(out_html_root, "w", encoding="utf-8") as f_clean:
                f_clean.write(html_data)
            with open(out_html_web, "w", encoding="utf-8") as f_out:
                f_out.write(html_data)
            converted_count += 1
            print(f"    [OK] Saved cleaned HTML to {out_html_root} and {out_html_web}")
    except Exception as e:
        print(f"    [WARN] Failed to convert {fname}: {e}")

print(f"\n[SUCCESS] Successfully converted and cleaned {converted_count} notebooks into standalone HTML viewers!")
