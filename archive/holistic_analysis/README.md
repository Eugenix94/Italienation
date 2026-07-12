# 🌐 Italienation: Open Science Observatory & Data Laboratory (`holistic_analysis/`)

Welcome to the **Holistic Analysis & Open Data Repository** of the *Italienation* project. 

In the spirit of **Open Science and public scholarship**, we do not present closed, dogmatic policy prescriptions. Instead, this repository serves as an **open observatory and empirical laboratory** that gathers, cleans, and synthesizes multi-scale evidence across **11 distinct domains**, **815,000+ teaching records**, and **113 years of fiscal history (1913–2026)**.

---

## 📖 The Extensive Definition & Theoretical Anatomy of *Italienation* (*Italienazione*)

To understand Italian educational and youth labor market dynamics, we must move beyond short, synthetic summaries. **Italienation** (*Italienazione*) is a profound, multi-generational, structural equilibrium that spans seven interconnected sociological, economic, and institutional dimensions:

1. **Etymological & Conceptual Genesis (*Structural Anomie*):** A neologism fusing *Italy* and *Alienation*, describing a chronic condition where public institutions, economic incentives, and educational structures systematically estrange youth (*NEETs*, early school leavers, precarious workers, young researchers) from active civic and economic participation.
2. **Intergenerational Breakdown & Demographic Winter (*Inverno Demografico*):** Operating alongside a birth rate of `1.20 children per woman` and an aging population, public wealth is disproportionately allocated toward passive incumbent preservation (pensions, senior welfare, debt servicing) while forward-looking human capital investments (schools, universities, research labs) face four decades of structural retrenchment.
3. **Territorial Dualism & Municipal Urban Penalty (*Penalità Urbana*):** Where municipal nursery seat coverage (<code>0–2 years</code>) drops below `15%` across Southern metropolitan capitals (`Napoli, Catania, Palermo`), youth NEET rates systematically exceed `25% to 35%` (`r = -0.88`), pre-sorting educational inequality before age three.
4. **Pedagogical Segregation & Workforce Precariato (*Giungla del Precariato*):** Secondary schools suffer from rigid age-14 tracking (*Licei* vs *Tecnici* vs *Professionali*) coupled with massive teaching instability: `18.5%` of classroom chairs and **over 60% of special needs (*Sostegno*) chairs** are filled by temporary annual substitutes (`Supplenti`), destroying pedagogical continuity for vulnerable students.
5. **Higher Education Bottleneck & Brain Drain (*Fuga dei Cervelli*):** Chronic university underfunding (`MUR`) and rigid academic recruitment structures drive over **40,000+ young graduates to emigrate abroad annually** because domestic micro-enterprises cannot offer competitive R&D wages or meritocratic ladders.
6. **Labor Market Trap & Real Wage Stagnation (*Lavoro Povero*):** Italy holds the highest youth NEET rate (`16.1%`) in the EU-27 and is the only OECD economy where real wages declined between 1990 and 2024, locking youth into precarious, low-wage dependency well into adulthood.
7. **The Open Science Imperative:** Because *Italienation* is a complex web of interlocking historical and economic feedback loops, no single dogma can resolve it. It demands an **Open Science Collaborative Observatory** where global researchers and citizens can freely interrogate raw data, test hypotheses, and debate structural solutions.

---

## 📂 Repository Structure & Access

```
holistic_analysis/
│
├── 📖 README.md                             <-- Open Science Guide & Definitional Framework
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
│   ├── index.html (THE SOLE HTML FILE: 7-dimension definition, live tables, reflection prompts, & diagnostics)
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
- **📖 Extensive Definition & Theoretical Anatomy:** Explores the 7 core pillars of *Italienation* (`Etymology`, `Demographic Winter`, `Urban Penalty`, `Precariato`, `Brain Drain`, `Wage Stagnation`, `Open Science`).
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
