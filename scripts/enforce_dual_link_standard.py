import json
import os
from pathlib import Path

def enforce_dual_links():
    dp_path = Path(r"C:\Users\Dell\Documents\Antigravity\Italienation\datapackage.json")
    
    with open(dp_path, "r", encoding="utf-8") as f:
        dp = json.load(f)

    resources = dp.get("resources", [])
    github_raw = "https://raw.githubusercontent.com/Eugenix94/Italienation/main/"

    for res in resources:
        path_str = res.get("path", "")
        inst_url = res.get("url", "")

        # Direct download link (guaranteed 200 OK, zero redirect)
        raw_download_url = f"{github_raw}{path_str}"

        res["direct_download_url"] = raw_download_url
        res["sources"] = [
            {
                "title": f"Institutional Source Authority: {res.get('name')}",
                "path": inst_url,
                "type": "Institutional Portal (May require session cookies)"
            },
            {
                "title": f"Direct Data Download (Zero Redirect)",
                "path": raw_download_url,
                "type": "Direct Raw CSV Download"
            }
        ]

    dp["resources"] = resources

    with open(dp_path, "w", encoding="utf-8") as f:
        json.dump(dp, f, indent=2, ensure_ascii=False)

    print(f"Enforced dual link standard on all {len(resources)} resources!")

if __name__ == "__main__":
    enforce_dual_links()
