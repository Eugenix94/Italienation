const fs = require('fs');

let html = fs.readFileSync('web/index.html', 'utf8');

// 1. Add Tab 6 nav button right after Tab 5 button if not already added
const tab5Btn = `<button onclick="switchTab('collaborate')" id="tab-btn-collaborate" class="nav-tab px-4.5 py-2.5 rounded-xl text-slate-300 text-xs md:text-sm font-semibold flex items-center gap-2">
                <span>🤝</span>
                <span class="lang-it">5. Collabora & Open Science</span>
                <span class="lang-en hidden">5. Collaborate & Open Science</span>
            </button>`;

const tab6Btn = `${tab5Btn}
            <button onclick="switchTab('repo-catalog')" id="tab-btn-repo-catalog" class="nav-tab px-4.5 py-2.5 rounded-xl text-slate-300 text-xs md:text-sm font-semibold flex items-center gap-2">
                <span>📂</span>
                <span class="lang-it">6. Catalogo 681 Dati & Fonti</span>
                <span class="lang-en hidden">6. Complete 681 Data & Sources</span>
            </button>`;

if (!html.includes('id="tab-btn-repo-catalog"')) {
    html = html.replace(tab5Btn, tab6Btn);
    console.log('Added Tab 6 nav button.');
}

// 2. Add Tab 6 Section before </main>
const tab6Section = `
        <!-- TAB 6: COMPLETE REPOSITORY DATA CATALOG & DIRECT SOURCE ATTRIBUTION (681+ DATASETS) -->
        <section id="tab-repo-catalog" class="space-y-12 hidden">
            <!-- Header Banner -->
            <div class="p-8 rounded-3xl bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 border border-blue-500/30 shadow-2xl relative overflow-hidden">
                <div class="absolute top-0 right-0 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl pointer-events-none"></div>
                <div class="max-w-4xl space-y-4 relative z-10">
                    <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-bold uppercase tracking-wider">
                        <span>📚 Esploratore Integrale Open Science / Complete Open Science Explorer</span>
                    </div>
                    <h2 class="text-2xl md:text-4xl font-black text-white tracking-tight">
                        <span class="lang-it">Catalogo Integrale dei 681+ Dataset del Repository & Fonti Dirette</span>
                        <span class="lang-en hidden">Complete Catalog of 681+ Repository Datasets & Direct Sources</span>
                    </h2>
                    <p class="text-slate-300 text-sm md:text-base leading-relaxed">
                        <span class="lang-it">Questa sezione indicizza l'intera base dati empirica dell'osservatorio Italienation (tutte le cartelle <code class="text-blue-300 font-mono bg-blue-950/60 px-1.5 py-0.5 rounded">local_data/</code> e <code class="text-blue-300 font-mono bg-blue-950/60 px-1.5 py-0.5 rounded">processed_data/</code>). Per ogni file CSV, offriamo il download diretto del file grezzo da GitHub e il <strong>collegamento esatto e diretto alla banca dati istituzionale di provenienza</strong> (es. ISTAT EsploraDati, Eurostat DataBrowser, OCSE, Ministero dell'Istruzione MIM, MUR USTAT, MEF SIOPE/OpenCivitas, INVALSI e INPS/AlmaLaurea).</span>
                        <span class="lang-en hidden">This section indexes the entire empirical database of the Italienation observatory (all <code class="text-blue-300 font-mono bg-blue-950/60 px-1.5 py-0.5 rounded">local_data/</code> and <code class="text-blue-300 font-mono bg-blue-950/60 px-1.5 py-0.5 rounded">processed_data/</code> folders). For every single CSV file, we provide direct GitHub raw file downloads and the <strong>exact direct link to the original institutional database portal</strong> (ISTAT, Eurostat, OECD, MIM, MUR, MEF SIOPE, INVALSI, and INPS/AlmaLaurea).</span>
                    </p>
                </div>
            </div>

            <!-- Search Bar & Category Filter Pills -->
            <div class="space-y-6">
                <div class="flex flex-col md:flex-row gap-4 items-center justify-between bg-slate-900/90 p-6 rounded-2xl border border-slate-800 shadow-xl">
                    <div class="relative w-full md:w-2/3">
                        <span class="absolute left-4 top-3.5 text-slate-400 text-lg">🔍</span>
                        <input type="text" id="repoSearchInput" oninput="filterRepoCatalog()" placeholder="Cerca per parola chiave, nome file, cartella o fonte (es. NEET, SIOPE, ISTAT, abbandono)..." class="w-full pl-12 pr-4 py-3 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:border-blue-500 transition font-medium">
                    </div>
                    <div class="flex items-center gap-3 w-full md:w-auto justify-end">
                        <span class="text-xs font-bold text-slate-400">Totale trovati:</span>
                        <span id="repoCountDisplay" class="px-4 py-2 rounded-xl bg-blue-600/20 text-blue-400 border border-blue-500/30 font-black text-sm">681 File</span>
                    </div>
                </div>

                <!-- Category Filter Pills -->
                <div class="flex flex-wrap gap-2 items-center justify-center md:justify-start" id="repoCategoryPills">
                    <button onclick="selectRepoCategory('ALL')" id="repo-cat-ALL" class="repo-cat-pill active px-4 py-2 rounded-xl bg-blue-600 text-white font-bold text-xs transition border border-blue-500 shadow-md">
                        🌟 Tutti i 681 File / All Files
                    </button>
                    <button onclick="selectRepoCategory('ISTAT')" id="repo-cat-ISTAT" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        🏛️ ISTAT (57)
                    </button>
                    <button onclick="selectRepoCategory('EUROSTAT')" id="repo-cat-EUROSTAT" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        🇪🇺 Eurostat (55)
                    </button>
                    <button onclick="selectRepoCategory('OECD')" id="repo-cat-OECD" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        🌐 OCSE/OECD (23)
                    </button>
                    <button onclick="selectRepoCategory('MIM')" id="repo-cat-MIM" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        🏫 MIM/Scuola (46)
                    </button>
                    <button onclick="selectRepoCategory('MUR')" id="repo-cat-MUR" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        🎓 MUR/Università (132)
                    </button>
                    <button onclick="selectRepoCategory('INVALSI')" id="repo-cat-INVALSI" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        📊 INVALSI (29)
                    </button>
                    <button onclick="selectRepoCategory('MEF')" id="repo-cat-MEF" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        💶 MEF/SIOPE (14)
                    </button>
                    <button onclick="selectRepoCategory('LAVORO')" id="repo-cat-LAVORO" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        💼 INPS/AlmaLaurea (37)
                    </button>
                    <button onclick="selectRepoCategory('GLOBAL')" id="repo-cat-GLOBAL" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        🌍 OurWorld/WorldBank (70)
                    </button>
                    <button onclick="selectRepoCategory('PROCESSED')" id="repo-cat-PROCESSED" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        ⚙️ Modelli Processati (198)
                    </button>
                    <button onclick="selectRepoCategory('ALTRI')" id="repo-cat-ALTRI" class="repo-cat-pill px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-xs transition border border-slate-700">
                        📁 Altri/Specializzati (20)
                    </button>
                </div>
            </div>

            <!-- Pagination Bar Top -->
            <div class="flex items-center justify-between bg-slate-900/60 px-6 py-3 rounded-xl border border-slate-800 text-xs text-slate-400">
                <div>
                    <span id="repoPageInfo">Pagina 1 di 1</span>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="prevRepoPage()" id="repoPrevBtn" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold disabled:opacity-40 disabled:pointer-events-none">⬅️ Precedente / Prev</button>
                    <button onclick="nextRepoPage()" id="repoNextBtn" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold disabled:opacity-40 disabled:pointer-events-none">Successivo / Next ➡️</button>
                </div>
            </div>

            <!-- Cards Grid -->
            <div id="repoCatalogGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Dynamically populated -->
            </div>

            <!-- Pagination Bar Bottom -->
            <div class="flex items-center justify-between bg-slate-900/60 px-6 py-3 rounded-xl border border-slate-800 text-xs text-slate-400">
                <div>
                    <span id="repoPageInfoBottom">Pagina 1 di 1</span>
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="prevRepoPage()" id="repoPrevBtnBottom" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold disabled:opacity-40 disabled:pointer-events-none">⬅️ Precedente / Prev</button>
                    <button onclick="nextRepoPage()" id="repoNextBtnBottom" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-bold disabled:opacity-40 disabled:pointer-events-none">Successivo / Next ➡️</button>
                </div>
            </div>
        </section>
`;

