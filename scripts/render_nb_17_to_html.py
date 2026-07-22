#!/usr/bin/env python3
"""
render_nb_17_to_html.py — Renders Notebook 17 to HTML inside web/rendered_notebooks/
"""
import os
import sys
import nbformat

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(errors='replace')

def convert_nb_to_html(nb_filename, out_filename):
    nb_path = os.path.join("notebooks", nb_filename)
    out_path = os.path.join("web", "rendered_notebooks", out_filename)
    if not os.path.exists(nb_path):
        print(f"File not found: {nb_path}")
        return
    
    try:
        from nbconvert import HTMLExporter
        html_exporter = HTMLExporter()
        html_exporter.template_name = 'classic'
        nb = nbformat.read(nb_path, as_version=4)
        (body, resources) = html_exporter.from_notebook_node(nb)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(body)
        print(f"Converted via nbconvert: {nb_path} -> {out_path} ({len(body)} bytes)")
    except Exception as e:
        print(f"Fallback direct HTML generator for {nb_filename} due to: {e}")
        nb = nbformat.read(nb_path, as_version=4)
        html_parts = [
            '<!DOCTYPE html><html lang="it"><head><meta charset="UTF-8"><title>' + nb_filename + '</title>',
            '<style>',
            'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #09090b; color: #f4f4f5; max-width: 1100px; margin: 0 auto; padding: 2rem; line-height: 1.6; }',
            '.cell { margin-bottom: 2rem; background: #18181b; border: 1px solid #27272a; border-radius: 12px; padding: 1.5rem; }',
            '.cell-md { border: none; background: transparent; padding: 0.5rem 0; }',
            '.cell-md h1, .cell-md h2, .cell-md h3 { color: #818cf8; margin-top: 1.5rem; }',
            'pre { background: #000; padding: 1rem; border-radius: 8px; overflow-x: auto; color: #a5b4fc; font-family: monospace; font-size: 0.85rem; }',
            'a { color: #38bdf8; text-decoration: none; }',
            'a:hover { text-decoration: underline; }',
            'table { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: 0.85rem; }',
            'th, td { border: 1px solid #27272a; padding: 0.6rem; text-align: left; }',
            'th { background: #27272a; color: #fff; }',
            '</style></head><body>',
            f'<h1>📒 {nb_filename}</h1>',
            f'<p style="color: #a1a1aa;">Rendered from Italienation Open-Science Observatory Repository.</p><hr style="border-color: #27272a; margin: 2rem 0;">'
        ]
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                source = cell.source.replace('\n', '<br>')
                html_parts.append(f'<div class="cell cell-md">{source}</div>')
            elif cell.cell_type == 'code':
                code_text = cell.source
                html_parts.append(f'<div class="cell"><strong>Python Code:</strong><pre>{code_text}</pre></div>')
        html_parts.append('</body></html>')
        html_content = "\n".join(html_parts)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Converted via fallback: {nb_path} -> {out_path} ({len(html_content)} bytes)")

if __name__ == "__main__":
    os.makedirs(os.path.join("web", "rendered_notebooks"), exist_ok=True)
    convert_nb_to_html("17_curricular_fragmentation_and_cultural_capital_synthesis.ipynb", "17_curricular_fragmentation_and_cultural_capital_synthesis.html")
