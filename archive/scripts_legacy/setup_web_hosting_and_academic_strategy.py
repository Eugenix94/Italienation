#!/usr/bin/env python3
"""
setup_web_hosting_and_academic_strategy.py

1. Sets up instant, zero-config web hosting compatibility for both GitHub Pages (`/index.html` + `.nojekyll`)
   and Netlify (`netlify.toml`).
2. Creates the comprehensive `ACADEMIC_AND_GRANT_STRATEGY.md` strategic guide for PNRR/Horizon Europe grant
   acquisition and high-impact peer-reviewed publication pathways.
"""

import os
import shutil

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

print(f"[{ROOT_DIR}] Configuring Web Hosting compatibility (GitHub Pages & Netlify)...")

# 1. Create root index.html that seamlessly loads the Open Science Observatory
root_index_path = os.path.join(ROOT_DIR, "index.html")
# We copy the unified index.html from holistic_analysis/interactive_web_experience/index.html to the root,
# updating relative paths so that whether served from root or from folder, all images/data load perfectly.
src_web_index = os.path.join(ROOT_DIR, "holistic_analysis", "interactive_web_experience", "index.html")
src_web_img = os.path.join(ROOT_DIR, "holistic_analysis", "interactive_web_experience", "universal_synthesis_master_dashboard.png")

if os.path.exists(src_web_index):
    with open(src_web_index, "r", encoding="utf-8") as f_in:
        html_content = f_in.read()
    
    # Adjust relative paths when served from root
    html_content_root = html_content.replace('src="universal_synthesis_master_dashboard.png"', 'src="holistic_analysis/interactive_web_experience/universal_synthesis_master_dashboard.png"')
    html_content_root = html_content_root.replace('<code>../data_panels/</code>', '<code>holistic_analysis/data_panels/</code>')
    html_content_root = html_content_root.replace('<code>../jupyter_notebook/italienation_holistic_master_analysis.ipynb</code>', '<code>holistic_analysis/jupyter_notebook/italienation_holistic_master_analysis.ipynb</code>')
    
    with open(root_index_path, "w", encoding="utf-8") as f_out:
        f_out.write(html_content_root)
    print(f"[SUCCESS] Created root index.html for instant GitHub Pages / Netlify deployment: {root_index_path}")

# 2. Create .nojekyll for GitHub Pages (ensures folders/files starting with underscores or special names aren't ignored)
nojekyll_path = os.path.join(ROOT_DIR, ".nojekyll")
with open(nojekyll_path, "w", encoding="utf-8") as f_noj:
    f_noj.write("# Prevents GitHub Pages from running Jekyll processing, allowing direct HTML/JS/CSS hosting\n")
print("[SUCCESS] Created .nojekyll")

# 3. Create netlify.toml for Netlify configuration
netlify_path = os.path.join(ROOT_DIR, "netlify.toml")
netlify_content = """[build]
  publish = "."
  command = "echo 'Deploying static Open Science Observatory'"

[[headers]]
  for = "/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    X-Frame-Options = "DENY"
    X-XSS-Protection = "1; mode=block"

[[redirects]]
  from = "/data/*"
  to = "/holistic_analysis/data_panels/:splat"
  status = 200
"""
with open(netlify_path, "w", encoding="utf-8") as f_net:
    f_net.write(netlify_content)
print("[SUCCESS] Created netlify.toml")

