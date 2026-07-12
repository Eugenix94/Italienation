# Italienation: Citizen-First Open Science Observatory on the Italian Educational Pipeline & NEET Exclusion

**Repository & OSF Intent**: Empirical validation of the Extended Social Mobility Triangle with School Track (O-T-E-D) across Italian NUTS-2 regions and European benchmarks.

## Canonical Provenance & Dataflow Registry

Every empirical indicator across our citizen observatory is directly linked to an official national or international statistical authority with persistent identifiers and SDMX flow definitions to guarantee 100% scientific reproducibility and democratic transparency.

### `istat_repeaters_upper_secondary`: Ripetenti per anno di corso e indirizzo scolastico nella Scuola Secondaria di II Grado / *Upper Secondary Grade Repeaters by Year of Course and School Track*

- **Institution & Authority**: `ISTAT (Istituto Nazionale di Statistica)`
- **Official Data Portal**: [ISTAT SDMX Open Data Portal (I.Stat / Esploradati)](https://esploradati.istat.it/databrowser/#/it/dw/categories/IT1,Z0800,1.0/I_EDUC/DCIS_SCUOLE/52_1044_DF_DCIS_SCUOLE_15)
- **SDMX Flow ID / Table Code**: `52_1044_DF_DCIS_SCUOLE_15`
- **Historical Coverage**: `2015/2016 – 2024/2025`
- **Key Variables Executed**: `OBS_VALUE (Tasso di bocciatura %), TYPE_SCHOOL (LIC, TEC, VOC), SCHOOL_YEAR (FIR, SEC, THIR, ALL), TYPE_SCHOOL_MANAGEMENT (PUB, PRI, ALL)`
- **Theoretical Role in Extended OED Triangle (`O-T-E-D`)**: Measures Track-to-Education friction (T -> E). Proves the 18.0% first-year failure concentration in Istituti Professionali.

---

### `openpolis_neet_and_poverty`: Tasso di Giovani NEET (15–29 anni) e Povertà Educativa Regionale / Provinciale / *Youth NEET Rate (15–29 years) and Territorial Educational Poverty*

- **Institution & Authority**: `Openpolis & ISTAT (Osservatorio Povertà Educativa Con i Bambini)`
- **Official Data Portal**: [Openpolis Dati Aperti / ISTAT Rilevazione sulle Forze di Lavoro (RFL)](https://www.openpolis.it/parole/che-cosa-si-intende-per-neet/)
- **SDMX Flow ID / Table Code**: `ISTAT RFL / Openpolis API`
- **Historical Coverage**: `2018 – 2024`
- **Key Variables Executed**: `tasso_neet_15_29_pct, abbandono_scolastico_precoce_elet_pct`
- **Theoretical Role in Extended OED Triangle (`O-T-E-D`)**: Measures the ultimate social and labor market destination (D) resulting from early school leaving (ELET).

---

### `eurydice_structures_and_elet`: Strutture dei Sistemi Educativi Europei (ISCED 0–4) e Indicatori Politici ELET / *European Education System Structures (ISCED 0–4) and ELET System-Level Policy Indicators*

- **Institution & Authority**: `EURYDICE Network (European Education and Culture Executive Agency - EACEA / European Commission)`
- **Official Data Portal**: [Eurydice Data and Visuals / Eurydice Open Data](https://eurydice.eacea.ec.europa.eu/data-and-visuals/european-education-structures)
- **SDMX Flow ID / Table Code**: `EURYDICE_STRUCTURES_2025_2026 / ELET_2024_2025`
- **Historical Coverage**: `2024/2025 – 2025/2026`
- **Key Variables Executed**: `Starting age, Duration, ISCED category, Compulsory education age, Early warning systems (Indicator 1), IEPs (Indicator 2), CPD competences (Indicator 3)`
- **Theoretical Role in Extended OED Triangle (`O-T-E-D`)**: Provides the structural system parameters (Tracking Age T, Bocciatura legal rules) to conduct comparative causal analysis between Italy and European benchmarks.

---

### `mur_university_tuition_and_dropout`: Contribuzione Media Studentesca e Tasso di Abbandono Universitario al Primo Anno / *Average University Tuition Fees and First-Year University Dropout Rate*

- **Institution & Authority**: `MUR (Ministero dell'Università e della Ricerca - Ufficio Statistica)`
- **Official Data Portal**: [Portale Dati dell'Istruzione Superiore (Dati Aperti MUR)](https://dati.mur.gov.it/)
- **SDMX Flow ID / Table Code**: `MUR_PARQUET_2025_Contribuzione_media / MUR_PARQUET_Tasso_di_abbandono`
- **Historical Coverage**: `2011/2012 – 2024/2025`
- **Key Variables Executed**: `Contribuzione_media_paganti_eur, Tasso_abbandono_primo_anno_pct, COD_ATENEO`
- **Theoretical Role in Extended OED Triangle (`O-T-E-D`)**: Measures downstream tertiary progression shock (E -> D), showing how high school repetition predetermines first-year university dropout.

---

### `oecd_wb_international_tracking_benchmark`: Benchmark Internazionale OCSE/World Bank: Età di Tripartizione vs. Tasso Lordo di Iscrizione Terziaria / *OECD/World Bank International Benchmark: Tracking Age vs. Gross Tertiary Enrollment Rate*

- **Institution & Authority**: `OECD (Education at a Glance) & World Bank (EdStats Database)`
- **Official Data Portal**: [OECD Data Explorer / World Bank Open Data](https://data.oecd.org/eduresource/public-spending-on-education.htm)
- **SDMX Flow ID / Table Code**: `OECD_EAG_2024_B1_C1 / WB_EDSTATS_SE.TER.ENRR`
- **Historical Coverage**: `2020 – 2024`
- **Key Variables Executed**: `tracking_age, public_spending_pct_gdp, tertiary_enrollment_gross_pct, learning_poverty_pct`
- **Theoretical Role in Extended OED Triangle (`O-T-E-D`)**: Proves empirically that unified comprehensive secondary systems (>16 years tracking age) achieve +14.4% higher university enrollment than early tripartite models.

---

### `mim_siope_municipal_infrastructure`: Spesa Comunale SIOPE per Alunno e Anagrafe Edilizia Scolastica (Agibilità e Barriere Architettoniche) / *SIOPE Municipal Cash Expenditure per Pupil and School Building Safety Registry*

- **Institution & Authority**: `MIM (Ministero dell'Istruzione e del Merito) & MEF (Banca d'Italia SIOPE)`
- **Official Data Portal**: [Portale Unico Dati della Scuola (MIM Open Data) & SIOPE Open Data](https://dati.istruzione.it/esplora/rilascio-dati/anagrafe-edilizia-scolastica)
- **SDMX Flow ID / Table Code**: `MIM_EDILIZIA_AGIBILITA / MEF_SIOPE_CASSA_COMUNI`
- **Historical Coverage**: `2021 – 2024`
- **Key Variables Executed**: `siope_cassa_alunno_eur, cert_agibilita_pct, barriere_arch_pct`
- **Theoretical Role in Extended OED Triangle (`O-T-E-D`)**: Measures the baseline institutional and territorial resources (O -> School Environment) before secondary tracking begins.

---
