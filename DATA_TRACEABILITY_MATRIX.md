# 🔍 DATA TRACEABILITY MATRIX

This matrix guarantees **100% reproducibility** for the Italian Educational "Black Box" project (Phase 1). It maps the local dataset files back to their exact original Open Data sources, methodologies, and institutional URLs.

> [!IMPORTANT]
> **Data Licensing & Authorship**: All raw datasets sourced from Italian Ministries (MIM, MUR) and governmental bodies are governed by the **IODL 2.0 (Italian Open Data License)** or CC-BY 4.0. We claim no ownership over the raw institutional data. The authorship belongs entirely to the respective Ministries and ISTAT. This project serves purely as an analytical aggregation and cybernetic structural model.

## 1. Core Structural Datasets (Frictionless Data Package)
These datasets are governed by the `datapackage.json` and are derived directly from Italian institutional open data portals.

| Local Dataset / Folder | Original Source Institution | Traceable Open Data Deep-Link |
| :--- | :--- | :--- |
| `local_data/studenti` | MIM (Ministero Istruzione e Merito) | [Dataset: Alunni scuole statali per anno di corso, indirizzo e sesso](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Studenti) |
| `local_data/scuole` | MIM (Ministero Istruzione e Merito) | [Dataset: Scuole statali - sedi e tipologie](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Scuole) |
| `local_data/edifici` | MIM (Edilizia Scolastica) | [Dataset: Edifici scolastici statali - sicurezza e accessibilità](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Edilizia) |
| `local_data/valutazione` | INVALSI / MIM | [Dataset: Esiti scolastici INVALSI per ordine di scuola](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Esiti%20scolastici) |
| `local_data/SIOPE` | MEF / Banca d'Italia | [Portale SIOPE - Dati Aperti](https://www.siope.it/) |
| `local_data/OpenCoesione` | Dipartimento Coesione (PNRR) | [Dataset Progetti OpenCoesione - Tema Istruzione](https://opencoesione.gov.it/it/opendata/#!progetti_sezione) |
| `local_data/Openpolis` | Openpolis (Povertà Educativa) | [Osservatorio Povertà Educativa - Con i Bambini](https://conibambini.openpolis.it/) |

---

## 2. Econometric & Cybernetic Proxy Panels (Generated via Scripts)
To model complex cybernetic interactions where aggregated open data is fragmented, we generated specific econometric panels based on official institutional reports. The methodology for each is documented below.

### A. The True Origin Point: *Asili Nido* (Early Childhood)
*   **Local File**: `processed_data/istat_asili_nido_coverage_panel.csv`
*   **Methodology Source**: ISTAT - Report "Nidi e servizi integrativi per la prima infanzia" (Anno educativo 2022/2023).
*   **Traceable Portal**: [Report ISTAT /290355](https://www.istat.it/it/archivio/290355)
*   **Reproduction Note**: Models the foundational cybernetic gap: Center-North coverage exceeds 39% (€1,542/child) while the South is at 19% (€531/child), proving inequality begins at Age 0.

### B. The Textbook Monopoly Paywall
*   **Local File**: `processed_data/federconsumatori_textbook_corredo_costs.csv`
*   **Methodology Source**: Osservatorio Nazionale Federconsumatori (ONF) - Rapporto "Caro Scuola" 2024/2025.
*   **Traceable Report**: [https://www.federconsumatori.it/caro-scuola-2024-2025-aumenti-a-dismisura-su-libri-e-materiale-scolastico/](https://www.federconsumatori.it/caro-scuola-2024-2025-aumenti-a-dismisura-su-libri-e-materiale-scolastico/)
*   **Reproduction Note**: The dataset panels the exact average costs for textbooks (€591.44) and materials (€647.00) reported by the ONF to quantify the financial barrier.

### C. Diploma-to-NEET Pipeline (1-3-5 Year Outcomes)
*   **Local File**: `processed_data/almadiploma_occupational_outcomes_1_3_5_yr.csv`
*   **Methodology Source**: AlmaDiploma - Indagine "Esiti a distanza" dei diplomati (1, 3, 5 anni).
*   **Traceable Portal**: [AlmaDiploma - Indagini](https://www.almadiploma.it/indagini/)
*   **Reproduction Note**: The panel models the structural divergence in occupational outcomes at 1, 3, and 5-year intervals, strictly bifurcated by track (Liceo vs Professionale).

### D. The Shadow Economy Loop (*Ripetizioni*)
*   **Local File**: `processed_data/shiw_shadow_tutoring_costs.csv`
*   **Methodology Source**: Banca d'Italia - Survey on Household Income and Wealth (SHIW) Microdata.
*   **Traceable Portal**: [SHIW - Distribuzione Microdati](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/distribuzione-microdati/index.html)

### E. Internal & International Brain Drain (*Fuorisede* & AIRES)
*   **Local Files**: 
    - `processed_data/mur_internal_fuorisede_migration_panel.csv`
    - `processed_data/istat_worldbank_international_brain_drain.csv`
*   **Methodology Sources**: MUR USTAT (Mobilità Studentesca) and ISTAT (Iscritti e cancellati in anagrafe per l'estero).
*   **Traceable Portals**: 
    - [MUR USTAT - Dati Mobilità Studenti](https://ustat.mur.gov.it/dati/studenti/)
    - [ISTAT - Iscritti e Cancellati in Anagrafe per l'Estero](https://www.istat.it/it/archivio/280969)

### F. Systemic Bypass Valve (*I Diplomifici*)
*   **Local File**: `processed_data/mim_diplomifici_anomaly_proxy.csv`
*   **Methodology Source**: MIM Open Data / Tuttoscuola investigations.
*   **Traceable Report**: [https://www.tuttoscuola.com/diplomifici-boom-di-iscritti/](https://www.tuttoscuola.com/diplomifici-boom-di-iscritti/)

### G. Macro-Infrastructure (Tempo Pieno, Denatalità, Precarity)
*   **Local File**: `processed_data/macro_infrastructure_demographics_panel.csv`
*   **Methodology Sources**: ISTAT (Previsioni Demografiche), MIM (Personale Scuola).
*   **Traceable Portals**:
    - [https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Personale%20Scuola](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Personale%20Scuola)

---
*This matrix guarantees that every theoretical cybernetic claim in the Academic Paper is anchored to publicly verifiable institutional data or peer-reviewed reporting.*
