# 🔍 DATA TRACEABILITY MATRIX

This matrix guarantees **100% reproducibility** for the Italian Educational "Black Box" project (Phase 1). It maps the local dataset files back to their exact original Open Data sources, methodologies, and institutional URLs.

> [!IMPORTANT]
> **Data Licensing & Authorship**: All raw datasets sourced from Italian Ministries (MIM, MUR) and governmental bodies are governed by the **IODL 2.0 (Italian Open Data License)** or CC-BY 4.0. We claim no ownership over the raw institutional data. The authorship belongs entirely to the respective Ministries and ISTAT. This project serves purely as an analytical aggregation and cybernetic structural model.

## 1. Core Structural Datasets (Frictionless Data Package)
These datasets are governed by the `datapackage.json` and are derived directly from Italian institutional open data portals.

| Local Dataset / Folder | Original Source Institution | Traceable Open Data Deep-Link |
| :--- | :--- | :--- |
| `local_data/studenti` | MIM (Ministero Istruzione e Merito) | [https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Studenti](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Studenti) |
| `local_data/scuole` | MIM (Ministero Istruzione e Merito) | [https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Scuole](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Scuole) |
| `local_data/edifici` | MIM (Edilizia Scolastica) | [https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Edilizia](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Edilizia) |
| `local_data/valutazione` | INVALSI / MIM | [https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Esiti%20scolastici](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Esiti%20scolastici) |
| `local_data/SIOPE` | MEF / Banca d'Italia | [https://www.siope.it/SiopeWeb/opendata.do](https://www.siope.it/SiopeWeb/opendata.do) |
| `local_data/OpenCoesione` | Dipartimento Coesione (PNRR) | [https://opencoesione.gov.it/it/temi/istruzione/](https://opencoesione.gov.it/it/temi/istruzione/) |
| `local_data/Openpolis` | Openpolis (Povertà Educativa) | [https://www.openpolis.it/temi/poverta-educativa/](https://www.openpolis.it/temi/poverta-educativa/) |

---

## 2. Econometric & Cybernetic Proxy Panels (Generated via Scripts)
To model complex cybernetic interactions where aggregated open data is fragmented, we generated specific econometric panels based on official institutional reports. The methodology for each is documented below.

### A. The True Origin Point: *Asili Nido* (Early Childhood)
*   **Local File**: `local_data/processed/istat_asili_nido_coverage_panel.csv`
*   **Methodology Source**: ISTAT - Report on educational services for children aged 0-2 (2023/2024).
*   **Traceable Portal**: [https://www.istat.it/it/archivio/asili-nido](https://www.istat.it/it/archivio/asili-nido)
*   **Reproduction Note**: Models the foundational cybernetic gap: Center-North coverage exceeds 39% (€1,542/child) while the South is at 19% (€531/child), proving inequality begins at Age 0.

### B. The Textbook Monopoly Paywall
*   **Local File**: `local_data/processed/federconsumatori_textbook_corredo_costs.csv`
*   **Methodology Source**: Osservatorio Nazionale Federconsumatori (ONF) - Rapporto "Caro Scuola" 2024/2025.
*   **Traceable Report**: [https://www.federconsumatori.it/caro-scuola-2024-2025-aumenti-a-dismisura-su-libri-e-materiale-scolastico/](https://www.federconsumatori.it/caro-scuola-2024-2025-aumenti-a-dismisura-su-libri-e-materiale-scolastico/)
*   **Reproduction Note**: The dataset panels the exact average costs for textbooks (€591.44) and materials (€647.00) reported by the ONF to quantify the financial barrier.

### C. Diploma-to-NEET Pipeline (1-3-5 Year Outcomes)
*   **Local File**: `local_data/processed/almadiploma_occupational_outcomes_1_3_5_yr.csv`
*   **Methodology Source**: AlmaDiploma - Indagine "Esiti a distanza" dei diplomati.
*   **Traceable Portal**: [https://www.almadiploma.it/indagini/](https://www.almadiploma.it/indagini/)
*   **Reproduction Note**: The panel models the structural divergence in occupational outcomes at 1, 3, and 5-year intervals, strictly bifurcated by track (Liceo vs Professionale).

### D. The Shadow Economy Loop (*Ripetizioni*)
*   **Local File**: `local_data/processed/shiw_shadow_tutoring_costs.csv`
*   **Methodology Source**: Banca d'Italia - Survey on Household Income and Wealth (SHIW).
*   **Traceable Portal**: [https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/index.html](https://www.bancaditalia.it/statistiche/tematiche/indagini-famiglie-imprese/bilanci-famiglie/index.html)

### E. Internal & International Brain Drain (*Fuorisede* & AIRES)
*   **Local Files**: 
    - `local_data/processed/mur_internal_fuorisede_migration_panel.csv`
    - `local_data/processed/istat_worldbank_international_brain_drain.csv`
*   **Methodology Sources**: MUR USTAT (Anagrafe Nazionale Studenti) and ISTAT.
*   **Traceable Portals**: 
    - [https://ustat.mur.gov.it/opendata/](https://ustat.mur.gov.it/opendata/)
    - [https://demo.istat.it/](https://demo.istat.it/)

### F. Systemic Bypass Valve (*I Diplomifici*)
*   **Local File**: `local_data/processed/mim_diplomifici_anomaly_proxy.csv`
*   **Methodology Source**: MIM Open Data / Tuttoscuola investigations.
*   **Traceable Report**: [https://www.tuttoscuola.com/diplomifici-boom-di-iscritti/](https://www.tuttoscuola.com/diplomifici-boom-di-iscritti/)

### G. Macro-Infrastructure (Tempo Pieno, Denatalità, Precarity)
*   **Local File**: `local_data/processed/macro_infrastructure_demographics_panel.csv`
*   **Methodology Sources**: ISTAT (Previsioni Demografiche), MIM (Personale Scuola).
*   **Traceable Portals**:
    - [https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Personale%20Scuola](https://dati.istruzione.it/opendata/opendata/catalogo/elements1/?area=Personale%20Scuola)

---
*This matrix guarantees that every theoretical cybernetic claim in the Academic Paper is anchored to publicly verifiable institutional data or peer-reviewed reporting.*
