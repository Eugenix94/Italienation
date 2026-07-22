import json
from pathlib import Path

def build_v6():
    print("Loading data for v6 frontend...")
    
    with open('processed_data/provincial_map_agg.json', 'r', encoding='utf-8') as f:
        provincial_data = json.load(f)
        
    with open('processed_data/curriculum_matrix.json', 'r', encoding='utf-8') as f:
        curriculum_matrix = json.load(f)

    with open('original_frontend.html', 'r', encoding='utf-8') as f:
        html = f.read()

    head_injection = """
    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    <style>
        #map { height: 500px; width: 100%; border-radius: 1rem; z-index: 10; border: 1px solid rgba(63,63,70,.5); }
        .leaflet-container { background: #09090b; font-family: 'Inter', sans-serif; }
        .leaflet-popup-content-wrapper { background: #18181b; color: #fafafa; border: 1px solid #3f3f46; border-radius: 0.5rem; }
        .leaflet-popup-tip { background: #18181b; border: 1px solid #3f3f46; }
    </style>
</head>
"""
    html = html.replace('</head>', head_injection)

    desk_nav_inj = """<a href="#geospatial"><span class="i18n" data-it="🗺️ Territorio" data-en="🗺️ Geospatial"></span></a>
            <a href="#comparison">"""
    html = html.replace('<a href="#comparison">', desk_nav_inj)

    geospatial_html = """
<!-- ========================== -->
<!-- §2.5 GEOSPATIAL REALITY    -->
<!-- ========================== -->
<section id="geospatial" class="space-y-6 pt-12">
    <h2 class="text-2xl sm:text-3xl font-extrabold text-white"><span class="i18n" data-it="🗺️ Mappa delle Disuguaglianze" data-en="🗺️ The Geospatial Reality"></span></h2>
    <p class="text-zinc-500 text-sm"><span class="i18n" data-it="Densità e tipologia delle scuole superiori per provincia. Clicca sulle bolle per il Profilatore Regionale." data-en="Density and typology of upper secondary schools by province. Click bubbles for the Regional Profiler."></span></p>
    
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div class="lg:col-span-3">
            <div id="map" class="shadow-2xl"></div>
        </div>
        
        <div id="sidebar" class="glass rounded-2xl p-6 border border-indigo-500/30 bg-gradient-to-br from-zinc-900 to-indigo-950/20 hidden lg:flex flex-col h-full shadow-xl">
            <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg font-black text-white uppercase tracking-wider">Regional Profiler</h3>
                <span id="sidebar-title" class="text-xs font-bold text-indigo-400 bg-indigo-500/10 px-2 py-1 rounded">NUTS-3</span>
            </div>
            
            <div id="sidebar-stats" class="grid grid-cols-1 gap-4 mb-6">
                <!-- Populated via JS -->
            </div>
            
            <div class="mt-auto">
                <div class="text-[10px] text-zinc-500 font-bold uppercase tracking-widest mb-2 text-center">Track Distribution</div>
                <div class="w-full h-40 relative"><canvas id="regionalPie"></canvas></div>
            </div>
        </div>
    </div>
</section>
"""
    html = html.replace('</section>\n\n<!-- ================================= -->\n<!-- §3 ITALY vs WORLD COMPARISON', '</section>\n' + geospatial_html + '\n<!-- ================================= -->\n<!-- §3 ITALY vs WORLD COMPARISON')

    calc_html = """
    <!-- THE TRIPARTITE CALCULATOR -->
    <div class="glass rounded-2xl p-6 border border-emerald-500/30 bg-gradient-to-br from-emerald-950/20 to-zinc-900/60 mt-8">
        <div class="flex items-center gap-3 mb-4">
            <span class="text-2xl">🧮</span>
            <h3 class="text-xl font-bold text-white"><span class="i18n" data-it="Calcolatore del Rischio NEET" data-en="NEET Risk Calculator"></span></h3>
        </div>
        <p class="text-sm text-zinc-400 mb-6"><span class="i18n" data-it="Seleziona area geografica e percorso scolastico per stimare il rischio di abbandono e la vulnerabilità lavorativa." data-en="Select geographic area and school track to estimate dropout risk and labor vulnerability."></span></p>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-6">
            <div>
                <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-1">Select Region</label>
                <select id="calcRegion" class="w-full bg-zinc-900 border border-zinc-700 text-zinc-200 rounded-lg p-2 text-sm">
                    <option value="12">North (e.g. Lombardy)</option>
                    <option value="18">Center (e.g. Lazio)</option>
                    <option value="28">South (e.g. Campania/Sicily)</option>
                </select>
            </div>
            <div>
                <label class="block text-[10px] font-bold text-zinc-500 uppercase tracking-widest mb-1">School Track</label>
                <select id="calcType" class="w-full bg-zinc-900 border border-zinc-700 text-zinc-200 rounded-lg p-2 text-sm">
                    <option value="liceo">Liceo (Academic)</option>
                    <option value="tech">Istituto Tecnico</option>
                    <option value="prof">Istituto Professionale</option>
                </select>
            </div>
        </div>
        
        <div class="grid grid-cols-2 gap-4 text-center">
            <div class="bg-zinc-950/80 p-4 rounded-xl border border-red-500/20 shadow-inner">
                <div class="text-3xl font-black text-red-400" id="calcDropout">--%</div>
                <div class="text-[10px] font-bold text-zinc-500 uppercase mt-1">Grade Repetition Risk</div>
            </div>
            <div class="bg-zinc-950/80 p-4 rounded-xl border border-amber-500/20 shadow-inner">
                <div class="text-3xl font-black text-amber-400" id="calcPrecarity">--%</div>
                <div class="text-[10px] font-bold text-zinc-500 uppercase mt-1">Est. NEET Probability</div>
            </div>
        </div>
    </div>
    
    <!-- CURRICULUM MATRIX -->
    <div class="glass rounded-2xl p-6 border border-zinc-700 mt-8" id="curriculum-matrix">
        <h3 class="text-xl font-bold text-white mb-2"><span class="i18n" data-it="Matrice del Capitale Culturale" data-en="Cultural Capital Matrix"></span></h3>
        <p class="text-sm text-zinc-400 mb-4"><span class="i18n" data-it="Materie insegnate per ramo (Frequenza adozioni libri di testo)." data-en="Subjects taught per branch (Textbook adoption frequency)."></span></p>
        
        <div class="flex gap-2 mb-4">
            <button onclick="renderCurriculum('Liceo')" class="curr-tab active px-3 py-1 rounded bg-blue-600/20 text-blue-400 border border-blue-500/50 text-xs font-bold uppercase">Liceo</button>
            <button onclick="renderCurriculum('Tecnico')" class="curr-tab px-3 py-1 rounded bg-emerald-600/20 text-emerald-400 border border-emerald-500/50 text-xs font-bold uppercase">Tecnico</button>
            <button onclick="renderCurriculum('Professionale')" class="curr-tab px-3 py-1 rounded bg-orange-600/20 text-orange-400 border border-orange-500/50 text-xs font-bold uppercase">Professionale</button>
        </div>
        
        <div class="max-h-64 overflow-y-auto bg-zinc-950/80 rounded border border-zinc-800 p-2">
            <table class="w-full text-left text-xs text-zinc-300">
                <thead class="sticky top-0 bg-zinc-900">
                    <tr><th class="p-2 font-bold uppercase tracking-widest text-zinc-500">Subject</th><th class="p-2 font-bold uppercase tracking-widest text-zinc-500 text-right">Schools</th></tr>
                </thead>
                <tbody id="curr-tbody">
                </tbody>
            </table>
        </div>
    </div>
"""
    html = html.replace('<!-- LEGISLATIVE MILESTONES SWITCHER -->', calc_html + '\n    <!-- LEGISLATIVE MILESTONES SWITCHER -->')

    frontiers_html = """
<!-- ========================== -->
<!-- §5.5 METHODOLOGICAL FRONTIERS -->
<!-- ========================== -->
<section id="frontiers" class="space-y-6 pt-12">
    <h2 class="text-2xl sm:text-3xl font-extrabold text-white"><span class="i18n" data-it="⚠️ Punti Ciechi dei Dati (Limiti Metodologici)" data-en="⚠️ Methodological Frontiers (Blind Spots)"></span></h2>
    <p class="text-zinc-500 text-sm"><span class="i18n" data-it="I dati amministrativi non sono neutri. Nascondono fratture sociologiche profonde (Dati ISTAT, SVIMEZ, INVALSI 2023-2024)." data-en="Administrative data is not neutral. It masks deep sociological fractures (ISTAT, SVIMEZ, INVALSI data 2023-2024)."></span></p>
    
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <!-- Card 1 -->
        <div class="glass rounded-xl p-5 border-l-4 border-l-amber-500 transition-all hover:bg-amber-900/10">
            <h3 class="text-base font-bold text-amber-400 mb-2">1. Lavoro Nero (Shadow Economy)</h3>
            <p class="text-xs text-zinc-400 leading-relaxed mb-3">Administrative data treats informal labor as unemployment. In reality, the ISTAT 2025 report reveals <span class="font-bold text-amber-300">3.13 million irregular workers</span> in 2023, generating 10.2% of the national GDP (€217B). The NEET data partially masks a thriving, highly exploitative parallel economy.</p>
            <span class="text-[9px] uppercase tracking-widest font-bold text-amber-500 bg-amber-500/10 px-2 py-1 rounded">Source: ISTAT (2025)</span>
        </div>
        <!-- Card 2 -->
        <div class="glass rounded-xl p-5 border-l-4 border-l-amber-500 transition-all hover:bg-amber-900/10">
            <h3 class="text-base font-bold text-amber-400 mb-2">2. Gendered Caregiving Chasm</h3>
            <p class="text-xs text-zinc-400 leading-relaxed mb-3">A massive percentage of female NEETs are engaged in full-time, unpaid domestic labor. ISTAT (2024) confirms <span class="font-bold text-amber-300">29% of female NEETs are inactive due to family responsibilities</span>, compared to just 2.7% of men. The data falsely labels them as "inactive".</p>
            <span class="text-[9px] uppercase tracking-widest font-bold text-amber-500 bg-amber-500/10 px-2 py-1 rounded">Source: ISTAT (2024)</span>
        </div>
        <!-- Card 3 -->
        <div class="glass rounded-xl p-5 border-l-4 border-l-amber-500 transition-all hover:bg-amber-900/10">
            <h3 class="text-base font-bold text-amber-400 mb-2">3. Demographic Attrition</h3>
            <p class="text-xs text-zinc-400 leading-relaxed mb-3">The "fuga dei talenti" (brain drain) acts as a statistical centrifuge. The SVIMEZ 2024 Report states <span class="font-bold text-amber-300">350,000 graduates under 35 left the South between 2002 and 2024</span>, costing the South €6.8 billion annually. This shifting denominator artificially inflates local NEET rates.</p>
            <span class="text-[9px] uppercase tracking-widest font-bold text-amber-500 bg-amber-500/10 px-2 py-1 rounded">Source: SVIMEZ Report (2024)</span>
        </div>
        <!-- Card 4 -->
        <div class="glass rounded-xl p-5 border-l-4 border-l-amber-500 transition-all hover:bg-amber-900/10">
            <h3 class="text-base font-bold text-amber-400 mb-2">4. Dispersione Implicita</h3>
            <p class="text-xs text-zinc-400 leading-relaxed mb-3">Not all dropouts leave the system. INVALSI 2024 tests reveal that <span class="font-bold text-amber-300">6.6% of students graduate without basic functional literacy</span>. The system passes them anyway, creating a massive cohort who possess a diploma but no employable skills.</p>
            <span class="text-[9px] uppercase tracking-widest font-bold text-amber-500 bg-amber-500/10 px-2 py-1 rounded">Source: INVALSI (2024)</span>
        </div>
    </div>
</section>
"""
    html = html.replace('<!-- ====================== -->\n<!-- §6 RAW DATA SOURCES    -->', frontiers_html + '\n<!-- ====================== -->\n<!-- §6 RAW DATA SOURCES    -->')

    js_payload = f"""
    <!-- UI JS PAYLOAD -->
    <script>
        // 1. Map Initialization
        try {{
            const map = L.map('map', {{ center: [41.8719, 12.5674], zoom: 6, zoomControl: false }});
            L.control.zoom({{ position: 'bottomright' }}).addTo(map);
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{ attribution: '&copy; CARTO', maxZoom: 20 }}).addTo(map);

            const provData = {json.dumps(provincial_data)};
            
            // Loop over provinces and add proportional circles
            for (const prov in provData) {{
                const d = provData[prov];
                if(d.lat && d.lon) {{
                    // Calculate a proportional radius (min 5, max 30)
                    const radius = Math.max(5, Math.min(30, Math.sqrt(d.Total) * 1.5));
                    
                    // Determine dominant color
                    let color = '#3b82f6'; // Liceo
                    if (d.Professionale > d.Liceo && d.Professionale > d.Tecnico) color = '#f97316';
                    else if (d.Tecnico > d.Liceo && d.Tecnico > d.Professionale) color = '#10b981';

                    const marker = L.circleMarker([d.lat, d.lon], {{
                        radius: radius,
                        fillColor: color,
                        color: '#09090b',
                        weight: 1,
                        opacity: 1,
                        fillOpacity: 0.7
                    }});
                    
                    marker.provData = d;
                    marker.bindPopup(`<div class="font-bold text-white text-sm mb-1">${{prov}}</div><div class="text-xs text-zinc-300">Total Schools: ${{d.Total}}</div>`);
                    marker.addTo(map);
                    
                    marker.on('click', function(e) {{
                        const p = e.target.provData;
                        document.getElementById('sidebar').classList.remove('hidden');
                        document.getElementById('sidebar-title').innerText = p.provincia || prov;
                        
                        document.getElementById('sidebar-stats').innerHTML = `
                            <div class="bg-zinc-950/80 p-3 rounded-xl border border-zinc-700/50">
                                <div class="text-[10px] text-zinc-400 font-bold uppercase mb-1">Total Secondary Schools</div>
                                <div class="text-2xl font-black text-white">${{p.Total}}</div>
                            </div>
                        `;

                        if (window.rPie) window.rPie.destroy();
                        window.rPie = new Chart(document.getElementById('regionalPie'), {{
                            type: 'doughnut',
                            data: {{
                                labels: ['Liceo', 'Tecnico', 'Professionale'],
                                datasets: [{{ data: [p.Liceo, p.Tecnico, p.Professionale], backgroundColor: ['#3b82f6', '#10b981', '#f97316'], borderWidth: 0 }}]
                            }},
                            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
                        }});
                    }});
                }}
            }}
        }} catch(e) {{ console.log("Map init failed", e); }}

        // 2. Calculator Logic
        const calcRegion = document.getElementById('calcRegion');
        const calcType = document.getElementById('calcType');
        function updateCalculator() {{
            if(!calcRegion || !calcType) return;
            const r = parseFloat(calcRegion.value);
            const t = calcType.value;
            let dropout = (t === 'liceo') ? 3 : (t === 'tech') ? 9 : 14.8;
            if (r > 20) dropout += 4;
            document.getElementById('calcDropout').innerText = dropout.toFixed(1) + '%';
            document.getElementById('calcPrecarity').innerText = (20 + (r/2)).toFixed(1) + '%';
        }}
        if(calcRegion && calcType) {{
            calcRegion.addEventListener('change', updateCalculator);
            calcType.addEventListener('change', updateCalculator);
            updateCalculator();
        }}
        
        // 3. Curriculum Matrix Logic
        const curriculumMatrix = {json.dumps(curriculum_matrix)};
        function renderCurriculum(branch) {{
            // update tabs
            document.querySelectorAll('.curr-tab').forEach(btn => {{
                btn.classList.remove('active');
                if(btn.innerText === branch) btn.classList.add('active');
            }});
            
            const tbody = document.getElementById('curr-tbody');
            if(!tbody) return;
            
            const subjects = curriculumMatrix[branch] || [];
            tbody.innerHTML = subjects.map(s => `
                <tr class="border-b border-zinc-800/50 hover:bg-zinc-800/20 transition-colors">
                    <td class="p-2">${{s.subject}}</td>
                    <td class="p-2 text-right font-mono text-zinc-400">${{s.schools}}</td>
                </tr>
            `).join('');
        }}
        // Init table
        renderCurriculum('Liceo');
        
    </script>
</body>"""
    html = html.replace('</body>', js_payload)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully built v6 frontend at index.html")

if __name__ == '__main__':
    build_v6()
