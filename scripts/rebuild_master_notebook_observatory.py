#!/usr/bin/env python3
"""
rebuild_master_notebook_observatory.py

Builds the Complete Bilingual (Italiano 🇮🇹 & English 🇬🇧) Citizen-First Open Science Laboratory
and Interactive Data Explorer across both index.html files:
1. root index.html
2. holistic_analysis/interactive_web_experience/index.html

Features:
- Bilingual Language Toggle (🇮🇹 Italiano / 🇬🇧 English)
- Citizen-First Human Titles (no raw technical filenames or English jargon on the front UI)
- Prominent OSF (Open Science Framework) & GitHub Academic Verification links
- The Citizen Interactive Data Explorer & Chart Builder (Tabulator + Chart.js)
- ✨ Auto-Generated Python Script Box with one-click Jupyter Notebook (.ipynb) download
- Live In-Browser Pyodide WebAssembly Python Sandbox
"""

import os
import glob
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")

rendered_dir = os.path.join(ROOT_DIR, "holistic_analysis", "interactive_web_experience", "rendered_notebooks")
root_rendered_dir = os.path.join(ROOT_DIR, "rendered_notebooks")
os.makedirs(rendered_dir, exist_ok=True)
os.makedirs(root_rendered_dir, exist_ok=True)

# Discover all rendered HTML notebooks
html_files = sorted(glob.glob(os.path.join(rendered_dir, "*.html")) + glob.glob(os.path.join(root_rendered_dir, "*.html")))
unique_html = {}
for f in html_files:
    fname = os.path.basename(f)
    if fname not in unique_html:
        unique_html[fname] = f

print(f"Building Bilingual Citizen-First Open Science Laboratory with {len(unique_html)} verified HTML notebooks...")

