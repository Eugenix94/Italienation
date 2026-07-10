# 🌐 Italienation: Open Science Observatory & Data Laboratory (`holistic_analysis/`)

Welcome to the **Holistic Analysis & Open Data Repository** of the *Italienation* project. 

In the spirit of **Open Science and public scholarship**, we do not present closed, dogmatic policy prescriptions. Instead, this repository serves as an **open observatory and empirical laboratory** that gathers, cleans, and synthesizes multi-scale evidence across **11 distinct domains**, **815,000+ teaching records**, and **113 years of fiscal history (1913–2026)**.

Our explicit goal is to invite **researchers, data scientists, educators, citizens, and policymakers** to access the data directly, test alternative hypotheses, debate structural paradoxes, and contribute their own reflections on Italy's educational and youth labor market dynamics.

---

## 📂 Repository Structure & Access

```
holistic_analysis/
│
├── 📖 README.md                             <-- Open Science Guide & Domain Overview
│
├── 📊 data_panels/                          <-- 13 OPEN-SOURCE DATA PANELS (Clean CSVs ready for public analysis)
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
├── 🌐 interactive_web_experience/           <-- THE OPEN SCIENCE INTERACTIVE WEB OBSERVATORY
│   ├── index.html (THE SOLE HTML FILE: open-ended exploration, reflection prompts, live tables, & diagnostic logs)
│   └── universal_synthesis_master_dashboard.png (High-resolution 300 DPI 6-panel correlation visualization)
│
└── 💻 jupyter_notebook/                     <-- THE EXECUTABLE OPEN-SOURCE NOTEBOOK
    └── italienation_holistic_master_analysis.ipynb (Self-contained executable Python pipeline)
```

---

## ⭐ Exploring the Open Science Observatory (`index.html`)

To provide an intuitive, zero-setup environment for reflection and exploration, we have consolidated our findings into **ONE SINGLE INTERACTIVE HTML OBSERVATORY**:

👉 **Double-click [`interactive_web_experience/index.html`](./interactive_web_experience/index.html) in your browser!**

Inside `index.html`, you will find:
- **📌 Open Science Observatory & Paradoxes:** Explores the 4 core structural dilemmas (`Fiscal Re-allocation`, `Early Childhood Urban Penalty`, `Transition Evaluation Severity`, and `Workforce Continuity vs Flexibility`).
- **💡 Open Research Prompts:** Dedicated callout boxes inviting researchers and citizens to investigate specific confounding variables and territorial nuances.
- **📊 Live Interactive Data Tables:** Direct inspection of municipal nursery seat coverage vs. NEET rates across 10 metropolitan capitals, national teacher *precariato* breakdowns, and regional tracking patterns.
- **💻 Executed Diagnostic Regressions:** Full, transparent execution outputs across all 14 cells of our Python analysis pipeline.
- **🤝 Community Reflection & Research Invitations:** Clear instructions on how to fork the data panels (`data_panels/`), modify regression models in Jupyter, and contribute findings via GitHub Issues and Discussions.

---

## 🔬 Invitation to Analyze the 13 Open Data Panels (`data_panels/`)

Every single dataset in `data_panels/` is open-source and ready for download. Whether you are an academic researcher building econometrics models, a data science student practicing panel regressions, or a journalist investigating territorial inequalities, you are invited to explore:

| File Name | Domain Covered | Research Invitation & Key Dimensions |
| :--- | :--- | :--- |
| `01_macro_fiscal_expenditure_1913_2026.csv` | **Macro-Fiscal Dynamics** | Explore the 113-year trajectory (`1984 Peak: 4.77% GDP` vs `2026: 3.95%`). How do demographic shifts and debt service interact with education spending? |
| `02_eurostat_social_scoreboard_eu27.csv` | **European Benchmarking** | Compare Italian youth NEET (`15-29`) and Early School Leaving (`18-24`) against all EU-27 member states. |
| `03_covid19_age_selective_scarring.csv` | **Pandemic Scarring** | Analyze quarterly labor market shocks separating transitioning youth (`15-29`) from adult incumbents (`35-49`). |
| `04_transition_jump_trap_bocciature_panel.csv` | **Secondary Evaluation** | Investigate the correlation between regional 9th-grade repetition rates (*bocciature*) and subsequent school dropout. |
| `05_tripartite_upper_secondary_tracking.csv` | **Socio-Economic Tracking** | Study regional enrollment distributions across *Licei*, *Istituti Tecnici*, and *Istituti Professionali*. |
| `06_teacher_workforce_precariato_815k_posts.csv` | **Teacher Anatomy** | Examine the structural precariousness (`18.5% overall`) versus the sharp divergence in special needs (*Sostegno*: `>60% precarious`). |
| `07_university_mur_academic_staff_ford_gender.csv` | **University Faculty Sorting** | Analyze gender representation across Fields of Research (`FoRD 02 Engineering: 70% male`). |
| `08_openpolis_metropolitan_urban_penalty.csv` | **Municipal Urban Penalty** | Test the intense negative correlation (`r = -0.88`) between 0-2 nursery coverage and youth NEET incidence across 10 capitals. |
| `09_invalsi_foundational_competency_gaps.csv` | **Competency Deficits** | Cross-reference North-South territorial reading and mathematics proficiency gaps with local socio-economic indicators. |
| `10_household_financial_burden_textbook_tax.csv` | **Household Cost Burden** | Quantify the out-of-pocket textbook expenditure burden (`€700-€1,300/yr`) across secondary school tracks. |

---

## 🤝 How to Contribute to the Open Science Dialogue

1. **Fork & Experiment:** Fork this repository, open `jupyter_notebook/italienation_holistic_master_analysis.ipynb`, and test your own statistical specifications.
2. **Open GitHub Issues:** Share your empirical interpretations, point out confounding factors, or propose additional open datasets to include.
3. **Engage in Public Reflection:** Use our visual correlation engine to foster evidence-based dialogue within your university, school, or community organization.

---
*Created by the Italienation Open Science Collaborative. Dedicated to transparent, open-source educational inquiry.*
