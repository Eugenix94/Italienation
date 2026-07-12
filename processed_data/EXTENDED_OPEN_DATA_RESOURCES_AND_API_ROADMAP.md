# 🌐 Italienation: Extended Open Data Resources & API Integration Directory

**Purpose**: A definitive open-science roadmap identifying **10 high-value external statistical portals, SDMX REST endpoints, and institutional observatories** capable of extending our 26-domain repository across Italian NUTS-2 regions, municipalities, and EU benchmarks.

---

## 🏛️ Top 10 Institutional Open Data Resources for Future Ingestion

### 1. `ISTAT_SDMX_API`: ISTAT I.Stat & Data Browser SDMX REST API
* **English Name**: ISTAT National Statistical Institute - SDMX REST API Endpoint
* **Official Portal URL**: [https://www.istat.it/it/dati-analisi-e-prodotti/bancare-dati/i-stat](https://www.istat.it/it/dati-analisi-e-prodotti/bancare-dati/i-stat)
* **SDMX / REST API Endpoint**: `https://esploradati.istat.it/SDMXWS/rest/data/`
* **Key Datasets Available for Extraction**:
  - EU-SILC Household Income and Intergenerational Educational Transmission (`Indagine sul Reddito e Condizioni di Vita`)
  - Early Childhood Care (Asili Nido 0-2 anni) Municipal & Provincial Coverage Rates (`Indagine Servizi Sociali Comuni`)
  - Youth Brain Drain (`Emigrazione Under-35 / Cancellazioni Anagrafiche AIRE per Provincia e Titolo di Studio`)
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends Origin ($O$) by quantifying exact provincial Asili Nido coverage (`#1 structural determinant of female youth inactivity`) and intergenerational educational mobility.

---

### 2. `MIM_PORTALE_UNICO_SCUOLA`: MIM Portale Unico dei Dati della Scuola - Open Data & Anagrafe
* **English Name**: Ministry of Education and Merit (MIM) - Open Data Portal & Registry
* **Official Portal URL**: [https://dati.istruzione.it/opendata/opendata/](https://dati.istruzione.it/opendata/opendata/)
* **SDMX / REST API Endpoint**: `https://dati.istruzione.it/opendata/api/v1/datasets`
* **Key Datasets Available for Extraction**:
  - School Building Infrastructure & Safety Registry (`Anagrafe Edilizia Scolastica SNAES - >40,000 edifici, vulnerabilità sismica, palestre, banda ultralarga`)
  - Teacher Precariato & Annual Substitutes (`Anagrafe Docenti e ATA: cattedre di ruolo vs supplenti annuali 30/06 e 31/08 per provincia e indirizzo`)
  - Class Overcrowding (`Alunni per Classe / Classi Pollaio nei gradi della secondaria`)
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends Tracking ($T$) by exposing exact teacher stability (`supplenze precari > 30% in VOC/TEC`) and structural building safety across individual school institutes.

---

### 3. `INVALSI_STATISTICO_API`: INVALSI Open Data & Gestione Dati Servizio Statistico
* **English Name**: National Institute for the Evaluation of the Education System (INVALSI) - Statistical Service
* **Official Portal URL**: [https://serviziostatistico.invalsi.it/open-data/](https://serviziostatistico.invalsi.it/open-data/)
* **SDMX / REST API Endpoint**: `https://serviziostatistico.invalsi.it/api/data/`
* **Key Datasets Available for Extraction**:
  - School-level ESCS Quintiles & Longitudinal Cohort Tracing (`Dati longitudinali Grado 2 -> Grado 13`)
  - School Value-Added (`Valore Aggiunto della Scuola: Effetto Scuola depurato dal background socio-economico ESCS`)
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends Education ($E$) by isolating pure pedagogical effectiveness (`Valore Aggiunto`) from initial socio-economic origin ($O$).

---

### 4. `INPS_OSSERVATORIO_PRECARIATO`: INPS Open Data & Osservatorio sul Precariato e sull'Apprendistato
* **English Name**: National Social Security Institute (INPS) - Labor Market & Apprenticeship Observatory
* **Official Portal URL**: [https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche/dati-cartacei---osservatori-statistici/osservatorio-sul-precariato.html](https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche/dati-cartacei---osservatori-statistici/osservatorio-sul-precariato.html)
* **SDMX / REST API Endpoint**: `https://dati.inps.it/api/v1/dataset/`
* **Key Datasets Available for Extraction**:
  - Monthly/Annual Contract Activations & Terminations by Age Bracket (`<25, 25-29, 30-34 anni`) and Province (`Tempo Indeterminato vs Determinato/Stagionale`)
  - Dual Apprenticeship vs Professional Apprenticeship (`Apprendistato art. 43 vs art. 44 per Provincia e Settore Produttivo`)
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends Destination ($D$) by diagnosing exact labor market contract precarity and tracing why dual vocational training (`Sistema Duale`) struggles in Southern provinces.

---

### 5. `INDIRE_ITS_MONITORING`: INDIRE & MIM Monitoraggio Nazionale ITS Academies (ISCED 4)
* **English Name**: National Institute for Documentation, Innovation and Educational Research (INDIRE) - ITS Academies Observatory
* **Official Portal URL**: [https://www.indire.it/progetto/its-istituti-tecnici-superiori/](https://www.indire.it/progetto/its-istituti-tecnici-superiori/)
* **SDMX / REST API Endpoint**: `https://dati.indire.it/its/api/v1/`
* **Key Datasets Available for Extraction**:
  - Directory of all 140+ ITS Foundations across Italian Regions
  - 1-Year and 3-Year Post-Diploma Employment Absorption Rates (`Tasso di occupazione coerente > 85% in Lombardia/Veneto/Emilia-Romagna`)
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends Education to Destination ($E \rightarrow D$) by documenting the high-performance post-secondary vocational training alternative (`ITS Academies ISCED 4`) capable of neutralizing NEET status.

---

### 6. `ALMALAUREA_CONSORTIUM_API`: Consorzio Interuniversitario AlmaLaurea - Open Data & Indagini sui Laureati
* **English Name**: AlmaLaurea Inter-University Consortium - Open Data API & Graduate Surveys
* **Official Portal URL**: [https://www.almalaurea.it/universita/dati-e-indagini](https://www.almalaurea.it/universita/dati-e-indagini)
* **SDMX / REST API Endpoint**: `https://dati.almalaurea.it/api/v2/surveys/`
* **Key Datasets Available for Extraction**:
  - Net Monthly Wages (`Retribuzione netta mensile a 1, 3, 5 anni`) by University and Degree Class (`Ingegneria vs Lettere vs Economia`)
  - Educational Mismatch & Over-Education (`Percentuale di laureati che svolgono mansioni che non richiedono la laurea`)
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends Destination ($D$) by measuring exact economic returns to university degrees across disciplines and quantifying brain drain pull factors.

---

### 7. `EUROSTAT_SDMX_REST`: Eurostat SDMX REST API & Database Esplorativo Europeo
* **English Name**: Eurostat European Statistical Office - SDMX REST API & Data Browser
* **Official Portal URL**: [https://ec.europa.eu/eurostat/data/database](https://ec.europa.eu/eurostat/data/database)
* **SDMX / REST API Endpoint**: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/`
* **Key Datasets Available for Extraction**:
  - Labor Force Survey Regional Series (`lfst_r_lfse_att: NEET NUTS-2 by Gender and Age`)
  - Early Leavers from Education and Training (`edat_lfse_16: ELET by NUTS-2 Region`)
  - Structure of Earnings Survey (`earn_ses_pub: Hourly earnings deciles across EU states`)
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends International Benchmarking by providing real-time REST API queries across all EU-27 NUTS-2 regions for ELET and NEET monitoring.

---

### 8. `MEF_PNRR_ITALIA_DOMANI`: MEF RGS & Italia Domani - Open Data PNRR Missione 4 (Istruzione e Ricerca)
* **English Name**: Ministry of Economy and Finance (MEF) - National Recovery and Resilience Plan (PNRR) Open Data Portal
* **Official Portal URL**: [https://www.italiadomani.gov.it/it/open-data.html](https://www.italiadomani.gov.it/it/open-data.html)
* **SDMX / REST API Endpoint**: `https://dati.italiadomani.gov.it/api/v1/projects`
* **Key Datasets Available for Extraction**:
  - PNRR Missione 4 Investimenti (`M4C1I1.1 Asili Nido, M4C1I1.3 Scuola 4.0, M4C1I1.4 Dispersione Scolastica, M4C1I3.1 Nuove Competenze STEM`)
  - Project Level SAL (`Stato di Avanzamento Lavori, Importo PNRR, Comune Beneficiario, Cronoprogramma`)
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends Policy DIY Simulation by tracking real-time deployment of €30+ Billion in PNRR public infrastructure and pedagogical interventions.

---

### 9. `ANPAL_GOL_MONITORING`: ANPAL & MLPS - Sistema Informativo Lavoro e Programma GOL (Garanzia Occupabilità Lavoratori)
* **English Name**: National Agency for Active Labor Policies (ANPAL) - Active Labor Market Program (GOL) Observatory
* **Official Portal URL**: [https://www.anpal.gov.it/dati-e-pubblicazioni](https://www.anpal.gov.it/dati-e-pubblicazioni)
* **SDMX / REST API Endpoint**: `https://dati.anpal.gov.it/api/v1/gol/`
* **Key Datasets Available for Extraction**:
  - GOL Youth Profiling (`Assessment di distanza dal mercato del lavoro per NEET 15-29 anni`)
  - Active Labor Market Upskilling & Reskilling Insertion Rates by Region
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends Destination ($D$) by analyzing active labor policy remedies designed to rescue long-term NEETs from welfare dependency.

---

### 10. `BANK_OF_ITALY_SHIW`: Banca d'Italia - Indagine sui Bilanci delle Famiglie (SHIW / Indagine sul Reddito e Ricchezza)
* **English Name**: Bank of Italy - Survey on Household Income and Wealth (SHIW)
* **Official Portal URL**: [https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/index.html](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/index.html)
* **SDMX / REST API Endpoint**: `https://infostat.bancaditalia.it/inq/rest/sdmx/data/`
* **Key Datasets Available for Extraction**:
  - Household Wealth & Private Tutoring Expenditure (`Spesa delle famiglie per ripetizioni private e scuole paritarie`)
  - Financial Literacy & Intergenerational Wealth Transfer (`Alfabetizzazione finanziaria giovani adulti`)
* **Strategic Extension Value ($O \rightarrow T \rightarrow E \rightarrow D$)**: Extends Household Burden ($O$) by quantifying private out-of-pocket compensatory spending (`ripetizioni private`) used by wealthier families to avoid grade repetition (`bocciatura`).

---

## 🛠️ Automated Query Client (`scripts/query_external_open_data_apis.py`)

To enable dynamic, programmatic retrieval from these external endpoints, researchers can utilize the modular query bridge provided in our repository.

*Produced by the Italienation Scientific Humility & Open Science Audit Team.*