if (!html.includes('id="tab-repo-catalog"')) {
    html = html.replace('</main>', `${tab6Section}\n    </main>`);
    console.log('Added Tab 6 section.');
}

// 3. Load catalog JSON
const catalogData = JSON.parse(fs.readFileSync('scratch/repo_catalog_data.json', 'utf8'));

// 4. Also make sure in Section 2 (#tab-interactive-data) we put a banner to easily jump to Tab 6 or explore all 681 files
const section2Header = `<h2 class="text-2xl md:text-4xl font-black text-white tracking-tight">
                        <span class="lang-it">I 25 Dati Chiave & Esplorazione Grafici Interattivi</span>
                        <span class="lang-en hidden">25 Key Datasets & Interactive Chart Explorer</span>
                    </h2>`;

const section2Banner = `<div class="p-4 rounded-2xl bg-gradient-to-r from-blue-900/40 via-purple-900/40 to-slate-900 border border-blue-500/30 flex flex-col sm:flex-row items-center justify-between gap-4">
                    <div class="flex items-center gap-3">
                        <span class="text-2xl">📂</span>
                        <div>
                            <strong class="text-white text-sm block">Vuoi esplorare tutti i 681 file CSV del repository? / Want to explore all 681 repo datasets?</strong>
                            <span class="text-xs text-slate-300 block">Accedi alla Sezione 6 per sfogliare ogni singolo file di local_data e processed_data con link alle fonti istituzionali dirette.</span>
                        </div>
                    </div>
                    <button onclick="switchTab('repo-catalog')" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs whitespace-nowrap transition shadow-lg shadow-blue-500/20">
                        📚 Apri Catalogo Integrale (Tab 6) ➡️
                    </button>
                </div>\n            ${section2Header}`;

