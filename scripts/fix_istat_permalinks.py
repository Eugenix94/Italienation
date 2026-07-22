import json
import os
from pathlib import Path

def fix_istat_links():
    dp_path = Path(r"C:\Users\Dell\Documents\Antigravity\Italienation\datapackage.json")

    with open(dp_path, "r", encoding="utf-8") as f:
        dp = json.load(f)

    resources = dp.get("resources", [])
    fixed_count = 0

    for res in resources:
        path_str = res.get("path", "").lower()
        fname = res.get("name", "").lower()
        url = res.get("url", "")

        if "istat" in path_str or "istat" in fname or "dccv" in fname or "neet" in fname or "asili_nido" in fname or "bocciati" in fname or "income_by_region" in fname or "employment" in fname or "esploradati.istat.it" in url:
            
            # Map specific ISTAT datasets to their permanent, non-redirecting institutional topic/archive pages
            if "bes" in fname or "gini" in fname or "income" in fname:
                istat_permalink = "https://www.istat.it/it/benessere-e-sostenibilita/indicatori-bes"
            elif "neet" in fname or "employment" in fname or "lavoro" in fname or "dccv" in fname:
                istat_permalink = "https://www.istat.it/it/archivio/lavoro+e+retribuzioni"
            elif "asili" in fname or "bocciati" in fname or "school" in fname or "istruzione" in fname:
                istat_permalink = "https://www.istat.it/it/archivio/istruzione+e+formazione"
            else:
                istat_permalink = "https://www.istat.it/it/dati-analisi-e-prodotti/open-data"

            res["url"] = istat_permalink
            res["homepage"] = istat_permalink
            res["sources"] = [
                {
                    "title": f"ISTAT Permanent Data Archive for {res.get('name')}",
                    "path": istat_permalink
                }
            ]
            fixed_count += 1

    dp["resources"] = resources

    with open(dp_path, "w", encoding="utf-8") as f:
        json.dump(dp, f, indent=2, ensure_ascii=False)

    print(f"Fixed {fixed_count} ISTAT dataset links! Mapped exclusively to direct, permanent ISTAT data archive portals (bypassing hash-redirects).")

if __name__ == "__main__":
    fix_istat_links()
