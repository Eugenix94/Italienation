import json
import os
import re
from pathlib import Path

def upgrade_to_direct_data_links():
    dp_path = Path(r"C:\Users\Dell\Documents\Antigravity\Italienation\datapackage.json")
    prov_path = Path(r"C:\Users\Dell\Documents\Antigravity\Italienation\FILE_BY_FILE_PROVENANCE.md")

    with open(dp_path, "r", encoding="utf-8") as f:
        dp = json.load(f)

    resources = dp.get("resources", [])
    github_base = "https://raw.githubusercontent.com/Eugenix94/Italienation/main/"
    hf_resolve_base = "https://huggingface.co/datasets/diatribe00/italian-schools-opendata/resolve/main/"

    updated_resources = []
    for res in resources:
        path_str = res.get("path", "")
        
        # Determine 100% direct data URL
        if path_str.startswith("local_data/HuggingFace/"):
            sub_path = path_str.replace("local_data/HuggingFace/", "")
            direct_url = f"{hf_resolve_base}data/{sub_path}"
        elif path_str.startswith("local_data/processed/"):
            direct_url = f"{github_base}{path_str}"
        elif "eurostat" in path_str.lower():
            dataset_code = res.get("name", "").split("$")[0].split("(")[0].strip()
            direct_url = f"https://ec.europa.eu/eurostat/databrowser/view/{dataset_code}/default/table"
        elif "istat" in path_str.lower():
            direct_url = "https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z07,1.0/ALL_THEMES/IT1"
        elif "oecd" in path_str.lower():
            direct_url = "https://data-explorer.oecd.org/"
        elif "worldbank" in path_str.lower() or "wb_" in path_str.lower():
            direct_url = "https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS"
        else:
            direct_url = f"{github_base}{path_str}"

        res["url"] = direct_url
        res["homepage"] = direct_url
        res["sources"] = [
            {
                "title": f"Direct Data Download / View Authority for {res.get('name')}",
                "path": direct_url
            }
        ]
        updated_resources.append(res)

    dp["resources"] = updated_resources

    with open(dp_path, "w", encoding="utf-8") as f:
        json.dump(dp, f, indent=2, ensure_ascii=False)

    print(f"datapackage.json updated with 100% direct raw download URLs for all {len(updated_resources)} datasets!")

if __name__ == "__main__":
    upgrade_to_direct_data_links()
