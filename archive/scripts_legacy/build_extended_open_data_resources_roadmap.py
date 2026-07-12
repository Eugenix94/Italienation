import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT_DIR / "local_data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

print("=== BUILDING EXTENDED OPEN DATA RESOURCES & API ROADMAP ===")

extended_resources = [
    {
        "resource_id": "ISTAT_SDMX_API",
        "name_it": "ISTAT I.Stat & Data Browser SDMX REST API",
        "name_en": "ISTAT National Statistical Institute - SDMX REST API Endpoint",
        "portal_url": "https://www.istat.it/it/dati-analisi-e-prodotti/bancare-dati/i-stat",
        "api_endpoint": "https://esploradati.istat.it/SDMXWS/rest/data/",
        "key_datasets": [
            "EU-SILC Household Income and Intergenerational Educational Transmission (`Indagine sul Reddito e Condizioni di Vita`)",
            "Early Childhood Care (Asili Nido 0-2 anni) Municipal & Provincial Coverage Rates (`Indagine Servizi Sociali Comuni`)",
            "Youth Brain Drain (`Emigrazione Under-35 / Cancellazioni Anagrafiche AIRE per Provincia e Titolo di Studio`)"
        ],
        "extension_value": "Extends Origin ($O$) by quantifying exact provincial Asili Nido coverage (`#1 structural determinant of female youth inactivity`) and intergenerational educational mobility."
    },
    {
        "resource_id": "MIM_PORTALE_UNICO_SCUOLA",
        "name_it": "MIM Portale Unico dei Dati della Scuola - Open Data & Anagrafe",
        "name_en": "Ministry of Education and Merit (MIM) - Open Data Portal & Registry",
        "portal_url": "https://dati.istruzione.it/opendata/opendata/",
        "api_endpoint": "https://dati.istruzione.it/opendata/api/v1/datasets",
        "key_datasets": [
            "School Building Infrastructure & Safety Registry (`Anagrafe Edilizia Scolastica SNAES - >40,000 edifici, vulnerabilità sismica, palestre, banda ultralarga`)",
            "Teacher Precariato & Annual Substitutes (`Anagrafe Docenti e ATA: cattedre di ruolo vs supplenti annuali 30/06 e 31/08 per provincia e indirizzo`)",
            "Class Overcrowding (`Alunni per Classe / Classi Pollaio nei gradi della secondaria`)"
        ],
        "extension_value": "Extends Tracking ($T$) by exposing exact teacher stability (`supplenze precari > 30% in VOC/TEC`) and structural building safety across individual school institutes."
    },
    {
        "resource_id": "INVALSI_STATISTICO_API",
        "name_it": "INVALSI Open Data & Gestione Dati Servizio Statistico",
        "name_en": "National Institute for the Evaluation of the Education System (INVALSI) - Statistical Service",
        "portal_url": "https://serviziostatistico.invalsi.it/open-data/",
        "api_endpoint": "https://serviziostatistico.invalsi.it/api/data/",
        "key_datasets": [
            "School-level ESCS Quintiles & Longitudinal Cohort Tracing (`Dati longitudinali Grado 2 -> Grado 13`)",
            "School Value-Added (`Valore Aggiunto della Scuola: Effetto Scuola depurato dal background socio-economico ESCS`)"
        ],
        "extension_value": "Extends Education ($E$) by isolating pure pedagogical effectiveness (`Valore Aggiunto`) from initial socio-economic origin ($O$)."
    },
    {
        "resource_id": "INPS_OSSERVATORIO_PRECARIATO",
        "name_it": "INPS Open Data & Osservatorio sul Precariato e sull'Apprendistato",
        "name_en": "National Social Security Institute (INPS) - Labor Market & Apprenticeship Observatory",
        "portal_url": "https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche/dati-cartacei---osservatori-statistici/osservatorio-sul-precariato.html",
        "api_endpoint": "https://dati.inps.it/api/v1/dataset/",
        "key_datasets": [
            "Monthly/Annual Contract Activations & Terminations by Age Bracket (`<25, 25-29, 30-34 anni`) and Province (`Tempo Indeterminato vs Determinato/Stagionale`)",
            "Dual Apprenticeship vs Professional Apprenticeship (`Apprendistato art. 43 vs art. 44 per Provincia e Settore Produttivo`)"
        ],
        "extension_value": "Extends Destination ($D$) by diagnosing exact labor market contract precarity and tracing why dual vocational training (`Sistema Duale`) struggles in Southern provinces."
    },
    {
        "resource_id": "INDIRE_ITS_MONITORING",
        "name_it": "INDIRE & MIM Monitoraggio Nazionale ITS Academies (ISCED 4)",
        "name_en": "National Institute for Documentation, Innovation and Educational Research (INDIRE) - ITS Academies Observatory",
        "portal_url": "https://www.indire.it/progetto/its-istituti-tecnici-superiori/",
        "api_endpoint": "https://dati.indire.it/its/api/v1/",
        "key_datasets": [
            "Directory of all 140+ ITS Foundations across Italian Regions",
            "1-Year and 3-Year Post-Diploma Employment Absorption Rates (`Tasso di occupazione coerente > 85% in Lombardia/Veneto/Emilia-Romagna`)"
        ],
        "extension_value": "Extends Education to Destination ($E \\rightarrow D$) by documenting the high-performance post-secondary vocational training alternative (`ITS Academies ISCED 4`) capable of neutralizing NEET status."
    },
    {
        "resource_id": "ALMALAUREA_CONSORTIUM_API",
        "name_it": "Consorzio Interuniversitario AlmaLaurea - Open Data & Indagini sui Laureati",
        "name_en": "AlmaLaurea Inter-University Consortium - Open Data API & Graduate Surveys",
        "portal_url": "https://www.almalaurea.it/universita/dati-e-indagini",
        "api_endpoint": "https://dati.almalaurea.it/api/v2/surveys/",
        "key_datasets": [
            "Net Monthly Wages (`Retribuzione netta mensile a 1, 3, 5 anni`) by University and Degree Class (`Ingegneria vs Lettere vs Economia`)",
            "Educational Mismatch & Over-Education (`Percentuale di laureati che svolgono mansioni che non richiedono la laurea`)"
        ],
        "extension_value": "Extends Destination ($D$) by measuring exact economic returns to university degrees across disciplines and quantifying brain drain pull factors."
    },
    {
        "resource_id": "EUROSTAT_SDMX_REST",
        "name_it": "Eurostat SDMX REST API & Database Esplorativo Europeo",
        "name_en": "Eurostat European Statistical Office - SDMX REST API & Data Browser",
        "portal_url": "https://ec.europa.eu/eurostat/data/database",
        "api_endpoint": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/",
        "key_datasets": [
            "Labor Force Survey Regional Series (`lfst_r_lfse_att: NEET NUTS-2 by Gender and Age`)",
            "Early Leavers from Education and Training (`edat_lfse_16: ELET by NUTS-2 Region`)",
            "Structure of Earnings Survey (`earn_ses_pub: Hourly earnings deciles across EU states`)"
        ],
        "extension_value": "Extends International Benchmarking by providing real-time REST API queries across all EU-27 NUTS-2 regions for ELET and NEET monitoring."
    },
    {
        "resource_id": "MEF_PNRR_ITALIA_DOMANI",
        "name_it": "MEF RGS & Italia Domani - Open Data PNRR Missione 4 (Istruzione e Ricerca)",
        "name_en": "Ministry of Economy and Finance (MEF) - National Recovery and Resilience Plan (PNRR) Open Data Portal",
        "portal_url": "https://www.italiadomani.gov.it/it/open-data.html",
        "api_endpoint": "https://dati.italiadomani.gov.it/api/v1/projects",
        "key_datasets": [
            "PNRR Missione 4 Investimenti (`M4C1I1.1 Asili Nido, M4C1I1.3 Scuola 4.0, M4C1I1.4 Dispersione Scolastica, M4C1I3.1 Nuove Competenze STEM`)",
            "Project Level SAL (`Stato di Avanzamento Lavori, Importo PNRR, Comune Beneficiario, Cronoprogramma`)"
        ],
        "extension_value": "Extends Policy DIY Simulation by tracking real-time deployment of €30+ Billion in PNRR public infrastructure and pedagogical interventions."
    },
    {
        "resource_id": "ANPAL_GOL_MONITORING",
        "name_it": "ANPAL & MLPS - Sistema Informativo Lavoro e Programma GOL (Garanzia Occupabilità Lavoratori)",
        "name_en": "National Agency for Active Labor Policies (ANPAL) - Active Labor Market Program (GOL) Observatory",
        "portal_url": "https://www.anpal.gov.it/dati-e-pubblicazioni",
        "api_endpoint": "https://dati.anpal.gov.it/api/v1/gol/",
        "key_datasets": [
            "GOL Youth Profiling (`Assessment di distanza dal mercato del lavoro per NEET 15-29 anni`)",
            "Active Labor Market Upskilling & Reskilling Insertion Rates by Region"
        ],
        "extension_value": "Extends Destination ($D$) by analyzing active labor policy remedies designed to rescue long-term NEETs from welfare dependency."
    },
    {
        "resource_id": "BANK_OF_ITALY_SHIW",
        "name_it": "Banca d'Italia - Indagine sui Bilanci delle Famiglie (SHIW / Indagine sul Reddito e Ricchezza)",
        "name_en": "Bank of Italy - Survey on Household Income and Wealth (SHIW)",
        "portal_url": "https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/index.html",
        "api_endpoint": "https://infostat.bancaditalia.it/inq/rest/sdmx/data/",
        "key_datasets": [
            "Household Wealth & Private Tutoring Expenditure (`Spesa delle famiglie per ripetizioni private e scuole paritarie`)",
            "Financial Literacy & Intergenerational Wealth Transfer (`Alfabetizzazione finanziaria giovani adulti`)"
        ],
        "extension_value": "Extends Household Burden ($O$) by quantifying private out-of-pocket compensatory spending (`ripetizioni private`) used by wealthier families to avoid grade repetition (`bocciatura`)."
    }
]

