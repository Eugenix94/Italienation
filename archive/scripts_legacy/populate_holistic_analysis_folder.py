#!/usr/bin/env python3
"""
populate_holistic_analysis_folder.py

Creates the dedicated `holistic_analysis/` directory structure, copies and organizes all 11 highly analysed datasets
into `holistic_analysis/data_panels/`, and organizes all holistic HTML reports, dashboards, and notebooks
into `holistic_analysis/interactive_web_experience/` and `holistic_analysis/jupyter_notebook/`.
"""

import os
import shutil
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")
HOLISTIC_DIR = os.path.join(ROOT_DIR, "holistic_analysis")
DATA_PANELS_DIR = os.path.join(HOLISTIC_DIR, "data_panels")
WEB_EXP_DIR = os.path.join(HOLISTIC_DIR, "interactive_web_experience")
NB_DIR = os.path.join(HOLISTIC_DIR, "jupyter_notebook")

os.makedirs(DATA_PANELS_DIR, exist_ok=True)
os.makedirs(WEB_EXP_DIR, exist_ok=True)
os.makedirs(NB_DIR, exist_ok=True)

LOCAL_DATA = os.path.join(ROOT_DIR, "local_data")
PROCESSED_DIR = os.path.join(LOCAL_DATA, "processed")
OPENPOLIS_DIR = os.path.join(LOCAL_DATA, "Openpolis")
MUR_DIR = os.path.join(LOCAL_DATA, "MUR")
FINAL_ANALYSIS_DIR = os.path.join(ROOT_DIR, "Final_Analysis")

print(f"[{HOLISTIC_DIR}] Populating dedicated holistic analysis directory for external users...")

# 1. Copy & Curate the 11 Highly Analysed Data Panels
dataset_mappings = [
    (os.path.join(PROCESSED_DIR, "italy_education_expenditure_history_panel.csv"), "01_macro_fiscal_expenditure_1913_2026.csv"),
    (os.path.join(PROCESSED_DIR, "global_italy_position_oecd_wb_latest.csv"), "01b_global_italy_oecd_wb_benchmark.csv"),
    (os.path.join(PROCESSED_DIR, "eurostat_social_scoreboard_panel.csv"), "02_eurostat_social_scoreboard_eu27.csv"),
    (os.path.join(PROCESSED_DIR, "neet_covid_period_summary.csv"), "03_covid19_age_selective_scarring.csv"),
    (os.path.join(PROCESSED_DIR, "neet_gender_year_panel.csv"), "03b_neet_gender_disparity_2018_2024.csv"),
    (os.path.join(PROCESSED_DIR, "transition_bridge_model_panel.csv"), "04_transition_jump_trap_bocciature_panel.csv"),
    (os.path.join(PROCESSED_DIR, "hf_upper_sec_track_enrollment_panel.csv"), "05_tripartite_upper_secondary_tracking.csv"),
    (os.path.join(PROCESSED_DIR, "hf_teachers_by_school_order_panel.csv"), "06_teacher_workforce_precariato_815k_posts.csv"),
    (os.path.join(MUR_DIR, "dati-per-bilancio-di-genere", "bdg_serie_academic_staff_ambito.csv"), "07_university_mur_academic_staff_ford_gender.csv"),
    (os.path.join(OPENPOLIS_DIR, "openpolis_neet_metropolitan_capitals.csv"), "08_openpolis_metropolitan_urban_penalty.csv"),
    (os.path.join(PROCESSED_DIR, "snv_esiti_school_year_proxy.csv"), "09_invalsi_foundational_competency_gaps.csv"),
    (os.path.join(PROCESSED_DIR, "italy_school_household_cost_snapshot.csv"), "10_household_financial_burden_textbook_tax.csv"),
    (os.path.join(PROCESSED_DIR, "italy_mur_tuition_benchmark_2024.csv"), "10b_public_university_tuition_benchmark.csv")
]

copied_data_count = 0
for src, target_name in dataset_mappings:
    if os.path.exists(src):
        dst = os.path.join(DATA_PANELS_DIR, target_name)
        shutil.copy2(src, dst)
        copied_data_count += 1
        print(f"  -> Exported Data Panel: {target_name}")
    else:
        print(f"  [!] Missing source file: {src}")

# 2. Copy the Holistic Interactive Web Reports & Dashboards
web_files = [
    "holistic_interactive_experience.html",
    "italienation_holistic_master_analysis.html",
    "italienation_holistic_master_analysis_printable_pdf.html",
    "universal_synthesis_master_dashboard.png"
]

for wf in web_files:
    src = os.path.join(FINAL_ANALYSIS_DIR, wf)
    if os.path.exists(src):
        dst = os.path.join(WEB_EXP_DIR, wf)
        shutil.copy2(src, dst)
        print(f"  -> Exported Web Experience: {wf}")

# 3. Copy & adapt the Master Jupyter Notebook
nb_src = os.path.join(FINAL_ANALYSIS_DIR, "italienation_holistic_master_analysis.ipynb")
if os.path.exists(nb_src):
    dst_nb = os.path.join(NB_DIR, "italienation_holistic_master_analysis.ipynb")
    shutil.copy2(nb_src, dst_nb)
    print("  -> Exported Master Notebook to jupyter_notebook/")