# 4. Create ACADEMIC_AND_GRANT_STRATEGY.md
strategy_path = os.path.join(ROOT_DIR, "ACADEMIC_AND_GRANT_STRATEGY.md")
strategy_content = """# 🎓 Academic Efficiency & Grant Strategy Guide (`ACADEMIC_AND_GRANT_STRATEGY.md`)

This strategic roadmap outlines the exact pathways to maximize the academic impact, scientific efficiency, peer-reviewed publication success, and grant acquisition potential (*PNRR Missione 4* & *Horizon Europe Cluster 2*) of the **Italienation Open Science Observatory**.

---

## 🏛️ 1. Grant Acquisition Strategy (`PNRR & Horizon Europe`)

Our multi-scale data synthesis across 11 domains directly targets two major international funding streams. By structuring our data panels (`holistic_analysis/data_panels/`) and interactive visual engine as open-source deliverables, we fulfill the strict **Open Science & FAIR Data (Findable, Accessible, Interoperable, Reusable)** mandates required by EU grant evaluators.

### A. Horizon Europe: Cluster 2 (`Culture, Creativity and Inclusive Society`)
* **Target Destinations:**
  * `HORIZON-CL2-2026-TRANSFORMATIONS`: *Socio-economic transformations, reducing inequalities, and fostering territorial cohesion.*
  * `HORIZON-CL2-2026-DEMOCRACY`: *Strengthening democratic participation and institutional trust among youth cohorts.*
* **Our Competitive Advantage & Pitch:**
  Traditional socio-economic proposals rely on static, historical survey data. *Italienation* offers a **live, multi-scale, reproducible computational pipeline** that bridges macro-fiscal expenditure curves (`1913–2026`) directly to municipal nursery seat coverage across 10 metropolitan capitals (`r = -0.88`). We can propose expanding our open data architecture into a pan-European comparative observatory (*Euro-Alienation*) across Mediterranean economies (Spain, Greece, Portugal, Italy).
* **Recommended Funding Request:** `€2.5M – €4.0M` Research and Innovation Action (RIA) consortium.

### B. PNRR Missione 4 (`Istruzione e Ricerca`) & Missione 5 (`Inclusione e Coesione`)
* **Target Pillars:**
  * **Missione 4, Componente 1:** *Potenziamento dell’offerta dei servizi di istruzione: dagli asili nido alle università.*
  * **Missione 5, Componente 1:** *Politiche per il lavoro e contrasto alle povertà educative territoriali.*
* **Our Competitive Advantage & Pitch:**
  The Italian government faces strict monitoring deadlines to verify the impact of its `€4.6 billion` PNRR allocation for *Asili Nido* and schools. Our repository already provides the exact baseline counterfactual diagnostic: the negative correlation between nursery seat coverage and youth NEET rates (`r = -0.88`) and the tracking of teacher *precariato* (`815,482 posts`). We can partner with regional research centers or university departments to act as an independent open data evaluation monitor.

---

## 📝 2. Peer-Reviewed Publication Pathways

By separating our empirical contributions into modular components, we can generate a high-impact multi-paper publication cluster rather than a single monograph:

### Paper 1: The Data Descriptors & FAIR Repository
* **Target Journal:** *Scientific Data (Nature Portfolio)* or *Journal of Open Humanities and Data*.
* **Title:** *"Italienation: A Multi-Scale Open Data Panel on Public Education Expenditure, Municipal Infrastructure, and Youth Transitions in Italy (1913–2026)"*.
* **Core Contribution:** Formalizing and peer-reviewing our 13 curated CSV panels (`holistic_analysis/data_panels/`), documenting schema mappings, and validating data integrity across ISTAT, MUR, Openpolis, and Eurostat sources.

### Paper 2: The Empirical & Territorial Analysis
* **Target Journal:** *Journal of European Social Policy*, *Socio-Economic Review*, or *Social Indicators Research*.
* **Title:** *"The Early Childhood Urban Penalty: Municipal Infrastructure Deficits and Youth NEET Equilibria across Italian Metropolitan Capitals"*.
* **Core Contribution:** Demonstrating the empirical paradox of early childhood care infrastructure (`r = -0.88` metropolitan correlation) and the structural transition jump trap from 9th-grade evaluation severity (`bocciature`) to high school dropout.

### Paper 3: The Educational Labor Market & Faculty Sorting
* **Target Journal:** *Higher Education*, *Studies in Higher Education*, or *European Journal of Education*.
* **Title:** *"The Dual Precariato: Classroom Teaching Instability and Faculty Gender Pyramid Inversion in Italian Higher Education"*.
* **Core Contribution:** Analyzing our `815,482` teaching posts dataset alongside MUR academic staffing series (`FoRD 02 Engineering: 70% male dominance`), diagnosing the institutional roots of the brain drain (*Fuga dei Cervelli*).

---

## ⚡ 3. Academic Efficiency & Computational Workflow Best Practices

To maintain peak scientific efficiency as the open-source community contributes to the repository, we recommend adopting the following four standards:

1. **Automated Continuous Integration (CI/CD Data Validation):**
   * Implement GitHub Actions workflows that automatically execute `jupyter_notebook/italienation_holistic_master_analysis.ipynb` via `nbclient` on every Pull Request. If a community contributor submits new provincial data, the CI pipeline verifies that all regression models converge cleanly before merging.
2. **DOI Assignment via Zenodo:**
   * Connect our GitHub repository (`Eugenix94/Italienation`) directly to **Zenodo**. Whenever we publish a GitHub Release (e.g., `v1.0.0-capstone`), Zenodo automatically generates a permanent **Digital Object Identifier (DOI)**. This allows academic researchers globally to formally cite our exact data panels in their peer-reviewed papers.
3. **Reproducible Environment Lock (`uv.lock` & `pyproject.toml`):**
   * Maintain strict dependency pins across `pandas`, `numpy`, `nbclient`, and `matplotlib` so that our regressions yield identical coefficients whether run on a Windows workstation in Rome or a high-performance cluster in Brussels.
4. **Community Contribution Governance (`CONTRIBUTING.md`):**
   * Establish clear guidelines for local citizen scientists submitting provincial case studies, ensuring all territorial datasets include clear `ESCS` context indices and official ISTAT municipal codes (`Codice ISTAT Comune`).

---
*Prepared by the Italienation Open Science Collaborative to bridge open computational data with global academic impact.*
"""

with open(strategy_path, "w", encoding="utf-8") as f_st:
    f_st.write(strategy_content)

print(f"[SUCCESS] Created comprehensive ACADEMIC_AND_GRANT_STRATEGY.md in {ROOT_DIR}")
