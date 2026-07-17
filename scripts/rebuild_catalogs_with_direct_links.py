import os
import re
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL_DATA = ROOT / "local_data"
PROCESSED_DATA = ROOT / "processed_data"
WEB_DIR = ROOT / "web"

# Load registries if available for exact matching
reg_urls = {}
for reg_name in ["SCIENTIFIC_OPEN_DATA_PORTAL_REGISTRY.json", "OFFICIAL_OPEN_DATA_DIRECT_LINKS_AND_VERIFICATION_PORTAL.json"]:
    reg_path = PROCESSED_DATA / reg_name
    if reg_path.exists():
        try:
            with open(reg_path, "r", encoding="utf-8") as f:
                items = json.load(f)
                if isinstance(items, list):
                    for it in items:
                        if isinstance(it, dict):
                            pfile = it.get("processed_file", "").replace("\\", "/")
                            url = it.get("direct_source_url") or it.get("portal_url") or it.get("portal_browse_url")
                            if pfile and url:
                                reg_urls[pfile.lower()] = url
                            if it.get("id") and url:
                                reg_urls[it["id"].lower()] = url
        except Exception as e:
            print(f"Note: could not read {reg_name}: {e}")

def get_direct_link(file_path):
    p_clean = file_path.replace("\\", "/")
    p_lower = p_clean.lower()
    fname = Path(file_path).name.lower()
    
    # 1. Check direct registry match
    for k, url in reg_urls.items():
        if k in p_lower:
            return url

    # 2. Institutional frameworks (our repo files)
    if "/institutional_frameworks/" in p_lower:
        return f"https://github.com/Eugenix94/Italienation/blob/main/{p_clean}"

    # 3. Eurostat exact flow/table codes
    if "/eurostat/" in p_lower or "estat_" in fname or "$" in fname:
        # e.g., ESTAT_EDAT_LFSE_22$DEFAULTVIEW_1.0 or edat_lfse_20 or tps00203
        m = re.search(r'(?:estat_)?([a-z0-9_]{6,25})(?:\$|_df_|\.csv|\.xml|_1\.0|_2\.0)', fname)
        if m:
            code = m.group(1).lower().replace("estat_", "")
            if re.match(r'^[a-z]+_[a-z0-9_]+$|^[a-z]{3}\d{5}$', code):
                return f"https://ec.europa.eu/eurostat/databrowser/view/{code}/default/table?lang=en"
        return "https://ec.europa.eu/eurostat/databrowser/explore/all/education?lang=en"

    # 4. HuggingFace exact dataset tree/blob links
    if "/huggingface/" in p_lower:
        sub = p_clean.split("HuggingFace/")[-1] if "HuggingFace/" in p_clean else p_clean.split("huggingface/")[-1]
        return f"https://huggingface.co/datasets/diatribe00/italian-schools-opendata/blob/main/{sub}"

    # 5. ISTAT exact SDMX flows or indicator direct pages
    if "/istat/" in p_lower or "dccv_" in fname or "dcis_" in fname or "neet" in fname:
        # Check exact SDMX flow IDs in filename first
        m = re.search(r'([a-z0-9_]+_df_[a-z0-9_]+|(?:dccv|dcis|dcca|dcbb|ocal|educ)_[a-z0-9_]+)', fname)
        if m:
            flow = m.group(1).upper()
            if flow != "OCAL_DATA":
                return f"https://esploradati.istat.it/datapage?id={flow}"
        
        # Specific topic matching for Istat files
        if "neet" in fname:
            return "https://esploradati.istat.it/datapage?id=DCCV_NEET1"
        if "early_school_leavers" in fname or "ripetent" in fname or "boccia" in fname or "taxscuola" in fname:
            return "https://esploradati.istat.it/datapage?id=DCCV_TAXSCUOLA"
        if "diplomat" in fname or "graduates" in fname or "laureat" in fname:
            return "https://esploradati.istat.it/datapage?id=DCCV_LAUR"
        if "household" in fname or "poverty" in fname or "spending" in fname or "afford" in fname or "saving" in fname or "burden" in fname:
            return "https://esploradati.istat.it/datapage?id=DCCV_SPESAFAM"
        if "labour" in fname or "occupat" in fname or "job_search" in fname or "employment" in fname:
            return "https://esploradati.istat.it/datapage?id=DCCV_OCCUPAT"
        if "school" in fname or "scuol" in fname or "student" in fname or "infanzia" in fname or "primaria" in fname or "sec1" in fname or "sec2" in fname:
            return "https://esploradati.istat.it/datapage?id=DCIS_SCUOLE"
        return "https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0800,1.0/I_EDUC"

    # 6. MIM / MinIstruzione exact catalog subfolders
    if "/ministruzione/" in p_lower or "/mim/" in p_lower:
        for sub in ["adozioni_libri_di_testo", "edilizia_scolastica", "edifici", "personale_scuola", "scuole", "sistema_nazionale_di_valutazione", "studenti", "valutazione", "esiti"]:
            if sub in p_lower or sub in fname:
                return f"https://dati.istruzione.it/opendata/opendata/catalogo/elementi1/{sub}/"
        return "https://dati.istruzione.it/opendata/opendata/catalogo/elementi1/"

    # 7. MUR exact USTAT sections
    if "/mur/" in p_lower:
        if "iscritt" in fname or "immatricolat" in fname:
            return "https://ustat.mur.gov.it/dati/didattica/italia/iscritti"
        if "laureat" in fname or "esit" in fname or "abbandon" in fname:
            return "https://ustat.mur.gov.it/dati/didattica/italia/laureati"
        if "diritto" in fname or "bors" in fname or "tass" in fname or "esonero" in fname:
            return "https://ustat.mur.gov.it/dati/diritto-allo-studio/"
        return "https://ustat.mur.gov.it/dati/didattica/italia/atenei"

    # 8. INVALSI direct reports & statistical open data
    if "/invalsi/" in p_lower:
        if "2024" in fname:
            return "https://www.invalsiopen.it/risultati/risultati-invalsi-2024/"
        return "https://invalsi-open.cineca.it/index.php?get=statistiche"

    # 9. MEF SIOPE cash spending portals
    if "/mef/" in p_lower or "/siope/" in p_lower:
        return "https://opencivitas.mef.gov.it/it/data"

    # 10. INPS statistical observatories
    if "/inps/" in p_lower:
        return "https://servizi2.inps.it/servizi/statistiche/DataBrowser/"

    # 11. AlmaLaurea graduate survey direct links
    if "/almalaurea/" in p_lower:
        if "occupazion" in fname or "carrier" in fname or "retribuzion" in fname:
            return "https://www.almalaurea.it/universita/indagini/laureati/condizione-occupazionale"
        if "profilo" in fname or "diplomat" in fname:
            return "https://www.almalaurea.it/universita/indagini/laureati/profilo"
        return "https://www.almalaurea.it/universita/dati-e-ricerche/indagini"

    # 12. OECD / OCSE Education at a Glance / PISA
    if "/oecd/" in p_lower or "/ocse/" in p_lower:
        if "pisa" in fname:
            return "https://www.oecd.org/pisa/data/"
        if "earn" in fname or "wage" in fname or "retribuzion" in fname:
            return "https://data.oecd.org/earn/average-wages.htm"
        return "https://www.oecd.org/en/publications/education-at-a-glance-2024_c00cad36-en.html"

    # 13. World Bank / Our World in Data / SDG
    if "/worldbank/" in p_lower or "wb_wdi" in fname or "api_hd.hci" in fname:
        if "hci" in fname:
            return "https://data.worldbank.org/indicator/HD.HCI.OVRL"
        if "gini" in fname or "pov" in fname:
            return "https://data.worldbank.org/indicator/SI.POV.GINI"
        return "https://data.worldbank.org/indicator"
    if "/ourworlddata/" in p_lower:
        return "https://ourworldindata.org/education"
    if "/uksdgstats/" in p_lower:
        return "https://sdgdata.gov.uk/4-1-1/"
    if "/openeurydice/" in p_lower:
        return "https://eurydice.eacea.ec.europa.eu/national-education-systems/italy/overview"
    if "/anpal/" in p_lower:
        return "https://www.anpal.gov.it/dati-e-pubblicazioni/osservatorio-mercato-del-lavoro"
    if "/openpolis/" in p_lower:
        return "https://www.openpolis.it/argomenti/poverta-educativa/"
    if "/opencoesione/" in p_lower:
        return "https://opencoesione.gov.it/it/dati/progetti/"

    # Default fallback to repository direct raw link
    return f"https://github.com/Eugenix94/Italienation/blob/main/{p_clean}"