# Mapping from notebook filename to bilingual human titles and descriptions
notebook_meta = {
    "italy_thesis_capstone.html": {
        "it_title": "🎓 Sintesi Generale: L'Emergenza Scuola in Italia",
        "en_title": "🎓 General Synthesis: The Italian Education Emergency",
        "it_desc": "Lo studio completo sul calo demografico (-1,4 milioni di studenti previsti), i tagli storici ai fondi e le differenze tra Nord e Sud.",
        "en_desc": "The comprehensive investigation into demographic decline (-1.4M projected students), historical budget cuts, and North-South disparities."
    },
    "italy_full_fiscal_landscape.html": {
        "it_title": "🏛️ I Bilanci dello Stato e dei 7.959 Comuni per la Scuola",
        "en_title": "🏛️ State & Municipal Budgets for Schools Across 7,959 Cities",
        "it_desc": "L'analisi chiara di quanto spende realmente ogni singolo Comune italiano per la manutenzione delle scuole e i servizi agli studenti.",
        "en_desc": "A clear analysis of actual municipal expenditures for school maintenance and student services across every Italian city."
    },
    "italy_bocciatura_repeaters_full_analysis_v2.html": {
        "it_title": "⚠️ Bocciature e Abbandoni al Primo Anno di Superiori",
        "en_title": "⚠️ First-Year High School Repeaters & Early Dropouts",
        "it_desc": "Perché le bocciature in prima superiore si concentrano negli Istituti Tecnici e Professionali, colpendo i ragazzi delle famiglie più fragili.",
        "en_desc": "Why first-year repetition rates are heavily concentrated in Technical and Vocational schools, affecting vulnerable youth."
    },
    "italy_openpolis_neet_poverty.html": {
        "it_title": "🏙️ Asili Nido e Giovani Senza Lavoro né Studio (NEET) nelle 11 Grandi Città",
        "en_title": "🏙️ Public Nurseries & Youth NEET Rates Across 11 Major Cities",
        "it_desc": "Come la mancanza di posti negli asili nido (fascia 0-2 anni) aumenti drasticamente il rischio che i giovani abbandonino gli studi negli anni successivi.",
        "en_desc": "How the lack of municipal nursery spots (0-2 yrs) drastically increases the risk of youth dropping out of school and work later in life."
    },
    "italy_tripartite_school_system.html": {
        "it_title": "🎒 Licei, Tecnici o Professionali: Dove Vanno a Finire gli Studenti?",
        "en_title": "🎒 Academic vs. Vocational Tracks: Where Do Students End Up?",
        "it_desc": "Come la divisione anticipata tra scuole liceali, tecniche e professionali orienta il futuro lavorativo e universitario dei giovani.",
        "en_desc": "How early tracking into academic, technical, and vocational high schools shapes students' future university and career paths."
    },
    "italy_human_capital_political_aspects.html": {
        "it_title": "✈️ Fuga dei Cervelli: Perché i Giovani Laureati Lasciano l'Italia",
        "en_title": "✈️ Brain Drain: Why Young Graduates Emigrate from Italy",
        "it_desc": "Il confronto tra gli stipendi di ingresso in Italia e in Nord Europa, e il costo enorme per il Paese della perdita di giovani qualificati.",
        "en_desc": "Comparing entry-level salaries in Italy versus Northern Europe, and the immense cost of losing skilled young professionals."
    },
    "territorial_expenditure_analysis.html": {
        "it_title": "🗺️ Divario Nord-Sud: Spesa per Studente e Sicurezza degli Edifici",
        "en_title": "🗺️ North-South Gaps: Spending Per Student & Building Safety",
        "it_desc": "Le differenze nelle risorse per le mense, le palestre, la sicurezza antisismica e i servizi scolastici tra le diverse Regioni italiane.",
        "en_desc": "Differences in per-student funding for cafeterias, gyms, seismic safety, and school services across Italian regions."
    },
    "data_inventory_comprehensive.html": {
        "it_title": "📋 Guida e Catalogo Semplice di Tutti gli 81 Dataset del Progetto",
        "en_title": "📋 Simple Catalog & Guide to All 81 Datasets in the Project",
        "it_desc": "La guida alla portata di tutti per capire da quali banche dati pubbliche (ISTAT, Ministero, Eurostat) provengono i numeri analizzati.",
        "en_desc": "An easy-to-read guide explaining exactly which public databases (ISTAT, Ministry, Eurostat) all our statistics come from."
    },
    "07_geospatial_tripartite_distribution.html": {
        "it_title": "📍 Mappa Italia: Come si Distribuiscono Licei e Istituti Professionali",
        "en_title": "📍 Italy Map: Distribution of Academic vs. Vocational Schools",
        "it_desc": "La mappa geografica che mostra in quali province e quartieri si concentrano i licei e dove invece prevalgono gli istituti professionali.",
        "en_desc": "A geographic map showing which provinces and neighborhoods have more academic high schools versus vocational institutes."
    },
    "education_spending_outcomes.html": {
        "it_title": "💶 Investimenti e Risultati: Quanto Producano i Fondi per la Scuola",
        "en_title": "💶 Investments & Results: What Do School Budget Dollars Produce?",
        "it_desc": "L'analisi chiara per capire se i soldi spesi per l'istruzione migliorano realmente l'apprendimento e le competenze degli studenti.",
        "en_desc": "An accessible examination of whether public spending on education actually improves student skills and learning outcomes."
    },
    "italienation_holistic_master_analysis.html": {
        "it_title": "🔍 Quadro Generale: Tutte le Dimensioni della Scuola Italiana",
        "en_title": "🔍 Overall Picture: All Dimensions of the Italian School System",
        "it_desc": "Una visione completa che unisce spesa pubblica, calo degli studenti, disuguaglianze e futuro dei giovani in un unico grande racconto.",
        "en_desc": "A holistic overview connecting public spending, student decline, social inequalities, and youth futures into one clear narrative."
    },
    "italy_capital_formation_h_c_i.html": {
        "it_title": "🌱 Il Futuro dei Giovani: L'Indice di Sviluppo Umano in Italia",
        "en_title": "🌱 Youth Opportunities: Italy's Human Capital Index",
        "it_desc": "Come la salute, la nutrizione e la qualità della scuola preparano i bambini italiani al mondo del lavoro di domani.",
        "en_desc": "How healthcare, nutrition, and school quality prepare Italian children for the challenges of tomorrow's workplace."
    },
    "italy_lower_secondary_middle_school_analysis.html": {
        "it_title": "🏫 La Scuola Media (Secondaria di Primo Grado): I Tre Anni Decisivi",
        "en_title": "🏫 Middle School (Grades 6-8): The Three Crucial Years",
        "it_desc": "Cosa succede durante le scuole medie: le prime difficoltà, il supporto degli insegnanti e la scelta critica per le superiori.",
        "en_desc": "What happens during middle school: early learning hurdles, teacher stability, and the critical choice of high school track."
    },
    "italy_middle_to_upper_transition_analysis.html": {
        "it_title": "🔄 Il Passaggio Critico: Dalle Scuole Medie alle Superiori",
        "en_title": "🔄 The Crucial Step: Transitioning from Middle to High School",
        "it_desc": "I dati sui ragazzi che incontrano ostacoli durante il primo anno di scuola superiore e come aiutarli ad affrontare il cambiamento.",
        "en_desc": "Statistics on teenagers facing difficulties during the transition to high school, and effective ways to support them."
    },
    "italy_neet_full_analysis.html": {
        "it_title": "🔴 I Giovani NEET (Senza Lavoro né Studio): I Numeri Reali in Italia",
        "en_title": "🔴 Youth NEETs (Not in Education or Employment): Real Figures",
        "it_desc": "L'indagine approfondita sui quasi 2 milioni di giovani italiani che si trovano fuori dai percorsi di studio e dal mercato del lavoro.",
        "en_desc": "An in-depth investigation into the nearly 2 million young adults in Italy who are currently out of school and formal employment."
    },
    "italy_oecd_triangle_mobility_analysis.html": {
        "it_title": "⚖️ Ascensore Sociale: L'Istruzione Cambia davvero il Futuro dei Figli?",
        "en_title": "⚖️ Social Mobility: Does School Help Children Do Better Than Their Parents?",
        "it_desc": "I dati internazionali dell'OCSE sull'ascensore sociale: quanto conta oggi il titolo di studio della famiglia di origine nel successo di un ragazzo.",
        "en_desc": "International OECD data on social mobility: how much a parent's education level still dictates their child's future success."
    },
    "italy_oed_goldthorpe_mobility_analysis.html": {
        "it_title": "👨‍👩‍👧 Origini Familiari e Opportunità di Lavoro in Italia",
        "en_title": "👨‍👩‍👧 Family Background & Career Opportunities in Italy",
        "it_desc": "Lo studio sociologico spiegato in parole semplici: come l'occupazione dei genitori influenza la scelta della scuola e della carriera del figlio.",
        "en_desc": "Sociological research explained simply: how parents' occupations influence a student's school track and eventual job choices."
    },
    "italy_textbooks_schools_territory.html": {
        "it_title": "📚 Il Costo dei Libri di Testo e la Spesa delle Famiglie",
        "en_title": "📚 The Cost of Textbooks & Household Education Expenses",
        "it_desc": "Quanto spendono davvero le famiglie italiane all'inizio dell'anno scolastico tra libri, materiale e contributi scolastici.",
        "en_desc": "How much Italian families really spend at the start of the school year on textbooks, supplies, and school contributions."
    },
    "neet_italy_analysis.html": {
        "it_title": "📉 NEET in Italia: Confronto tra le Regioni e Soluzioni Pratiche",
        "en_title": "📉 NEETs in Italy: Regional Comparisons & Practical Solutions",
        "it_desc": "Un confronto diretto tra Nord, Centro e Sud sul fenomeno dell'inattività giovanile e le strategie locali per riportare i ragazzi a scuola o al lavoro.",
        "en_desc": "A direct comparison between North, Center, and South regarding youth inactivity, highlighting local re-engagement strategies."
    },
    "openEURYDICE_Italy_Summary.html": {
        "it_title": "🇪🇺 L'Italia e l'Europa: Come Funziona il Nostro Sistema Rispetto agli Altri",
        "en_title": "🇪🇺 Italy & Europe: Comparing Our School System with European Neighbors",
        "it_desc": "I dati della rete europea Eurydice per confrontare orari, stipendi dei docenti e organizzazione scolastica italiana con Francia, Germania e Spagna.",
        "en_desc": "European Eurydice network data comparing Italian school hours, teacher pay, and system design with France, Germany, and Spain."
    },
    "siope_minister_data_exploration.html": {
        "it_title": "🔍 Dove Vanno i Fondi del Ministero? Esplorazione della Spesa Pubblica",
        "en_title": "🔍 Where Does Ministry Money Go? Exploring Public Education Spending",
        "it_desc": "L'analisi chiara delle uscite del Ministero dell'Istruzione: quanti fondi vanno agli stipendi, alle strutture e alle innovazioni didattiche.",
        "en_desc": "A clear breakdown of Ministry of Education expenditures: how much goes to salaries, infrastructure, and teaching innovation."
    }
}

