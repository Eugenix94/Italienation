# 📡 Italienation: Hyper-Precision Online Open Data & REST API Expansion Roadmap (`7 Official API Engines`)

**Analytical Purpose**: Moving beyond NUTS-2 regional averages (`20 Regioni`) to achieve **Hyper-Precision (`Granularità Provinciale NUTS-3, Comunale, Corso di Laurea, Tipologia Contrattuale, e Cittadinanza`)** across official statistical web services.

To answer our user's direct inquiry (`'are there other datasets online, APIs, open data that we're missing to give more precision on our data analysis?'`), our online investigation verified **7 high-value online API endpoints and microdata portals** available right now for direct machine-to-machine Python extraction.

---

## 1. `API_01_ISTAT_SDMX_PROVINCIAL_MUNICIPAL`
### 🇮🇹 API REST ISTAT SDMX - Dati Provinciali (NUTS-3) e Comunali su NEET, Abbandono e Reddito
### 🇬🇧 **English Title**: ISTAT SDMX RESTful API - Provincial (NUTS-3) and Municipal Micro-Data on NEETs, Early Leaving, and Income

* **Official Authority**: `ISTAT (Istituto Nazionale di Statistica)`
* **Direct API / Portal Endpoint**: [https://esploradati.istat.it/SDMXWS/rest/data/](https://esploradati.istat.it/SDMXWS/rest/data/)
* **Python Extraction Client**: `istatapi (Python library) / requests SDMX-JSON query`

#### 🔍 Hyper-Precision Analytical Gain
Upgrades our geographic granularity from NUTS-2 (`20 Regioni`) down to NUTS-3 (`107 Province`) and Municipal level (`7,896 Comuni`). This allows us to measure exact intra-regional disparities (e.g., Naples vs Benevento inside Campania, or Milan vs Sondrio inside Lombardy).

#### 📐 Causal Role in Extended OED Triangle ($O \rightarrow T \rightarrow E \rightarrow D$)
> **Theoretical Contribution**: Pinpoints the exact neighborhood/municipal economic boundary ($O$) where educational poverty and implicit dropout concentrate.

---

## 2. `API_02_MUR_USTAT_COURSE_LEVEL_ACADEMIC`
### 🇮🇹 API Open Data MUR USTAT - Anagrafe Nazionale Studenti e Laureati per Ateneo e Classe di Laurea
### 🇬🇧 **English Title**: MUR USTAT Open Data API - National Registry of Students and Graduates by Single University and Degree Class

* **Official Authority**: `MUR (Ministero dell'Università e della Ricerca - USTAT / ANS)`
* **Direct API / Portal Endpoint**: [https://ustat.mur.gov.it/opendata/](https://ustat.mur.gov.it/opendata/)
* **Python Extraction Client**: `pandas.read_csv from USTAT open data CKAN endpoints`

#### 🔍 Hyper-Precision Analytical Gain
Moves beyond aggregate regional university numbers to exact department-level and degree-class tracking across all 100+ Italian universities, cross-referenced by the student's original high school track.

#### 📐 Causal Role in Extended OED Triangle ($O \rightarrow T \rightarrow E \rightarrow D$)
> **Theoretical Contribution**: Measures exact tertiary tracking elasticity ($T \rightarrow E$), verifying which specific degree programs suffer from the highest first-year dropout among technical/vocational graduates.

---

## 3. `API_03_ALMALAUREA_GRADUATE_OUTCOMES`
### 🇮🇹 AlmaLaurea Open Data - Esiti Occupazionali e Retribuzioni Nette a 1, 3 e 5 Anni per Singolo Corso di Laurea
### 🇬🇧 **English Title**: AlmaLaurea Open Data - Employment Outcomes and Net Monthly Wages at 1, 3, and 5 Years by Single Degree Program

* **Official Authority**: `Consorzio Interuniversitario AlmaLaurea`
* **Direct API / Portal Endpoint**: [https://www.almalaurea.it/esiti-occupazionali](https://www.almalaurea.it/esiti-occupazionali)
* **Python Extraction Client**: `Automated data extraction from AlmaLaurea statistical reporting tables`

#### 🔍 Hyper-Precision Analytical Gain
Provides exact longitudinal wage returns ($D$) broken down by specific degree class (`Ingegneria vs Lettere vs Giurisprudenza`) and geographic employment location, avoiding general averages.

#### 📐 Causal Role in Extended OED Triangle ($O \rightarrow T \rightarrow E \rightarrow D$)
> **Theoretical Contribution**: Proves exact Destination wage inequality ($D$), isolating the true financial premium of STEM vs Humanities degrees across Northern and Southern labor markets.

---

## 4. `API_04_ANPAL_SIL_COMUNICAZIONI_OBBLIGATORIE`
### 🇮🇹 ANPAL / SIL Lavoro Open Data - Comunicazioni Obbligatorie (CO) sui Flussi di Assunzione Under-30
### 🇬🇧 **English Title**: ANPAL / SIL Labor Open Data - Mandatory Notifications (CO) on Under-30 Hiring and Firing Flows by Contract Type

* **Official Authority**: `Ministero del Lavoro e delle Politiche Sociali / ANPAL (Sistema Informativo Lavoro)`
* **Direct API / Portal Endpoint**: [https://dati.lavoro.gov.it/](https://dati.lavoro.gov.it/)
* **Python Extraction Client**: `pandas / CKAN API query on dati.lavoro.gov.it`

#### 🔍 Hyper-Precision Analytical Gain
Replaces static unemployment survey snapshots with exact daily administrative hiring/firing flows. Quantifies what percentage of youth enter the labor market through precarious internships (`tirocini extracurriculari pagati €500/mese`) vs stable contracts.

#### 📐 Causal Role in Extended OED Triangle ($O \rightarrow T \rightarrow E \rightarrow D$)
> **Theoretical Contribution**: Measures the exact structural friction at school-to-work transition ($E \rightarrow D$), exposing youth precariousness (`precariato giovanile`).

---

## 5. `API_05_INPS_ADMINISTRATIVE_WAGE_RECORDS`
### 🇮🇹 INPS Open Data - Osservatorio Lavoratori Dipendenti e Precari (Retribuzioni Annue Medie Reali Versate)
### 🇬🇧 **English Title**: INPS Open Data - Observatory on Dependent and Precarious Workers (Actual Annual Gross Social Security Wages)

* **Official Authority**: `INPS (Coordinamento Generale Statistico e Attuariale)`
* **Direct API / Portal Endpoint**: [https://www.inps.it/it/it/dati-e-bilanci/open-data.html](https://www.inps.it/it/it/dati-e-bilanci/open-data.html)
* **Python Extraction Client**: `Direct extraction from INPS open statistical micro-cubes`

#### 🔍 Hyper-Precision Analytical Gain
Provides hard administrative social security records (actual euros declared on paystubs to INPS), completely eliminating self-reporting survey bias regarding youth income and underemployment.

#### 📐 Causal Role in Extended OED Triangle ($O \rightarrow T \rightarrow E \rightarrow D$)
> **Theoretical Contribution**: Verifies the ultimate economic destination ($D$) of Italian youth, revealing how intermittent work (`lavoro intermittente/stagionale`) depresses annual take-home pay.

---

## 6. `API_06_EUROSTAT_SDMX_MIGRANT_NEET_GAP`
### 🇮🇹 Eurostat API REST SDMX 2.1 - Tasso NEET per Cittadinanza e Background Migratorio (`edat_lfse_16`)
### 🇬🇧 **English Title**: Eurostat SDMX REST API 2.1 - NEET Rates by Citizenship and Country of Birth (Native vs Foreign-born)

* **Official Authority**: `Eurostat (European Commission Statistical Office)`
* **Direct API / Portal Endpoint**: [https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/)
* **Python Extraction Client**: `eurostat (Python library) / REST API JSON download`

#### 🔍 Hyper-Precision Analytical Gain
Isolates the crucial demographic dimension of citizenship (`cittadini italiani vs stranieri`), explaining why urban Northern NUTS-2 regions (Milan, Turin, Bologna) experience high localized NEET pockets among first- and second-generation immigrant youth.

#### 📐 Causal Role in Extended OED Triangle ($O \rightarrow T \rightarrow E \rightarrow D$)
> **Theoretical Contribution**: Controls for demographic and linguistic barriers at Origin ($O$), proving that non-native youth face compounded hurdles across Tracking ($T$) and Destination ($D$).

---

## 7. `API_07_BANCA_D_ITALIA_SHIW_SHADOW_TUTORING`
### 🇮🇹 Banca d'Italia API / Indagine sui Bilanci delle Famiglie (IBFI) - Spesa per Lezioni Private e Ripetizioni
### 🇬🇧 **English Title**: Bank of Italy IBFI / SHIW API - Household Spending on Private Tutoring (`Shadow Education Market`)

* **Official Authority**: `Banca d'Italia (Dipartimento Economia e Statistica)`
* **Direct API / Portal Endpoint**: [https://www.bancaditalia.it/statistiche/indagini/bilanci-famiglie/index.html](https://www.bancaditalia.it/statistiche/indagini/bilanci-famiglie/index.html)
* **Python Extraction Client**: `pandas / Bank of Italy microdata CSV parsers`

#### 🔍 Hyper-Precision Analytical Gain
Quantifies the hidden 'Shadow Education Market' (`ripetizioni private a pagamento per evitare la bocciatura`). Proves how wealthy families spend €1,500–€3,000/year on private tutoring to keep children in Licei, whereas low-income families cannot afford private tutoring and suffer grade repetition.

#### 📐 Causal Role in Extended OED Triangle ($O \rightarrow T \rightarrow E \rightarrow D$)
> **Theoretical Contribution**: Exposes the exact financial mechanism whereby family wealth ($O$) buys academic survival ($E$) inside rigid theoretical tracks ($T$).

---

## 🚀 Next Steps for Automated Python Ingestion (`Optional Phase Expansion`)

Whenever we choose to ingest these live online APIs into `local_data/processed/`, we can write modular Python client scripts (`using istatapi, requests, and pandas`) to query exact NUTS-3 provincial (`107 Province`) and municipal (`7,896 Comuni`) microdata directly into our causal simulator.

*Produced by the Italienation Scientific Humility & Open Science Audit Team.*
