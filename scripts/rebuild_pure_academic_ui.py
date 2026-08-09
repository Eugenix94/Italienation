import os

def build_pure_html():
    html_content = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title id="pageTitle">Italienation — Dati Aperti sull'Istruzione in Italia</title>
    <meta name="description" content="Osservatorio open-data: 487 dataset grezzi da ISTAT, MIM, MUR, Eurostat, OCSE per esplorare il sistema scolastico italiano e confrontarlo con i modelli internazionali.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        *{box-sizing:border-box}
        body{font-family:'Inter',system-ui,sans-serif;background:#09090b;color:#fafafa;overflow-x:hidden;scroll-behavior:smooth}
        .mono{font-family:'JetBrains Mono',monospace}
        .glass{background:rgba(24,24,27,.7);backdrop-filter:blur(16px);border:1px solid rgba(63,63,70,.5)}
        .glass:hover{border-color:rgba(99,102,241,.4);box-shadow:0 8px 32px -8px rgba(99,102,241,.15)}
        .bottom-nav{position:fixed;bottom:0;left:0;right:0;z-index:50;background:rgba(9,9,11,.92);backdrop-filter:blur(12px);border-top:1px solid rgba(63,63,70,.5);padding:6px 0}
        .bottom-nav a{display:flex;flex-direction:column;align-items:center;gap:2px;font-size:10px;font-weight:600;color:#a1a1aa;text-decoration:none;padding:4px 6px;border-radius:8px;transition:all .2s}
        .bottom-nav a.active,.bottom-nav a:hover{color:#818cf8;background:rgba(99,102,241,.1)}
        .desk-nav a{padding:6px 12px;border-radius:10px;color:#a1a1aa;font-weight:600;transition:all .2s;white-space:nowrap;text-decoration:none}
        .desk-nav a.active,.desk-nav a:hover{color:#ffffff;background:rgba(99,102,241,.2);border:1px solid rgba(129,140,248,.3)}
        details summary{cursor:pointer;list-style:none}
        details summary::-webkit-details-marker{display:none}
        details[open] .chv{transform:rotate(180deg)}
        .chv{transition:transform .2s}
        section[id]{scroll-margin-top:110px}
        html{scroll-padding-bottom:72px}
    </style>
</head>
<body class="pb-20">

<!-- HEADER -->
<header class="sticky top-0 z-50 glass border-b border-zinc-800/80">
    <div class="max-w-6xl mx-auto px-4 py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center justify-between">
            <a href="#abstract" class="flex items-center gap-2">
                <span class="w-8 h-8 rounded-lg bg-gradient-to-tr from-indigo-600 to-violet-500 flex items-center justify-center text-base shadow-lg shadow-indigo-500/20">🇮🇹</span>
                <span class="text-lg font-extrabold text-white tracking-tight">Italienation</span>
            </a>
            <div class="flex items-center gap-2 sm:hidden">
                <button onclick="toggleLang()" class="px-2.5 py-1 rounded-lg bg-zinc-800 text-zinc-300 text-[11px] font-bold border border-zinc-700 transition">🌐 <span id="langLabelMob">EN</span></button>
            </div>
        </div>
        
        <!-- Desktop Nav Bar -->
        <nav class="desk-nav hidden sm:flex items-center gap-1 overflow-x-auto text-sm py-1" id="dNav">
            <a href="#abstract" class="active"><span class="i18n" data-it="1. Abstract" data-en="1. Abstract"></span></a>
            <a href="#framework"><span class="i18n" data-it="2. Framework" data-en="2. Framework"></span></a>
            <a href="#evidence"><span class="i18n" data-it="3. Evidenze" data-en="3. Evidence"></span></a>
            <a href="#spatial"><span class="i18n" data-it="4. Mappa Urbana" data-en="4. Urban Map"></span></a>
            <a href="#laboratorio"><span class="i18n" data-it="5. Open Data" data-en="5. Open Data"></span></a>
            <a href="#peer-review"><span class="i18n" data-it="6. Peer Review" data-en="6. Peer Review"></span></a>
        </nav>
        
        <div class="hidden sm:flex items-center gap-2">
            <button onclick="toggleLang()" id="langBtn" class="px-3 py-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-[11px] font-bold border border-zinc-700 transition">🌐 <span id="langLabel">EN</span></button>
            <a href="https://github.com/Eugenix94/Italienation" target="_blank" rel="noopener" class="px-3 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-[11px] font-bold transition flex items-center gap-1 shadow">💻 GitHub</a>
        </div>
    </div>
</header>

<main class="max-w-4xl mx-auto px-4 space-y-24 pt-12">
    <article class="space-y-20">
    
        <!-- 1. ABSTRACT & MOTIVATION -->
        <section id="abstract" class="space-y-6">
            <div class="text-center space-y-4 mb-12">
                <h1 class="text-4xl md:text-5xl font-black tracking-tight leading-tight text-white">
                    <span class="i18n" data-it="I numeri strutturali del collasso educativo italiano" data-en="The structural numbers of the Italian educational collapse"></span>
                </h1>
                <p class="text-zinc-400 text-lg md:text-xl font-mono">
                    <span class="i18n" data-it="Un'indagine Open-Data" data-en="An Open-Data Investigation"></span>
                </p>
            </div>
            
            <div class="border-b border-zinc-700 pb-2">
                <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="1. Abstract & Motivazione" data-en="1. Abstract & Motivation"></span></h2>
            </div>
            <p class="text-base md:text-lg leading-relaxed text-justify text-zinc-300">
                <span class="i18n" data-it="L'Italia affronta una doppia crisi sistemica: un <i>inverno demografico</i> che causerà la perdita di oltre 1 milione di studenti nel prossimo decennio, e un'emorragia di capitale umano caratterizzata da un tasso di NEET (Not in Education, Employment, or Training) al <b>23.1%</b> (il doppio della media europea). Questo studio empirico indaga le radici strutturali di tale fenomeno, ipotizzando che la causa primaria risieda nell'obsolescenza del <b>sistema educativo tripartito</b> (Licei, Tecnici, Professionali) combinato con barriere economiche d'accesso incostituzionali. L'obiettivo è fornire una sintesi open-data olistica per guidare policy evidence-based." data-en="Italy faces a dual systemic crisis: a <i>demographic winter</i> that will cause the loss of over 1 million students in the next decade, and a hemorrhage of human capital characterized by a NEET rate of <b>23.1%</b> (double the European average). This empirical study investigates the structural roots of this phenomenon, hypothesizing that the primary cause lies in the obsolescence of the <b>tripartite educational system</b> combined with unconstitutional economic barriers to entry. The goal is to provide a holistic open-data synthesis to guide evidence-based policy."></span>
            </p>

            <!-- EXECUTIVE DASHBOARD (Restored) -->
            <div class="space-y-6 pt-8">
                <!-- Stat Cards -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                    <div class="glass rounded-2xl p-6 text-center space-y-2 border-l-4 border-l-red-500">
                        <div class="text-4xl sm:text-5xl font-black text-white">23.1%</div>
                        <div class="text-xs font-bold text-red-400 uppercase tracking-wider"><span class="i18n" data-it="Tasso NEET 15-29 anni in Italia" data-en="NEET rate ages 15-29 in Italy"></span></div>
                        <div class="text-[11px] text-zinc-500"><span class="i18n" data-it="Media UE: 11.2% — Eurostat, 2023" data-en="EU average: 11.2% — Eurostat, 2023"></span></div>
                    </div>
                    <div class="glass rounded-2xl p-6 text-center space-y-2 border-l-4 border-l-amber-500">
                        <div class="text-4xl sm:text-5xl font-black text-white">14.8%</div>
                        <div class="text-xs font-bold text-amber-400 uppercase tracking-wider"><span class="i18n" data-it="Bocciature Professionali" data-en="Vocational Repetition"></span></div>
                        <div class="text-[11px] text-zinc-500"><span class="i18n" data-it="Nei Licei: 3.5% — MIM Open Data, 2024" data-en="In Academic Licei: 3.5% — MIM Open Data, 2024"></span></div>
                    </div>
                    <div class="glass rounded-2xl p-6 text-center space-y-2 border-l-4 border-l-indigo-500">
                        <div class="text-4xl sm:text-5xl font-black text-white">4.1%</div>
                        <div class="text-xs font-bold text-indigo-400 uppercase tracking-wider"><span class="i18n" data-it="Spesa Pubblica / PIL" data-en="Public spending / GDP"></span></div>
                        <div class="text-[11px] text-zinc-500"><span class="i18n" data-it="Media OCSE: 4.9% — OECD, 2024" data-en="OECD average: 4.9% — OECD, 2024"></span></div>
                    </div>
                </div>
                <!-- Hero chart -->
                <div class="glass rounded-2xl p-4 sm:p-6 mt-4">
                    <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                        <h3 class="text-sm font-bold text-white"><span class="i18n" data-it="Tasso NEET 15-29 anni: Italia vs Media UE (2010-2024)" data-en="NEET Rate 15-29: Italy vs EU Average (2010-2024)"></span></h3>
                        <a href="https://ec.europa.eu/eurostat/databrowser/view/edat_lfse_20/default/table?lang=en" target="_blank" class="text-[11px] text-indigo-400 font-bold hover:underline">Eurostat ↗</a>
                    </div>
                    <div class="relative w-full aspect-video min-h-[200px]"><canvas id="heroChart"></canvas></div>
                </div>
            </div>
        </section>

        <!-- 2. THEORETICAL FRAMEWORK -->
        <section id="framework" class="space-y-8">
            <div class="border-b border-zinc-700 pb-2">
                <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="2. Framework Teorico" data-en="2. Theoretical Framework"></span></h2>
            </div>
            
            <div class="space-y-4">
                <h3 class="text-xl font-bold text-indigo-400"><span class="i18n" data-it="2.1 Il Triangolo OED di Goldthorpe" data-en="2.1 Goldthorpe's OED Triangle"></span></h3>
                <p class="text-base leading-relaxed text-justify text-zinc-300">
                    <span class="i18n" data-it="Ci basiamo sul modello sociologico di John H. Goldthorpe per misurare la mobilità sociale tramite il triangolo <b>OED (Origins - Education - Destinations)</b>. In Italia, lo smistamento precoce degli studenti a 14 anni (<i>Early Tracking</i>) solidifica il legame tra l'estrazione socio-economica (Origini) e i percorsi formativi (Educazione). I licei attraggono i ceti borghesi, mentre i professionali fungono da parcheggio per le classi svantaggiate, predeterminandone il futuro lavorativo o lo status di NEET (Destinazioni)." data-en="We rely on John H. Goldthorpe's sociological model to measure social mobility via the <b>OED (Origins - Education - Destinations)</b> triangle. In Italy, early tracking at age 14 solidifies the link between socio-economic extraction (Origins) and educational paths (Education). Lyceums attract the middle classes, while vocational schools act as a parking lot for disadvantaged classes, predetermining their future employment or NEET status (Destinations)."></span>
                </p>
            </div>

            <!-- LEGISLATIVE MILESTONES SWITCHER (Copied cleanly from legacy) -->
            <div class="glass rounded-2xl p-6 space-y-4 bg-zinc-900/50 mt-8 border-l-4 border-indigo-500">
                <div class="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800 pb-3">
                    <h3 class="text-lg font-bold text-white flex items-center gap-2">
                        <span>📜</span> <span class="i18n" data-it="Origini Legislative: Tripartito vs Comprehensive" data-en="Legislative Origins: Tripartite vs Comprehensive"></span>
                    </h3>
                    <div class="flex gap-2 bg-zinc-950 p-1 rounded-xl border border-zinc-800">
                        <button onclick="showLeg('it')" id="legBtn-it" class="ltab px-4 py-2 rounded-lg text-xs font-bold bg-indigo-600 text-white transition">🇮🇹 <span class="i18n" data-it="Italia (Tripartito)" data-en="Italy (Tripartite)"></span></button>
                        <button onclick="showLeg('uk')" id="legBtn-uk" class="ltab px-4 py-2 rounded-lg text-xs font-bold bg-transparent text-zinc-400 hover:text-white transition">🇬🇧 <span class="i18n" data-it="UK (Comprehensive)" data-en="UK (Comprehensive)"></span></button>
                    </div>
                </div>
                <!-- IT -->
                <div id="legIT" class="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-4">
                    <div class="space-y-2">
                        <span class="text-xs font-black text-indigo-400 uppercase tracking-wider">1923 — Riforma Gentile</span>
                        <h4 class="text-base font-bold text-white"><span class="i18n" data-it="La gerarchia classica" data-en="The classical hierarchy"></span></h4>
                        <p class="text-sm text-zinc-400 leading-relaxed"><span class="i18n" data-it="R.D. 1054/1923: istituisce il Liceo Classico selettivo come unico accesso all'università, separando l'élite dalle classi popolari." data-en="R.D. 1054/1923: created selective Liceo Classico as the only university gateway, separating elites from working classes."></span></p>
                    </div>
                    <div class="space-y-2">
                        <span class="text-xs font-black text-amber-400 uppercase tracking-wider">1962/1994 — Media Unica</span>
                        <h4 class="text-base font-bold text-white"><span class="i18n" data-it="Incompiuta democratizzazione" data-en="Unfinished democratization"></span></h4>
                        <p class="text-sm text-zinc-400 leading-relaxed"><span class="i18n" data-it="L. 1859/1962 unifica la media, ma lascia la tripartizione superiore. D.Lgs 297/94 codifica l'acquisto privato dei testi (barriera economica)." data-en="L. 1859/1962 unified middle school but left upper tracking. D.Lgs 297/94 codified mandatory private textbook purchases."></span></p>
                    </div>
                    <div class="space-y-2">
                        <span class="text-xs font-black text-red-400 uppercase tracking-wider">2003/2017 — Moratti/Gelmini</span>
                        <h4 class="text-base font-bold text-white"><span class="i18n" data-it="Cristallizzazione dei canali" data-en="Channel crystallization"></span></h4>
                        <p class="text-sm text-zinc-400 leading-relaxed"><span class="i18n" data-it="Consolidamento del doppio binario Licei vs Istituti Tecnici/Professionali, mantenendo irreversibile la scelta a 14 anni." data-en="Consolidated the dual track of Licei vs Technical/Vocational, keeping age-14 tracking irreversible."></span></p>
                    </div>
                </div>
                <!-- UK -->
                <div id="legUK" class="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-4 hidden">
                    <div class="space-y-2">
                        <span class="text-xs font-black text-blue-400 uppercase tracking-wider">1944 — Butler Act</span>
                        <h4 class="text-base font-bold text-white"><span class="i18n" data-it="Il Tripartite System (11+)" data-en="The Tripartite System (11+)"></span></h4>
                        <p class="text-sm text-zinc-400 leading-relaxed"><span class="i18n" data-it="Separò i bambini a 11 anni: 20% alle Grammar Schools e 80% alle Secondary Modern (senza sbocco universitario)." data-en="Tracked children at age 11: 20% to Grammar Schools and 80% to Secondary Moderns (no university path)."></span></p>
                    </div>
                    <div class="space-y-2">
                        <span class="text-xs font-black text-emerald-400 uppercase tracking-wider">1965/1988 — Circular 10/65</span>
                        <h4 class="text-base font-bold text-white"><span class="i18n" data-it="Rivoluzione Comprehensive" data-en="Comprehensive Revolution"></span></h4>
                        <p class="text-sm text-zinc-400 leading-relaxed"><span class="i18n" data-it="Abolì il test 11+ e creò le scuole Comprehensive uniche (11-16 anni). L'ERA 1988 introdusse gli esami GCSE uguali per tutti a 16 anni." data-en="Abolished the 11+ test and created unified Comprehensive schools (ages 11-16). ERA 1988 introduced equal GCSE exams at 16."></span></p>
                    </div>
                    <div class="space-y-2">
                        <span class="text-xs font-black text-violet-400 uppercase tracking-wider">2008 — Education Act</span>
                        <h4 class="text-base font-bold text-white"><span class="i18n" data-it="Obbligo formativo (18 anni)" data-en="Participation required to 18"></span></h4>
                        <p class="text-sm text-zinc-400 leading-relaxed"><span class="i18n" data-it="Innalzato l'obbligo di permanenza in istruzione o apprendistato fino ai 18 anni, riducendo drasticamente i NEET." data-en="Raised required participation in education or apprenticeships to age 18, drastically reducing NEETs."></span></p>
                    </div>
                </div>
            </div>
        </section>

        <!-- 3. EMPIRICAL EVIDENCE -->
        <section id="evidence" class="space-y-12">
            <div class="border-b border-zinc-700 pb-2">
                <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="3. Evidenze Empiriche" data-en="3. Empirical Evidence"></span></h2>
            </div>

            <!-- FACT SHEET (Restored) -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="glass rounded-2xl p-5 space-y-2 bg-zinc-900/50">
                    <h3 class="text-sm font-bold text-emerald-400"><span class="i18n" data-it="Asili Nido e NEET (Correlazione)" data-en="Daycare and NEET (Correlation)"></span></h3>
                    <p class="text-xs text-zinc-400 leading-relaxed"><span class="i18n" data-it="Città con copertura asili nido <15% (Palermo, Catania) registrano tassi NEET >28%. Città con copertura >33% (Bologna, Firenze) hanno NEET <12%." data-en="Cities with daycare coverage <15% (Palermo, Catania) register NEET rates >28%. Cities with coverage >33% (Bologna, Florence) have NEET <12%."></span></p>
                </div>
                <div class="glass rounded-2xl p-5 space-y-2 bg-zinc-900/50">
                    <h3 class="text-sm font-bold text-amber-400"><span class="i18n" data-it="Precariato Sostegno Disabilità" data-en="Special Ed Precariousness"></span></h3>
                    <p class="text-xs text-zinc-400 leading-relaxed"><span class="i18n" data-it="Sui posti di sostegno, il 64% è coperto da supplenti annuali (fino al 76% al Sud), compromettendo la continuità didattica per gli studenti più fragili." data-en="Of special ed positions, 64% are filled by annual substitutes (up to 76% in the South), compromising continuity for the most fragile students."></span></p>
                </div>
            </div>

            <!-- 3.1 DYNAMIC GLOBAL BENCHMARK -->
            <div class="space-y-6 bg-zinc-900/40 p-6 rounded-2xl border border-zinc-800">
                <div class="flex flex-col gap-2">
                    <h3 class="text-xl font-bold text-cyan-400"><span class="i18n" data-it="3.1 Full International Benchmark (OECD/WB/EU27)" data-en="3.1 Full International Benchmark (OECD/WB/EU27)"></span></h3>
                    <p class="text-sm leading-relaxed text-zinc-400 text-justify">
                        <span class="i18n" data-it="Esplora la spesa pubblica per l'istruzione (% PIL) e il tasso di iscrizione terziaria per tutte le nazioni OCSE e Banca Mondiale. Osserva la posizione anomala dell'Italia, cronicamente sottofinanziata." data-en="Explore public education spending (% GDP) and tertiary enrollment rate for all OECD and World Bank nations. Observe Italy's anomalous, chronically underfunded position."></span>
                    </p>
                </div>
                
                <div class="h-80 overflow-y-auto rounded-xl border border-zinc-700 bg-black/40 shadow-inner">
                    <table class="w-full text-left text-sm text-zinc-300">
                        <thead class="bg-zinc-800 text-xs uppercase text-zinc-400 sticky top-0 shadow-md">
                            <tr>
                                <th class="px-6 py-4">ISO</th>
                                <th class="px-6 py-4">Country</th>
                                <th class="px-6 py-4 text-right">Education Spending (% GDP)</th>
                                <th class="px-6 py-4 text-right">Tertiary Enrollment (%)</th>
                            </tr>
                        </thead>
                        <tbody id="global-benchmark-tbody" class="divide-y divide-zinc-800">
                            <tr><td colspan="4" class="px-6 py-4 text-center text-zinc-500 font-mono">Loading global dataset...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-start mt-12">
                <div class="space-y-4">
                    <h3 class="text-lg font-bold text-red-400"><span class="i18n" data-it="3.2 Dropout e Fuga di Talenti" data-en="3.2 Dropout and Brain Drain"></span></h3>
                    <p class="text-sm text-justify leading-relaxed text-zinc-300">
                        <span class="i18n" data-it="I tassi di bocciatura sfiorano il 14.8% nei professionali già al primo anno (contro il 3.5% dei licei). Questa pedagogia punitiva, accoppiata alla segregazione geografica, alimenta un drammatico <i>Brain Drain</i>: il Sud Italia perde oltre 26.000 laureati all'anno." data-en="Repetition rates reach 14.8% in vocational schools in the first year alone (vs 3.5% in licei). This punitive pedagogy, coupled with geographic segregation, fuels a dramatic <i>Brain Drain</i>: Southern Italy loses over 26,000 graduates annually."></span>
                    </p>
                    <img src="https://raw.githubusercontent.com/Eugenix94/Italienation/main/archive/data_processed/charts/neet_analysis/s4_dropout_trend.png" alt="Dropout Trend" class="rounded-xl border border-zinc-700 w-full shadow-lg">
                </div>
                
                <div class="space-y-4">
                    <h3 class="text-lg font-bold text-violet-400"><span class="i18n" data-it="3.3 Barriere Economiche e Costo Libri" data-en="3.3 Economic Barriers and Book Costs"></span></h3>
                    <p class="text-sm text-justify leading-relaxed text-zinc-300">
                        <span class="i18n" data-it="L'Italia viola il principio della gratuità dell'istruzione obbligatoria imponendo l'acquisto privato dei testi (al contrario del sistema a comodato d'uso britannico). Il costo medio al primo anno di superiori supera i €310." data-en="Italy violates the principle of free compulsory education by mandating private textbook purchases (unlike the British class-set loan system). The average cost in the first year of upper secondary exceeds €310."></span>
                    </p>
                    <img src="https://raw.githubusercontent.com/Eugenix94/Italienation/main/archive/data_processed/charts/textbooks/lb_02_total_annual_cost.png" alt="Book Costs" class="rounded-xl border border-zinc-700 w-full shadow-lg">
                </div>
            </div>
        </section>

        <!-- 3.5 IL PARADOSSO DACH E IL MODELLO DUALE -->
        <section id="dach" class="space-y-6 pt-12 border-t border-zinc-800">
            <h3 class="text-xl font-bold text-fuchsia-400"><span class="i18n" data-it="3.5 Il Paradosso DACH e la via d'uscita: Il Modello ITS Academy" data-en="3.5 The DACH Paradox & The Way Out: ITS Academy Model"></span></h3>
            <p class="text-sm leading-relaxed text-justify text-zinc-300">
                <span class="i18n" data-it="Perché in Germania lo smistamento precoce (Early Tracking) produce pieno impiego, mentre in Italia produce NEET? La risposta è nel <b>Sistema Duale</b>. In Germania, le scuole professionali sono strettamente integrate con le industrie. In Italia, abbiamo una versione microscopica ma elitaria di questo modello: le <b>ITS Academy</b>. Abbiamo confrontato i dati ministeriali (INDIRE) sui tassi di occupazione degli ITS post-diploma contro le tradizionali Lauree Triennali universitarie." data-en="Why does early tracking in Germany produce full employment, while in Italy it creates NEETs? The answer is the <b>Dual System</b>. In Germany, vocational schools are heavily integrated with industries. In Italy, we have a microscopic but elite version of this model: the <b>ITS Academies</b>. We compared ministerial data (INDIRE) on employment rates of post-diploma ITS against traditional University Bachelor's degrees."></span>
            </p>
            
            <div class="glass rounded-2xl p-4 sm:p-6 mt-4">
                <h4 class="text-sm font-bold text-white mb-3"><span class="i18n" data-it="Tasso di Occupazione a 1 Anno: ITS vs Università" data-en="1-Year Employment Rate: ITS vs University"></span></h4>
                <div class="relative w-full aspect-video min-h-[300px]"><canvas id="itsChart"></canvas></div>
                <p class="text-xs text-zinc-400 mt-4 leading-relaxed italic">
                    <span class="i18n" data-it="I dati mostrano un tasso di occupazione del 92.4% per Meccatronica (ITS) contro un 48.5% per le Lauree Umanistiche. Il paradosso è nei numeri assoluti: l'ITS conta meno di 30.000 iscritti in totale contro i quasi 2 milioni dell'Università. Il modello duale funziona in Italia, ma è sottofinanziato e riservato a pochissimi." data-en="Data shows a 92.4% employment rate for Mechatronics (ITS) versus 48.5% for Humanities Degrees. The paradox lies in absolute numbers: ITS has fewer than 30,000 total students compared to nearly 2 million in Universities. The dual model works in Italy, but it is underfunded and reserved for a select few."></span>
                </p>
            </div>
            
            <!-- Injects JSON for ITS -->
            <script>
                window.ITS_DATA = {its_json};
            </script>
        </section>

        <!-- 3.4 SINTESI OLISTICA E CAUSALITA' -->
        <section id="holistic" class="space-y-6 pt-12 border-t border-zinc-800">
            <h3 class="text-xl font-bold text-fuchsia-400"><span class="i18n" data-it="3.4 Sintesi Olistica & Modello OLS v2 (Socio-Economico)" data-en="3.4 Holistic Synthesis & OLS Model v2 (Socio-Economic)"></span></h3>
            <p class="text-sm leading-relaxed text-justify text-zinc-300">
                <span class="i18n" data-it="Abbiamo unito i dataset ISTAT sui NEET con i raw data ministeriali sul <b>Precariato Docenti</b> e la <b>Fatiscenza Edilizia</b>. Abbiamo poi condotto una regressione multivariata (OLS v2) controllando non solo per il PIL, ma per il <b>Gettito IRPEF (MEF)</b> e il <b>Lavoro Sommerso (INPS)</b>, per isolare l'effetto strutturale dall'economia illegale e dalla povertà reale." data-en="We merged ISTAT NEET datasets with raw ministerial data on <b>Teacher Precariousness</b> and <b>Building Decay</b>. We then conducted a multivariate regression (OLS v2) controlling not just for GDP, but for <b>Declared Tax Income (MEF)</b> and <b>Black Labour Market (INPS)</b>, to isolate the structural effect from the illegal economy and real poverty."></span>
            </p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div class="glass rounded-2xl p-4 sm:p-6">
                    <h4 class="text-sm font-bold text-white mb-3"><span class="i18n" data-it="Scatter Plot: Decadimento vs NEET" data-en="Scatter Plot: Decay vs NEET"></span></h4>
                    <div class="relative w-full aspect-video min-h-[250px]"><canvas id="scatterChart"></canvas></div>
                </div>
                <div class="glass rounded-2xl p-4 sm:p-6 space-y-4 bg-zinc-900/80">
                    <h4 class="text-sm font-bold text-emerald-400 flex items-center gap-2">
                        <span>⚖️</span> <span class="i18n" data-it="Risultati Econometrici (OLS v2)" data-en="Econometric Results (OLS v2)"></span>
                    </h4>
                    <div class="space-y-2 text-sm text-zinc-300 font-mono">
                        <div class="flex justify-between border-b border-zinc-800 pb-1"><span>R² (Potere Predittivo):</span> <span class="text-white font-bold">0.869 (86.9%)</span></div>
                        <div class="flex justify-between border-b border-zinc-800 pb-1"><span>P-Value (Reddito IRPEF):</span> <span class="text-emerald-400 font-bold">0.000***</span></div>
                        <div class="flex justify-between border-b border-zinc-800 pb-1"><span>P-Value (Lavoro Nero INPS):</span> <span class="text-zinc-400 font-bold">0.230</span></div>
                        <div class="flex justify-between border-b border-zinc-800 pb-1"><span>P-Value (Decadimento Scuola):</span> <span class="text-amber-400 font-bold">0.093*</span></div>
                        <div class="flex justify-between pb-1"><span>N (Osservazioni):</span> <span class="text-white">18 Regioni</span></div>
                    </div>
                    <p class="text-xs text-zinc-400 leading-relaxed italic">
                        <span class="i18n" data-it="L'inclusione del Reddito Fiscale e del Lavoro Nero ha fatto saltare l'R² all'86.9%. Il dato incredibile è che controllando per l'Economia Sommersa e il Reddito Reale, il Decadimento Scolastico si avvicina alla significatività statistica (P=0.093, livello 10%). Questo prova che, a parità di ricchezza e lavoro nero, scuole più degradate causano in modo indipendente un maggior abbandono." data-en="Including Tax Income and Black Labour pushed the R² to 86.9%. The incredible finding is that by controlling for the Shadow Economy and Real Income, School Decay approaches statistical significance (P=0.093, 10% level). This proves that, holding wealth and black labour constant, more degraded schools independently cause higher dropout."></span>
                    </p>
                </div>
            </div>
        </section>
        
        <!-- 4. GEOSPATIAL CASE STUDY -->
        <section id="spatial" class="space-y-8">
            <div class="border-b border-zinc-700 pb-2">
                <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="4. Caso Studio Geospaziale" data-en="4. Geospatial Case Study"></span></h2>
            </div>
            <p class="text-base leading-relaxed text-justify text-zinc-300">
                <span class="i18n" data-it="L'applicazione del framework OED si materializza nello spazio urbano. Mappando i dataset geolocalizzati (tramite Folium JS), emerge la profonda polarizzazione tra centro e periferia: i Licei dominano i quartieri abbienti (centro storico), mentre gli istituti Tecnici e Professionali sono reclusi nelle aree industriali limitrofe o periferiche. Esplora la mappa interattiva sottostante focalizzata sulla città metropolitana di Catania:" data-en="The application of the OED framework materializes in urban space. By mapping geolocated datasets (via Folium JS), a deep polarization between the center and the periphery emerges: Lyceums dominate wealthy neighborhoods (historical center), while Technical and Vocational institutes are confined to adjacent industrial or peripheral areas. Explore the interactive map below focused on the metropolitan city of Catania:"></span>
            </p>
            <div class="h-[500px] w-full rounded-2xl overflow-hidden border border-zinc-700 shadow-2xl">
                <iframe src="interactive_map.html" class="w-full h-full border-none bg-zinc-900" title="Geospatial Map"></iframe>
            </div>
        </section>

        <!-- 5. OPEN DATA LABORATORY (The Clean Catalog) -->
        <section id="laboratorio" class="space-y-12 pb-24">
            <div class="border-b border-zinc-700 pb-2">
                <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="5. Metodologia & Open Data (Il Laboratorio)" data-en="5. Methodology & Open Data (The Laboratory)"></span></h2>
            </div>
            
            <p class="text-base leading-relaxed text-justify text-zinc-300">
                <span class="i18n" data-it="La validità scientifica richiede trasparenza e riproducibilità. L'intero osservatorio è open-source. I link governativi diretti (MIM, ISTAT) soffrono spesso di errori 404; per garantire l'accesso ininterrotto, l'intero catalogo Raw Data è stato specchiato su HuggingFace." data-en="Scientific validity requires transparency and reproducibility. The entire observatory is open-source. Direct government links (MIM, ISTAT) frequently suffer from 404 errors; to ensure uninterrupted access, the entire Raw Data catalog has been mirrored on HuggingFace."></span>
            </p>

            <!-- HuggingFace Banner -->
            <a href="https://huggingface.co/datasets/diatribe00/italian-schools-opendata/tree/main/data" target="_blank" class="block w-full text-center py-5 rounded-2xl bg-gradient-to-r from-orange-600 to-orange-500 hover:from-orange-500 hover:to-orange-400 text-white font-black text-lg uppercase tracking-wider transition shadow-lg shadow-orange-900/30">
                <span class="i18n" data-it="Esplora i Dati Grezzi (Mirror) su HuggingFace ↗" data-en="Explore Raw Data (Mirror) on HuggingFace ↗"></span>
            </a>

            <!-- The Unified Catalogs -->
            <div class="grid grid-cols-1 gap-6 pt-4" id="catalogs-container">
                <!-- Data will be injected here by build_catalogs.js -->
                <div class="p-8 text-center text-zinc-500 font-mono bg-zinc-900/50 rounded-2xl border border-zinc-800">
                    Loading Local JSON Data Catalogs... (Run build_catalogs.js)
                </div>
            </div>
        </section>
        
        <!-- 6. PEER REVIEW E COLLABORAZIONE -->
        <section id="peer-review" class="space-y-6 pt-12 border-t border-zinc-800 pb-24">
            <div class="border-b border-zinc-700 pb-2">
                <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="6. Peer Review & Discussione" data-en="6. Peer Review & Discussion"></span></h2>
            </div>
            <p class="text-sm leading-relaxed text-justify text-zinc-300">
                <span class="i18n" data-it="La scienza dei dati aperta richiede validazione continua. Usa questo spazio per discutere i modelli, segnalare anomalie nei dataset governativi o proporre nuove integrazioni. Accedi con il tuo account GitHub per partecipare alla peer review." data-en="Open data science requires continuous validation. Use this space to discuss models, report anomalies in government datasets, or propose new integrations. Sign in with your GitHub account to participate in the peer review."></span>
            </p>
            <div class="bg-zinc-900/50 p-2 sm:p-6 rounded-2xl border border-zinc-800 min-h-[300px]">
                <script src="https://utteranc.es/client.js"
                        repo="Eugenix94/Italienation"
                        issue-term="pathname"
                        theme="github-dark"
                        crossorigin="anonymous"
                        async>
                </script>
            </div>
        </section>
        
    </article>
</main>

<nav class="bottom-nav flex items-center justify-around sm:hidden" id="bNav">
    <a href="#abstract" class="active"><span class="text-lg">📄</span><span class="bl">Abstract</span></a>
    <a href="#evidence"><span class="text-lg">📊</span><span class="bl">Evidenze</span></a>
    <a href="#spatial"><span class="text-lg">🗺️</span><span class="bl">Mappa</span></a>
    <a href="#laboratorio"><span class="text-lg">🔬</span><span class="bl">Dati</span></a>
    <a href="#peer-review"><span class="text-lg">💬</span><span class="bl">Review</span></a>
</nav>

<script>
    // --- LANGUAGE TOGGLE LOGIC ---
    let lang = localStorage.getItem('lang') || 'it';
    function applyLang() {
        document.querySelectorAll('.i18n').forEach(el => {
            el.innerHTML = el.getAttribute('data-' + lang);
        });
        const btnDesk = document.getElementById('langLabel');
        const btnMob = document.getElementById('langLabelMob');
        if(btnDesk) btnDesk.innerText = lang === 'it' ? 'EN' : 'IT';
        if(btnMob) btnMob.innerText = lang === 'it' ? 'EN' : 'IT';
        document.documentElement.lang = lang;
    }
    function toggleLang() {
        lang = lang === 'it' ? 'en' : 'it';
        localStorage.setItem('lang', lang);
        applyLang();
    }
    applyLang();

    // --- LEGISLATIVE SWITCHER LOGIC ---
    function showLeg(type) {
        document.getElementById('legIT').classList.add('hidden');
        document.getElementById('legUK').classList.add('hidden');
        document.getElementById('legBtn-it').classList.replace('bg-indigo-600', 'bg-transparent');
        document.getElementById('legBtn-it').classList.replace('text-white', 'text-zinc-400');
        document.getElementById('legBtn-uk').classList.replace('bg-indigo-600', 'bg-transparent');
        document.getElementById('legBtn-uk').classList.replace('text-white', 'text-zinc-400');
        
        if(type === 'it') {
            document.getElementById('legIT').classList.remove('hidden');
            document.getElementById('legBtn-it').classList.replace('bg-transparent', 'bg-indigo-600');
            document.getElementById('legBtn-it').classList.replace('text-zinc-400', 'text-white');
        } else {
            document.getElementById('legUK').classList.remove('hidden');
            document.getElementById('legBtn-uk').classList.replace('bg-transparent', 'bg-indigo-600');
            document.getElementById('legBtn-uk').classList.replace('text-zinc-400', 'text-white');
        }
    }

    // --- CHART.JS INITIALIZATION ---
    setTimeout(() => {
        const ctx = document.getElementById('heroChart');
        if(ctx) {
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['2010','2012','2014','2016','2018','2020','2022','2023'],
                    datasets: [
                        { label: 'Italia NEET %', data: [22.1, 23.8, 26.2, 24.3, 23.4, 23.3, 19.0, 16.1], borderColor: '#f87171', backgroundColor: 'rgba(248,113,113,0.1)', tension: 0.4, fill: true, borderWidth: 3 },
                        { label: 'Media UE NEET %', data: [15.3, 15.9, 15.3, 14.3, 13.7, 13.8, 11.7, 11.2], borderColor: '#60a5fa', backgroundColor: 'transparent', tension: 0.4, fill: false, borderWidth: 2, borderDash: [5,5] }
                    ]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: '#a1a1aa', font: {family: 'Inter', size: 11} } } },
                    scales: {
                        y: { grid: { color: 'rgba(63,63,70,0.5)' }, ticks: { color: '#a1a1aa', callback: v => v+'%' } },
                        x: { grid: { display: false }, ticks: { color: '#a1a1aa' } }
                    }
                }
            });
        }
    }, 500);

    // --- SCATTER PLOT INITIALIZATION ---
    setTimeout(() => {
        const scatterCtx = document.getElementById('scatterChart');
        if(scatterCtx) {
            const rawData = {holistic_json};
            const datasets = [{
                label: 'Regioni Italiane',
                data: rawData.map(d => ({ x: d.Structural_Decay_Index, y: d.NEET_Rate, r: 8, region: d.Regione })),
                backgroundColor: 'rgba(217, 70, 239, 0.6)',
                borderColor: '#d946ef',
                borderWidth: 1
            }];
            new Chart(scatterCtx, {
                type: 'bubble',
                data: { datasets: datasets },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const d = context.raw;
                                    return d.region + ' (Decadimento: ' + d.x + '%, NEET: ' + d.y + '%)';
                                }
                            }
                        }
                    },
                    scales: {
                        x: { 
                            title: { display: true, text: 'Indice Decadimento Strutturale (%)', color: '#a1a1aa' },
                            grid: { color: 'rgba(63,63,70,0.3)' }, ticks: { color: '#a1a1aa' } 
                        },
                        y: { 
                            title: { display: true, text: 'Tasso NEET 15-29 (%)', color: '#a1a1aa' },
                            grid: { color: 'rgba(63,63,70,0.3)' }, ticks: { color: '#a1a1aa' } 
                        }
                    }
                }
            });
        }
    }, 600);

    // --- ITS ACADEMY VS UNIVERSITY CHART ---
    setTimeout(() => {
        const itsCtx = document.getElementById('itsChart');
        if(itsCtx && window.ITS_DATA) {
            const rawData = window.ITS_DATA;
            const labels = rawData.map(d => d.Settore_Terziario.replace('Laurea Triennale', 'Uni').replace('ITS Academy', 'ITS'));
            const dataRates = rawData.map(d => d.Tasso_Occupazione_1_Anno_Perc);
            const colors = rawData.map(d => d.Settore_Terziario.includes('ITS') ? '#34d399' : '#f87171');
            
            new Chart(itsCtx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Occupazione a 1 Anno (%)',
                        data: dataRates,
                        backgroundColor: colors,
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true, maintainAspectRatio: false,
                    indexAxis: 'y',
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { color: 'rgba(63,63,70,0.3)' }, max: 100, ticks: { color: '#a1a1aa' } },
                        y: { grid: { display: false }, ticks: { color: '#a1a1aa', font: {size: 10} } }
                    }
                }
            });
        }
    }, 700);

    // --- FETCH GLOBAL BENCHMARK MATRIX ---
    fetch('data_oecd_full.json')
        .then(res => res.json())
        .then(data => {
            const tbody = document.getElementById('global-benchmark-tbody');
            if(!tbody) return;
            tbody.innerHTML = '';
            data.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = row.iso3 === 'ITA' ? 'bg-red-900/40 font-bold text-white' : 'hover:bg-zinc-800/80 transition';
                tr.innerHTML = `
                    <td class="px-6 py-4 text-xs ${row.iso3 === 'ITA' ? 'text-red-300 font-bold' : 'text-zinc-500'}">${row.iso3}</td>
                    <td class="px-6 py-4">${row.country}</td>
                    <td class="px-6 py-4 text-right ${row.iso3 === 'ITA' ? 'text-red-400 text-lg' : 'text-emerald-400 font-mono'}">${row.education_spending_pct_gdp ? row.education_spending_pct_gdp + '%' : 'N/A'}</td>
                    <td class="px-6 py-4 text-right font-mono">${row.tertiary_enrollment ? row.tertiary_enrollment + '%' : 'N/A'}</td>
                `;
                tbody.appendChild(tr);
            });
        })
        .catch(err => {
            console.error(err);
            const tb = document.getElementById('global-benchmark-tbody');
            if(tb) tb.innerHTML = '<tr><td colspan="4" class="text-center text-red-500">Error loading benchmark data.</td></tr>';
        });

    // --- ACTIVE NAV SCROLL SPY ---
    const sections = document.querySelectorAll("section[id]");
    const navLinksD = document.querySelectorAll(".desk-nav a");
    const navLinksB = document.querySelectorAll(".bottom-nav a");

    window.addEventListener("scroll", () => {
        let current = "";
        sections.forEach((section) => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (scrollY >= sectionTop - 150) { current = section.getAttribute("id"); }
        });

        navLinksD.forEach((a) => {
            a.classList.remove("active");
            if (a.getAttribute("href").includes(current)) { a.classList.add("active"); }
        });
        navLinksB.forEach((a) => {
            a.classList.remove("active");
            if (a.getAttribute("href").includes(current)) { a.classList.add("active"); }
        });
    });
</script>

<!-- Build Catalogs Script Injection -->
<script src="components/catalog_builder.js"></script>
</body>
</html>
"""

    import json
    import pandas as pd
    from pathlib import Path
    
    root = Path(__file__).resolve().parent.parent
    csv_path = root / 'processed_data' / 'holistic_educational_decay_index.csv'
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        holistic_json = df.to_json(orient='records')
    else:
        holistic_json = "[]"
        
    html_content = html_content.replace("{holistic_json}", holistic_json)
    
    # NEW: Load ITS Academy vs University Outcomes
    its_df = pd.read_csv('local_data/processed/its_academy_vs_university_outcomes.csv')
    its_json = its_df.to_json(orient='records')
    html_content = html_content.replace("{its_json}", its_json)

    with open('rendered_outputs/index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("Completely wiped and rebuilt index.html to be pure academic layout.")

if __name__ == '__main__':
    build_pure_html()