def categorize(file_path):
    p = file_path.lower()
    if "/institutional_frameworks/" in p: return {"cat": "Comparative/Legal", "inst": "OECD / Eurydice / Legislative"}
    if "/istat/" in p: return {"cat": "ISTAT", "inst": "ISTAT Open Data"}
    if "/eurostat/" in p or "estat_" in p: return {"cat": "Eurostat", "inst": "Eurostat SDMX"}
    if "/huggingface/" in p: return {"cat": "MIM", "inst": "Ministero Istruzione (HuggingFace Mirror)"}
    if "/oecd/" in p or "/ocse/" in p: return {"cat": "OECD", "inst": "OECD Education at a Glance"}
    if "/ministruzione/" in p or "/mim/" in p: return {"cat": "MIM", "inst": "Ministero Istruzione"}
    if "/mur/" in p: return {"cat": "MUR", "inst": "MUR/USTAT Anagrafe"}
    if "/invalsi/" in p: return {"cat": "INVALSI", "inst": "INVALSI Open Data"}
    if "/mef/" in p or "/siope/" in p: return {"cat": "MEF/SIOPE", "inst": "MEF/OpenCivitas"}
    if "/inps/" in p: return {"cat": "INPS", "inst": "INPS Open Data"}
    if "/almalaurea/" in p: return {"cat": "AlmaLaurea", "inst": "AlmaLaurea Consorzio"}
    if "/anpal/" in p: return {"cat": "ANPAL", "inst": "ANPAL Mercato del Lavoro"}
    if "/openpolis/" in p: return {"cat": "Openpolis", "inst": "Openpolis Povertà Educativa"}
    if "/opencoesione/" in p: return {"cat": "OpenCoesione", "inst": "OpenCoesione Progetti"}
    if "/ourworlddata/" in p or "/worldbank/" in p or "wb_wdi" in p or "api_hd.hci" in p: return {"cat": "Global", "inst": "World Bank / Our World in Data"}
    if "/uksdgstats/" in p: return {"cat": "UK SDG", "inst": "UK Office for National Statistics"}
    if "/openeurydice/" in p: return {"cat": "Eurydice", "inst": "European Commission Eurydice"}
    return {"cat": "Other", "inst": "Various Institutional Sources"}

