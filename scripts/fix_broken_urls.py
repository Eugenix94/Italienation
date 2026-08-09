import json
import os

REPLACEMENTS = {
    "https://unica.istruzione.gov.it/it/open-data": "https://dati.istruzione.it/opendata/opendata/catalogo",
    "https://www.federconsumatori.it/costi-scolastici-oss": "https://www.federconsumatori.it/",
    "https://opencoesione.gov.it/it/progetti/": "https://opencoesione.gov.it/it/opendata/",
    "https://www.openpolis.it/esercizi-di-potere/": "https://www.openpolis.it/"
}

TARGET_FILES = [
    "datapackage.json",
    "rendered_outputs/catalog_raw.json",
    "rendered_outputs/catalog_processed.json"
]

def apply_replacements(data):
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if isinstance(v, str):
                for old, new in REPLACEMENTS.items():
                    if old in v:
                        v = v.replace(old, new)
                new_dict[k] = v
            else:
                new_dict[k] = apply_replacements(v)
        return new_dict
    elif isinstance(data, list):
        return [apply_replacements(item) for item in data]
    else:
        if isinstance(data, str):
            for old, new in REPLACEMENTS.items():
                if old in data:
                    data = data.replace(old, new)
        return data

def main():
    total_files_fixed = 0
    
    for filepath in TARGET_FILES:
        if not os.path.exists(filepath):
            print(f"Skipping {filepath} (does not exist)")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
                continue
                
        # To count how many replacements, we can just do string replace on the raw text too
        with open(filepath, 'r', encoding='utf-8') as f:
            raw_text = f.read()
            
        count = 0
        for old in REPLACEMENTS.keys():
            count += raw_text.count(old)
            
        if count > 0:
            fixed_data = apply_replacements(data)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(fixed_data, f, indent=2, ensure_ascii=False)
            print(f"Fixed {count} instances in {filepath}")
            total_files_fixed += 1
        else:
            print(f"No broken links found in {filepath}")
            
    print(f"\nDone! Modified {total_files_fixed} files.")

if __name__ == '__main__':
    main()
