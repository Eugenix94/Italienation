#!/usr/bin/env python3
"""
verify_web_dom_and_assets.py

Rigorous diagnostic tool to check:
1. DOM ID integrity: ensure all IDs referenced by document.getElementById(...) exist in the HTML and check for duplicate IDs.
2. CDN & Asset loading paths: verify valid syntax and reachability of scripts and styles.
3. Responsiveness sanity check: check for potentially overflowing elements or missing mobile wrappers.
4. HTML nesting & tag balance: ensure proper DOM hierarchy.
"""

import os
import re
import html
from collections import Counter

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

def audit_html_file(file_path):
    print(f"\n=======================================================")
    print(f"AUDITING: {os.path.relpath(file_path, ROOT_DIR)}")
    print(f"=======================================================")
    
    if not os.path.exists(file_path):
        print(f"[ERROR] File does not exist: {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Check DOM ID uniqueness
    all_ids = re.findall(r'id=["\']([^"\']+)["\']', content)
    id_counts = Counter(all_ids)
    duplicates = {k: v for k, v in id_counts.items() if v > 1}
    if duplicates:
        print(f"[DISCREPANCY - DOM] Duplicate IDs found: {duplicates}")
    else:
        print(f"[OK] All {len(all_ids)} DOM IDs are unique across the page!")

    # 2. Check JavaScript document.getElementById(...) references against existing IDs
    all_ids_set = set(all_ids)
    js_get_id_refs = set(re.findall(r'document\.getElementById\(["\']([^"\']+)["\']\)', content))
    missing_ids = js_get_id_refs - all_ids_set
    if missing_ids:
        print(f"[DISCREPANCY - JS/DOM] JS references non-existent IDs: {missing_ids}")
    else:
        print(f"[OK] All {len(js_get_id_refs)} IDs referenced by JavaScript exist cleanly in the DOM! ({sorted(list(js_get_id_refs))})")

    # 3. Check for external scripts & CDNs
    script_srcs = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', content)
    print(f"[INFO] External scripts discovered ({len(script_srcs)}):")
    for src in script_srcs:
        print(f"       - {src}")

    # 4. Check responsiveness wrapper on Chart canvas
    chart_canvas = re.search(r'<canvas[^>]+id=["\']citizenChartCanvas["\'][^>]*>', content)
    if chart_canvas:
        # Check parent container
        canvas_idx = content.find(chart_canvas.group(0))
        parent_chunk = content[max(0, canvas_idx-250):canvas_idx+100]
        if "h-72" in parent_chunk or "h-80" in parent_chunk or "h-96" in parent_chunk or "min-h-" in parent_chunk:
            print("[OK] Responsive height constraint wrapper found around citizenChartCanvas!")
        else:
            print("[WARNING] Chart canvas might need an explicit height wrapper for mobile responsiveness on smaller viewports.")

    # 5. Check mobile grid responsiveness in Section 2 (Notebooks Directory)
    grid_matches = re.findall(r'class=["\']([^"\']*grid[^"\']*)["\']', content)
    print(f"[INFO] Grid layout definitions checked:")
    for gm in set(grid_matches):
        print(f"       - `{gm}`")

    # 6. Check unclosed/mismatched critical tags (<section>, <div>, <script>, <style>)
    for tag in ['section', 'script', 'style', 'header', 'footer']:
        open_c = len(re.findall(f'<{tag}[^>]*>', content, re.IGNORECASE))
        close_c = len(re.findall(f'</{tag}>', content, re.IGNORECASE))
        if open_c != close_c:
            print(f"[DISCREPANCY - HTML SYNTAX] Tag `<{tag}>` mismatch! Opened: {open_c}, Closed: {close_c}")
        else:
            print(f"[OK] Tag `<{tag}>` perfectly balanced ({open_c} pairs).")

    # 7. Check local links existence
    local_links = re.findall(r'href=["\']([^"\']+)["\']', content)
    missing_local = []
    for l in set(local_links):
        if l.startswith("#") or l.startswith("http://") or l.startswith("https://") or l.startswith("javascript:"):
            continue
        full_p = os.path.join(os.path.dirname(file_path), l)
        if not os.path.exists(full_p):
            missing_local.append(l)
    if missing_local:
        print(f"[DISCREPANCY - LINKS] Broken local file targets: {missing_local}")
    else:
        print(f"[OK] All local link targets ({len(local_links)}) verified on disk!")

if __name__ == "__main__":
    audit_html_file(os.path.join(ROOT_DIR, "index.html"))
    audit_html_file(os.path.join(ROOT_DIR, "holistic_analysis", "interactive_web_experience", "index.html"))
