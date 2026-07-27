import json
import csv
from pathlib import Path
import urllib.parse

def main():
    dp_path = Path(r"C:\Users\Dell\Documents\Antigravity\Italienation\datapackage.json")
    local_data_dir = Path(r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data")
    
    with open(dp_path, "r", encoding="utf-8") as f:
        dp = json.load(f)

    # 1. Build an exact URL map from manifests
    url_map = {}
    for p in local_data_dir.rglob('manifest*.*'):
        try:
            if p.suffix == '.json':
                with open(p, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        for item in data:
                            filename = item.get("path", "")
                            if filename: filename = Path(filename).name
                            else: filename = item.get("name", "")
                            
                            url = item.get("url")
                            if not url and "flow_id" in item:
                                url = f"https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z07,1.0/ALL_THEMES/IT1,{item['flow_id']},1.0"
                            if filename and url:
                                url_map[filename] = url
                                url_map[filename.lower().replace(".csv", "").replace(".xml", "")] = url
            elif p.suffix == '.csv':
                with open(p, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        filename = row.get("filename") or row.get("name")
                        url = row.get("url") or row.get("source_url")
                        if filename and url:
                            url_map[filename] = url
                            url_map[filename.lower().replace(".csv", "").replace(".xml", "")] = url
        except Exception:
            pass

    resources = dp.get("resources", [])
    fixed_count = 0

    for res in resources:
        path_str = res.get("path", "")
        fname = Path(path_str).name
        url = res.get("url", "")
        
        # Check if it's one of the generic ISTAT links or if it needs to be updated
        is_generic_istat = url and ("istat.it/it/archivio" in url or "istat.it/it/benessere" in url or "istat.it/it/dati-analisi" in url or "istat.it/statistiche-per-temi" in url)
        
        if is_generic_istat or "istat" in fname.lower() or "dccv" in fname.lower():
            exact_url = url_map.get(fname)
            if not exact_url:
                fuzzy = fname.lower().replace(".csv", "").replace(".xml", "")
                exact_url = url_map.get(fuzzy)
                
            if not exact_url:
                # Fallback to ISTAT Esploradati Search query using the filename (this drops them right on the exact search)
                clean_name = fname.replace(".csv", "")
                # URL encode the search text properly
                encoded_name = urllib.parse.quote(clean_name)
                exact_url = f"https://esploradati.istat.it/databrowser/#/it/dw/search?TEXT={encoded_name}"
            
            # Now update the resource
            res["url"] = exact_url
            res["homepage"] = exact_url
            
            # Find and update the Institutional Source in sources array
            sources = res.get("sources", [])
            for s in sources:
                if "Institutional" in s.get("title", "") or "ISTAT" in s.get("title", "") or "Source Authority" in s.get("title", ""):
                    s["path"] = exact_url
                    s["title"] = f"Institutional Source Authority: {res.get('name')}"
            
            fixed_count += 1

    dp["resources"] = resources

    with open(dp_path, "w", encoding="utf-8") as f:
        json.dump(dp, f, indent=2, ensure_ascii=False)
        
    print(f"Fixed {fixed_count} ISTAT datasets, restoring direct DataBrowser and Search links!")

if __name__ == "__main__":
    main()