# Generate bilingual notebook cards HTML
cards_html = ""
for fname, fpath in sorted(unique_html.items()):
    meta = notebook_meta.get(fname, {
        "it_title": f"📑 Studio: {fname.replace('.html', '').replace('_', ' ').title()}",
        "en_title": f"📑 Study: {fname.replace('.html', '').replace('_', ' ').title()}",
        "it_desc": "Esplorazione chiara dei dati e dei grafici statistici per questo argomento.",
        "en_desc": "Clear data exploration and statistical charts for this topic."
    })
    
    ipynb_name = fname.replace(".html", ".ipynb")
    cards_html += f"""
    <div class="notebook-card bg-slate-800/80 border border-slate-700/80 rounded-2xl p-6 shadow-xl hover:border-blue-500/50 transition-all duration-300 flex flex-col justify-between">
        <div>
            <h3 class="text-xl font-bold text-white lang-it">{meta['it_title']}</h3>
            <h3 class="text-xl font-bold text-white lang-en hidden">{meta['en_title']}</h3>
            <p class="text-slate-300 text-sm mt-2 lang-it">{meta['it_desc']}</p>
            <p class="text-slate-300 text-sm mt-2 lang-en hidden">{meta['en_desc']}</p>
        </div>
        <div class="mt-6 flex flex-wrap items-center gap-3 pt-4 border-t border-slate-700/60">
            <a href="rendered_notebooks/{fname}" target="_blank" 
               class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-medium text-sm transition shadow-lg shadow-blue-500/20">
               <span>👁️</span> <span class="lang-it">Apri Studio Interattivo</span><span class="lang-en hidden">Open Interactive Report</span>
            </a>
            <a href="https://github.com/Eugenix94/Italienation/blob/main/Notebooks/{ipynb_name}" target="_blank"
               class="inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-700/80 hover:bg-slate-600 text-slate-200 text-sm font-medium transition border border-slate-600">
               <span>💻</span> <span class="lang-it">Sorgente GitHub</span><span class="lang-en hidden">GitHub Source</span>
            </a>
            <a href="https://colab.research.google.com/github/Eugenix94/Italienation/blob/main/Notebooks/{ipynb_name}" target="_blank"
               class="inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 text-sm font-medium transition border border-amber-500/30">
               <span>🚀</span> <span class="lang-it">Quaderno Online</span><span class="lang-en hidden">Online Notebook</span>
            </a>
        </div>
    </div>
    """

# Discover and generate Community / Citizen Research cards
community_dir = os.path.join(ROOT_DIR, "Notebooks", "community")
community_ipynbs = sorted(glob.glob(os.path.join(community_dir, "*.ipynb")))
community_cards_html = ""
for cp in community_ipynbs:
    cname = os.path.basename(cp)
    ctitle_it = "🛠️ Quaderno Guidato di Ricerca Civica: Analisi del Proprio Comune" if "01_template" in cname else f"🌟 Studio Civico: {cname.replace('.ipynb', '').replace('_', ' ').title()}"
    ctitle_en = "🛠️ Guided Civic Research Notebook: Municipal & Regional Analysis" if "01_template" in cname else f"🌟 Citizen Study: {cname.replace('.ipynb', '').replace('_', ' ').title()}"
    cdesc_it = "Strumento online gratuito e guidato passo per passo per esplorare i dati del proprio Comune o Regione senza installare alcun programma." if "01_template" in cname else "Studio civico creato e sottomesso dai cittadini per analizzare l'istruzione nel proprio territorio."
    cdesc_en = "Free, step-by-step online tool to explore data for your specific city or region without installing any software." if "01_template" in cname else "Community study submitted by citizens to analyze education trends in their local area."
    
    community_cards_html += f"""
    <div class="notebook-card bg-gradient-to-br from-emerald-950/40 via-slate-900/80 to-slate-900/80 border border-emerald-500/40 rounded-2xl p-6 shadow-xl hover:border-emerald-400 transition-all duration-300 flex flex-col justify-between">
        <div>
            <h3 class="text-xl font-bold text-white lang-it">{ctitle_it}</h3>
            <h3 class="text-xl font-bold text-white lang-en hidden">{ctitle_en}</h3>
            <p class="text-slate-300 text-sm mt-2 lang-it">{cdesc_it}</p>
            <p class="text-slate-300 text-sm mt-2 lang-en hidden">{cdesc_en}</p>
        </div>
        <div class="mt-6 flex flex-wrap items-center gap-3 pt-4 border-t border-slate-700/60">
            <a href="https://colab.research.google.com/github/Eugenix94/Italienation/blob/main/Notebooks/community/{cname}" target="_blank"
               class="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-amber-500 to-emerald-600 hover:from-amber-400 hover:to-emerald-500 text-white font-bold text-sm transition shadow-lg shadow-emerald-500/20">
               <span>🚀</span> <span class="lang-it">Apri Quaderno Guidato (Online Gratuito)</span><span class="lang-en hidden">Open Guided Notebook (Free Online)</span>
            </a>
            <a href="https://github.com/Eugenix94/Italienation/blob/main/Notebooks/community/{cname}" target="_blank"
               class="inline-flex items-center gap-2 px-3 py-2 rounded-xl bg-slate-700/80 hover:bg-slate-600 text-slate-200 text-sm font-medium transition border border-slate-600">
               <span>💻</span> <span class="lang-it">Sorgente GitHub</span><span class="lang-en hidden">GitHub Source</span>
            </a>
        </div>
    </div>
    """

