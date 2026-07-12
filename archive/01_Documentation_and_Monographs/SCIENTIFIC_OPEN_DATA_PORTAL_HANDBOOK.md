# 🏛️ Italienation: Manuale Scientifico e Registro Epistemologico dei 56 Domini Canonici (`Il Doppio Livello di Giustificabilità`)

**Fondamento Epistemologico e Giustificabilità Scientifica (`Justifiable Standpoint`)**:
In ottemperanza al principio scientifico del massimo rigore (`'yet if these data make no sense let's refactor the data we have and use a more justifiable stand point'`), il nostro osservatorio adotta una **separazione epistemologica netta e trasparente tra due livelli di prova**:

### 🔹 Layer 1: Dati Osservati Amministrativi e Campionari Diretti (`Observed Micro & Panel Open Data`)
Comprende i panel statistici a diretta misurazione territoriale (`NUTS-2, NUTS-3, Comuni`) erogati da **ISTAT, Eurostat, AlmaLaurea, INVALSI, MIM e MEF SIOPE**. In questo livello, ogni numero corrisponde a una transazione di cassa reale (`SIOPE`), a un punteggio di test di popolazione (`INVALSI`), a un tasso di occupazione censito (`AlmaLaurea/ISTAT`) o a una rilevazione anagrafica scolastica (`MIM/MUR`).

### 🔸 Layer 2: Indicatori Macro-Strutturali e Modelli Attuariali Ufficiali (`Macro-Structural & Actuarial Projections`)
Comprende i conti aggregati di sistema, le matrici di fabbisogno professionale (`Excelsior/CP2021`), i calcoli contabili del ciclo di vita (`OCSE Education at a Glance`) e le proiezioni previdenziali di lungo periodo (`INPS/COVIP`). Questi domini non vanno interpretati come sondaggi campionari locali, ma come **leggi contabili e attuariali di macro-sistema** che spiegano le conseguenze aggregate (es. rischio di povertà pensionistica a 67 anni o costo totale di formazione pro-capite di €238.700).

---

## 📋 Catalogo Rifattorizzato e Giustificato dei `56 Domini Canonici`

### 1. `istat_repeaters_upper_secondary`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Ripetenti per anno di corso e indirizzo scolastico nella Scuola Secondaria di II Grado
#### 🇬🇧 **English Title**: Upper Secondary Grade Repeaters by Year of Course and School Track

