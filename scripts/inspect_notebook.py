import json

with open('Notebooks/education_spending_outcomes.ipynb') as f:
    nb = json.load(f)

print(f"Cells: {len(nb['cells'])}")
for i, c in enumerate(nb['cells']):
    src = ''.join(c['source'])
    print(f"  [{i}] {c['cell_type']}: {src[:120].strip()}")
