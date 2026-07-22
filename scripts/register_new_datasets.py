import json
import os

datapackage_path = r"C:\Users\Dell\Documents\Antigravity\Italienation\datapackage.json"

with open(datapackage_path, "r", encoding="utf-8") as f:
    data = json.load(f)

resources = data.get("resources", [])

new_entries = [
    {
        "name": "subject_textbook_costs_by_track_2026",
        "path": "local_data/processed/subject_textbook_costs_by_track_2026.csv",
        "description": "Subject-by-subject textbook expenditure, print vs digital pricing, and ministerial ceiling overruns across all upper secondary branches.",
        "format": "csv",
        "mediatype": "text/csv",
        "license": "CC-BY-4.0"
    },
    {
        "name": "international_tripartite_vs_comprehensive_matrix",
        "path": "local_data/processed/international_tripartite_vs_comprehensive_matrix.csv",
        "description": "Comparative benchmark of Italy's early tracking tripartite system vs UK Comprehensive, Finland, Germany Dual System, and France Eurydice metrics.",
        "format": "csv",
        "mediatype": "text/csv",
        "license": "CC-BY-4.0"
    }
]

existing_names = {r["name"] for r in resources}
for entry in new_entries:
    if entry["name"] not in existing_names:
        resources.append(entry)

data["resources"] = resources

with open(datapackage_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"datapackage.json updated. Total registered resources: {len(resources)}")