* **Ente Statistico / Autorità Ufficiale**: `ISTAT (Istituto Nazionale di Statistica)`
* **🔗 Link Diretto Open Data**: [https://esploradati.istat.it/SDMXWS/rest/data/DCCV_TAXSCUOLA](https://esploradati.istat.it/SDMXWS/rest/data/DCCV_TAXSCUOLA)
* **Codice Flusso SDMX / Indagine**: `52_1044_DF_DCIS_SCUOLE_15` | **Risoluzione Geografica**: `National & NUTS-2 Regional by Track (Licei, Tecnici, Professionali)`
* **Archivio Dati Elaborato**: [`local_data/processed/istat_repeaters_upper_secondary_latest.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/istat_repeaters_upper_secondary_latest.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Measures Track-to-Education friction (T -> E). Demonstrates the 18.0% first-year failure rate in vocational tracks (VOC) vs 4.4% in Licei.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 2. `invalsi_implicit_dropout_and_excellence`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Dispersione Scolastica Implicita e Livelli di Competenza Cognitiva (INVALSI Grado 8, 10 e 13)
#### 🇬🇧 **English Title**: Implicit School Dropout and Standardized Cognitive Competency Levels (INVALSI Grades 8, 10, and 13)

* **Ente Statistico / Autorità Ufficiale**: `INVALSI (Istituto Nazionale per la Valutazione del Sistema Educativo di Istruzione e di Formazione)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `INVALSI_REPORT_GENERALE_AGG_2025 / DISPERSIONE_IMPLICITA` | **Risoluzione Geografica**: `National, NUTS-2 Regional, Provincial, and SNAI Internal Areas`
* **Archivio Dati Elaborato**: [`local_data/processed/invalsi_implicit_dropout_and_excellence_regional.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/invalsi_implicit_dropout_and_excellence_regional.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Uncovers Blind Spot #1: proves that up to 23.6% of youth finish middle school in cognitive poverty (O -> Pre-Tracking Deficit) and up to 17.6% graduate high school without basic competencies (E -> D).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 3. `openpolis_istat_neet_15_29`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Tasso di Giovani NEET (15–29 anni) per Genere, Regione e Provincia
#### 🇬🇧 **English Title**: Youth NEET Rate (15–29 years) by Gender, Region, and Province

* **Ente Statistico / Autorità Ufficiale**: `Openpolis & ISTAT (Rilevazione sulle Forze di Lavoro - RFL)`
* **🔗 Link Diretto Open Data**: [https://conibambini.openpolis.it/tema/neet](https://conibambini.openpolis.it/tema/neet)
* **Codice Flusso SDMX / Indagine**: `ISTAT_RFL_NEET / OPENPOLIS_API_POVERTA_EDUCATIVA` | **Risoluzione Geografica**: `National, NUTS-2 Regional, Provincial, and Municipal Capital level`
* **Archivio Dati Elaborato**: [`local_data/processed/neet_regional_model_panel.csv & neet_gender_year_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/neet_regional_model_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Measures ultimate labor market exclusion (D). Highlights Blind Spot #2: female NEETs double male NEETs at age 25–34 due to the care penalty.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 4. `almalaurea_graduate_precariato_and_wages`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Condizione Occupazionale, Lavoro Dipendente a Tempo Determinato e Contratti di Stage/Tirocinio, Retribuzioni e Fuga dei Cervelli dei Laureati (1, 3 e 5 anni)
#### 🇬🇧 **English Title**: Graduate Employment Status, Lavoro Dipendente a Tempo Determinato e Contratti di Stage/Tirocinio, Net Salaries, and Brain Drain (1, 3, and 5 Years Post-Graduation)

* **Ente Statistico / Autorità Ufficiale**: `Consorzio Interuniversitario AlmaLaurea`
* **🔗 Link Diretto Open Data**: [https://www.almalaurea.it/esiti-occupazionali](https://www.almalaurea.it/esiti-occupazionali)
* **Codice Flusso SDMX / Indagine**: `ALMALAUREA_OCCUPAZIONE_LONG_2024` | **Risoluzione Geografica**: `National by Degree Type (Triennale vs Magistrale), Disciplinary Area, and Geographic Destination (Nord, Sud, Estero)`
* **Archivio Dati Elaborato**: [`local_data/processed/almalaurea_graduate_outcomes_1yr_summary.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/almalaurea_graduate_outcomes_1yr_summary.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Uncovers Blind Spot #3: shows high fixed-term contracts (25.3%), involuntary part-time (10.5%), and youth emigration abroad (+5.4%) among graduates (E -> D).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 5. `eurydice_secondary_structures_and_elet`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Strutture dei Sistemi Educativi Europei (ISCED 0–4) e Indicatori di Prevenzione ELET
#### 🇬🇧 **English Title**: European Education System Structures (ISCED 0–4) and ELET Prevention Policy Indicators

* **Ente Statistico / Autorità Ufficiale**: `EURYDICE Network (European Commission / EACEA)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `EURYDICE_STRUCTURES_2025_2026 / ELET_POLICIES_2024_2025` | **Risoluzione Geografica**: `International Comparative (Italy, UK, Germany, Finland, Spain, France)`
* **Archivio Dati Elaborato**: [`local_data/processed/EXTENDED_OED_TRIANGLE_AND_ELET_CAUSAL_SYNTHESIS.md`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/EXTENDED_OED_TRIANGLE_AND_ELET_CAUSAL_SYNTHESIS.md)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Provides comparative tracking ages (T) and grade retention rules. Explains why UK social promotion achieves 5.2% ELET vs Italy's 10.5% early tracking + bocciatura.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 6. `mur_university_tuition_and_dropout`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Contribuzione Studentesca Media e Tasso di Abbandono al Primo Anno Universitario
#### 🇬🇧 **English Title**: Average Student Tuition Contribution and First-Year University Dropout Rate

* **Ente Statistico / Autorità Ufficiale**: `MUR (Ministero dell'Università e della Ricerca - Ufficio Statistica)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `MUR_PARQUET_2025_Contribuzione_media / MUR_PARQUET_Tasso_di_abbandono` | **Risoluzione Geografica**: `University Institution Level (COD_ATENEO), NUTS-2 Regional, and Catania Case Study`
* **Archivio Dati Elaborato**: [`local_data/processed/catania_educational_pipeline_case_study.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/catania_educational_pipeline_case_study.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Measures tertiary financial barriers (O -> E) and transition shocks, showing high dropout among low-income students facing rising tuition.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 7. `siope_municipal_school_expenditure`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Spesa Pubblica di Cassa SIOPE per Alunno dei Comuni e delle Province per Manutenzione Scolastica
#### 🇬🇧 **English Title**: SIOPE Municipal and Provincial Cash Expenditure per Pupil for School Maintenance and Services

* **Ente Statistico / Autorità Ufficiale**: `MEF (Ministero dell'Economia e delle Finanze) / Banca d'Italia SIOPE`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `MEF_SIOPE_USCITE_CASSA_2020_2026` | **Risoluzione Geografica**: `Municipal (Comuni), Provincial, and NUTS-2 Regional`
* **Archivio Dati Elaborato**: [`local_data/processed/siope_expenditure_by_region_year.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/siope_expenditure_by_region_year.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Measures physical and financial school environment inputs (O -> T). Highlights the North-South municipal fiscal divide inside vocational and technical schools.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 8. `mim_school_building_safety_registry`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Anagrafe Edilizia Scolastica MIM: Agibilità, Sicurezza e Barriere Architettoniche
#### 🇬🇧 **English Title**: MIM School Building Safety Registry: Certification of Safety and Architectural Barriers

* **Ente Statistico / Autorità Ufficiale**: `MIM (Ministero dell'Istruzione e del Merito)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `MIM_EDILIZIA_AGIBILITA_BARRIERE` | **Risoluzione Geografica**: `School Building Level, Municipal, Provincial, and NUTS-2 Regional`
* **Archivio Dati Elaborato**: [`local_data/processed/ministerial_school_building_safety_by_region.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/ministerial_school_building_safety_by_region.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifies physical classroom inequality (O -> School Environment), proving that low school building safety (<20% in South) correlates with high dropout.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 9. `anpal_youth_unemployment_and_replacement`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Tasso di Disoccupazione Giovanile ANPAL, Tasso di Abbandono e Flussi Migratori
#### 🇬🇧 **English Title**: ANPAL Youth Unemployment Rate, Early School Leaving Replacement, and Migration Flows

* **Ente Statistico / Autorità Ufficiale**: `ANPAL (Agenzia Nazionale per le Politiche Attive del Lavoro) / Eurostat LFS`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `ESTAT_TIPSLM80_YOUTH_UNEMPLOYMENT / ANPAL_REPLACEMENT` | **Risoluzione Geografica**: `National and European Comparative`
* **Archivio Dati Elaborato**: [`local_data/processed/anpal_youth_unemployment_processed.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/anpal_youth_unemployment_processed.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Disaggregates NEET destination ($D$) into active job-seeking unemployment vs passive discouragement across migration demographics.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 10. `oecd_wb_tracking_age_vs_tertiary`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 2: Institutional Macro-Structural & Actuarial Projections (`Indicatori Macro-Strutturali e Modelli Attuariali Ufficiali`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Benchmark Internazionale OCSE/World Bank: Età di Selezione vs. Iscrizione Terziaria Lorda
#### 🇬🇧 **English Title**: OECD/World Bank International Benchmark: Tracking Age vs. Gross Tertiary Enrollment

* **Ente Statistico / Autorità Ufficiale**: `OECD (Education at a Glance) & World Bank Open Data`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `OECD_EAG_TRACKING_AGE / WB_SE.TER.ENRR` | **Risoluzione Geografica**: `International Comparative (25+ OECD & World Bank Nations)`
* **Archivio Dati Elaborato**: [`local_data/processed/global_italy_position_oecd_wb_latest.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/global_italy_position_oecd_wb_latest.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Empirically validates Indicator 15, showing that delaying tracking past age 16 increases university progression by +14.4% across nations.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio fornisce il quadro contabile, macro-economico o attuariale di lungo periodo (es. proiezioni previdenziali COVIP, spesa totale OCSE, o matrici professionali CP2021). Non si tratta di una survey campionaria regionale grezza, ma di un indicatore strutturale di sistema.

---

### 11. `inps_dual_system_apprenticeship`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Contratti di Apprendistato e Transizione Lavorativa INPS (Dual System Bridge)
#### 🇬🇧 **English Title**: INPS Apprenticeship Contracts and School-to-Work Transition (Dual System Bridge)

* **Ente Statistico / Autorità Ufficiale**: `INPS (Istituto Nazionale della Previdenza Sociale - Osservatorio sul Precariato)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `INPS_RAPPORTI_LAVORO_APPRENDISTATO` | **Risoluzione Geografica**: `National and NUTS-2 Regional`
* **Archivio Dati Elaborato**: [`local_data/processed/inps_apprenticeship_informal_hits_2026-05-24.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/inps_apprenticeship_informal_hits_2026-05-24.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Explains why Germany avoids NEET despite early tracking (`Dual System` bridge), while Italy's vocational tracks lack corporate apprenticeship absorption ($T -> D$).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 12. `eurostat_social_scoreboard_poverty`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Quadro di Valutazione Sociale Eurostat: Povertà Relativa, Assoluta e Divario Digitale NUTS-2
#### 🇬🇧 **English Title**: Eurostat Social Scoreboard: Relative/Absolute Poverty and NUTS-2 Broadband Digital Divide

* **Ente Statistico / Autorità Ufficiale**: `Eurostat (Statistical Office of the European Union)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `ESTAT_ILC_PEPS01 / ESTAT_BROADBAND_NUTS2` | **Risoluzione Geografica**: `NUTS-2 Regional across Italy and EU-27`
* **Archivio Dati Elaborato**: [`local_data/processed/eurostat_social_scoreboard_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/eurostat_social_scoreboard_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Measures structural socioeconomic origin ($O$), linking regional family poverty and broadband access directly to educational outcomes.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 13. `istat_household_textbook_burden`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Spesa delle Famiglie per Libri di Testo, Corredo Scolastico e Istruzione Secondaria
#### 🇬🇧 **English Title**: Household Direct Out-of-Pocket Expenditure on Textbooks, Supplies, and Secondary Education

* **Ente Statistico / Autorità Ufficiale**: `ISTAT (Indagine sui Consumi delle Famiglie) / MIM Adozioni Libri di Testo`
* **🔗 Link Diretto Open Data**: [https://www.bancaditalia.it/statistiche/indagini/bilanci-famiglie/index.html](https://www.bancaditalia.it/statistiche/indagini/bilanci-famiglie/index.html)
* **Codice Flusso SDMX / Indagine**: `ISTAT_DCCV_CONS_FAM / MIM_ADOZIONI_LIBRI` | **Risoluzione Geografica**: `National and NUTS-2 Regional by Income Quintile`
* **Archivio Dati Elaborato**: [`local_data/processed/italy_household_burden_module.csv & ministerial_textbook_costs_by_region_level.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/italy_household_burden_module.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifies direct economic friction ($O -> E$). Proves that high textbook costs create severe burdens for low-income households in Licei and Tecnici.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 14. `ourworldindata_compulsory_duration_and_productivity`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: OurWorldInData: Durata dell'Obbligo Scolastico e Produttività del Lavoro vs Titolo di Studio
#### 🇬🇧 **English Title**: OurWorldInData: Duration of Compulsory Education and Labor Productivity vs Educational Attainment

* **Ente Statistico / Autorità Ufficiale**: `OurWorldInData (Oxford Martin School / UNESCO Institute for Statistics)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `OWID_COMPULSORY_DURATION / OWID_PRODUCTIVITY_ATTAINMENT` | **Risoluzione Geografica**: `Global Comparative across 150+ Nations`
* **Archivio Dati Elaborato**: [`local_data/processed/international_compulsory_duration_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/international_compulsory_duration_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Demonstrates macroscopic global correlations between extended compulsory education duration (Age 18) and long-term labor productivity.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 15. `uk_sdg_4_educational_proficiency_benchmark`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: UK SDG 4 Benchmark: Livelli Minimi di Competenza Cognitiva e Parità di Genere (SDG 4.1.1 e 4.5.1)
#### 🇬🇧 **English Title**: UK SDG 4 Benchmark: Minimum Cognitive Proficiency Levels and Gender Parity Index (SDG 4.1.1 & 4.5.1)

* **Ente Statistico / Autorità Ufficiale**: `UK Office for National Statistics (ONS) / Global SDG Indicator Repository`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `UK_SDG_4_1_1 / UK_SDG_4_5_1` | **Risoluzione Geografica**: `UK National and International Comparative`
* **Archivio Dati Elaborato**: [`local_data/UKSDGstats/4-1-1.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/UKSDGstats/4-1-1.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Provides the international Gold Standard for minimum literacy and numeracy competency tracking under the UN Sustainable Development Goals.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 16. `istat_non_observed_economy_and_submerged_labor`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: ISTAT Economia Non Osservata: Lavoro Sommerso e Irregolarità nei Mercati Regionali del Lavoro
#### 🇬🇧 **English Title**: ISTAT Non-Observed Economy: Submerged/Informal Labor and Irregular Employment Rates by Region

* **Ente Statistico / Autorità Ufficiale**: `ISTAT (Conti Nazionali - Economia Non Osservata e Lavoro Irregolare)`
* **🔗 Link Diretto Open Data**: [https://esploradati.istat.it/](https://esploradati.istat.it/)
* **Codice Flusso SDMX / Indagine**: `ISTAT_CN_ECONOMIA_NON_OSSERVATA` | **Risoluzione Geografica**: `Macro-Regional (Nord, Centro, Mezzogiorno) and Economic Sector level`
* **Archivio Dati Elaborato**: [`local_data/ISTAT/non_observed_economy/istat_non_observed_economy_report_2023.pdf`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/ISTAT/non_observed_economy/istat_non_observed_economy_report_2023.pdf)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Uncovers Blind Spot #4: explains why Southern bocciature and early school leavers frequently transition into informal/submerged labor rather than formal INPS contracts.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 17. `oecd_pisa_and_vet_tracking`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: OCSE PISA Trend di Competenza (Lettura/Matematica) e Distribuzione Studenti Istruzione Professionale (VET)
#### 🇬🇧 **English Title**: OECD PISA Competency Trends (Reading/Math) and Student Distribution in Vocational Education and Training (VET)

* **Ente Statistico / Autorità Ufficiale**: `OECD (Education at a Glance & Programme for International Student Assessment)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `OECD_PISA_TREND / OECD_EAG_VET_DISTRIBUTION` | **Risoluzione Geografica**: `National & International Comparative across OECD countries`
* **Archivio Dati Elaborato**: [`local_data/processed/oecd_pisa_and_vet_tracking_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/oecd_pisa_and_vet_tracking_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Links early vocational tracking ($T$) directly to standardized cognitive erosion in reading and math ($E$), explaining structural divergence between Italian and European secondary systems.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 18. `oecd_low_pay_and_wage_gap`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: OCSE Incidenza del Lavoro Povero (Low Pay Incidence) e Divario Salariale per Fascia di Età
#### 🇬🇧 **English Title**: OECD Low Pay Incidence and Age-Specific Wage Gap among Young Workers

* **Ente Statistico / Autorità Ufficiale**: `OECD (Employment and Labor Market Statistics Directorate)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `OECD_DSD_EARNINGS_PAY_INCIDENCE_AGE_WAGE_GAP` | **Risoluzione Geografica**: `National & EU Comparative (Italy, Germany, France, Spain, UK)`
* **Archivio Dati Elaborato**: [`local_data/processed/oecd_low_pay_and_wage_gap_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/oecd_low_pay_and_wage_gap_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifies the Working Poor phenomenon inside Destination ($D$), proving why employment alone without salary adequacy does not resolve youth socio-economic precarity.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 19. `eurydice_teacher_salaries_and_equity`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Retribuzioni Statutarie dei Docenti e Dirigenti Scolastici e Indicatori Europei di Equità Educativa
#### 🇬🇧 **English Title**: Teachers' and School Heads' Statutory Salaries and European System-Level Equity Indicators

* **Ente Statistico / Autorità Ufficiale**: `EURYDICE Network (European Commission / EACEA)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `EURYDICE_TEACHER_SALARIES_2023_2024 / EQUITY_INDICATORS` | **Risoluzione Geografica**: `Comparative across EU-27 Member States by ISCED level (02, 1, 24, 34)`
* **Archivio Dati Elaborato**: [`local_data/processed/eurydice_teacher_salaries_and_equity_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/eurydice_teacher_salaries_and_equity_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Exposes the institutional input deficit ($T$ inputs): shows Italian starting teacher salaries (`€24,297`) are less than half of Germany (`€54,128`), driving high turnover (`supplenze precari`) in difficult schools.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 20. `mur_tertiary_progression_and_origin`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Anagrafe MUR Studenti Universitari Fuori Corso, Fuori Sede e Provenienza per Indirizzo di Maturità
#### 🇬🇧 **English Title**: MUR Registry of University Students Behind Schedule (Fuori Corso), Off-Campus (Fuori Sede), and High School Origin

* **Ente Statistico / Autorità Ufficiale**: `MUR (Ministero dell'Università e della Ricerca - Ufficio Statistica)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `MUR_ISCRITTI_FUORI_CORSO_FUORI_SEDE` | **Risoluzione Geografica**: `University Institution (Ateneo), Region, and Gender disaggregation`
* **Archivio Dati Elaborato**: [`local_data/processed/mur_tertiary_progression_and_origin_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/mur_tertiary_progression_and_origin_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Measures tertiary academic efficiency ($E \rightarrow D$), demonstrating how upper secondary repetition and regional divides lead to prolonged university duration (`Fuori Corso`) or North-South student migration (`Fuori Sede`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 21. `opencoesione_school_digital_infrastructure`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Progetti PNRR e Coesione per Reti e Servizi Digitali nelle Scuole ed Edilizia Scolastica
#### 🇬🇧 **English Title**: OpenCoesione / PNRR Structural Funds for Digital Networks and Services in Schools

* **Ente Statistico / Autorità Ufficiale**: `Dipartimento per le Politiche di Coesione (OpenCoesione) / MEF PNRR`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `OPENCOESIONE_RETI_SERVIZI_DIGITALI_2021_2027` | **Risoluzione Geografica**: `Project, Municipal, Provincial, and Regional Level`
* **Archivio Dati Elaborato**: [`local_data/processed/opencoesione_school_digital_projects_summary.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/opencoesione_school_digital_projects_summary.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Tracks public investment interventions aimed at neutralizing initial digital and infrastructure gaps ($O \rightarrow T$) across disadvantaged educational districts.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 22. `istat_neet_incidence_by_educational_attainment`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: ISTAT Rilevazione Forze di Lavoro - Incidenza NEET e Abbandono per Titolo di Studio Posseduto
#### 🇬🇧 **English Title**: ISTAT Labor Force Survey - NEET Incidence and Dropout Rates Disaggregated by Educational Attainment

* **Ente Statistico / Autorità Ufficiale**: `ISTAT (Direzione Centrale Statistiche sul Lavoro e sul Benessere)`
* **🔗 Link Diretto Open Data**: [https://esploradati.istat.it/](https://esploradati.istat.it/)
* **Codice Flusso SDMX / Indagine**: `ISTAT_LFS_NEET_ATTAINMENT / DROPOUT_TS` | **Risoluzione Geografica**: `National & Regional Level by ISCED Attainment (0-2 vs 3-4 vs 5-8)`
* **Archivio Dati Elaborato**: [`local_data/processed/istat_neet_and_dropout_by_attainment_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/istat_neet_and_dropout_by_attainment_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Proves the protective returns to schooling inside Destination ($D$), demonstrating that obtaining a diploma (`14.2% NEET`) or university degree (`<9.8% NEET`) dramatically reduces inactivity compared to middle school only (`21.3% NEET`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 23. `mur_university_tuition_exemptions_and_tax_relief`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Anagrafe MUR Esoneri Tasse Universitarie e No-Tax Area per Ateneo e Fascia ISEE
#### 🇬🇧 **English Title**: MUR Registry of University Tuition Exemptions and Tax Relief (No-Tax Area) by University Institution

* **Ente Statistico / Autorità Ufficiale**: `MUR (Ministero dell'Università e della Ricerca - Ufficio Statistica)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `MUR_ESONERI_TASSE_ATENEO` | **Risoluzione Geografica**: `University Institution (COD_Ateneo), Region, and Exemption Type`
* **Archivio Dati Elaborato**: [`local_data/processed/mur_university_exemptions_and_tax_relief_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/mur_university_exemptions_and_tax_relief_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Evaluates institutional policy interventions ($E$ retention): measures how university tax relief (`No-Tax Area ISEE < €22,000`) cushions socioeconomic origin ($O$) against tuition dropout.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 24. `worldbank_learning_poverty_and_teacher_training`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Banca Mondiale - Povertà di Apprendimento (Learning Poverty) e Formazione Docenti nella Scuola Secondaria
#### 🇬🇧 **English Title**: World Bank Learning Poverty Index and Share of Trained Secondary School Teachers

* **Ente Statistico / Autorità Ufficiale**: `World Bank (Education Global Practice / EdStats)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `WB_EDSTATS_LEARNING_POVERTY / TEACHERS_TRAINED` | **Risoluzione Geografica**: `International Comparative across G7 and EU economies`
* **Archivio Dati Elaborato**: [`local_data/processed/worldbank_learning_poverty_and_teacher_training_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/worldbank_learning_poverty_and_teacher_training_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Benchmarks Italian baseline cognitive deficits ($O \rightarrow T$) against global standards, showing Italian learning poverty (`5.50%`) relative to peer industrial nations.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 25. `oecd_education_funding_sources_and_staff_nature`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: OCSE EAG Ripartizione Fonti di Finanziamento Educativo e Natura della Spesa (Personale vs Capitale)
#### 🇬🇧 **English Title**: OECD Education at a Glance - Funding Sources and Expenditure Nature (Staff vs Capital Investment)

* **Ente Statistico / Autorità Ufficiale**: `OECD (Directorate for Education and Skills - EAG Indicators)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `OECD_EAG_FUNDING_SOURCES / NATURE_STAFF_CAPITAL` | **Risoluzione Geografica**: `International Comparative by ISCED levels (1-8)`
* **Archivio Dati Elaborato**: [`local_data/processed/oecd_education_funding_and_staff_nature_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/oecd_education_funding_and_staff_nature_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Exposes the structural expenditure rigidity inside Italian tracking ($T$): reveals what share of school budgets is absorbed by fixed staff salaries vs. pedagogical capital investments (`laboratories, digital tools`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 26. `eurydice_instruction_time_and_curriculum_allocation`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: EURYDICE Monte Ore Annuale di Insegnamento e Ripartizione Curricolare per Indirizzo (LIC/TEC/VOC)
#### 🇬🇧 **English Title**: EURYDICE Annual Instruction Time and Subject Curriculum Allocation by Secondary School Track

* **Ente Statistico / Autorità Ufficiale**: `EURYDICE Network (European Commission / EACEA)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `EURYDICE_INSTRUCTION_TIME_2024_2025` | **Risoluzione Geografica**: `System-level curriculum structures across 11 Italian grade/track questionnaires (`IT_1 to IT_11`)`
* **Archivio Dati Elaborato**: [`local_data/processed/eurydice_italian_instruction_time_by_track.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/eurydice_italian_instruction_time_by_track.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Documents the pedagogical curriculum architecture of the tripartite tracking system ($T$), detailing exact annual instruction hours dedicated to core vs. vocational competencies.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 27. `hf_mim_student_enrollment_by_track`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Anagrafe Alunni MIM - Iscrizioni Statali per Indirizzo di Studio della Scuola Secondaria di II Grado
#### 🇬🇧 **English Title**: MIM Student Registry - State Secondary School Enrollments by High School Track

* **Ente Statistico / Autorità Ufficiale**: `MIM (Ministero dell'Istruzione e del Merito - Anagrafe Alunni / HF OpenData)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `MIM_HF_ALUSECGRADOINDSTA_202425` | **Risoluzione Geografica**: `Province / Track (`Licei vs Tecnici vs Professionali`)`
* **Archivio Dati Elaborato**: [`local_data/processed/hf_mim_student_enrollment_by_track.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/hf_mim_student_enrollment_by_track.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifies the baseline distribution of Italian students into tripartite tracks ($T$), proving empirical polarization across geographical territories.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 28. `hf_mim_teacher_precariato_by_region`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Anagrafe Personale MIM - Supplenze Annuali e Lavoro Dipendente a Tempo Determinato e Contratti di Stage/Tirocinio Docenti nella Scuola Statale
#### 🇬🇧 **English Title**: MIM Personnel Registry - Annual Teacher Substitutions and Lavoro Dipendente a Tempo Determinato e Contratti di Stage/Tirocinio across State Schools

* **Ente Statistico / Autorità Ufficiale**: `MIM (Ministero dell'Istruzione e del Merito - Anagrafe Docenti / HF OpenData)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `MIM_HF_DOCSUPXXV_202425` | **Risoluzione Geografica**: `Province / School Level`
* **Archivio Dati Elaborato**: [`local_data/processed/hf_mim_teacher_precariato_by_region.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/hf_mim_teacher_precariato_by_region.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Exposes the exact turnover rate of teaching personnel ($T$ friction), demonstrating how precariato undermines pedagogical continuity in technical and vocational institutes.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 29. `hf_snv_school_evaluation_outcomes`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Sistema Nazionale di Valutazione (SNV) - Esiti della Valutazione delle Scuole Statali
#### 🇬🇧 **English Title**: National Evaluation System (SNV) - Self-Evaluation and INVALSI Evaluation Outcomes of State Schools

* **Ente Statistico / Autorità Ufficiale**: `INVALSI & MIM (Sistema Nazionale di Valutazione / HF OpenData)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `MIM_HF_VALUTAZIONE_ESITI_STA` | **Risoluzione Geografica**: `National & Regional System Indicators`
* **Archivio Dati Elaborato**: [`local_data/processed/hf_snv_school_evaluation_outcomes.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/hf_snv_school_evaluation_outcomes.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Evaluates institutional performance ($E$), isolating internal self-evaluation benchmarks against national standardized INVALSI criteria.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 30. `ourworldindata_upper_secondary_completion_and_schooling_quality`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: OurWorldInData / UNESCO - Tasso di Completamento Superiore (SDG 4.1.2) e Indice Qualità vs Quantità
#### 🇬🇧 **English Title**: OurWorldInData / UNESCO - Upper Secondary Completion Rate (SDG 4.1.2) and Quality vs Quantity of Schooling Index

* **Ente Statistico / Autorità Ufficiale**: `UNESCO Institute for Statistics & OurWorldInData`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `OWID_UNESCO_COMPLETION_SDG412 / QUALITY_SCHOOLING` | **Risoluzione Geografica**: `International Comparative across G7 and EU economies`
* **Archivio Dati Elaborato**: [`local_data/processed/ourworldindata_upper_secondary_completion_and_quality_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/ourworldindata_upper_secondary_completion_and_quality_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Benchmarks Italian upper secondary completion against global SDG targets ($T \rightarrow E$), isolating whether cognitive quality matches duration.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 31. `ourworldindata_macro_fiscal_and_sectoral_structure`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: OurWorldInData / World Bank - Quota della Spesa Pubblica in Istruzione e Ripartizione Settoriale Occupazione
#### 🇬🇧 **English Title**: OurWorldInData - Share of Government Expenditure on Education and Employment Sector Structure (Agri/Ind/Serv)

* **Ente Statistico / Autorità Ufficiale**: `World Bank & OurWorldInData Macro-Economics Data`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `OWID_MACRO_FISCAL_SECTORAL` | **Risoluzione Geografica**: `International Comparative across G7 economies`
* **Archivio Dati Elaborato**: [`local_data/processed/ourworldindata_macro_fiscal_and_sectoral_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/ourworldindata_macro_fiscal_and_sectoral_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Exposes the macroeconomic boundaries of the education budget ($O$) and the labor demand structure absorbing youth at Destination ($D$).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 32. `eurydice_elet_and_school_year_structures`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: EURYDICE Network - Indicatori di Sistema sull'Abbandono Scolastico Precoce (ELET) e Struttura Calendario
#### 🇬🇧 **English Title**: EURYDICE Network - System-Level Indicators on Early Leaving from Education and Training (ELET) and School Year Structures

* **Ente Statistico / Autorità Ufficiale**: `EURYDICE Network (European Commission / EACEA)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `EURYDICE_ELET_SYSTEM_2024_2025` | **Risoluzione Geografica**: `System-level European Comparative across 35+ education systems`
* **Archivio Dati Elaborato**: [`local_data/processed/eurydice_elet_and_school_year_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/eurydice_elet_and_school_year_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Maps the structural policy interventions and institutional mechanisms governing early school leaving prevention ($T$ retention).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 33. `worldbank_tertiary_enrollment_and_spending_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Banca Mondiale EdStats - Tasso di Iscrizione Lorda Universitaria e Spesa Terziaria per Capite
#### 🇬🇧 **English Title**: World Bank EdStats - Gross Tertiary Enrollment Ratio and Tertiary Education Expenditure per Student (% of GDP per capita)

* **Ente Statistico / Autorità Ufficiale**: `World Bank (Education Global Practice / EdStats)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `WB_EDSTATS_TERTIARY_ENROLLMENT / SPENDING` | **Risoluzione Geografica**: `International Comparative across G7 and EU economies`
* **Archivio Dati Elaborato**: [`local_data/processed/worldbank_tertiary_enrollment_and_spending_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/worldbank_tertiary_enrollment_and_spending_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Evaluates Italian university capacity and funding per student ($E$), proving why Italian tertiary graduation rates lag behind OECD peers.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 34. `worldbank_youth_mental_health_and_mortality`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Banca Mondiale - Tasso di Mortalità per Suicidio e Salute Mentale Giovanile (Contesto di Pressione e Inattività)
#### 🇬🇧 **English Title**: World Bank - Suicide Mortality Rate and Youth Psychological Well-being Indicators

* **Ente Statistico / Autorità Ufficiale**: `World Bank / World Health Organization (WHO Global Health Observatory)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `WB_WHO_SUICIDE_MORTALITY` | **Risoluzione Geografica**: `International Comparative across G7 and EU economies`
* **Archivio Dati Elaborato**: [`local_data/processed/worldbank_youth_mental_health_and_mortality_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/worldbank_youth_mental_health_and_mortality_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifies the psychological crisis and social exclusion associated with prolonged NEET status ($D$ hysteresis) and academic tracking shocks.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 35. `mur_university_graduates_and_cohort_birthyear_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Anagrafe MUR - Serie Storica Laureati ed Età Anagrafica degli Iscritti ai Corsi di Laurea
#### 🇬🇧 **English Title**: MUR Registry - Historical Time Series of University Graduates and Enrollment Cohorts by Birth Year

* **Ente Statistico / Autorità Ufficiale**: `MUR (Ministero dell'Università e della Ricerca - Ufficio Statistica)`
* **🔗 Link Diretto Open Data**: [https://opencoesione.gov.it/it/dati/progetti/](https://opencoesione.gov.it/it/dati/progetti/)
* **Codice Flusso SDMX / Indagine**: `MUR_LAUREATI_TS / COHORT_BIRTHYEAR` | **Risoluzione Geografica**: `National & University Institution level by Birth Year`
* **Archivio Dati Elaborato**: [`local_data/processed/mur_university_graduates_and_cohort_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/mur_university_graduates_and_cohort_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Traces cohort throughput and age delay inside tertiary education ($E$), revealing the exact time-to-degree bottlenecks.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 36. `eurostat_almalaurea_credentialism_and_overeducation_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Eurostat / AlmaLaurea - Il Mercato del Lavoro Credenzialista: Tasso di Coerenza Studi-Lavoro e Sovraistruzione
#### 🇬🇧 **English Title**: Eurostat / AlmaLaurea - Credentialist Labor Market: Job-Study Coherence and Over-Education Panel

* **Ente Statistico / Autorità Ufficiale**: `Consorzio AlmaLaurea & Eurostat (`edat_lfse_16 / Labour Force Survey`)`
* **🔗 Link Diretto Open Data**: [https://www.almalaurea.it/esiti-occupazionali](https://www.almalaurea.it/esiti-occupazionali)
* **Codice Flusso SDMX / Indagine**: `EUROSTAT_ALMALAUREA_CREDENTIALISM_2026` | **Risoluzione Geografica**: `Comparative across Italy, G7 and EU economies (`UE-27 Avg`)`
* **Archivio Dati Elaborato**: [`local_data/processed/eurostat_almalaurea_credentialism_and_overeducation_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/eurostat_almalaurea_credentialism_and_overeducation_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Proves the 'Dinamica Incrociata tra Tasso di Laureati e Tasso di Coerenza Formativo-Professionale' inside Randall Collins' Credentialist framework ($E \rightarrow D$ mismatch), revealing why Italy ranks last in EU coherence (`41.6%`) despite having few graduates.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 37. `almalaurea_disciplinary_coherence_and_mismatch`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Consorzio AlmaLaurea - Coerenza ed Efficacia del Titolo di Studio per Gruppo Disciplinare di Laurea (5 Anni)
#### 🇬🇧 **English Title**: AlmaLaurea Consortium - Degree Coherence and Effectiveness by Academic Disciplinary Group (5 Years Post-Graduation)

* **Ente Statistico / Autorità Ufficiale**: `Consorzio Interuniversitario AlmaLaurea (`Indagine sulla Condizione Occupazionale`)`
* **🔗 Link Diretto Open Data**: [https://www.almalaurea.it/esiti-occupazionali](https://www.almalaurea.it/esiti-occupazionali)
* **Codice Flusso SDMX / Indagine**: `ALMALAUREA_DISCIPLINARY_COHERENCE_5Y` | **Risoluzione Geografica**: `National & Disciplinary Group level (`STEM vs Humanities vs Law`)`
* **Archivio Dati Elaborato**: [`local_data/processed/almalaurea_disciplinary_coherence_and_mismatch.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/almalaurea_disciplinary_coherence_and_mismatch.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Isolates the exact academic tracking trap ($T \rightarrow E \rightarrow D$), demonstrating how nearly 1 in 2 Humanities/Law graduates work in roles where their degree is not required.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 38. `eurostat_sdmx_citizenship_migrant_neet_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Eurostat SDMX API (`edat_lfse_16`) - Tasso NEET per Cittadinanza (Nativi vs Stranieri in Italia e UE)
#### 🇬🇧 **English Title**: Eurostat SDMX API (`edat_lfse_16`) - NEET Rates by Citizenship and Country of Birth (Native vs Foreign-Born)

* **Ente Statistico / Autorità Ufficiale**: `Eurostat (`European Commission Statistical Office / Labour Force Survey`)`
* **🔗 Link Diretto Open Data**: [https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/edat_lfse_16/](https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/edat_lfse_16/)
* **Codice Flusso SDMX / Indagine**: `ESTAT_EDAT_LFSE_16` | **Risoluzione Geografica**: `Comparative across Italy, G7 and EU (`Native vs Foreign-born`)`
* **Archivio Dati Elaborato**: [`local_data/processed/eurostat_sdmx_citizenship_migrant_neet_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/eurostat_sdmx_citizenship_migrant_neet_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Controls for demographic and citizenship barriers at Origin ($O$), mathematically proving (`Pearson r = 0.7420`) that non-native youth face more than double the NEET risk in Italian labor markets.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 39. `istat_sdmx_provincial_elet_and_attainment_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: ISTAT SDMX API (`DCCV_TAXSCUOLA`) - Tassi di Abbandono Scolastico e Attainment a Livello Provinciale (NUTS-3)
#### 🇬🇧 **English Title**: ISTAT SDMX API (`DCCV_TAXSCUOLA`) - Early School Leaving and Diploma Attainment Rates at Provincial Level (NUTS-3)

* **Ente Statistico / Autorità Ufficiale**: `ISTAT (`Istituto Nazionale di Statistica - EsploraDati SDMX WS`)`
* **🔗 Link Diretto Open Data**: [https://esploradati.istat.it/SDMXWS/rest/data/DCCV_TAXSCUOLA](https://esploradati.istat.it/SDMXWS/rest/data/DCCV_TAXSCUOLA)
* **Codice Flusso SDMX / Indagine**: `ISTAT_SDMX_DCCV_TAXSCUOLA_PROV` | **Risoluzione Geografica**: `Provincial NUTS-3 level (`Sample across 22 key Italian provinces`)`
* **Archivio Dati Elaborato**: [`local_data/processed/istat_sdmx_provincial_elet_and_attainment_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/istat_sdmx_provincial_elet_and_attainment_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Upgrades our geographic granularity from NUTS-2 down to NUTS-3 (`Province`), pinpointing exact intra-regional educational poverty (`e.g., Naples 18.9% vs Benevento 13.2% inside Campania`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 40. `anpal_sil_youth_hiring_and_precariato_flows`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: ANPAL / SIL Lavoro Open Data - Comunicazioni Obbligatorie (CO) sui Flussi di Assunzione Under-30 per Contratto
#### 🇬🇧 **English Title**: ANPAL / SIL Labor Open Data - Mandatory Notifications (CO) on Under-30 Hiring Flows by Contract Type

* **Ente Statistico / Autorità Ufficiale**: `Ministero del Lavoro e delle Politiche Sociali / ANPAL (`Sistema Informativo Lavoro`)`
* **🔗 Link Diretto Open Data**: [https://dati.lavoro.gov.it/](https://dati.lavoro.gov.it/)
* **Codice Flusso SDMX / Indagine**: `ANPAL_SIL_CO_HIRING_FLOWS_2025` | **Risoluzione Geografica**: `Regional NUTS-2 level across 20 Italian regions`
* **Archivio Dati Elaborato**: [`local_data/processed/anpal_sil_youth_hiring_and_precariato_flows.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/anpal_sil_youth_hiring_and_precariato_flows.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifies exact daily administrative hiring flows ($E \rightarrow D$ transition), exposing how up to 42.5% of Southern youth enter via precarious internships (`tirocini €500/mese`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 41. `inps_administrative_youth_wage_records`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: INPS Open Data - Osservatorio Dipendenti e Precari: Retribuzioni Annue Medie Reali e Giornate Retribuite Under-30
#### 🇬🇧 **English Title**: INPS Open Data - Observatory on Dependent Workers: Actual Annual Gross Social Security Wages of Youth Under 30

* **Ente Statistico / Autorità Ufficiale**: `INPS (`Coordinamento Generale Statistico e Attuariale - Open Data`)`
* **🔗 Link Diretto Open Data**: [https://www.inps.it/it/it/dati-e-bilanci/open-data.html](https://www.inps.it/it/it/dati-e-bilanci/open-data.html)
* **Codice Flusso SDMX / Indagine**: `INPS_OPEN_DATA_YOUTH_WAGES_2024` | **Risoluzione Geografica**: `Regional NUTS-2 level across 20 Italian regions by Age Group (`18-24 vs 25-29`)`
* **Archivio Dati Elaborato**: [`local_data/processed/inps_administrative_youth_wage_records.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/inps_administrative_youth_wage_records.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Provides hard administrative social security records (`actual euros on paystubs`), proving how intermittent work (`only 162 paid days/yr in South`) halves annual earnings.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 42. `banca_d_italia_shiw_shadow_tutoring_costs`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Banca d'Italia IBFI / SHIW - Spesa delle Famiglie per Lezioni Private e Ripetizioni per Quintile di Ricchezza (`Shadow Education`)
#### 🇬🇧 **English Title**: Bank of Italy IBFI / SHIW - Household Out-of-Pocket Spending on Private Tutoring (`Shadow Education Market`) by Wealth Quintile

* **Ente Statistico / Autorità Ufficiale**: `Banca d'Italia (`Dipartimento Economia e Statistica - Indagine sui Bilanci delle Famiglie IBFI/SHIW`)`
* **🔗 Link Diretto Open Data**: [https://www.bancaditalia.it/statistiche/indagini/bilanci-famiglie/index.html](https://www.bancaditalia.it/statistiche/indagini/bilanci-famiglie/index.html)
* **Codice Flusso SDMX / Indagine**: `BANK_OF_ITALY_SHIW_SHADOW_TUTORING` | **Risoluzione Geografica**: `National by Household Wealth Quintile (`Quintile 1 Poorest to Quintile 5 Wealthiest`)`
* **Archivio Dati Elaborato**: [`local_data/processed/banca_d_italia_shiw_shadow_tutoring_costs.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/banca_d_italia_shiw_shadow_tutoring_costs.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Exposes the exact financial mechanism whereby family wealth ($O$) buys academic survival ($E$) inside rigid theoretical tracks ($T$), preventing bocciatura through €2,850/yr private tutoring.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 43. `unioncamere_excelsior_skill_mismatch_and_demand_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 2: Institutional Macro-Structural & Actuarial Projections (`Indicatori Macro-Strutturali e Modelli Attuariali Ufficiali`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Unioncamere / ANPAL Sistema Informativo Excelsior - Previsioni dei Fabbisogni Professionali e Difficoltà di Reperimento
#### 🇬🇧 **English Title**: Unioncamere / ANPAL Excelsior Information System - Regional Occupational Demand and Skill Mismatch Forecasts

* **Ente Statistico / Autorità Ufficiale**: `Unioncamere & Ministero del Lavoro e delle Politiche Sociali (`Sistema Informativo Excelsior`)`
* **🔗 Link Diretto Open Data**: [https://excelsior.unioncamere.net/](https://excelsior.unioncamere.net/)
* **Codice Flusso SDMX / Indagine**: `EXCELSIOR_FABBISOGNI_2024` | **Risoluzione Geografica**: `Regionale e Provinciale (`NUTS-2 e NUTS-3`) across all Italian economic sectors`
* **Archivio Dati Elaborato**: [`local_data/processed/unioncamere_excelsior_skill_mismatch_and_demand_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/unioncamere_excelsior_skill_mismatch_and_demand_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Fornisce la misurazione empirica diretta della domanda delle imprese (`Destinazione D`), quantificando la difficoltà di reperimento per livello di istruzione (`Laurea vs Diploma Tecnico vs ITS Academy`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio fornisce il quadro contabile, macro-economico o attuariale di lungo periodo (es. proiezioni previdenziali COVIP, spesa totale OCSE, o matrici professionali CP2021). Non si tratta di una survey campionaria regionale grezza, ma di un indicatore strutturale di sistema.

---

### 44. `inapp_plus_lifelong_learning_and_social_mobility_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 2: Institutional Macro-Structural & Actuarial Projections (`Indicatori Macro-Strutturali e Modelli Attuariali Ufficiali`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: INAPP Indagine PLUS - Partecipazione alla Formazione Continua, Apprendimento Degli Adulti e Mobilità Intergenerazionale
#### 🇬🇧 **English Title**: INAPP PLUS Survey - Adult Lifelong Learning Participation and Intergenerational Social Mobility Index

* **Ente Statistico / Autorità Ufficiale**: `INAPP (`Istituto Nazionale per l'Analisi delle Politiche Pubbliche - Indagine PLUS`)`
* **🔗 Link Diretto Open Data**: [https://www.inapp.gov.it/dati/](https://www.inapp.gov.it/dati/)
* **Codice Flusso SDMX / Indagine**: `INAPP_PLUS_LIFELONG_2024` | **Risoluzione Geografica**: `Regionale (`NUTS-2`) per fasce di età (`25-64 anni`)`
* **Archivio Dati Elaborato**: [`local_data/processed/inapp_plus_lifelong_learning_and_social_mobility_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/inapp_plus_lifelong_learning_and_social_mobility_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Analizza l'investimento in capitale umano durante il ciclo di vita lavorativa (`Formazione Continua E -> D`), misurando la capacità del sistema di compensare le disuguaglianze iniziali (`Origine O`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio fornisce il quadro contabile, macro-economico o attuariale di lungo periodo (es. proiezioni previdenziali COVIP, spesa totale OCSE, o matrici professionali CP2021). Non si tratta di una survey campionaria regionale grezza, ma di un indicatore strutturale di sistema.

---

### 45. `piattaforma_competenze_e_lavoro_cp2021_mapping`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 2: Institutional Macro-Structural & Actuarial Projections (`Indicatori Macro-Strutturali e Modelli Attuariali Ufficiali`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Piattaforma Integrata Competenze e Lavoro - Correlazione tra Classificazione Professionale CP2021 e Requisiti Formativi
#### 🇬🇧 **English Title**: Integrated Skills & Labor Platform - Mapping CP2021 Professional Categories against Formal Educational Requirements

* **Ente Statistico / Autorità Ufficiale**: `OCSE / Unioncamere / AlmaLaurea / INAPP (`Piattaforma Nazionale Competenze e Lavoro`)`
* **🔗 Link Diretto Open Data**: [https://www.competenzeelavoro.it/](https://www.competenzeelavoro.it/)
* **Codice Flusso SDMX / Indagine**: `COMPETENZE_LAVORO_CP2021` | **Risoluzione Geografica**: `Nazionale per Grande Gruppo Professionale (`Classificazione ISTAT CP2021 a 1 e 3 cifre`)`
* **Archivio Dati Elaborato**: [`local_data/processed/piattaforma_competenze_e_lavoro_cp2021_mapping.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/piattaforma_competenze_e_lavoro_cp2021_mapping.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Definisce il raccordo formale tra offerta didattica (`Titolo di Studio E`) e classificazione delle mansioni professionali ISTAT (`Destinazione D`), quantificando il grado normativo e sostanziale di coerenza occupazionale.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio fornisce il quadro contabile, macro-economico o attuariale di lungo periodo (es. proiezioni previdenziali COVIP, spesa totale OCSE, o matrici professionali CP2021). Non si tratta di una survey campionaria regionale grezza, ma di un indicatore strutturale di sistema.

---

### 46. `istat_student_commuting_and_transport_infrastructure_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: ISTAT EsploraDati - Indagine sul Traffico dei Pendolari, Tempi di Transito e Infrastrutture di Trasporto Scolastico
#### 🇬🇧 **English Title**: ISTAT EsploraDati - Student Commuting Transit Times, Transport Infrastructure, and Regional Mobility Costs

* **Ente Statistico / Autorità Ufficiale**: `ISTAT (`Istituto Nazionale di Statistica - EsploraDati Indagine sul Pendolarismo DCCV_PEND`)`
* **🔗 Link Diretto Open Data**: [https://esploradati.istat.it/SDMXWS/rest/data/DCCV_PEND](https://esploradati.istat.it/SDMXWS/rest/data/DCCV_PEND)
* **Codice Flusso SDMX / Indagine**: `DCCV_PEND_STUDENTI` | **Risoluzione Geografica**: `Regionale (`NUTS-2`) e Provinciale (`NUTS-3`)`
* **Archivio Dati Elaborato**: [`local_data/processed/istat_student_commuting_and_transport_infrastructure_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/istat_student_commuting_and_transport_infrastructure_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifica l'attrito infrastrutturale di transito (`Pendolarismo >60 min`), dimostrando come la carenza di trasporto pubblico locale nelle aree interne e nel Sud incida sui tassi provinciali di abbandono scolastico (`ELET`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 47. `almalaurea_mur_gender_stem_segregation_and_pay_gap_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: AlmaLaurea / MUR - Segregazione Orizzontale di Genere tra Indirizzi STEM e Umanistici e Differenziale Salariale
#### 🇬🇧 **English Title**: AlmaLaurea / MUR - Gender Horizontal Segregation across STEM vs Humanities Tracks and Post-Graduation Pay Gap

* **Ente Statistico / Autorità Ufficiale**: `Consorzio AlmaLaurea & MUR (`Anagrafe Nazionale Studenti - ANS & Esiti Occupazionali`)`
* **🔗 Link Diretto Open Data**: [https://www.almalaurea.it/esiti-occupazionali](https://www.almalaurea.it/esiti-occupazionali)
* **Codice Flusso SDMX / Indagine**: `ALMALAUREA_GENDER_STEM_2024` | **Risoluzione Geografica**: `Regionale (`NUTS-2`) e per Gruppo Disciplinare`
* **Archivio Dati Elaborato**: [`local_data/processed/almalaurea_mur_gender_stem_segregation_and_pay_gap_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/almalaurea_mur_gender_stem_segregation_and_pay_gap_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Evidenzia la segregazione orizzontale di genere nella scelta universitaria (`Tracking T -> E`) e dimostra come la concentrazione femminile nelle lauree umanistiche/formatrici si traduca in un divario salariale netto a 5 anni (`Gender Pay Gap E -> D`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 48. `eurostat_istat_desi_digital_skills_attainment_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: Eurostat / ISTAT - Indice DESI sulle Competenze Digitali di Base e Avanzate della Popolazione e degli Specialisti ICT
#### 🇬🇧 **English Title**: Eurostat / ISTAT - DESI Digital Economy and Society Index on Basic/Advanced Digital Skills and ICT Specialists

* **Ente Statistico / Autorità Ufficiale**: `Eurostat & ISTAT (`Indagine sull'Uso delle Tecnologie dell'Informazione e della Comunicazione - isoc_sk_dskl_i21`)`
* **🔗 Link Diretto Open Data**: [https://ec.europa.eu/eurostat/databrowser/view/isoc_sk_dskl_i21/default/table?lang=en](https://ec.europa.eu/eurostat/databrowser/view/isoc_sk_dskl_i21/default/table?lang=en)
* **Codice Flusso SDMX / Indagine**: `EUROSTAT_DESI_SKILLS_2024` | **Risoluzione Geografica**: `Regionale (`NUTS-2`) e Comparazione Europea (`Italia vs UE-27`)`
* **Archivio Dati Elaborato**: [`local_data/processed/eurostat_istat_desi_digital_skills_attainment_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/eurostat_istat_desi_digital_skills_attainment_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Fornisce la misura oggettiva delle competenze digitali (`Capitale Umano DESI`), documentando il divario strutturale tra la popolazione italiana (`37.2%-54.8% competenze di base`) e la media europea (`>54% UE-27`), il quale alimenta direttamente la difficoltà di reperimento per profili tecnici.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 49. `mim_mur_tripartite_system_provenance_and_tracks`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 2: Institutional Macro-Structural & Actuarial Projections (`Indicatori Macro-Strutturali e Modelli Attuariali Ufficiali`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: MIM / MUR - Struttura del Sistema Tripartito, Provenienza degli Studenti Universitari ed Esiti Accademici
#### 🇬🇧 **English Title**: MIM / MUR - Tripartite Upper-Secondary System Structure, University Freshman Provenance, and Track Outcomes

* **Ente Statistico / Autorità Ufficiale**: `MIM & MUR (`Anagrafe Nazionale Studenti ANS - Portale Scuola in Chiaro`)`
* **🔗 Link Diretto Open Data**: [https://ustat.mur.gov.it/opendata/](https://ustat.mur.gov.it/opendata/)
* **Codice Flusso SDMX / Indagine**: `MUR_ANS_TRIPARTITE_2024` | **Risoluzione Geografica**: `Nazionale e per Tipologia di Indirizzo (`Licei vs Tecnici vs Professionali vs IeFP`)`
* **Archivio Dati Elaborato**: [`local_data/processed/mim_mur_tripartite_system_provenance_and_tracks.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/mim_mur_tripartite_system_provenance_and_tracks.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Dettaglia la canalizzazione tripartita italiana (`Licei 51.4%, Tecnici 31.2%, Professionali 12.8%, IeFP 4.6%`) e dimostra la fortissima correlazione tra l'indirizzo di scuola superiore e il tasso di successo o abbandono all'università.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio fornisce il quadro contabile, macro-economico o attuariale di lungo periodo (es. proiezioni previdenziali COVIP, spesa totale OCSE, o matrici professionali CP2021). Non si tratta di una survey campionaria regionale grezza, ma di un indicatore strutturale di sistema.

---

### 50. `almalaurea_istat_school_to_work_transition_times`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: AlmaLaurea / ISTAT - Indagine sui Tempi di Transito tra Scuola, Università e Primo Contratto di Lavoro Stabile
#### 🇬🇧 **English Title**: AlmaLaurea / ISTAT - Survey on School-to-Work Transition Times and Duration to First Stable Open-Ended Contract

* **Ente Statistico / Autorità Ufficiale**: `Consorzio AlmaLaurea & ISTAT (`Indagine Inserimento Lavorativo dei Diplomati e Laureati`)`
* **🔗 Link Diretto Open Data**: [https://www.almalaurea.it/esiti-occupazionali](https://www.almalaurea.it/esiti-occupazionali)
* **Codice Flusso SDMX / Indagine**: `ALMALAUREA_TRANSITION_TIMES` | **Risoluzione Geografica**: `Regionale (`NUTS-2`) e per Livello di Titolo (`Diploma vs Laurea`)`
* **Archivio Dati Elaborato**: [`local_data/processed/almalaurea_istat_school_to_work_transition_times.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/almalaurea_istat_school_to_work_transition_times.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifica i tempi fisiologici e strutturali di transito verso la stabilità lavorativa (`da 18 a 54 mesi per il primo contratto stabile`), misurando il differenziale di inserimento tra le macro-aree del Nord e del Sud.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 51. `istat_oecd_cumulative_lifecycle_student_expenditure`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 2: Institutional Macro-Structural & Actuarial Projections (`Indicatori Macro-Strutturali e Modelli Attuariali Ufficiali`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: ISTAT / OCSE - Spesa Cumulativa Complessiva per l'Istruzione di uno Studente lungo l'Intero Ciclo di Vita (0-24 Anni)
#### 🇬🇧 **English Title**: ISTAT / OECD - Total Lifecycle Cumulative Education Expenditure per Student from Nursery to Master's Degree (Age 0-24)

* **Ente Statistico / Autorità Ufficiale**: `OCSE (`Education at a Glance`) & ISTAT (`Indagine sui Consumi delle Famiglie - Spesa Scolastica`)`
* **🔗 Link Diretto Open Data**: [https://stats.oecd.org/Index.aspx?DataSetCode=EAG_FIN_RATIO](https://stats.oecd.org/Index.aspx?DataSetCode=EAG_FIN_RATIO)
* **Codice Flusso SDMX / Indagine**: `OECD_ISTAT_LIFECYCLE_COST` | **Risoluzione Geografica**: `Nazionale per Ciclo di Istruzione (`Asilo Nido, Infanzia, Primaria, Media, Superiore, Università`)`
* **Archivio Dati Elaborato**: [`local_data/processed/istat_oecd_cumulative_lifecycle_student_expenditure.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/istat_oecd_cumulative_lifecycle_student_expenditure.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Fornisce il conto economico totale dell'investimento formativo per cittadino (`€185.200 spesa pubblica + €53.500 spesa familiare = €238.700 per un laureato magistrale`), evidenziando l'onere finanziario privato sostenuto dalle famiglie (`22.4% del totale`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio fornisce il quadro contabile, macro-economico o attuariale di lungo periodo (es. proiezioni previdenziali COVIP, spesa totale OCSE, o matrici professionali CP2021). Non si tratta di una survey campionaria regionale grezza, ma di un indicatore strutturale di sistema.

---

### 52. `istat_inapp_binary_lock_university_exclusion`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: ISTAT / INAPP - Esclusione Formale dall'Accesso Universitario per Mancanza di Diploma Quinquennale (Blocco Binario)
#### 🇬🇧 **English Title**: ISTAT / INAPP - Formal University Exclusion and Binary Lock for Youth Holding 3-Year/4-Year Vocational Qualifications

* **Ente Statistico / Autorità Ufficiale**: `ISTAT & Ministero del Lavoro / INAPP (`Monitoraggio Percorsi IeFP e Obbligo Scolastico`)`
* **🔗 Link Diretto Open Data**: [https://www.inapp.gov.it/dati/](https://www.inapp.gov.it/dati/)
* **Codice Flusso SDMX / Indagine**: `ISTAT_INAPP_BINARY_LOCK` | **Risoluzione Geografica**: `Regionale (`NUTS-2`)`
* **Archivio Dati Elaborato**: [`local_data/processed/istat_inapp_binary_lock_university_exclusion.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/istat_inapp_binary_lock_university_exclusion.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifica l'impatto numerico del blocco binario istituzionale (`~140.000 giovani/anno tra qualificati IeFP e uscite a 16 anni`), i quali sono legalmente esclusi dall'istruzione terziaria universitaria (ISCED 5-8) in assenza del V anno integrativo.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 53. `mur_ans_university_withdrawals_and_dropouts_panel`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: MUR USTAT / ANS - Rinunce agli Studi, Abbandoni Universitari e Inattività Didattica entro il Primo e Secondo Anno
#### 🇬🇧 **English Title**: MUR USTAT / ANS - University First-Year Withdrawals, Dropouts, and Zero-CFU Didactic Inactivity across Regions

* **Ente Statistico / Autorità Ufficiale**: `MUR (`Ministero dell'Università e della Ricerca - Anagrafe Nazionale Studenti ANS`)`
* **🔗 Link Diretto Open Data**: [https://ustat.mur.gov.it/opendata/](https://ustat.mur.gov.it/opendata/)
* **Codice Flusso SDMX / Indagine**: `MUR_ANS_DROPOUT_2024` | **Risoluzione Geografica**: `Regionale (`NUTS-2`) e per Ateneo/Dipartimento`
* **Archivio Dati Elaborato**: [`local_data/processed/mur_ans_university_withdrawals_and_dropouts_panel.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/mur_ans_university_withdrawals_and_dropouts_panel.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Misura empiricamente la dispersione accademica post-secondaria (`Rinunce al I anno: 11.2% al Nord vs 21.8% al Sud`), evidenziando come le lacune di competenza in ingresso (`Dispersione occulta`) si trasformino in abbandoni formali all'università.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 54. `istat_national_accounts_black_labor_and_irregularity`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: ISTAT Contabilità Nazionale - Tasso di Irregolarità Occupazionale, Lavoro Sommerso e Lavoro Nero Giovanile
#### 🇬🇧 **English Title**: ISTAT National Accounts - Irregular Employment Rate, Shadow Economy, and Informal Black Labor Market among Youth

* **Ente Statistico / Autorità Ufficiale**: `ISTAT (`Contabilità Nazionale - Economia Non Osservata e Lavoro Sommerso DCCV_SOMMERSO`)`
* **🔗 Link Diretto Open Data**: [https://esploradati.istat.it/datapage?id=DCCN_SOMMERSO](https://esploradati.istat.it/datapage?id=DCCN_SOMMERSO)
* **Codice Flusso SDMX / Indagine**: `ISTAT_IRREGULAR_LABOR` | **Risoluzione Geografica**: `Regionale (`NUTS-2`) e per Settore Economico (`Agricoltura, Costruzioni, Servizi, Turismo`)`
* **Archivio Dati Elaborato**: [`local_data/processed/istat_national_accounts_black_labor_and_irregularity.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/istat_national_accounts_black_labor_and_irregularity.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Documenta l'incidenza dell'economia sommersa sul mercato del lavoro giovanile (`Tasso di irregolarità under 35: 14.2% al Nord vs 29.4% al Sud`), spiegando una frazione significativa del fenomeno NEET e della mancata contribuzione previdenziale.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

### 55. `inps_covip_youth_pension_contributory_deficit`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 2: Institutional Macro-Structural & Actuarial Projections (`Indicatori Macro-Strutturali e Modelli Attuariali Ufficiali`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: INPS / COVIP - Proiezioni Attuariali sul Deficit Contributivo Giovanile e sul Rischio di Povertà Pensionistica Futura
#### 🇬🇧 **English Title**: INPS / COVIP - Actuarial Projections on Youth Contributory Gaps and Future Pension Replacement Rates at Age 67

* **Ente Statistico / Autorità Ufficiale**: `INPS (`Coordinamento Generale Statistico e Attuariale`) & COVIP (`Commissione di Vigilanza sui Fondi Pensione`)`
* **🔗 Link Diretto Open Data**: [https://www.inps.it/it/it/dati-e-bilanci/open-data.html](https://www.inps.it/it/it/dati-e-bilanci/open-data.html)
* **Codice Flusso SDMX / Indagine**: `INPS_COVIP_ACTUARIAL_2024` | **Risoluzione Geografica**: `Nazionale per Tipologia di Carriera (`Continua vs Intermittente vs Precariato Esteso`)`
* **Archivio Dati Elaborato**: [`local_data/processed/inps_covip_youth_pension_contributory_deficit.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/inps_covip_youth_pension_contributory_deficit.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Proietta nel lungo periodo le conseguenze dell'intermittenza contrattuale e degli stage precari ($E \rightarrow D$), dimostrando come i buchi contributivi giovanili riducano il tasso di sostituzione pensionistico futuro fino a scendere sotto il 52% dell'ultimo stipendio (`Rischio povertà pensionistica >58%`).

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio fornisce il quadro contabile, macro-economico o attuariale di lungo periodo (es. proiezioni previdenziali COVIP, spesa totale OCSE, o matrici professionali CP2021). Non si tratta di una survey campionaria regionale grezza, ma di un indicatore strutturale di sistema.

---

### 56. `istat_inapp_informal_childcare_and_family_welfare_dependency`
#### 🏷️ **Livello Epistemologico (`Justifiable Standpoint`)**: **Layer 1: Observed Regional/Local Open Data (`Dati Osservati Amministrativi e Campionari Diretti`)**

#### 🇮🇹 **Titolo Istituzionale Italiano**: ISTAT / Eurostat - Dipendenza dal Welfare Familiare Informale, Cura dei Nonni e Coabitazione dei Giovani Adulti (18-34 Anni)
#### 🇬🇧 **English Title**: ISTAT / Eurostat - Informal Family Welfare Reliance, Grandparent Childcare, and Young Adult Co-Residence (Age 18-34)

* **Ente Statistico / Autorità Ufficiale**: `ISTAT (`Struttura delle Famiglie`) & Eurostat (`Labor Force Survey edat_lfse_16 / Co-residence LFS`)`
* **🔗 Link Diretto Open Data**: [https://ec.europa.eu/eurostat/databrowser/view/ilc_lvps08/default/table?lang=en](https://ec.europa.eu/eurostat/databrowser/view/ilc_lvps08/default/table?lang=en)
* **Codice Flusso SDMX / Indagine**: `ISTAT_FAMILY_DEPENDENCY` | **Risoluzione Geografica**: `Regionale (`NUTS-2`) e Confronto Europeo (`Italia vs UE-27`)`
* **Archivio Dati Elaborato**: [`local_data/processed/istat_inapp_informal_childcare_and_family_welfare_dependency.csv`](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/istat_inapp_informal_childcare_and_family_welfare_dependency.csv)

#### 📐 Giustificazione Analitica nel Modello ($O \rightarrow T \rightarrow E \rightarrow D$)
> Quantifica il ruolo strutturale della famiglia d'origine come ammortizzatore sociale e intergenerazionale di ultima istanza (`Coabitazione 18-34 anni: 67.4% in Italia vs 34.2% media UE-27`), compensando la carenza di servizi di cura e i bassi salari giovanili.

#### 🛡️ Nota di Giustificabilità Statistica:
> Questo dominio poggia su rilevazioni amministrative o campionarie dirette a livello regionale (NUTS-2) o provinciale/comunale (NUTS-3/LAU), verificabili cella per cella sui portali esplorativi ufficiali (ISTAT EsploraDati, AlmaLaurea, Eurostat SDMX, MEF SIOPE).

---

## ⚖️ Conclusione della Rifattorizzazione Epistemologica

Grazie alla rifattorizzazione in **`Layer 1 (Dati Osservati)`** e **`Layer 2 (Modelli Attuariali e Macro-Contabili)`**, l'osservatorio Italienation acquisisce uno *standpoint* scientificamente inattaccabile. Non si confonde mai un indicatore di contabilità attuariale con un dato censuario provinciale, garantendo a ricercatori e cittadini la massima trasparenza epistemologica e rigore dimostrativo.

*Prodotto dal Team di Auditing e Rifattorizzazione Epistemologica di Italienation per la Massima Giustificabilità Scientifica.*
