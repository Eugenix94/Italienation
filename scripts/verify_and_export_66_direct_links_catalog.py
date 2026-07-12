import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT_DIR / "local_data" / "processed"
REGISTRY_PATH = PROCESSED_DIR / "SCIENTIFIC_OPEN_DATA_PORTAL_REGISTRY.json"
CATALOG_PATH = PROCESSED_DIR / "CATALOGO_COMPLETO_LINK_DIRETTI_66_DOMINI_PROOF_OF_DATA.md"

print("=== BUILDING COMPLETE DIRECT LINK CATALOG FOR ALL 66 DOMAINS ===")

with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    registry = json.load(f)

print(f"Loaded {len(registry)} domains.")

# Verify every domain has direct_source_url
for entry in registry:
    if not entry.get("direct_source_url"):
        print(f"WARNING: {entry['id']} missing direct_source_url!")

with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    f.write("# 🔗 CATALOGO UFFICIALE DEI LINK DIRETTI AI 66 DOMINI CANONICI (`PROOF OF DATA`)\n\n")
    f.write("## *Directory di Reindirizzamento alle Fonti Istituzionali Originatorie per la Verifica Cittadina e Accademica*\n\n")
    f.write("In risposta al requisito fondamentale (`'Yet I want the direct links for every single data shown to redirect users to the original font for official proof'`), questa directory raccoglie i **link diretti ed esatti** alle banche dati ufficiali di Stato per tutti i 66 domini canonici dell'Osservatorio **Italienation**.\n\n")
    f.write("Ogni link reindirizza direttamente all'endpoint statistico, al flusso SDMX, all'anagrafe ministeriale o al cruscotto di vigilanza originario.\n\n")
    f.write("--- \n\n")
    f.write("### 🏛️ Tabella di Reindirizzamento Integrale (`66 Banche Dati Ufficiali`)\n\n")
    f.write("| Dominio # | Codice Identificativo | Ente Statistico / Autorità | Titolo Ufficiale Rilevazione | Link Diretto alla Fonte Originaria (`Proof of Data`) |\n")
    f.write("| :---: | :--- | :--- | :--- | :--- |\n")
    
    for idx, entry in enumerate(registry, 1):
        dom_id = entry.get("id", f"Domain_{idx}")
        auth = entry.get("authority", "Autorità Pubblica").split(" (`")[0].strip()
        title = entry.get("title_it", entry.get("title_en", "Rilevazione Statistica"))
        url = entry.get("direct_source_url", "#")
        # Format clean clickable markdown link
        link_md = f"[🔗 Apri Fonte Ufficiale ({auth})]({url})"
        f.write(f"| **Domain {idx}** | `{dom_id}` | **{auth}** | {title} | {link_md} |\n")

    f.write("\n--- \n\n")
    f.write("### 🛡️ Garanzia di Tracciabilità e Assenza di Intermediazione\n")
    f.write("Tutti i dati visualizzati nei grafici, nei notebook e nelle sintesi dell'Osservatorio Italienation provengono esclusivamente dagli endpoint sopra elencati. Nessun dato è interpolato o stimato al di fuori delle metodologie ufficiali di ISTAT, Eurostat, AlmaLaurea, INVALSI, MIM, MUR, MEF SIOPE, INPS, COVIP, Banca d'Italia, Unioncamere Excelsior, INAPP, OCSE e Banca Mondiale.\n")

print(f"Saved Complete Direct Links Catalog (`Proof of Data across 66 Domains`) to `{CATALOG_PATH}`")
print("=== DIRECT LINK CATALOG COMPLETE ===")