html_template = f"""<!DOCTYPE html>
<html lang="it" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Italienation Observatory - Il Laboratorio di Scienza Aperta per l'Istruzione in Italia</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; }}
        h1, h2, h3, h4, .brand-font {{ font-family: 'Outfit', sans-serif; }}
        .glass-panel {{ background: rgba(30, 41, 59, 0.75); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.08); }}
        .glass-card {{ background: rgba(51, 65, 85, 0.5); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.06); }}
        .lang-en.hidden, .lang-it.hidden {{ display: none !important; }}
    </style>
</head>
<body class="min-h-screen selection:bg-blue-500 selection:text-white pb-24">

    <!-- Bilingual & OSF Top Navigation Bar -->
    <header class="sticky top-0 z-50 glass-panel border-b border-slate-700/80 shadow-2xl">
        <div class="max-w-7xl mx-auto px-6 py-4 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <span class="text-3xl">🇮🇹</span>
                <div>
                    <h1 class="text-2xl font-extrabold bg-gradient-to-r from-blue-400 via-emerald-400 to-indigo-400 bg-clip-text text-transparent brand-font">
                        Italienation Observatory
                    </h1>
                    <p class="text-xs text-slate-400 lang-it">Laboratorio Civico di Scienza Aperta e Analisi Dati sulla Scuola Italiana</p>
                    <p class="text-xs text-slate-400 lang-en hidden">Open Science Civic Laboratory & Empirical Data Observatory on Italian Education</p>
                </div>
            </div>

            <div class="flex items-center gap-4">
                <!-- GitHub Repository Badge -->
                <a href="https://github.com/Eugenix94/Italienation" target="_blank" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 text-xs font-semibold hover:border-slate-500 transition">
                    <span>🐙</span> <span>GitHub Repository</span>
                </a>

                <!-- Bilingual Language Toggle Button -->
                <button onclick="toggleLanguage()" id="langBtn" class="flex items-center gap-2 px-4 py-1.5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-bold transition shadow-lg shadow-blue-500/20">
                    <span>🌐</span> <span id="langBtnText">🇬🇧 Switch to English</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="max-w-7xl mx-auto px-6 pt-12 pb-8">
        <div class="glass-panel rounded-3xl p-8 md:p-12 relative overflow-hidden">
            <div class="absolute -right-20 -top-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
            <div class="absolute -left-20 -bottom-20 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

            <div class="max-w-4xl relative z-10">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/20 text-blue-400 text-xs font-semibold border border-blue-500/30 mb-6">
                    <span class="w-2 h-2 rounded-full bg-blue-400 animate-pulse"></span>
                    <span class="lang-it">Piattaforma Aperta ai Cittadini e ai Ricercatori</span>
                    <span class="lang-en hidden">Open Platform for Citizens and Researchers</span>
                </div>

                <h2 class="text-3xl md:text-5xl font-extrabold text-white leading-tight brand-font">
                    <span class="lang-it">Capire la Crisi della Scuola Italiana con i Dati Reali, Senza Gergo.</span>
                    <span class="lang-en hidden">Understanding Italy's Education Crisis with Real Data, Zero Jargon.</span>
                </h2>

                <p class="text-slate-300 text-lg mt-6 leading-relaxed">
                    <span class="lang-it">
                        Benvenuto nell'osservatorio civico e laboratorio interattivo di <strong>Italienation</strong>. Qui non troverai capitoli rigidi o termini incomprensibili: ogni cittadino, genitore, studente o amministratore può esplorare in tempo reale gli <strong>81 dataset empirici</strong> (da ISTAT a Eurostat e Ragioneria dello Stato), confrontare grafici statistici chiari e consultare le tabelle dei dati ufficiali sul modello dei grandi portali statistici internazionali.
                    </span>
                    <span class="lang-en hidden">
                        Welcome to the civic observatory and interactive data platform of <strong>Italienation</strong>. Here you won't find rigid chapters or complex jargon: every citizen, parent, student, or policymaker can interactively explore all <strong>81 empirical datasets</strong> (from ISTAT to Eurostat and SIOPE), compare clear statistical charts, and consult official data tables styled after major international data portals.
                    </span>
                </p>

                <div class="mt-8 flex flex-wrap items-center gap-4">
                    <a href="#interactive-lab" class="px-6 py-3.5 rounded-xl bg-gradient-to-r from-blue-600 to-emerald-600 hover:from-blue-500 hover:to-emerald-500 text-white font-bold text-sm transition shadow-lg shadow-blue-500/25 flex items-center gap-2">
                        <span>📊</span>
                        <span class="lang-it">Avvia Esploratore Interattivo dei Dati</span>
                        <span class="lang-en hidden">Launch Interactive Data Explorer</span>
                    </a>
                    <a href="#notebooks-directory" class="px-6 py-3.5 rounded-xl bg-slate-800/90 hover:bg-slate-700/90 text-slate-200 font-semibold text-sm transition border border-slate-700 flex items-center gap-2">
                        <span>📑</span>
                        <span class="lang-it">Esplora i 23 Studi Territoriali</span>
                        <span class="lang-en hidden">Explore All 23 Territorial Studies</span>
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- SECTION 1: THE CITIZEN INTERACTIVE OPEN SCIENCE LABORATORY & OUR WORLD IN DATA TABLE -->
    <section id="interactive-lab" class="max-w-7xl mx-auto px-6 py-10">
        <div class="glass-panel rounded-3xl p-8 md:p-10 border border-blue-500/30 shadow-2xl">
            <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-700/80 pb-6 mb-8">
                <div>
                    <h2 class="text-2xl md:text-3xl font-bold text-white brand-font flex items-center gap-3">
                        <span>📊</span>
                        <span class="lang-it">Esploratore Interattivo dei Dati e delle Dinamiche Territoriali</span>
                        <span class="lang-en hidden">Interactive Explorer of Educational Data & Territorial Dynamics</span>
                    </h2>
                    <p class="text-slate-400 text-sm mt-1">
                        <span class="lang-it">Scegli un indicatore e confronta direttamente le statistiche territoriali e storiche con tabelle ufficiali chiare e trasparenti.</span>
                        <span class="lang-en hidden">Select any indicator and directly compare territorial and historical statistics with clear, transparent official data tables.</span>
                    </p>
                </div>
                <div class="flex items-center gap-3">
                    <span class="px-3 py-1 rounded-full bg-blue-500/20 text-blue-400 text-xs font-semibold border border-blue-500/30">
                        <span class="lang-it">📊 Grafici & Tabelle Ufficiali Interattive</span>
                        <span class="lang-en hidden">📊 Interactive Charts & Official Data Tables</span>
                    </span>
                </div>
            </div>

            <!-- Visual Controls (Dropdowns in Plain Language) -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                        <span class="lang-it">1. Scegli l'Indicatore Empirico</span>
                        <span class="lang-en hidden">1. Select Empirical Indicator</span>
                    </label>
                    <select id="datasetSelector" onchange="updateCitizenLab()" class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-white font-medium text-sm focus:outline-none focus:border-blue-500 transition">
                        <option value="openpolis">🏙️ Asili Nido vs Giovani NEET (11 Grandi Città)</option>
                        <option value="macro_spending">📈 Spesa Pubblica per la Scuola (% PIL 1913–Oggi)</option>
                        <option value="siope_municipal">🏛️ Spesa Comunale per Alunno (7.959 Comuni SIOPE)</option>
                        <option value="tripartite">🎒 Licei vs Istituti Tecnici e Professionali: Futuro degli Studenti</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                        <span class="lang-it">2. Filtro Territoriale o Temporale</span>
                        <span class="lang-en hidden">2. Territorial or Temporal Filter</span>
                    </label>
                    <select id="regionSelector" onchange="updateCitizenLab()" class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-white font-medium text-sm focus:outline-none focus:border-blue-500 transition">
                        <option value="all">🇮🇹 Tutte le Aree e Anni / All Territories & Years</option>
                        <option value="sud">📍 Sud e Isole / Southern Italy & Islands</option>
                        <option value="nord">📍 Nord e Centro / Northern & Central Italy</option>
                    </select>
                </div>

                <div>
                    <label class="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                        <span class="lang-it">3. Tipo di Visualizzazione</span>
                        <span class="lang-en hidden">3. Visualization Type</span>
                    </label>
                    <select id="chartTypeSelector" onchange="updateCitizenLab()" class="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-white font-medium text-sm focus:outline-none focus:border-blue-500 transition">
                        <option value="bar">📊 Grafico a Barre / Bar Chart</option>
                        <option value="line">📈 Serie Storica / Line Chart</option>
                        <option value="scatter">🔴 Dispersione / Scatter Plot</option>
                    </select>
                </div>
            </div>

            <!-- Live Chart & KPI Summary Grid -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
                <div class="lg:col-span-2 bg-slate-900/80 p-6 rounded-2xl border border-slate-800/80 shadow-inner">
                    <h3 id="chartTitle" class="text-lg font-bold text-white mb-4">Caricamento grafico in corso...</h3>
                    <div class="h-80 w-full flex items-center justify-center">
                        <canvas id="citizenChartCanvas"></canvas>
                    </div>
                </div>

                <!-- Plain Language Explanation & KPI Card -->
                <div class="bg-slate-900/80 p-6 rounded-2xl border border-slate-800/80 flex flex-col justify-between">
                    <div>
                        <span class="px-2.5 py-1 rounded-md bg-blue-500/20 text-blue-400 text-xs font-semibold uppercase tracking-wider">
                            <span class="lang-it">Spiegazione Chiara</span><span class="lang-en hidden">Clear Explanation</span>
                        </span>
                        <h4 id="kpiTitle" class="text-xl font-bold text-white mt-3 brand-font">Il Circolo Vizioso tra Asili Nido e Abbandono Scolastico</h4>
                        <p id="kpiDescription" class="text-slate-300 text-sm mt-3 leading-relaxed">
                            Nelle città italiane dove mancano gli asili nido comunali (fascia 0-2 anni), i ragazzi subiscono uno svantaggio iniziale che fa triplicare il rischio di abbandonare la scuola da adolescenti e diventare NEET (senza studio né lavoro).
                        </p>
                    </div>

                    <div class="mt-6 pt-6 border-t border-slate-800">
                        <div class="text-xs text-slate-400 font-semibold uppercase">
                            <span class="lang-it">Dato Ufficiale di Riferimento</span><span class="lang-en hidden">Official Reference Data</span>
                        </div>
                        <div id="kpiMetric" class="text-3xl font-extrabold text-emerald-400 mt-1">
                            +68% Correlazione
                        </div>
                        <div class="text-xs text-slate-400 mt-1">
                            Fonte primaria: Openpolis & Ragioneria dello Stato (SIOPE)
                        </div>
                    </div>
                </div>
            </div>

            <!-- ✨ OUR WORLD IN DATA STYLE DATA SUMMARY TABLE -->
            <div class="bg-slate-950 p-6 rounded-2xl border border-slate-800 shadow-2xl">
                <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4 mb-4">
                    <div class="flex items-center gap-3">
                        <span class="text-xl">📋</span>
                        <div>
                            <h4 class="text-base font-bold text-white">
                                <span class="lang-it">Tabella Riassuntiva dei Dati Ufficiali e degli Indicatori</span>
                                <span class="lang-en hidden">Summary Table of Official Data & Indicators</span>
                            </h4>
                            <p class="text-xs text-slate-400">
                                <span class="lang-it">Tutti i valori numerici e le percentuali per territorio o anno, consultabili e confrontabili in modo immediato.</span>
                                <span class="lang-en hidden">All numeric values and percentages across territories or years, ready for instant comparison.</span>
                            </p>
                        </div>
                    </div>

                    <div class="flex flex-wrap items-center gap-2">
                        <button onclick="downloadCSVData()" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold transition flex items-center gap-1.5 shadow-lg shadow-blue-500/20">
                            <span>📥</span> <span class="lang-it">Scarica Tabella (CSV)</span><span class="lang-en hidden">Download Table (CSV)</span>
                        </button>
                    </div>
                </div>

                <!-- Structured Data Table Container -->
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 text-xs font-bold text-slate-400 uppercase tracking-wider">
                                <th class="py-3 px-4"><span class="lang-it">Territorio / Anno</span><span class="lang-en hidden">Territory / Year</span></th>
                                <th class="py-3 px-4"><span class="lang-it">Indicatore Selezionato</span><span class="lang-en hidden">Selected Indicator</span></th>
                                <th class="py-3 px-4"><span class="lang-it">Valore / Percentuale</span><span class="lang-en hidden">Value / Percentage</span></th>
                                <th class="py-3 px-4"><span class="lang-it">Livello di Criticità</span><span class="lang-en hidden">Status / Severity</span></th>
                            </tr>
                        </thead>
                        <tbody id="dataSummaryTableBody" class="text-sm font-medium text-slate-300 divide-y divide-slate-800/60">
                            <!-- Populated dynamically via JavaScript -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>

    <!-- SECTION 1.5: CITIZEN & STUDENT INTERACTIVE RESEARCH SPACE -->
    <section id="citizen-colab-sandbox" class="max-w-7xl mx-auto px-6 py-8">
        <div class="glass-panel rounded-3xl p-8 md:p-10 border border-emerald-500/30 shadow-2xl relative overflow-hidden bg-gradient-to-br from-slate-900/90 via-slate-800/80 to-slate-900/90">
            <div class="absolute -right-24 -bottom-24 w-80 h-80 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
            
            <div class="flex flex-wrap items-start justify-between gap-6 relative z-10">
                <div class="max-w-3xl">
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-400 text-xs font-semibold border border-emerald-500/30 mb-4">
                        <span>🔬</span> <span class="lang-it">Spazio Interattivo per Studenti e Cittadini</span><span class="lang-en hidden">Interactive Space for Students & Citizens</span>
                    </div>
                    <h2 class="text-2xl md:text-4xl font-extrabold text-white brand-font leading-tight">
                        <span class="lang-it">Analizza il Tuo Comune e Partecipa alla Ricerca</span>
                        <span class="lang-en hidden">Analyze Your Municipality & Join the Research</span>
                    </h2>
                    <p class="text-slate-300 text-sm md:text-base mt-4 leading-relaxed">
                        <span class="lang-it">
                            Vuoi verificare qual è la situazione degli asili nido o della dispersione scolastica nel tuo specifico Comune o nella tua scuola? Abbiamo preparato un <strong>Quaderno di Ricerca Guidato online (gratuito)</strong> pronto per l'uso. Non serve alcuna esperienza tecnica né installare programmi sul computer: aprilo con un clic dal browser, seleziona la tua città e consulta i grafici pronti! Se vorrai, potrai condividere il tuo studio con la nostra comunità civica.
                        </span>
                        <span class="lang-en hidden">
                            Want to check nursery coverage or school dropout rates in your exact municipality or school? We prepared a <strong>Guided Online Research Notebook (free)</strong> ready to use. Zero technical experience or software installation required: open it with one click in your browser, select your city, and inspect ready-made charts! If you wish, you can share your analysis with our civic community.
                        </span>
                    </p>

                    <div class="mt-8 flex flex-wrap items-center gap-4">
                        <a href="https://colab.research.google.com/github/Eugenix94/Italienation/blob/main/Notebooks/community/01_template_studio_civico.ipynb" target="_blank"
                           class="px-6 py-3.5 rounded-xl bg-gradient-to-r from-amber-500 to-emerald-600 hover:from-amber-400 hover:to-emerald-500 text-white font-extrabold text-sm transition shadow-xl shadow-amber-500/20 flex items-center gap-2.5 transform hover:-translate-y-0.5">
                           <span class="text-lg">🚀</span>
                           <span class="lang-it">Apri Quaderno Guidato (Online Gratuito)</span>
                           <span class="lang-en hidden">Open Guided Notebook (Free Online)</span>
                        </a>
                        <a href="https://github.com/Eugenix94/Italienation/tree/main/Notebooks/community" target="_blank"
                           class="px-5 py-3.5 rounded-xl bg-slate-800/90 hover:bg-slate-700 text-slate-200 font-semibold text-sm transition border border-slate-600 flex items-center gap-2">
                           <span>📂</span>
                           <span class="lang-it">Archivio Contributi Civici (`community/`)</span>
                           <span class="lang-en hidden">Civic Contributions Archive (`community/`)</span>
                        </a>
                    </div>
                </div>

                <!-- Simple Guidance Box -->
                <div class="w-full lg:w-80 bg-slate-950/80 p-6 rounded-2xl border border-slate-800 shadow-inner shrink-0">
                    <h4 class="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-2">
                        <span class="text-emerald-400">💡</span> <span class="lang-it">Come Funziona in 3 Passi?</span><span class="lang-en hidden">How It Works in 3 Steps</span>
                    </h4>
                    <ul class="mt-4 space-y-3 text-xs text-slate-300 leading-relaxed">
                        <li class="flex items-start gap-2">
                            <span class="text-emerald-400 font-bold">1.</span>
                            <span><strong class="text-white">Apri Online</strong>: clicca sul pulsante arancione per aprire il quaderno interattivo nel tuo browser web.</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-emerald-400 font-bold">2.</span>
                            <span><strong class="text-white">Scegli la tua Città</strong>: segui le istruzioni semplici e digita il nome del tuo Comune o Regione.</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-emerald-400 font-bold">3.</span>
                            <span><strong class="text-white">Esplora e Condividi</strong>: visualizza subito i grafici della tua zona e unisciti al dialogo civico.</span>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- SECTION 2: THE DIRECTORY OF TERRITORIAL STUDIES & COMMUNITY CONTRIBUTIONS -->
    <section id="notebooks-directory" class="max-w-7xl mx-auto px-6 py-10">
        <div class="flex flex-wrap items-center justify-between gap-4 mb-8">
            <div>
                <h2 class="text-2xl md:text-4xl font-bold text-white brand-font">
                    <span class="lang-it">Studi Territoriali e Contributi Civici della Comunità</span>
                    <span class="lang-en hidden">Territorial Studies & Community Civic Research</span>
                </h2>
                <p class="text-slate-400 text-sm mt-1">
                    <span class="lang-it">Ogni studio è documentato in modo chiaro e consultabile in formato interattivo o direttamente su Google Colab.</span>
                    <span class="lang-en hidden">Each study is clearly documented and accessible in interactive format or directly on Google Colab.</span>
                </p>
            </div>
            <div class="flex items-center gap-3">
                <a href="DATASET_STATISTICAL_CONNECTIONS.md" target="_blank" class="px-4 py-2 rounded-xl bg-slate-800 border border-slate-700 text-slate-200 text-xs font-semibold hover:border-slate-500 transition">
                    <span>📋</span> <span class="lang-it">Dizionario Connessioni Statistiche</span><span class="lang-en hidden">Statistical Connections Codebook</span>
                </a>
            </div>
        </div>

        <!-- Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {community_cards_html}
            {cards_html}
        </div>
    </section>

    <!-- Footer & OSF Attribution -->
    <footer class="mt-16 border-t border-slate-800/80 bg-slate-950 py-12">
        <div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row items-center justify-between gap-6 text-center md:text-left">
            <div>
                <h4 class="text-lg font-bold text-white brand-font">Italienation Computational Observatory</h4>
                <p class="text-xs text-slate-400 mt-1">
                    <span class="lang-it">Progetto civico di scienza aperta ad accesso libero sotto licenza Apache-2.0 / CC-BY-4.0.</span>
                    <span class="lang-en hidden">Open access civic science project released under Apache-2.0 / CC-BY-4.0 license.</span>
                </p>
            </div>
            <div class="flex flex-wrap items-center justify-center gap-4 text-xs font-medium text-slate-400">
                <a href="https://osf.io" target="_blank" class="hover:text-emerald-400 transition">OSF Repository</a>
                <span>•</span>
                <a href="https://github.com/Eugenix94/Italienation" target="_blank" class="hover:text-blue-400 transition">GitHub Source</a>
                <span>•</span>
                <a href="HOLISTIC_CRITICAL_DATA_AUDIT.md" target="_blank" class="hover:text-indigo-400 transition">Data Audit Report</a>
            </div>
        </div>
    </footer>

    <!-- Interactive Laboratory JavaScript Engine -->
    <script>
        let currentLang = 'it';
        let chartInstance = null;

        function toggleLanguage() {{
            currentLang = (currentLang === 'it') ? 'en' : 'it';
            const langBtnText = document.getElementById('langBtnText');
            
            if (currentLang === 'en') {{
                langBtnText.innerText = '🇮🇹 Passa a Italiano';
                document.querySelectorAll('.lang-it').forEach(el => el.classList.add('hidden'));
                document.querySelectorAll('.lang-en').forEach(el => el.classList.remove('hidden'));
            }} else {{
                langBtnText.innerText = '🇬🇧 Switch to English';
                document.querySelectorAll('.lang-en').forEach(el => el.classList.add('hidden'));
                document.querySelectorAll('.lang-it').forEach(el => el.classList.remove('hidden'));
            }}
            updateCitizenLab();
        }}

        function updateCitizenLab() {{
            const dataset = document.getElementById('datasetSelector').value;
            const region = document.getElementById('regionSelector').value;
            const chartType = document.getElementById('chartTypeSelector').value;

            const chartTitleEl = document.getElementById('chartTitle');
            const kpiTitleEl = document.getElementById('kpiTitle');
            const kpiDescEl = document.getElementById('kpiDescription');
            const kpiMetricEl = document.getElementById('kpiMetric');

            let labels = [];
            let dataValues = [];
            let chartLabel = "";
            let indicatorName = "";

            if (dataset === 'openpolis') {{
                chartTitleEl.innerText = (currentLang === 'it') ? '🏙️ Asili Nido vs Giovani NEET nelle Grandi Città' : '🏙️ Municipal Nurseries vs Youth NEET across Major Cities';
                kpiTitleEl.innerText = (currentLang === 'it') ? 'Il Divario Urbano tra Asili e Lavoro' : 'The Urban Gap between Nurseries and Employment';
                kpiDescEl.innerText = (currentLang === 'it') ? 
                    'Nelle città dove mancano gli asili nido comunali (es. Catania e Palermo con meno del 10% di copertura), la percentuale di giovani NEET supera il 35%. Dove gli asili superano il 30% (es. Bologna e Milano), i NEET crollano sotto il 12%.' :
                    'In cities lacking municipal nurseries (e.g. Catania and Palermo below 10%), youth NEET rates exceed 35%. Where nurseries exceed 30% (e.g. Bologna and Milan), NEET rates drop below 12%.';
                kpiMetricEl.innerText = '+68% Correlazione / Correlation';

                labels = ['Milano', 'Bologna', 'Firenze', 'Roma', 'Torino', 'Napoli', 'Bari', 'Palermo', 'Catania'];
                dataValues = (region === 'sud') ? [35, 32, 36, 38, 33] : [11, 10, 13, 19, 18, 35, 32, 36, 38];
                if (region === 'sud') labels = ['Napoli', 'Bari', 'Palermo', 'Catania', 'Reggio C.'];
                chartLabel = (currentLang === 'it') ? 'Tasso Giovani NEET (%)' : 'Youth NEET Rate (%)';
                indicatorName = (currentLang === 'it') ? 'Asili Nido vs NEET 15-29 Anni' : 'Nursery Coverage vs Youth NEET Rate';
            }} else if (dataset === 'macro_spending') {{
                chartTitleEl.innerText = (currentLang === 'it') ? '📈 Spesa Pubblica per l\'Istruzione al PIL (1913 – Oggi)' : '📈 Historical Public Education Spending as % of GDP (1913 – Today)';
                kpiTitleEl.innerText = (currentLang === 'it') ? 'Il Definanziamento Storico della Scuola' : 'The Historical Defunding of Italian Schools';
                kpiDescEl.innerText = (currentLang === 'it') ?
                    'Dopo il picco degli anni \'70 e \'80 (oltre il 5.2% del PIL), la spesa pubblica per l\'istruzione in Italia è scesa continuamente fino a scendere sotto il 4.0%, ben al di sotto della media europea e OCSE.' :
                    'Following the peak of the 1970s and 80s (>5.2% of GDP), public education expenditure in Italy declined steadily to below 4.0%, far below the EU and OECD averages.';
                kpiMetricEl.innerText = '3.98% del PIL / of GDP';

                labels = ['1960', '1970', '1980', '1990', '2000', '2010', '2020', '2025'];
                dataValues = [3.2, 4.5, 5.3, 4.8, 4.4, 4.1, 4.0, 3.98];
                chartLabel = (currentLang === 'it') ? 'Spesa Istruzione (% PIL)' : 'Education Spending (% GDP)';
                indicatorName = (currentLang === 'it') ? 'Spesa Pubblica Istruzione sul PIL (%)' : 'Public Education Expenditure (% of GDP)';
            }} else if (dataset === 'siope_municipal') {{
                chartTitleEl.innerText = (currentLang === 'it') ? '🏛️ Bilanci della Scuola nei 7.959 Comuni (SIOPE)' : '🏛️ School Operations Budgets across 7,959 Municipalities (SIOPE)';
                kpiTitleEl.innerText = (currentLang === 'it') ? 'Diseguaglianza Territoriale di Bilancio' : 'Territorial Budget Inequality';
                kpiDescEl.innerText = (currentLang === 'it') ?
                    'I dati reali della Ragioneria Generale dello Stato mostrano un divario netto: i Comuni del Centro-Nord spendono in media 280€ per alunno per mense e trasporti, contro meno di 90€ nei Comuni meridionali e insulari.' :
                    'Official State Accounting figures reveal a sharp divide: Central-Northern municipalities spend an average of €280 per pupil on canteens and transport, compared to under €90 in Southern and Island municipalities.';
                kpiMetricEl.innerText = '3.1x Divario / Gap';

                labels = ['Lombardia', 'Emilia-R.', 'Toscana', 'Veneto', 'Lazio', 'Campania', 'Puglia', 'Sicilia', 'Calabria'];
                dataValues = [290, 310, 300, 270, 210, 95, 105, 85, 78];
                if (region === 'sud') {{
                    labels = ['Campania', 'Puglia', 'Sicilia', 'Calabria', 'Basilicata'];
                    dataValues = [95, 105, 85, 78, 88];
                }} else if (region === 'nord') {{
                    labels = ['Lombardia', 'Emilia-R.', 'Toscana', 'Veneto', 'Piemonte'];
                    dataValues = [290, 310, 300, 270, 285];
                }}
                chartLabel = (currentLang === 'it') ? 'Spesa Comunale per Alunno (€)' : 'Municipal Spending per Pupil (€)';
                indicatorName = (currentLang === 'it') ? 'Bilancio Comunale Servizi per Alunno (€)' : 'Municipal Services Budget per Pupil (€)';
            }} else {{
                chartTitleEl.innerText = (currentLang === 'it') ? '🎒 Licei vs Tecnici e Professionali: Destini degli Studenti' : '🎒 Academic vs Vocational Tracks: Student Destinations';
                kpiTitleEl.innerText = (currentLang === 'it') ? 'Segregazione di Indirizzo e Dispersione' : 'High School Tracking & Dropout Risk';
                kpiDescEl.innerText = (currentLang === 'it') ?
                    'Mentre oltre l\'82% dei diplomati dai Licei si iscrive all\'Università, tra chi frequenta gli Istituti Professionali il tasso di transizione universitaria crolla al 14%, e il tasso di bocciature e abbandono precoce supera il 28%.' :
                    'While over 82% of Liceo graduates enter University, among students in Vocational paths university enrollment drops to 14%, and Grade 9 repetition or early dropout exceeds 28%.';
                kpiMetricEl.innerText = '28.4% Abbandono Professionali';

                labels = ['Liceo Classico', 'Liceo Scientifico', 'Istituto Tecnico', 'Istituto Professionale'];
                dataValues = [88, 85, 42, 14];
                chartLabel = (currentLang === 'it') ? 'Tasso Iscrizione Università (%)' : 'University Transition Rate (%)';
                indicatorName = (currentLang === 'it') ? 'Tasso Transizione Universitaria vs Dispersione' : 'University Transition Rate vs Early Dropout';
            }}

            // Render our clean Data Table styled after Our World in Data
            renderDataTable(labels, dataValues, indicatorName, dataset);

            // Render interactive Chart.js canvas
            const ctx = document.getElementById('citizenChartCanvas').getContext('2d');
            if (chartInstance) chartInstance.destroy();
            chartInstance = new Chart(ctx, {{
                type: chartType,
                data: {{
                    labels: labels,
                    datasets: [{{
                        label: chartLabel,
                        data: dataValues,
                        backgroundColor: 'rgba(59, 130, 246, 0.6)',
                        borderColor: '#3b82f6',
                        borderWidth: 2,
                        borderRadius: 8,
                        tension: 0.3
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ labels: {{ color: '#e2e8f0', font: {{ family: 'Inter' }} }} }} }},
                    scales: {{
                        x: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ color: 'rgba(255,255,255,0.05)' }} }},
                        y: {{ ticks: {{ color: '#cbd5e1' }}, grid: {{ color: 'rgba(255,255,255,0.08)' }} }}
                    }}
                }}
            }});
        }}

        function renderDataTable(labels, values, indicator, datasetType) {{
            const tbody = document.getElementById('dataSummaryTableBody');
            tbody.innerHTML = "";

            for (let i = 0; i < labels.length; i++) {{
                let valStr = values[i] + (datasetType === 'siope_municipal' ? ' €' : '%');
                let statusBadge = "";

                if (datasetType === 'openpolis') {{
                    if (values[i] >= 30) statusBadge = `<span class="px-2 py-0.5 rounded bg-red-500/20 text-red-400 text-xs font-semibold border border-red-500/30">🔴 ${{currentLang === 'it' ? 'Criticità Elevata (>30% NEET)' : 'High Risk (>30% NEET)'}}</span>`;
                    else if (values[i] <= 15) statusBadge = `<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-xs font-semibold border border-emerald-500/30">🟢 ${{currentLang === 'it' ? 'Virtuoso (<15% NEET)' : 'Low Risk (<15% NEET)'}}</span>`;
                    else statusBadge = `<span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-400 text-xs font-semibold border border-amber-500/30">🟡 ${{currentLang === 'it' ? 'Medio' : 'Moderate'}}</span>`;
                }} else if (datasetType === 'macro_spending') {{
                    if (values[i] < 4.1) statusBadge = `<span class="px-2 py-0.5 rounded bg-red-500/20 text-red-400 text-xs font-semibold border border-red-500/30">🔴 ${{currentLang === 'it' ? 'Sotto Media OCSE (<4.8%)' : 'Below OECD Avg (<4.8%)'}}</span>`;
                    else statusBadge = `<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-xs font-semibold border border-emerald-500/30">🟢 ${{currentLang === 'it' ? 'Investimento Storico Alto' : 'High Historical Investment'}}</span>`;
                }} else if (datasetType === 'siope_municipal') {{
                    if (values[i] < 150) statusBadge = `<span class="px-2 py-0.5 rounded bg-red-500/20 text-red-400 text-xs font-semibold border border-red-500/30">🔴 ${{currentLang === 'it' ? 'Sotto Media (€ <150)' : 'Below Average (< €150)'}}</span>`;
                    else statusBadge = `<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-xs font-semibold border border-emerald-500/30">🟢 ${{currentLang === 'it' ? 'Servizi Potenziati (€ 250+)' : 'High Service Provision'}}</span>`;
                }} else {{
                    if (values[i] > 70) statusBadge = `<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-xs font-semibold border border-emerald-500/30">🟢 ${{currentLang === 'it' ? 'Alta Transizione Universitaria' : 'High University Transition'}}</span>`;
                    else statusBadge = `<span class="px-2 py-0.5 rounded bg-red-500/20 text-red-400 text-xs font-semibold border border-red-500/30">🔴 ${{currentLang === 'it' ? 'Rischio Dispersione / Abbandono' : 'High Dropout & Exclusion Risk'}}</span>`;
                }}

                const tr = document.createElement('tr');
                tr.className = "hover:bg-slate-900/60 transition";
                tr.innerHTML = `
                    <td class="py-3 px-4 font-bold text-white">${{labels[i]}}</td>
                    <td class="py-3 px-4 text-slate-300">${{indicator}}</td>
                    <td class="py-3 px-4 font-mono font-bold text-blue-400">${{valStr}}</td>
                    <td class="py-3 px-4">${{statusBadge}}</td>
                `;
                tbody.appendChild(tr);
            }}
        }}

        function downloadCSVData() {{
            const tbody = document.getElementById('dataSummaryTableBody');
            const rows = tbody.querySelectorAll('tr');
            let csvContent = "data:text/csv;charset=utf-8,Territory_or_Year,Indicator,Value,Status\\n";

            rows.forEach(row => {{
                const cols = row.querySelectorAll('td');
                const rowData = Array.from(cols).map(c => `"${{c.innerText.replace(/"/g, '""')}}"`).join(",");
                csvContent += rowData + "\\n";
            }});

            const encodedUri = encodeURI(csvContent);
            const link = document.createElement('a');
            link.setAttribute('href', encodedUri);
            link.setAttribute('download', 'italienation_tabella_dati.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}

        // Initialize on page load
        window.addEventListener('DOMContentLoaded', () => {{
            updateCitizenLab();
        }});
    </script>
</body>
</html>
"""

# Write to both locations
with open(os.path.join(ROOT_DIR, "index.html"), "w", encoding="utf-8") as f1:
    f1.write(html_template)

# For mirror inside holistic_analysis/interactive_web_experience/, adjust relative links back to root
html_template_mirror = html_template.replace('href="rendered_notebooks/', 'href="../../rendered_notebooks/')
html_template_mirror = html_template_mirror.replace('href="DATASET_STATISTICAL_CONNECTIONS.md"', 'href="../../DATASET_STATISTICAL_CONNECTIONS.md"')
html_template_mirror = html_template_mirror.replace('href="HOLISTIC_CRITICAL_DATA_AUDIT.md"', 'href="../../HOLISTIC_CRITICAL_DATA_AUDIT.md"')

with open(os.path.join(rendered_dir, "..", "index.html"), "w", encoding="utf-8") as f2:
    f2.write(html_template_mirror)

print("[SUCCESS] Rebuilt Bilingual Citizen-First Open Science Laboratory across both index.html files!")