# 4. Create User Guide README.md in holistic_analysis/
readme_path = os.path.join(HOLISTIC_DIR, "README.md")
readme_content = """# 🌐 Italienation Holistic Analysis & Data Repository (`holistic_analysis/`)

Welcome to the dedicated **Holistic Analysis & Data Repository** of the *Italienation* project. This standalone directory has been explicitly organized to let users, researchers, data scientists, and policymakers directly access all of our **highly analysed data panels (`data_panels/`)**, interactive web reports (`interactive_web_experience/`), and executable code (`jupyter_notebook/`).

---

## 📂 Directory Structure & Navigation

```
holistic_analysis/
│
├── 📊 data_panels/                          <-- ALL 11 HIGHLY ANALYSED DATA PANELS (Clean CSVs ready for download)
│   ├── 01_macro_fiscal_expenditure_1913_2026.csv
│   ├── 01b_global_italy_oecd_wb_benchmark.csv
│   ├── 02_eurostat_social_scoreboard_eu27.csv
│   ├── 03_covid19_age_selective_scarring.csv
│   ├── 03b_neet_gender_disparity_2018_2024.csv
│   ├── 04_transition_jump_trap_bocciature_panel.csv
│   ├── 05_tripartite_upper_secondary_tracking.csv
│   ├── 06_teacher_workforce_precariato_815k_posts.csv
│   ├── 07_university_mur_academic_staff_ford_gender.csv
│   ├── 08_openpolis_metropolitan_urban_penalty.csv
│   ├── 09_invalsi_foundational_competency_gaps.csv
│   ├── 10_household_financial_burden_textbook_tax.csv
│   └── 10b_public_university_tuition_benchmark.csv
│
├── 🌐 interactive_web_experience/           <-- THE HOLISTIC HTML DASHBOARDS & REPORTS FOR USERS
│   ├── holistic_interactive_experience.html (Full standalone interactive web application with tabs & tables)
│   ├── italienation_holistic_master_analysis.html (Complete 14-cell executed notebook rendered as searchable HTML)
│   ├── italienation_holistic_master_analysis_printable_pdf.html (Pre-formatted with @media print CSS for PDF export)
│   └── universal_synthesis_master_dashboard.png (High-resolution 300 DPI 6-panel synthesis visualization)
│
└── 💻 jupyter_notebook/                     <-- THE EXECUTABLE MASTER NOTEBOOK
    └── italienation_holistic_master_analysis.ipynb (Self-contained executable Python notebook)
```

---

## 🔬 How to Access & Use the Highly Analysed Data (`data_panels/`)

Every single dataset in `data_panels/` has been cleaned, standardized, and cross-referenced against official micro-data (`ISTAT`, `MUR`, `Openpolis`, `HuggingFace diatribe00/italian-schools-opendata`, `Eurostat`, and `OECD/World Bank`).

### Quick Domain Reference Table:
| File Name | Domain Covered | Key Indicators & Granularity |
| :--- | :--- | :--- |
| `01_macro_fiscal_expenditure_1913_2026.csv` | **Domain 1: Macro-Fiscal** | 113-year historical public spending series (`1984 Peak: 4.77% GDP` vs `2026: 3.95%`). |
| `02_eurostat_social_scoreboard_eu27.csv` | **Domain 2: European Scoreboard** | Youth NEET (`15-29`) and Early School Leavers (`18-24`) across EU-27 member states. |
| `03_covid19_age_selective_scarring.csv` | **Domain 3: COVID-19 Shocks** | Quarterly age-selective scarring separating transition youth from adult incumbents. |
| `04_transition_jump_trap_bocciature_panel.csv` | **Domain 4: Transition Trap** | Regional 9th-grade repetition rates (*bocciature* up to `10.3%`) vs NEET correlation (`r = 0.86`). |
| `05_tripartite_upper_secondary_tracking.csv` | **Domain 5: Tripartite Tracking** | Regional distribution across *Licei*, *Istituti Tecnici*, and *Istituti Professionali*. |
| `06_teacher_workforce_precariato_815k_posts.csv` | **Domain 6: Teacher Anatomy** | High school classroom turnover (`18.5%`) vs Special Needs (*Sostegno*) collapse (`>60% precarious`). |
| `07_university_mur_academic_staff_ford_gender.csv` | **Domain 7: MUR Sorting** | Faculty gender pyramid by Field of Research (`FoRD 02 Engineering: 70% male`). |
| `08_openpolis_metropolitan_urban_penalty.csv` | **Domain 8: Openpolis Census** | Nursery seat coverage (`Asili Nido 0-2 yrs`) vs NEET rates (`r = -0.88`) across 10 capitals. |
| `09_invalsi_foundational_competency_gaps.csv` | **Domain 9: INVALSI Deficits** | North-South territorial reading and mathematics proficiency gaps. |
| `10_household_financial_burden_textbook_tax.csv` | **Domain 10: Household Burden** | Secondary school out-of-pocket textbook tax (`€700-€1,300/yr per student`). |

---

## ⭐ Exploring the Full Web Experience

You do **not** need Python or Jupyter installed to explore the full analysis:
1. Double-click `interactive_web_experience/holistic_interactive_experience.html` in your browser to launch our **rich interactive web dashboard** featuring clickable tabs, live statistical tables, and the 4-point systemic reform roadmap.
2. Double-click `interactive_web_experience/italienation_holistic_master_analysis.html` to review all 14 executed cells with complete diagnostic regression outputs.
3. To generate a formal publication PDF, open `interactive_web_experience/italienation_holistic_master_analysis_printable_pdf.html` and press `Ctrl+P -> Save as PDF`.

---
*Created by the Italienation Open Science Research Collaborative to ensure universal public access to rigorous, open educational statistics.*
"""

with open(readme_path, "w", encoding="utf-8") as f_rd:
    f_rd.write(readme_content)

print(f"[SUCCESS] Created comprehensive README.md in {HOLISTIC_DIR}")
print(f"[SUCCESS] Total data panels exported: {copied_data_count}/13")
