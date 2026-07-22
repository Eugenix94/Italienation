import os
import json

def generate_datapackage():
    base_dirs = ["../local_data", "../processed_data"]
    root_repo = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    datapackage = {
        "name": "italienation-osint-dataset",
        "title": "Italienation: An OSINT Educational Decay Dataset",
        "description": "100% Traced Open Science Data regarding Italian educational inequality, shadow economy, brain drain, and municipal funding.",
        "licenses": [
            {
                "name": "CC-BY-4.0",
                "title": "Creative Commons Attribution 4.0",
                "path": "https://creativecommons.org/licenses/by/4.0/"
            }
        ],
        "resources": []
    }
    
    for bdir in base_dirs:
        abs_bdir = os.path.abspath(os.path.join(os.path.dirname(__file__), bdir))
        if not os.path.exists(abs_bdir):
            continue
            
        for root, dirs, files in os.walk(abs_bdir):
            for file in files:
                if file.startswith('.') or file.endswith('.md') or file.endswith('.py') or file == 'FILE_BY_FILE_PROVENANCE_MANIFEST.csv':
                    continue
                    
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, root_repo).replace('\\', '/')
                
                # Determine format
                fmt = "unknown"
                if file.endswith('.csv'): fmt = "csv"
                elif file.endswith('.json'): fmt = "json"
                elif file.endswith('.parquet'): fmt = "parquet"
                elif file.endswith('.xlsx') or file.endswith('.xls'): fmt = "excel"
                elif file.endswith('.xml'): fmt = "xml"
                
                resource = {
                    "name": file.replace('.', '_').lower(),
                    "path": rel_path,
                    "format": fmt,
                    "bytes": os.path.getsize(full_path)
                }
                
                datapackage["resources"].append(resource)

    # Save to root of repo
    out_path = os.path.join(root_repo, "datapackage.json")
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(datapackage, f, indent=2)
        
    print(f"Successfully generated datapackage.json with {len(datapackage['resources'])} resources.")

if __name__ == "__main__":
    generate_datapackage()
