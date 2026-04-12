r"""
Run all code cells from italy_neet_full_analysis.ipynb as a plain Python script.
Uses matplotlib Agg (headless) and replaces display() with print().
Run from workspace root: .venv\Scripts\python.exe scripts/run_notebook_cells.py
"""
import json, re
from pathlib import Path
import matplotlib
matplotlib.use('Agg')

nb_path = Path('Notebooks/italy_neet_full_analysis.ipynb')
nb = json.loads(nb_path.read_text(encoding='utf-8'))

# Patch: replace display() with print(), plt.show() with plt.close()
def patch_cell(src):
    src = src.replace('display(', 'print(')
    src = src.replace('plt.show()', 'plt.close()')
    # savefig already calls plt.show() inside it - replace there too
    return src

globs = {}
errors = []
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] != 'code':
        continue
    src = ''.join(cell['source'])
    src = patch_cell(src)
    try:
        exec(compile(src, f'<cell {i}>', 'exec'), globs)
    except Exception as e:
        errors.append(f'Cell {i}: {e}')
        print(f'[CELL {i:02d} ERROR] {e}')

generated = sorted(Path('Notebooks/neet_outputs').glob('s*.png'))
print(f'\n{"="*60}')
print(f'Generated: {len(generated)} figures')
if errors:
    print(f'Errors ({len(errors)}):')
    for e in errors:
        print(f'  ✗ {e}')
else:
    print('All cells ran without errors.')
