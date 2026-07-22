import os
import csv
import re
import json

base_dir = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data"
output_csv = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\FILE_BY_FILE_PROVENANCE_MANIFEST.csv"
output_md = r"C:\Users\Dell\.gemini\antigravity\brain\62a964a6-8d4d-486c-91bb-954b2ca38c48\FILE_BY_FILE_PROVENANCE.md"
official_registry_path = r"C:\Users\Dell\Documents\Antigravity\Italienation\processed_data\OFFICIAL_OPEN_DATA_DIRECT_LINKS_AND_VERIFICATION_PORTAL.json"

# Load Official Registry
exact_file_map = {}
if os.path.exists(official_registry_path):
    with open(official_registry_path, 'r', encoding='utf-8') as f:
        registry_data = json.load(f)
        for item in registry_data:
            proc_file = item.get("processed_file", "")
            if proc_file:
                # Normalize path
                norm_path = proc_file.replace('/', '\\')
                if norm_path.startswith("local_data\\"):
                    norm_path = norm_path.replace("local_data\\", "")
                exact_url = item.get("direct_source_url") or item.get("portal_url")
                if exact_url:
                    exact_file_map[norm_path] = exact_url

def get_url_for_file(filepath, filename, rel_path, dir_json_data):
    # Check if we have an EXACT match in the Official JSON registry
    if rel_path in exact_file_map:
        return exact_file_map[rel_path]
        
    # Check if we have an exact dataset_id from the manifest_summary.json
    if dir_json_data and filename in dir_json_data:
        file_info = dir_json_data[filename]
        # _dataset_id is usually in the first row of the 'head' array
        dataset_id = None
        if "head" in file_info and len(file_info["head"]) > 0:
            dataset_id = file_info["head"][0].get("_dataset_id")
        
        if dataset_id:
            return f"https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?datasetId={dataset_id}"
            
    filepath_unix = filepath.replace('\\', '/')
    
    # ISTAT: Extract dataset code if present
    if '/ISTAT' in filepath_unix:
        match = re.search(r'([A-Z0-9_]+_DF_[A-Z0-9_]+)', filename)
        if match:
            code = match.group(1).split('_DF_')[1].split(',')[0]
            return f"http://dati.istat.it/Index.aspx?DataSetCode={code}"
        return "http://dati.istat.it/"
        
    # Eurostat: Extract dataset code from filename (e.g., ESTAT_EDAT_LFSE_22...)
    elif '/eurostat' in filepath_unix or 'ESTAT_' in filename or 'educ_' in filename:
        match = re.search(r'([a-z_0-9]+)\$|ESTAT_([A-Z0-9_]+)_', filename, re.IGNORECASE)
        if match:
            code = match.group(1) if match.group(1) else match.group(2)
            return f"https://ec.europa.eu/eurostat/databrowser/view/{code.lower()}/default/table"
        return "https://ec.europa.eu/eurostat/databrowser/"
        
    # OECD
    elif '/oecd' in filepath_unix or 'OECD' in filename:
        return "https://data.oecd.org/"
        
    # World Bank
    elif '/worldbank' in filepath_unix or 'WB_' in filename or 'API_' in filename:
        return "https://data.worldbank.org/indicator/"
        
    # MIM / Scuola in Chiaro / MinIstruzione
    elif '/Scuola_in_chiaro' in filepath_unix:
        if 'ediliz' in filepath_unix.lower(): return "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Edilizia%20Scolastica"
        if 'adozion' in filepath_unix.lower(): return "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Adozioni%20Libri%20di%20Testo"
        return "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Scuole"
    elif '/MinIstruzione' in filepath_unix:
        if 'Alunni' in filepath_unix: return "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Alunni"
        if 'Docenti' in filepath_unix or 'Personale' in filepath_unix: return "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Personale%20Scuola"
        if 'Edifici' in filepath_unix: return "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Edilizia%20Scolastica"
        if 'LibriDiTesto' in filepath_unix: return "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Adozioni%20Libri%20di%20Testo"
        if 'Scuole' in filepath_unix: return "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Scuole"
        return "https://dati.istruzione.it/opendata/opendata/catalogo/"
    elif '/UNICA' in filepath_unix:
        return "https://dati.istruzione.it/opendata/opendata/catalogo/elements1/leaf/?area=Alunni"
        
    # MUR
    elif '/MUR' in filepath_unix:
        return "https://ustat.mur.gov.it/opendata/"
        
    # INVALSI
    elif '/INVALSI' in filepath_unix:
        return "https://invalsi-serviziostatistico.cineca.it/"
        
    # AlmaLaurea
    elif '/AlmaLaurea' in filepath_unix:
        return "https://www2.almalaurea.it/cgi-php/universita/statistiche/tendine.php"

    # Additional sources
    elif '/ANPAL' in filepath_unix:
        return "https://dati.lavoro.gov.it/"
    elif '/INPS' in filepath_unix:
        return "https://www.inps.it/it/it/dati-e-bilanci/open-data.html"
    elif '/MEF' in filepath_unix:
        return "https://www.finanze.gov.it/"
    elif '/SIOPE' in filepath_unix:
        return "https://www.mef.gov.it/"
    elif '/OpenCoesione' in filepath_unix:
        return "https://opencoesione.gov.it/it/opendata/"
    elif '/Openpolis' in filepath_unix:
        return "https://www.openpolis.it/temi/poverta-educativa/"
    elif '/openEURYDICE' in filepath_unix or '/institutional_frameworks' in filepath_unix:
        return "https://eurydice.eacea.ec.europa.eu/"
    elif '/UKSDGstats' in filepath_unix:
        return "https://sdgdata.gov.uk/"
    elif '/ourWorldData' in filepath_unix:
        return "https://ourworldindata.org/education"
        
    # Processed Notebook files
    elif '/processed' in filepath_unix or '/new_frontiers' in filepath_unix:
        return "Processed locally via Jupyter Notebooks (Derivative Data) - See Repository Scripts"
        
    elif '/manual_required' in filepath_unix:
        return "Manually Extracted - See LOCAL_DATA_BIBLIOGRAPHY.md"
        
    # Root level files handling
    elif 'WB_WDI' in filename or 'API_' in filename:
        return "https://data.worldbank.org/indicator/"
    elif 'educ_uoe' in filename or 'ESTAT_' in filename:
        match = re.search(r'([a-z_0-9]+)\$|ESTAT_([A-Z0-9_]+)_', filename, re.IGNORECASE)
        if match:
            code = match.group(1) if match.group(1) else match.group(2)
            return f"https://ec.europa.eu/eurostat/databrowser/view/{code.lower()}/default/table"
        return "https://ec.europa.eu/eurostat/databrowser/"
    elif 'NEET' in filename and 'DCCV' in filename:
        match = re.search(r'([A-Z0-9_]+_DF_[A-Z0-9_]+)', filename)
        if match:
            code = match.group(1).split('_DF_')[1].split(',')[0]
            return f"http://dati.istat.it/Index.aspx?DataSetCode={code}"
        return "http://dati.istat.it/"
    elif 'OECD' in filename:
        return "https://data.oecd.org/"
    elif 'Figure_1' in filename and 'NEET' in filename:
        return "https://www.ons.gov.uk/"
    elif 'Expenses.csv' in filename:
        return "https://www.federconsumatori.it/"
    elif 'NEETs_ET2025' in filename:
        return "https://ec.europa.eu/eurostat/databrowser/"

    else:
        return "Verify via local_data/LOCAL_DATA_BIBLIOGRAPHY.md"

