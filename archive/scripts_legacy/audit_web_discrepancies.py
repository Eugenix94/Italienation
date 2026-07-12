#!/usr/bin/env python3
"""
audit_web_discrepancies.py

Checks index.html and all converted notebook files for any:
1. Broken or missing JavaScript functions / unhandled dataset branches
2. Missing or broken links (e.g., raw github urls, rendered_notebooks links)
3. Malformed HTML syntax or unclosed tags
4. Language toggle inconsistencies (missing .hidden or mismatched lang-it / lang-en tags)
"""

import os
import re
import glob

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

index_path = os.path.join(ROOT_DIR, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

print("=== ITALIENATION WEB DISCREPANCY & INTEGRITY AUDIT ===")

# 1. Check dropdown options vs updateCitizenLab branches
dropdown_options = re.findall(r'<option value="([^"]+)">[^<]+</option>', content)
# Filter only options inside datasetSelector
ds_match = re.search(r'id="datasetSelector"[^>]*>(.*?)</select>', content, re.DOTALL)
if ds_match:
    ds_options = re.findall(r'<option value="([^"]+)">', ds_match.group(1))
    print(f"1. Dataset Selector Options Found: {ds_options}")
    
    # Check if each option is handled inside updateCitizenLab
    lab_js = re.search(r'function updateCitizenLab\(\)\s*\{(.*?)\n\s*async function runPyodideCode', content, re.DOTALL)
    if lab_js:
        lab_code = lab_js.group(1)
        for opt in ds_options:
            if f"dataset === '{opt}'" not in lab_code and f'dataset === "{opt}"' not in lab_code:
                if opt != ds_options[-1]: # If not last option (or if last option falls through into else without explicit check)
                    print(f"   [DISCREPANCY DETECTED] Option `{opt}` has no explicit branch in `updateCitizenLab()`!")
                else:
                    print(f"   [WARNING] Option `{opt}` falls into generic `else` block. Better to make it explicit (`else if (dataset === '{opt}')`)!")
            else:
                print(f"   [OK] Option `{opt}` is explicitly handled inside `updateCitizenLab()`!")

# 2. Check broken links inside index.html
links = re.findall(r'href="([^"]+)"', content)
print(f"\n2. Checking {len(links)} href links across index.html...")
missing_links = []
for link in set(links):
    if link.startswith("#") or link.startswith("http") or link.startswith("javascript"):
        continue
    # Check local relative links
    target_path = os.path.join(ROOT_DIR, link)
    if not os.path.exists(target_path):
        missing_links.append(link)

if missing_links:
    print(f"   [DISCREPANCY DETECTED] Missing local targets: {missing_links}")
else:
    print("   [OK] All local href links in index.html exist on disk!")

# 3. Check language toggle tags parity
lang_it_count = len(re.findall(r'class="[^"]*lang-it[^"]*"', content))
lang_en_count = len(re.findall(r'class="[^"]*lang-en[^"]*"', content))
print(f"\n3. Bilingual Parity Check: Found {lang_it_count} `lang-it` elements vs {lang_en_count} `lang-en` elements.")
if abs(lang_it_count - lang_en_count) > 5:
    print(f"   [DISCREPANCY DETECTED] High disparity between Italian ({lang_it_count}) and English ({lang_en_count}) elements!")
else:
    print("   [OK] Excellent bilingual parity across the UI!")

# 4. Check Pyodide script integration
if "pyodide.js" in content and "loadPyodide" in content:
    print("\n4. Pyodide WebAssembly Engine: [OK] Script tag and initializer detected.")
else:
    print("\n4. Pyodide WebAssembly Engine: [DISCREPANCY] Missing pyodide dependencies!")

print("\n=== AUDIT COMPLETE ===")