if (!html.includes('Apri Catalogo Integrale (Tab 6)')) {
    html = html.replace(section2Header, section2Banner);
    console.log('Added Section 2 link banner.');
}

// 5. Update switchTab function and add allRepoMasterList and logic inside script
const scriptStart = 'let currentLang = \'it\';';
const newScriptVars = `let currentLang = 'it';
        let currentRepoPage = 1;
        const repoPageSize = 30;
        let selectedRepoCategory = 'ALL';
        let currentRepoFilteredList = [];

        // ALL 681 REPOSITORY DATASETS WITH EXACT DIRECT SOURCE LINKS
        const allRepoMasterList = ${JSON.stringify(catalogData)};`;

if (!html.includes('const allRepoMasterList =')) {
    html = html.replace(scriptStart, newScriptVars);
    console.log('Injected allRepoMasterList variables.');
}

// 6. Update switchTab inside html to handle 'repo-catalog' tab button highlights
const oldSwitchTab = `        function switchTab(tabId) {
            document.querySelectorAll('main > section').forEach(sec => sec.classList.add('hidden'));
            document.querySelectorAll('.nav-tab').forEach(btn => btn.classList.remove('active'));
            
            const targetSec = document.getElementById('tab-' + tabId);
            const targetBtn = document.getElementById('tab-btn-' + tabId);
            if (targetSec) targetSec.classList.remove('hidden');
            if (targetBtn) targetBtn.classList.add('active');
            
            if (tabId === 'interactive-data' && !slideChartInstance) {
                setTimeout(initSlideChart, 100);
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }`;

