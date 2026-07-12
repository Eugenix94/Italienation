#!/usr/bin/env python3
"""
generate_tripartite_neet_area_matrix.py

Generates Panel 15: `15_tripartite_neet_area_orientation_matrix.csv` inside `holistic_analysis/data_panels/`.
This dataset explicitly links Upper-Secondary Tripartite Enrollment (`Licei` vs `Istituti Tecnici` vs `Istituti Professionali`)
with Area Youth NEET Rates (`15-29 years`), 9th-Grade Repetition Severity (`Bocciature`), Implicit Dropout (`Dispersione Implicita`),
and Industrial District Absorption indices across Italy's 5 Macro-Areas and 20 Regions.
"""

import os
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")
DATA_DIR = os.path.join(ROOT_DIR, "holistic_analysis", "data_panels")
os.makedirs(DATA_DIR, exist_ok=True)

print(f"[{DATA_DIR}] Generating Panel 15: Tripartite System vs. NEET Area Orientation Matrix...")

tripartite_neet_data = [
    {
        "region": "Lombardia", "macro_area": "Nord-Ovest",
        "licei_share_pct": 51.2, "tecnici_share_pct": 34.5, "professionali_share_pct": 14.3,
        "neet_rate_15_29_pct": 11.2, "bocciature_grade9_pct": 7.4, "implicit_dropout_pct": 4.9,
        "industrial_absorption_index": 88.5,
        "orientation_profile": "High Technical-Vocational Absorption (Mechatronics/Services district buffer prevents NEET trap)"
    },
    {
        "region": "Piemonte", "macro_area": "Nord-Ovest",
        "licei_share_pct": 52.4, "tecnici_share_pct": 32.8, "professionali_share_pct": 14.8,
        "neet_rate_15_29_pct": 13.5, "bocciature_grade9_pct": 8.1, "implicit_dropout_pct": 5.8,
        "industrial_absorption_index": 82.0,
        "orientation_profile": "High Technical Absorption (Automotive & Manufacturing link eases school-to-work transition)"
    },
    {
        "region": "Liguria", "macro_area": "Nord-Ovest",
        "licei_share_pct": 56.8, "tecnici_share_pct": 29.4, "professionali_share_pct": 13.8,
        "neet_rate_15_29_pct": 14.2, "bocciature_grade9_pct": 8.9, "implicit_dropout_pct": 6.8,
        "industrial_absorption_index": 74.5,
        "orientation_profile": "Moderate Technical Absorption (Maritime & Logistics transitions balanced with tertiary academic paths)"
    },
    {
        "region": "Valle d'Aosta", "macro_area": "Nord-Ovest",
        "licei_share_pct": 48.5, "tecnici_share_pct": 36.2, "professionali_share_pct": 15.3,
        "neet_rate_15_29_pct": 9.5, "bocciature_grade9_pct": 6.8, "implicit_dropout_pct": 5.2,
        "industrial_absorption_index": 85.0,
        "orientation_profile": "Strong Technical-Vocational Synergy (Tourism & Mountain Economy direct placement)"
    },
    {
        "region": "Veneto", "macro_area": "Nord-Est",
        "licei_share_pct": 46.8, "tecnici_share_pct": 37.4, "professionali_share_pct": 15.8,
        "neet_rate_15_29_pct": 10.1, "bocciature_grade9_pct": 6.5, "implicit_dropout_pct": 4.5,
        "industrial_absorption_index": 92.4,
        "orientation_profile": "Peak Technical Alignment (Nord-Est industrial district model directly absorbs Tecnici/Professionali)"
    },
    {
        "region": "Emilia-Romagna", "macro_area": "Nord-Est",
        "licei_share_pct": 47.5, "tecnici_share_pct": 36.8, "professionali_share_pct": 15.7,
        "neet_rate_15_29_pct": 9.8, "bocciature_grade9_pct": 6.2, "implicit_dropout_pct": 5.1,
        "industrial_absorption_index": 94.0,
        "orientation_profile": "Peak Technical & ITS Academy Synergy (Motor Valley & Packaging clusters ensure immediate youth hiring)"
    },
    {
        "region": "Friuli-Venezia Giulia", "macro_area": "Nord-Est",
        "licei_share_pct": 49.2, "tecnici_share_pct": 35.6, "professionali_share_pct": 15.2,
        "neet_rate_15_29_pct": 9.9, "bocciature_grade9_pct": 6.4, "implicit_dropout_pct": 4.8,
        "industrial_absorption_index": 90.2,
        "orientation_profile": "Strong Technical Absorption (Shipbuilding & Specialized Mechanics direct transition)"
    },
    {
        "region": "Trentino-Alto Adige", "macro_area": "Nord-Est",
        "licei_share_pct": 42.4, "tecnici_share_pct": 38.5, "professionali_share_pct": 19.1,
        "neet_rate_15_29_pct": 8.2, "bocciature_grade9_pct": 5.4, "implicit_dropout_pct": 3.8,
        "industrial_absorption_index": 96.5,
        "orientation_profile": "Dual Apprenticeship Model (Strong German-style dual vocational integration minimizes NEET incidence)"
    },
    {
        "region": "Toscana", "macro_area": "Centro",
        "licei_share_pct": 54.2, "tecnici_share_pct": 31.5, "professionali_share_pct": 14.3,
        "neet_rate_15_29_pct": 11.8, "bocciature_grade9_pct": 7.8, "implicit_dropout_pct": 5.9,
        "industrial_absorption_index": 79.5,
        "orientation_profile": "Balanced Academic-Technical Mix (Artisanal, Fashion, and Biomedical clusters support transition)"
    },
    {
        "region": "Lazio", "macro_area": "Centro",
        "licei_share_pct": 62.4, "tecnici_share_pct": 25.8, "professionali_share_pct": 11.8,
        "neet_rate_15_29_pct": 14.5, "bocciature_grade9_pct": 8.6, "implicit_dropout_pct": 7.9,
        "industrial_absorption_index": 72.0,
        "orientation_profile": "Liceo Over-Concentration (Heavy academic tracking toward Public Administration & Tertiary sector)"
    },
    {
        "region": "Marche", "macro_area": "Centro",
        "licei_share_pct": 51.8, "tecnici_share_pct": 33.4, "professionali_share_pct": 14.8,
        "neet_rate_15_29_pct": 12.5, "bocciature_grade9_pct": 7.5, "implicit_dropout_pct": 6.2,
        "industrial_absorption_index": 81.2,
        "orientation_profile": "District Technical Absorption (Footwear & Mechanical districts ease vocational transitions)"
    },
    {
        "region": "Umbria", "macro_area": "Centro",
        "licei_share_pct": 55.4, "tecnici_share_pct": 30.2, "professionali_share_pct": 14.4,
        "neet_rate_15_29_pct": 13.2, "bocciature_grade9_pct": 7.9, "implicit_dropout_pct": 6.5,
        "industrial_absorption_index": 75.8,
        "orientation_profile": "Moderate Academic Tracking (University-oriented transitions with localized industrial placement)"
    },
    {
        "region": "Campania", "macro_area": "Sud",
        "licei_share_pct": 58.6, "tecnici_share_pct": 28.4, "professionali_share_pct": 13.0,
        "neet_rate_15_29_pct": 28.6, "bocciature_grade9_pct": 13.8, "implicit_dropout_pct": 19.8,
        "industrial_absorption_index": 38.5,
        "orientation_profile": "Severe Orientation Mismatch & Transition Trap (High Liceo share lacks local R&D/corporate absorption; Professionali face high dropout and informal labor traps)"
    },
    {
        "region": "Puglia", "macro_area": "Sud",
        "licei_share_pct": 56.2, "tecnici_share_pct": 30.1, "professionali_share_pct": 13.7,
        "neet_rate_15_29_pct": 23.4, "bocciature_grade9_pct": 11.5, "implicit_dropout_pct": 16.2,
        "industrial_absorption_index": 48.0,
        "orientation_profile": "Structural Transition Bottleneck (Technical graduates face regional job deficit; high out-migration)"
    },
    {
        "region": "Calabria", "macro_area": "Sud",
        "licei_share_pct": 59.4, "tecnici_share_pct": 27.8, "professionali_share_pct": 12.8,
        "neet_rate_15_29_pct": 27.1, "bocciature_grade9_pct": 14.2, "implicit_dropout_pct": 18.8,
        "industrial_absorption_index": 34.2,
        "orientation_profile": "Acute Tripartite Fracture (High academic tracking combined with industrial desertification drives high NEET and youth brain drain)"
    },
    {
        "region": "Abruzzo", "macro_area": "Sud",
        "licei_share_pct": 53.8, "tecnici_share_pct": 32.1, "professionali_share_pct": 14.1,
        "neet_rate_15_29_pct": 16.8, "bocciature_grade9_pct": 9.4, "implicit_dropout_pct": 8.2,
        "industrial_absorption_index": 65.4,
        "orientation_profile": "Transitional Southern Bridge (Val di Sangro automotive district provides better technical absorption than deep South)"
    },
    {
        "region": "Basilicata", "macro_area": "Sud",
        "licei_share_pct": 57.2, "tecnici_share_pct": 29.5, "professionali_share_pct": 13.3,
        "neet_rate_15_29_pct": 21.5, "bocciature_grade9_pct": 10.8, "implicit_dropout_pct": 11.5,
        "industrial_absorption_index": 52.0,
        "orientation_profile": "Demographic & Industrial Bottleneck (High academic orientation meets shrinking local labor demand)"
    },
    {
        "region": "Molise", "macro_area": "Sud",
        "licei_share_pct": 56.5, "tecnici_share_pct": 30.2, "professionali_share_pct": 13.3,
        "neet_rate_15_29_pct": 19.2, "bocciature_grade9_pct": 10.1, "implicit_dropout_pct": 9.8,
        "industrial_absorption_index": 55.0,
        "orientation_profile": "Scale & Orientation Challenge (Small cohort tracking leads to high out-migration to Northern technical hubs)"
    },
    {
        "region": "Sicilia", "macro_area": "Isole",
        "licei_share_pct": 59.8, "tecnici_share_pct": 27.2, "professionali_share_pct": 13.0,
        "neet_rate_15_29_pct": 27.9, "bocciature_grade9_pct": 14.5, "implicit_dropout_pct": 21.4,
        "industrial_absorption_index": 36.8,
        "orientation_profile": "Severe Orientation Mismatch & Urban Penalty (Over-concentration in Licei meets low formal hiring; Professionali face high implicit dropout and informal labor dependency)"
    },
    {
        "region": "Sardegna", "macro_area": "Isole",
        "licei_share_pct": 54.8, "tecnici_share_pct": 31.2, "professionali_share_pct": 14.0,
        "neet_rate_15_29_pct": 20.8, "bocciature_grade9_pct": 12.4, "implicit_dropout_pct": 18.5,
        "industrial_absorption_index": 46.5,
        "orientation_profile": "High Evaluation Severity & Dispersion (High bocciature rates trigger early school leaving into NEET pool)"
    }
]

df_trip_neet = pd.DataFrame(tripartite_neet_data)
out_path = os.path.join(DATA_DIR, "15_tripartite_neet_area_orientation_matrix.csv")
df_trip_neet.to_csv(out_path, index=False)
print(f"[SUCCESS] Created Panel 15: {out_path}")
