# 🌐 Italienation Holistic Analysis & Data Repository (`holistic_analysis/`)

Welcome to the dedicated **Holistic Analysis & Data Repository** of the *Italienation* project. This standalone directory has been explicitly organized to let users, researchers, data scientists, and policymakers directly access all of our **highly analysed data panels (`data_panels/`)** and our **unified interactive web experience (`interactive_web_experience/index.html`)**.

---

## 📂 Directory Structure & Navigation

```
holistic_analysis/
│
├── 📖 README.md                             <-- User Guide & Domain Navigation Table
│
├── 📊 data_panels/                          <-- ALL 13 HIGHLY ANALYSED DATA PANELS (Clean CSVs ready for download)
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
├── 🌐 interactive_web_experience/           <-- ONE SINGLE UNIFIED HTML WEB EXPERIENCE
│   ├── index.html (THE SOLE HTML FILE: contains all tabs, live tables, notebook diagnostics, and PDF print button)
│   └── universal_synthesis_master_dashboard.png (High-resolution 300 DPI 6-panel synthesis visualization)
│
└── 💻 jupyter_notebook/                     <-- THE EXECUTABLE MASTER NOTEBOOK
    └── italienation_holistic_master_analysis.ipynb (Self-contained executable Python notebook)
```

---

## ⭐ Exploring the Unified Web Experience (`index.html`)

To avoid any confusion from multiple HTML files, we have consolidated our entire interactive web dashboard, statistical data tables, notebook diagnostic outputs, and publication print tools into **ONE SINGLE HTML FILE**:

👉 **Double-click [`interactive_web_experience/index.html`](./interactive_web_experience/index.html) in your browser!**

Inside `index.html`, you can:
- **Switch instantly across 8 interactive tabs:** Overview, 6-Panel Dashboard, Openpolis Metropolitan Penalty, Teacher Precariato, Tripartite Tracking, Macro-Fiscal Expenditure Series, Full Executed Notebook Diagnostics, and The Final Blows (4-Point Policy Agenda).
- **Print or Export to PDF:** Click the **"🖨️ Print / Export to PDF"** button at the top right of the dashboard to automatically format and export a clean, publication-ready multi-page PDF document.

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
*Created by the Italienation Open Science Research Collaborative to ensure universal public access to rigorous, open educational statistics.*
