# Italienation: The Structural Double Penalty & Tripartite Illusion
**Data Release V2 (Complete Project Archive)**

## Overview
This repository contains the complete, reproducible dataset and codebase for the *Italienation* project. The research empirically demonstrates the "Structural Double Penalty" within the Italian educational system, wherein early tracking (at age 14) serves as a mechanism of class segregation, exacerbated by regressive state resource allocation (infrastructural decay and teacher precarity concentrated in vocational institutes).

## Contents of this Archive
*   `processed_data/`: Cleaned and normalized CSV/JSON files synthesizing 681 raw datasets from ISTAT, MIM, MUR, and Eurostat.
*   `notebooks/`: 60+ Jupyter notebooks detailing the econometric methodology, causal inference, and machine learning models (XGBoost/SHAP) used to validate the thesis.
*   `frontend/`: The complete React (Vite) source code for the interactive OED (Origin-Education-Destination) Dashboard and Data Catalog.
*   `docs/`: The full suite of methodological audits, metadata tracing, and the definitive `ITALIENATION_MASTER_REPORT.md`.

## Methodology
The core hypothesis was tested by linking MEF (Ministry of Economy) sub-municipal IRPEF tax data with MIM (Ministry of Education) school registries (`Scuole_in_chiaro`). Predictive modeling and correlation matrices confirmed that the probability of attending a Lyceum vs. a Vocational institute scales almost perfectly with neighborhood taxable income. 

Furthermore, data on architectural barriers and teacher tenures definitively shows that structural precarity is highest in the schools serving the most vulnerable demographic brackets, cementing the "Double Penalty."

## License
All data derived from public ministries is subject to Open Data policies (IODL 2.0 / CC BY 4.0). The codebase (React frontend, Python scripts) is released under the MIT License.

## Citation
Please use the Zenodo DOI generated for this release when referencing the data or the econometric methodology in academic publications.