out_json = PROCESSED_DIR / "EXTENDED_OPEN_DATA_RESOURCES_AND_API_ROADMAP.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(extended_resources, f, indent=2, ensure_ascii=False)
print(f"Saved complete Extended Open Data Directory (`{len(extended_resources)}` resources) to `{out_json}`")

out_md = PROCESSED_DIR / "EXTENDED_OPEN_DATA_RESOURCES_AND_API_ROADMAP.md"
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# 🌐 Italienation: Extended Open Data Resources & API Integration Directory\n\n")
    f.write("**Purpose**: A definitive open-science roadmap identifying **10 high-value external statistical portals, SDMX REST endpoints, and institutional observatories** capable of extending our 26-domain repository across Italian NUTS-2 regions, municipalities, and EU benchmarks.\n\n")
    f.write("---\n\n")
    f.write("## 🏛️ Top 10 Institutional Open Data Resources for Future Ingestion\n\n")
    
    for i, res in enumerate(extended_resources, 1):
        f.write(f"### {i}. `{res['resource_id']}`: {res['name_it']}\n")
        f.write(f"* **English Name**: {res['name_en']}\n")
        f.write(f"* **Official Portal URL**: [{res['portal_url']}]({res['portal_url']})\n")
        f.write(f"* **SDMX / REST API Endpoint**: `{res['api_endpoint']}`\n")
        f.write(f"* **Key Datasets Available for Extraction**:\n")
        for ds in res['key_datasets']:
            f.write(f"  - {ds}\n")
        f.write(f"* **Strategic Extension Value ($O \\rightarrow T \\rightarrow E \\rightarrow D$)**: {res['extension_value']}\n\n")
        f.write("---\n\n")

    f.write("## 🛠️ Automated Query Client (`scripts/query_external_open_data_apis.py`)\n\n")
    f.write("To enable dynamic, programmatic retrieval from these external endpoints, researchers can utilize the modular query bridge provided in our repository.\n\n")
    f.write("*Produced by the Italienation Scientific Humility & Open Science Audit Team.*\n")

print(f"Saved complete Extended Open Data Markdown directory (`{len(extended_resources)}` portals) to `{out_md}`")
print("=== EXTENDED OPEN DATA ROADMAP COMPLETE ===")
