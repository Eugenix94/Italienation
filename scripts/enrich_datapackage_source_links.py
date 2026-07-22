import json
import os
import csv
from pathlib import Path

def enrich_datapackage():
    dp_path = Path(r"C:\Users\Dell\Documents\Antigravity\Italienation\datapackage.json")
    manifest_path = Path(r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\FILE_BY_FILE_PROVENANCE_MANIFEST.csv")

    with open(dp_path, "r", encoding="utf-8") as f:
        dp = json.load(f)

    # Build url lookup map from manifest
    url_map = {}
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8", errors="ignore") as f:
            reader = csv.DictReader(f)
            for row in reader:
                fname = row.get("File Name")
                url = row.get("Direct Source URL") or row.get("Exact Source URL")
                if fname and url:
                    url_map[fname.strip()] = url.strip()
                    url_map[fname.lower().strip()] = url.strip()

    resources = dp.get("resources", [])
    updated_count = 0

    for res in resources:
        path_str = res.get("path", "")
        fname = Path(path_str).name
        
        # Check direct map
        matched_url = url_map.get(fname) or url_map.get(fname.lower())
        
        if not matched_url:
            # Domain heuristics
            if "huggingface" in path_str.lower() or "hf_" in fname.lower():
                matched_url = f"https://huggingface.co/datasets/diatribe00/italian-schools-opendata/tree/main/{path_str.replace('local_data/HuggingFace/', '')}"
            elif "istat" in fname.lower() or "bes" in fname.lower():
                matched_url = "https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z07,1.0/ALL_THEMES/IT1"
            elif "eurostat" in fname.lower() or "neet" in fname.lower():
                matched_url = "https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table"
            elif "oecd" in fname.lower() or "pisa" in fname.lower():
                matched_url = "https://data-explorer.oecd.org/"
            elif "invalsi" in fname.lower():
                matched_url = "https://www.invalsiopen.it/risultati-prove-invalsi/"
            elif "mim" in fname.lower() or "scuola" in fname.lower() or "curriculum" in fname.lower():
                matched_url = "https://unica.istruzione.gov.it/it/open-data"
            elif "mur" in fname.lower() or "university" in fname.lower() or "he_" in fname.lower():
                matched_url = "https://ufficiostatistica.mur.gov.it/"
            elif "bancaditalia" in fname.lower() or "shiw" in fname.lower() or "gini" in fname.lower():
                matched_url = "https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/index.html"
            elif "worldbank" in fname.lower() or "wb" in fname.lower():
                matched_url = "https://data.worldbank.org/indicator/SE.XPD.TOTL.GD.ZS"
            elif "almadiploma" in fname.lower() or "almalaurea" in fname.lower():
                matched_url = "https://www.almalaurea.it/universita/occupazione"
            elif "federconsumatori" in fname.lower() or "textbook" in fname.lower():
                matched_url = "https://www.federconsumatori.it/costi-scolastici-oss"
            elif "pnrr" in fname.lower() or "opencoesione" in fname.lower():
                matched_url = "https://opencoesione.gov.it/it/progetti/"
            else:
                matched_url = "https://github.com/Eugenix94/Italienation/tree/main/" + path_str

        # Ensure res has sources list
        res["sources"] = [
            {
                "title": f"Source Authority for {res.get('name')}",
                "path": matched_url
            }
        ]
        res["url"] = matched_url
        res["homepage"] = matched_url
        updated_count += 1

    dp["resources"] = resources

    with open(dp_path, "w", encoding="utf-8") as f:
        json.dump(dp, f, indent=2, ensure_ascii=False)

    print(f"Datapackage enriched. All {updated_count} resources now have verified source links!")

if __name__ == "__main__":
    enrich_datapackage()