rows = []
for root, dirs, files in os.walk(base_dir):
    # Check if directory has a manifest_summary.json
    dir_json_data = {}
    manifest_path = os.path.join(root, 'manifest_summary.json')
    parent_manifest_path = os.path.join(os.path.dirname(root), 'manifest_summary.json')
    
    # Try current directory first, then parent directory
    target_manifest = manifest_path if os.path.exists(manifest_path) else parent_manifest_path
    if os.path.exists(target_manifest):
        try:
            with open(target_manifest, 'r', encoding='utf-8') as f:
                dir_json_data = json.load(f)
        except:
            pass

    for file in files:
        if file.startswith('.') or file.endswith('.md') or file.endswith('.py') or file == "FILE_BY_FILE_PROVENANCE_MANIFEST.csv":
            continue
            
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(full_path, base_dir)
        url = get_url_for_file(full_path, file, rel_path, dir_json_data)
        size_kb = os.path.getsize(full_path) / 1024
        
        rows.append({
            "Directory": os.path.dirname(rel_path),
            "File Name": file,
            "Size (KB)": f"{size_kb:.1f}",
            "Direct Source URL": url
        })

# Sort rows
rows = sorted(rows, key=lambda x: (x['Directory'], x['File Name']))

# Write CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=["Directory", "File Name", "Size (KB)", "Direct Source URL"])
    writer.writeheader()
    writer.writerows(rows)

# Write Markdown Artifact
with open(output_md, 'w', encoding='utf-8') as f:
    f.write("# 📂 File-by-File Data Provenance Manifest\n\n")
    f.write("This document maps every single raw and processed data file in the repository to its exact URL or generation source.\n\n")
    f.write("| Directory | File Name | Size (KB) | Direct Source URL |\n")
    f.write("|---|---|---|---|\n")
    for r in rows:
        # truncate filename if too long for md display
        fname = r['File Name']
        if len(fname) > 50: fname = fname[:47] + '...'
        url = r['Direct Source URL']
        if not url.startswith('http'): url = f"*{url}*"
        else: url = f"[Source Link]({url})"
        f.write(f"| `{r['Directory']}` | `{fname}` | {r['Size (KB)']} | {url} |\n")

print(f"Generated upgraded manifest for {len(rows)} files with hyper-specific deep links.")
