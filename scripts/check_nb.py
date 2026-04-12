import json
from pathlib import Path
nb_path = Path('Notebooks/italy_neet_full_analysis.ipynb')
print('File size:', nb_path.stat().st_size, 'bytes')
nb = json.loads(nb_path.read_text(encoding='utf-8'))
print('nbformat:', nb['nbformat'])
cells = nb['cells']
code_cells = [c for c in cells if c['cell_type'] == 'code']
md_cells   = [c for c in cells if c['cell_type'] == 'markdown']
print(f'Total cells: {len(cells)} ({len(code_cells)} code, {len(md_cells)} markdown)')
for i, cell in enumerate(cells):
    src = ''.join(cell['source'])
    tag = cell['cell_type'][:4].upper()
    print(f'  [{i:02d}] {tag} | {src[:70].strip()}')
print()
print('JSON valid. Notebook ready.')
