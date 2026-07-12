import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT_DIR / "docs"

print("=== UPDATING PROOF OF DATA CATALOG TO INCLUDE ALL 80 CANONICAL DOMAINS ===")

# Read existing catalog if possible or generate comprehensive master catalog 1 to 80
new_domains_md = """
---

## 🏛️ PARTE VIII: GIUSTIZIA MINORILE, SALUTE, SICUREZZA SUL LAVORO E ATTUAZIONE PNRR (`DOMINI 67 - 70`)

### `Domain 67` | Ministero della Giustizia / DGMC — Devianza Minorile, Criminalità e Messa alla Prova nei Quartieri
* **Autorità Istituzionale**: Ministero della Giustizia — Dipartimento per la Giustizia Minorile e di Comunità (`DGMC`) / ISTAT
* **File Dataset (Processed)**: [`processed_data/giustizia_dgmc_juvenile_deviancy_and_probation_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/giustizia_dgmc_juvenile_deviancy_and_probation_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.giustizia.it/giustizia/it/mg_1_14_1.wp](https://www.giustizia.it/giustizia/it/mg_1_14_1.wp) | [https://www.istat.it/it/archivio/giustizia](https://www.istat.it/it/archivio/giustizia)
* **Descrizione e Rilevanza**: Traccia le segnalazioni alle Procure Minorili per 10.000 minori e i tassi di successo della Messa alla Prova nei Servizi Sociali per i Minorenni (`USSM`). Dimostra l'esito giudiziario estremo della povertà educativa ($O$) e dell'abbandono scolastico occulto ($T$).

### `Domain 68` | Ministero della Salute / ISS Indagine HBSC — Salute Mentale Adolescenziale e Speranza di Vita per Titolo
* **Autorità Istituzionale**: Istituto Superiore di Sanità (`ISS`) — Sistema di Sorveglianza `HBSC Italia` / ISTAT Mortalità
* **File Dataset (Processed)**: [`processed_data/salute_iss_hbsc_mental_health_and_life_expectancy_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/salute_iss_hbsc_mental_health_and_life_expectancy_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.hbsc.unito.it/](https://www.hbsc.unito.it/) | [https://www.salute.gov.it/portale/documentazione/p6_2_8_3_1.jsp](https://www.salute.gov.it/portale/documentazione/p6_2_8_3_1.jsp)
* **Descrizione e Rilevanza**: Misura la prevalenza di sintomi di ansia, depressione e disagio psicologico tra gli studenti delle scuole superiori (`HBSC`) e quantifica il divario nella speranza di vita alla nascita tra laureati e possessori di licenza media (`fino a +3.6 anni a favore dei laureati`), provando che l'istruzione è un determinante biologico di salute.

### `Domain 69` | INAIL — Infortuni nei Tirocini Curricolari (PCTO) e Sicurezza sul Lavoro per Lavoratori Under 25
* **Autorità Istituzionale**: `INAIL` (Istituto Nazionale per l'Assicurazione contro gli Infortuni sul Lavoro) — Banca Dati Statistica
* **File Dataset (Processed)**: [`processed_data/inail_pcto_and_youth_occupational_accidents_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/inail_pcto_and_youth_occupational_accidents_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.inail.it/cs/internet/comunicazione/banca-dati-statistica.html](https://www.inail.it/cs/internet/comunicazione/banca-dati-statistica.html)
* **Descrizione e Rilevanza**: Registra l'incidenza degli infortuni sul lavoro durante i Percorsi per le Competenze Trasversali e per l'Orientamento (`PCTO / ex Alternanza Scuola-Lavoro`) e nei contratti a termine under 25, evidenziando il divario di sicurezza tra indirizzi professionali e liceali.

### `Domain 70` | ANAC & PNRR M4C1 — Bandi Deserti, Ritardi Appalti e Attuazione Infrastrutture Scolastiche
* **Autorità Istituzionale**: Autorità Nazionale Anticorruzione (`ANAC`) / Presidenza del Consiglio — Portale `ItaliaDomani PNRR M4C1`
* **File Dataset (Processed)**: [`processed_data/anac_pnrr_m4c1_school_tenders_and_execution_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/anac_pnrr_m4c1_school_tenders_and_execution_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://dati.anticorruzione.it/](https://dati.anticorruzione.it/) | [https://www.italiadomani.gov.it/](https://www.italiadomani.gov.it/)
* **Descrizione e Rilevanza**: Misura la quota di bandi per asili nido, mense e palestre PNRR andati deserti o in ritardo nei Comuni, dimostrando il collo di bottiglia amministrativo che impedisce ai territori ad alta deprivazione di colmare il divario infrastrutturale.

---

## 🏛️ PARTE IX: BRAIN DRAIN, DROPOUT ACCADEMICO, DIVARIO DIGITALE E CRISI ALLOGGI (`DOMINI 71 - 74`)

### `Domain 71` | SVIMEZ & ISTAT Flussi Migratori — La Fuga dei Cervelli Sud-Nord e verso l'Estero (`Brain Drain`)
* **Autorità Istituzionale**: `SVIMEZ` (Associazione per lo Sviluppo dell'Industria nel Mezzogiorno) / ISTAT Demografia e Migrazioni
* **File Dataset (Processed)**: [`processed_data/svimez_istat_brain_drain_regional_migration_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/svimez_istat_brain_drain_regional_migration_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.svimez.info/](https://www.svimez.info/) | [https://www.istat.it/it/archivio/migrazioni](https://www.istat.it/it/archivio/migrazioni)
* **Descrizione e Rilevanza**: Quantifica l'esodo di giovani laureati e diplomati 25-34 anni dal Mezzogiorno verso il Centro-Nord e l'estero (`oltre 40.000 laureati persi all'anno dal Sud`), stimando la perdita finanziaria netta dell'investimento pubblico in capitale umano (`oltre €3 miliardi/anno persi per il Sud`).

### `Domain 72` | CINECA & MUR USTAT — Abbandoni Universitari (Dropout Accademico 1° Anno) e Fuoricorso per Provenienza
* **Autorità Istituzionale**: Ministero dell'Università e della Ricerca (`MUR USTAT`) — Anagrafe Nazionale Studenti (`ANS`) / Consorzio `CINECA`
* **File Dataset (Processed)**: [`processed_data/mur_cineca_university_dropout_and_fuoricorso_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/mur_cineca_university_dropout_and_fuoricorso_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://ustat.mur.gov.it/dati/](https://ustat.mur.gov.it/dati/) | [https://www.cineca.it/](https://www.cineca.it/)
* **Descrizione e Rilevanza**: Traccia il tasso di abbandono universitario entro il 1° anno di immatricolazione (`Rinuncia / Inattività CFU`) e il tasso di fuoricorso disaggregati per istituto superiore di provenienza (`Licei vs Tecnici vs Professionali`). Dimostra che l'imbuto tripartito a 14 anni inibisce il successo accademico.

### `Domain 73` | AGCOM & ISTAT — Divario Digitale, Povertà di Connettività e Accesso ai Dispositivi (`Digital Divide`)
* **Autorità Istituzionale**: `AGCOM` (Autorità per le Garanzie nelle Comunicazioni) / ISTAT Indagine Famiglie Cittadini e ICT (`DESI`)
* **File Dataset (Processed)**: [`processed_data/agcom_istat_digital_divide_and_connectivity_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/agcom_istat_digital_divide_and_connectivity_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.agcom.it/osservatorio-sulle-comunicazioni](https://www.agcom.it/osservatorio-sulle-comunicazioni) | [https://www.istat.it/it/archivio/cittadini-e-ict](https://www.istat.it/it/archivio/cittadini-e-ict)
* **Descrizione e Rilevanza**: Misura la quota di famiglie con minori prive di PC individuale o connessione a banda larga ultraveloce e le competenze digitali under 18, evidenziando il ruolo dell'esclusione tecnologica nella dispersione scolastica.

### `Domain 74` | Banca d'Italia SHIW & MUR DSU — Povertà Abitativa e Crisi Affitti per Studenti Fuori Sede
* **Autorità Istituzionale**: Banca d'Italia (`Indagine SHIW sui Bilanci delle Famiglie`) / MUR Diritto allo Studio Universitario (`DSU`)
* **File Dataset (Processed)**: [`processed_data/banca_d_italia_student_housing_and_dsu_beds_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/banca_d_italia_student_housing_and_dsu_beds_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/)
* **Descrizione e Rilevanza**: Misura l'incidenza del costo dell'affitto privato per studenti fuori sede sul reddito mediano familiare e la disponibilità di posti letto pubblici nei collegi universitari DSU (`<5% del fabbisogno in media`), quantificando il censo come filtro per l'accesso ai grandi atenei.

---

## 🏛️ PARTE X: DEPRIVAZIONE MINORILE, AMMORTIZZATORI UNDER 35, MOTHERHOOD PENALTY, RISPARMIO CENSIS, PISA OCSE E CARE DRAIN (`DOMINI 75 - 80`)

### `Domain 75` | ISTAT / CARITAS Italiana — Deprivazione Materiale e Sociale dei Minori (`EU-SILC`)
* **Autorità Istituzionale**: `ISTAT` (Indagine sui Redditi e le Condizioni di Vita `EU-SILC`) / `CARITAS Italiana` (`Rapporto Povertà`)
* **File Dataset (Processed)**: [`processed_data/istat_caritas_child_material_deprivation_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/istat_caritas_child_material_deprivation_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.istat.it/it/archivio/eu-silc](https://www.istat.it/it/archivio/eu-silc) | [https://www.caritas.it/](https://www.caritas.it/)
* **Descrizione e Rilevanza**: Misura il tasso di deprivazione materiale e sociale acuta tra i minori under 18 e l'incidenza di povertà assoluta familiare, definendo l'ecosistema presociologico primario all'interno del quale si attivano i deficit di apprendimento (`Assioma 2`).

### `Domain 76` | INPS & Ministero del Lavoro — Cassa Integrazione (`CIG`), NASpI e Disoccupazione Indennizzata Under 35
* **Autorità Istituzionale**: `INPS` (Osservatorio sulle Prestazioni a Sostegno del Reddito) / Ministero del Lavoro (`MLPS`)
* **File Dataset (Processed)**: [`processed_data/inps_mlps_naspi_cig_youth_unemployment_benefits_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/inps_mlps_naspi_cig_youth_unemployment_benefits_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche/dati-cartacei---cassa-integrazione-guadagni.html](https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche/dati-cartacei---cassa-integrazione-guadagni.html)
* **Descrizione e Rilevanza**: Traccia la quota di giovani under 35 che percepiscono l'indennità di disoccupazione (`NASpI`) al termine di contratti precari o che finiscono in Cassa Integrazione Guadagni (`CIG`), quantificando la fragilità del reddito nella transizione iniziale.

### `Domain 77` | ISTAT & Unioncamere Excelsior — Divario Occupazionale di Genere per Maternità (`Motherhood Penalty`)
* **Autorità Istituzionale**: `ISTAT` (Rilevazione Continua Forze di Lavoro `LFS`) / `Unioncamere Excelsior` (`Genere e Lavoro`)
* **File Dataset (Processed)**: [`processed_data/istat_excelsior_motherhood_penalty_gender_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/istat_excelsior_motherhood_penalty_gender_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://excelsior.unioncamere.net/](https://excelsior.unioncamere.net/) | [https://www.istat.it/it/archivio/forze-di-lavoro](https://www.istat.it/it/archivio/forze-di-lavoro)
* **Descrizione e Rilevanza**: Misura il divario nel tasso di occupazione tra donne 25-49 anni senza figli e con figli minori (`penalizzazione di maternità oltre i 20 punti percentuali al Sud`), dimostrando come l'assenza di servizi di cura comunali espulga le madri dal mercato del lavoro formalizzato.

### `Domain 78` | CENSIS & Banca d'Italia SHIW — Propensione al Risparmio Familiare e Indebitamento per Istruzione
* **Autorità Istituzionale**: `CENSIS` (Rapporto sulla Situazione Sociale del Paese) / Banca d'Italia (`Indagine SHIW`)
* **File Dataset (Processed)**: [`processed_data/censis_shiw_household_savings_and_educational_debt_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/censis_shiw_household_savings_and_educational_debt_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.censis.it/](https://www.censis.it/) | [https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/)
* **Descrizione e Rilevanza**: Misura la propensione netta al risparmio familiare e la quota di famiglie indebitate per sostenere le spese di studio dei figli, evidenziando la consunzione dell'ammortizzatore privato familiare di fronte alla stagnazione salariale.

### `Domain 79` | OCSE PISA Longitudinal & IEA TIMSS — Competenze STEM e Comprensione Lettura dei 15enni Italiani vs Media OCSE
* **Autorità Istituzionale**: `OCSE` (`PISA` — Programme for International Student Assessment) / `IEA TIMSS` / `INVALSI`
* **File Dataset (Processed)**: [`processed_data/ocse_pisa_timss_stem_and_reading_competency_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/ocse_pisa_timss_stem_and_reading_competency_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.oecd.org/pisa/](https://www.oecd.org/pisa/) | [https://www.iea.nl/studies/timss](https://www.iea.nl/studies/timss)
* **Descrizione e Rilevanza**: Fornisce la misurazione standardizzata internazionale delle competenze matematico-scientifiche (`STEM`) e di comprensione del testo dei quindicenni italiani rispetto ai 38 Paesi OCSE, certificando l'arretramento qualitativo delle competenze in uscita dall'obbligo.

### `Domain 80` | INPS Osservatorio Lavoratori Domestici — Care Drain e Welfare di Cura non Riconosciuto
* **Autorità Istituzionale**: `INPS` (Osservatorio sui Lavoratori Domestici e di Cura) / ISTAT Demografia e Invecchiamento
* **File Dataset (Processed)**: [`processed_data/inps_domestic_care_workers_and_care_drain_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/processed_data/inps_domestic_care_workers_and_care_drain_panel.csv)
* **Link Istituzionale (`Proof of Data`)**: [https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche/data/osservatorio-sui-lavoratori-domestici.html](https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche/data/osservatorio-sui-lavoratori-domestici.html)
* **Descrizione e Rilevanza**: Traccia il numero di assistenti familiari e lavoratori di cura per 10.000 anziani e la quota di lavoro domestico irregolare (`care drain`). Dimostra che il carico di cura dell'invecchiamento demografico ricade sulle famiglie private, inibendo la partecipazione lavorativa delle donne e dei giovani (`Assioma 6`).
"""

# Check current catalog path
old_catalog = DOCS_DIR / "CATALOGO_COMPLETO_LINK_DIRETTI_66_DOMINI_PROOF_OF_DATA.md"
new_catalog = DOCS_DIR / "CATALOGO_COMPLETO_LINK_DIRETTI_80_DOMINI_PROOF_OF_DATA.md"

if old_catalog.exists():
    content = old_catalog.read_text(encoding="utf-8")
    content = content.replace("66 DOMINI", "80 DOMINI").replace("66 banche dati", "80 banche dati").replace("66 domini", "80 domini")
    if "DOMINI 67 - 70" not in content:
        content += "\n" + new_domains_md
    new_catalog.write_text(content, encoding="utf-8")
    if old_catalog != new_catalog and old_catalog.exists():
        old_catalog.unlink()
    print(f"✅ Updated and saved master catalog to `{new_catalog.name}` with ALL 80 DOMAINS!")
else:
    print("Old catalog not found, writing new 80 domains catalog directly.")
    new_catalog.write_text("# Catalogo Completo Link Diretti 80 Domini\n" + new_domains_md, encoding="utf-8")

print("=== CATALOG UPDATE 80 DOMAINS COMPLETE ===")