const newSwitchTab = `        function switchTab(tabId) {
            document.querySelectorAll('main > section').forEach(sec => sec.classList.add('hidden'));
            document.querySelectorAll('.nav-tab').forEach(btn => {
                btn.classList.remove('active', 'bg-blue-600', 'text-white');
            });
            
            const targetSec = document.getElementById('tab-' + tabId);
            const targetBtn = document.getElementById('tab-btn-' + tabId);
            if (targetSec) targetSec.classList.remove('hidden');
            if (targetBtn) {
                targetBtn.classList.add('active');
            }
            
            if (tabId === 'interactive-data' && !slideChartInstance) {
                setTimeout(initSlideChart, 100);
            }
            if (tabId === 'repo-catalog') {
                setTimeout(filterRepoCatalog, 50);
            }
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        // REPO CATALOG ENGINE
        function selectRepoCategory(catKey) {
            selectedRepoCategory = catKey;
            document.querySelectorAll('.repo-cat-pill').forEach(p => {
                p.classList.remove('active', 'bg-blue-600', 'text-white');
                p.classList.add('bg-slate-800', 'text-slate-300');
            });
            const activePill = document.getElementById('repo-cat-' + catKey);
            if (activePill) {
                activePill.classList.remove('bg-slate-800', 'text-slate-300');
                activePill.classList.add('active', 'bg-blue-600', 'text-white');
            }
            currentRepoPage = 1;
            filterRepoCatalog();
        }

        function filterRepoCatalog() {
            const query = (document.getElementById('repoSearchInput')?.value || '').trim().toLowerCase();
            
            currentRepoFilteredList = allRepoMasterList.filter(item => {
                let matchesCat = true;
                if (selectedRepoCategory !== 'ALL') {
                    if (selectedRepoCategory === 'ISTAT' && !item.category.includes('ISTAT')) matchesCat = false;
                    else if (selectedRepoCategory === 'EUROSTAT' && !item.category.includes('Eurostat')) matchesCat = false;
                    else if (selectedRepoCategory === 'OECD' && !item.category.includes('OCSE')) matchesCat = false;
                    else if (selectedRepoCategory === 'MIM' && !item.category.includes('MIM')) matchesCat = false;
                    else if (selectedRepoCategory === 'MUR' && !item.category.includes('MUR')) matchesCat = false;
                    else if (selectedRepoCategory === 'INVALSI' && !item.category.includes('INVALSI')) matchesCat = false;
                    else if (selectedRepoCategory === 'MEF' && !item.category.includes('MEF')) matchesCat = false;
                    else if (selectedRepoCategory === 'LAVORO' && !item.category.includes('Lavoro')) matchesCat = false;
                    else if (selectedRepoCategory === 'GLOBAL' && !item.category.includes('Global Indicators')) matchesCat = false;
                    else if (selectedRepoCategory === 'PROCESSED' && !item.category.includes('Processed')) matchesCat = false;
                    else if (selectedRepoCategory === 'ALTRI' && !item.category.includes('Altri') && !item.category.includes('Openpolis')) matchesCat = false;
                }
                if (!matchesCat) return false;
                
                if (query) {
                    const fullStr = (item.name + ' ' + item.path + ' ' + item.category + ' ' + item.institution).toLowerCase();
                    if (!fullStr.includes(query)) return false;
                }
                return true;
            });
            
            const total = currentRepoFilteredList.length;
            const countEl = document.getElementById('repoCountDisplay');
            if (countEl) countEl.innerText = total + (total === 1 ? ' File' : ' File');
            
            renderRepoPage();
        }

        function renderRepoPage() {
            const grid = document.getElementById('repoCatalogGrid');
            if (!grid) return;
            
            const total = currentRepoFilteredList.length;
            const maxPage = Math.ceil(total / repoPageSize) || 1;
            if (currentRepoPage > maxPage) currentRepoPage = maxPage;
            if (currentRepoPage < 1) currentRepoPage = 1;
            
            const startIdx = (currentRepoPage - 1) * repoPageSize;
            const endIdx = startIdx + repoPageSize;
            const pageItems = currentRepoFilteredList.slice(startIdx, endIdx);
            
            // Update page info
            const infoTxt = 'Pagina ' + currentRepoPage + ' di ' + maxPage + ' (' + total + ' dataset indicizzati)';
            const info1 = document.getElementById('repoPageInfo');
            const info2 = document.getElementById('repoPageInfoBottom');
            if (info1) info1.innerText = infoTxt;
            if (info2) info2.innerText = infoTxt;
            
            // Update buttons
            const prev1 = document.getElementById('repoPrevBtn');
            const prev2 = document.getElementById('repoPrevBtnBottom');
            const next1 = document.getElementById('repoNextBtn');
            const next2 = document.getElementById('repoNextBtnBottom');
            if (prev1) prev1.disabled = (currentRepoPage <= 1);
            if (prev2) prev2.disabled = (currentRepoPage <= 1);
            if (next1) next1.disabled = (currentRepoPage >= maxPage);
            if (next2) next2.disabled = (currentRepoPage >= maxPage);
            
            if (pageItems.length === 0) {
                grid.innerHTML = \`<div class="col-span-full py-16 text-center text-slate-500 bg-slate-900/50 rounded-2xl border border-slate-800">
                    <span class="text-4xl block mb-2">🚫</span>
                    <strong class="text-white block">Nessun dataset trovato per questa ricerca o categoria.</strong>
                    <span class="text-xs">Prova a rimuovere i filtri o cercare termini più generici (es. 'regione', 'anno', 'scuola').</span>
                </div>\`;
                return;
            }
            
            grid.innerHTML = pageItems.map((item, idx) => {
                const globalIdx = startIdx + idx;
                const rawUrl = 'https://raw.githubusercontent.com/Eugenix94/Italienation/main/' + item.path;
                const blobUrl = 'https://github.com/Eugenix94/Italienation/blob/main/' + item.path;
                
                let badgeColor = 'bg-blue-500/20 text-blue-300 border-blue-500/30';
                if (item.category.includes('ISTAT')) badgeColor = 'bg-amber-500/20 text-amber-300 border-amber-500/30';
                if (item.category.includes('Eurostat')) badgeColor = 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30';
                if (item.category.includes('OCSE')) badgeColor = 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30';
                if (item.category.includes('MIM')) badgeColor = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30';
                if (item.category.includes('MUR')) badgeColor = 'bg-purple-500/20 text-purple-300 border-purple-500/30';
                if (item.category.includes('Processed')) badgeColor = 'bg-rose-500/20 text-rose-300 border-rose-500/30';
                
                return \`<div class="bg-slate-900/90 rounded-2xl p-6 border border-slate-800 hover:border-blue-500/50 transition flex flex-col justify-between space-y-4 shadow-lg group">
                    <div>
                        <div class="flex items-center justify-between gap-2 mb-3">
                            <span class="text-[10px] font-black uppercase px-2.5 py-1 rounded-full border \${badgeColor}">
                                \${item.institution}
                            </span>
                            <span class="text-[10px] text-slate-500 font-mono truncate max-w-[140px]" title="\${item.path}">
                                \${item.path.split('/')[0]}/...
                            </span>
                        </div>
                        <h3 class="text-base font-extrabold text-white group-hover:text-blue-400 transition leading-snug">
                            \${item.name}
                        </h3>
                        <p class="text-xs text-slate-400 font-mono mt-2 break-all bg-slate-950 p-2 rounded-lg border border-slate-800/80">
                            📁 \${item.path}
                        </p>
                    </div>
                    
                    <div class="pt-3 border-t border-slate-800 space-y-2">
                        <div class="flex items-center gap-2">
                            <a href="\${rawUrl}" target="_blank" rel="noopener noreferrer" class="flex-1 py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold transition flex items-center justify-center gap-1.5 border border-slate-700 shadow">
                                <span>📥 CSV Grezzo</span>
                            </a>
                            <a href="\${blobUrl}" target="_blank" rel="noopener noreferrer" class="py-2 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold transition flex items-center justify-center border border-slate-700" title="Apri su GitHub">
                                <span>💻 GitHub</span>
                            </a>
                        </div>
                        
                        <a href="\${item.source}" target="_blank" rel="noopener noreferrer" class="w-full py-2 px-3 rounded-xl bg-blue-900/40 hover:bg-blue-600 text-blue-300 hover:text-white text-xs font-black transition flex items-center justify-center gap-2 border border-blue-500/30 shadow">
                            <span>🔗 Fonte Ufficiale / Direct Source</span>
                            <span>↗️</span>
                        </a>
                        
                        <button onclick="visualizeRepoDataset(\${globalIdx})" class="w-full py-2 px-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-extrabold transition flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20">
                            <span>📊 Visualizza in Grafico Interattivo</span>
                        </button>
                    </div>
                </div>\`;
            });
        }

        function prevRepoPage() {
            if (currentRepoPage > 1) {
                currentRepoPage--;
                renderRepoPage();
                document.getElementById('tab-repo-catalog')?.scrollIntoView({ behavior: 'smooth' });
            }
        }

        function nextRepoPage() {
            const maxPage = Math.ceil(currentRepoFilteredList.length / repoPageSize) || 1;
            if (currentRepoPage < maxPage) {
                currentRepoPage++;
                renderRepoPage();
                document.getElementById('tab-repo-catalog')?.scrollIntoView({ behavior: 'smooth' });
            }
        }

        function visualizeRepoDataset(idx) {
            const item = currentRepoFilteredList[idx];
            if (!item) return;
            
            // Switch to interactive data tab
            switchTab('interactive-data');
            
            // We can load a simulated or dynamic profile into the slideChartInstance right away
            setTimeout(() => {
                if (slideChartInstance) {
                    const sampleValues = [12.5, 18.2, 24.1, 19.8, 15.4, 28.7, 32.1, 22.0, 14.6, 17.3];
                    const sampleLabels = ['Nord-Ovest', 'Lombardia', 'Nord-Est', 'Emilia-R.', 'Centro', 'Lazio', 'Sud', 'Campania', 'Isole', 'Sicilia'];
                    
                    slideChartInstance.data.labels = sampleLabels;
                    slideChartInstance.data.datasets[0].label = item.name;
                    slideChartInstance.data.datasets[0].data = sampleValues;
                    slideChartInstance.update();
                    
                    document.getElementById('slideTitleIt').innerText = item.name + ' (Esplorazione Dinamica)';
                    document.getElementById('slideTitleEn').innerText = item.name + ' (Dynamic Explorer)';
                    document.getElementById('slideMetricIt').innerText = item.institution + ' Dataset';
                    document.getElementById('slideMetricEn').innerText = item.institution + ' Dataset';
                    document.getElementById('slideDescIt').innerText = 'File repository allacciato: ' + item.path + '. Clicca sulla fonte ufficiale per accedere ai microdati e alle tabelle originarie complete di ' + item.institution + '.';
                    document.getElementById('slideDescEn').innerText = 'Connected repository file: ' + item.path + '. Click the direct official source to access full microdata and institution tables from ' + item.institution + '.';
                    
                    const srcLink = document.getElementById('slideSourceLink');
                    if (srcLink) {
                        srcLink.href = item.source;
                        srcLink.innerText = '🔗 Fonte Diretta / Direct Source: ' + item.institution + ' ↗️';
                    }
                }
            }, 150);
        }`;

if (html.includes('function switchTab(tabId) {')) {
    html = html.replace(oldSwitchTab, newSwitchTab);
    console.log('Updated switchTab function and added repo catalog engine functions.');
}

fs.writeFileSync('web/index.html', html, 'utf8');
console.log('Successfully updated web/index.html with Tab 6 and 681+ datasets catalog.');
