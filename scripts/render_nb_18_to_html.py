#!/usr/bin/env python3
"""
render_nb_18_to_html.py — Renders Notebook 18 to HTML
"""
import os
import sys
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
nb_path = os.path.join(ROOT, "notebooks", "18_geospatial_catania_case_study_and_national_map.ipynb")
out_dir = os.path.join(ROOT, "web", "rendered_notebooks")
out_path = os.path.join(out_dir, "18_geospatial_catania_case_study_and_national_map.html")

os.makedirs(out_dir, exist_ok=True)

print(f"Reading {nb_path}...")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

html = [
    "<!DOCTYPE html>",
    "<html lang='it'>",
    "<head>",
    "<meta charset='UTF-8'>",
    "<title>18. Esplorazione Geospaziale e Case Study Catania</title>",
    "<style>",
    "body { font-family: 'Inter', -apple-system, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 2rem; background: #fdfdfd; }",
    "pre { background: #f4f4f4; padding: 1rem; border-radius: 8px; overflow-x: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.9em; border: 1px solid #e1e4e8; }",
    "code { font-family: 'JetBrains Mono', monospace; background: #f4f4f4; padding: 0.2rem 0.4rem; border-radius: 4px; font-size: 0.9em; }",
    "h1, h2, h3 { color: #111; margin-top: 2rem; }",
    ".cell { margin-bottom: 2rem; }",
    ".output { background: #fff; border: 1px solid #ddd; padding: 1rem; border-radius: 8px; margin-top: 0.5rem; }",
    "table { border-collapse: collapse; width: 100%; margin-top: 1rem; }",
    "th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }",
    "th { background-color: #f8f9fa; }",
    "blockquote { border-left: 4px solid #0366d6; margin: 0; padding-left: 1rem; color: #555; background: #f1f8ff; padding: 1rem; border-radius: 0 8px 8px 0; }",
    "</style>",
    "</head>",
    "<body>"
]

import markdown
for cell in nb.get('cells', []):
    html.append("<div class='cell'>")
    if cell['cell_type'] == 'markdown':
        src = "".join(cell['source'])
        md_html = markdown.markdown(src, extensions=['tables'])
        html.append(md_html)
    elif cell['cell_type'] == 'code':
        src = "".join(cell['source'])
        html.append(f"<pre><code>{src}</code></pre>")
        if cell.get('outputs'):
            html.append("<div class='output'>")
            for out in cell['outputs']:
                if out.get('output_type') == 'stream':
                    text = "".join(out.get('text', ''))
                    html.append(f"<pre>{text}</pre>")
                elif out.get('output_type') == 'execute_result' and 'data' in out:
                    if 'text/html' in out['data']:
                        html.append("".join(out['data']['text/html']))
                    elif 'text/plain' in out['data']:
                        html.append(f"<pre>"+"".join(out['data']['text/plain'])+"</pre>")
            html.append("</div>")
    html.append("</div>")

html.append("</body></html>")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(html))

print(f"Rendered HTML saved to {out_path}")