def name_from_path(fp):
    base = Path(fp).stem
    clean = re.sub(r'[_-]+', ' ', base).title()
    return clean[:85]

print("=== Rebuilding Catalogs with Exact Direct Links ===")

raw_files = []
for root, dirs, files in os.walk(LOCAL_DATA):
    if 'processed' in root:
        continue
    for f in files:
        if f.endswith('.csv'):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            raw_files.append(rel)

raw_files.sort()
raw_catalog = []
for f in raw_files:
    c = categorize(f)
    direct_url = get_direct_link(f)
    raw_catalog.append({
        "path": f,
        "name": name_from_path(f),
        "category": c["cat"],
        "institution": c["inst"],
        "source": direct_url
    })

proc_files = []
for root, dirs, files in os.walk(PROCESSED_DATA):
    for f in files:
        if f.endswith('.csv'):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ROOT).replace("\\", "/")
            proc_files.append(rel)

proc_files.sort()
proc_catalog = []
for f in proc_files:
    direct_url = get_direct_link(f)
    proc_catalog.append({
        "path": f,
        "name": name_from_path(f),
        "category": "Processed",
        "institution": "Italienation Project (Experimental Analysis)",
        "source": direct_url
    })

with open(WEB_DIR / "catalog_raw.json", "w", encoding="utf-8") as f:
    json.dump(raw_catalog, f, indent=2, ensure_ascii=False)

with open(WEB_DIR / "catalog_processed.json", "w", encoding="utf-8") as f:
    json.dump(proc_catalog, f, indent=2, ensure_ascii=False)

print(f"Generated raw catalog: {len(raw_catalog)} items.")
print(f"Generated processed catalog: {len(proc_catalog)} items.")
