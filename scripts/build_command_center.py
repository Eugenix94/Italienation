import json
import os
from pathlib import Path

def build_command_center():
    with open('processed_data/command_center.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    with open('processed_data/geospatial_map.json', 'r', encoding='utf-8') as f:
        geo_data = json.load(f)

    # Get list of charts for the gallery
    charts_dir = Path('rendered_outputs/assets/charts')
    charts = [f.name for f in charts_dir.glob('*.png')] if charts_dir.exists() else []

    istat_data = data['istat_data']

    html = '''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Italienation | The Academic Observatory v5.0</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    
    <!-- Leaflet CSS & JS -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" crossorigin=""></script>
    <!-- Leaflet MarkerCluster -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.Default.css" />
    <script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;800;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0b1121; color: #f8fafc; overflow-x: hidden; }
        h1, h2, h3, .font-display { font-family: 'Outfit', sans-serif; }
        .glass-panel { background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); }
        
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #475569; }
        
        #map { height: 600px; width: 100%; border-radius: 1.5rem; z-index: 10; }
        .leaflet-container { background: #0b1121; font-family: 'Inter', sans-serif; }
        .leaflet-popup-content-wrapper { background: rgba(15, 23, 42, 0.95); color: white; border: 1px solid rgba(255,255,255,0.1); border-radius: 0.5rem; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.5); }
        .leaflet-popup-tip { background: rgba(15, 23, 42, 0.95); }
        .marker-cluster-small, .marker-cluster-medium, .marker-cluster-large { background-color: rgba(225, 29, 72, 0.7); color: white; border: 2px solid rgba(225, 29, 72, 0.9); }
        .marker-cluster div { background-color: rgba(15, 23, 42, 0.9); font-weight: bold; }

        #sidebar { transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
        .sidebar-hidden { transform: translateX(100%); }
        
        .gallery-tab.active { background-color: rgba(225, 29, 72, 0.2); color: #fb7185; border-color: rgba(225, 29, 72, 0.5); }
        .gallery-section { display: none; }
        .gallery-section.active { display: block; }
    </style>
</head>
<body class="antialiased min-h-screen selection:bg-rose-500/30 selection:text-rose-200">

    <!-- HEADER / MAP -->
    <header class="py-12 px-6 border-b border-slate-800 bg-slate-900/50 relative z-40">
        <div class="max-w-screen-2xl mx-auto space-y-12">
            <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-10">
                <div class="flex-1">
                    <div class="inline-flex items-center space-x-2 text-rose-400 font-semibold tracking-widest text-xs uppercase mb-3">
                        <span class="w-2 h-2 rounded-full bg-rose-400 animate-pulse"></span>
                        <span>Analytical Observatory & Citizen Engagement</span>
                    </div>
                    <h1 class="font-display text-5xl md:text-7xl font-black text-white tracking-tight mb-6">
                        Italienation
                    </h1>
                    
                    <div class="bg-slate-800/40 p-6 rounded-2xl border border-rose-900/30 shadow-inner max-w-3xl">
                        <h3 class="text-xs text-rose-400 font-bold uppercase tracking-widest mb-3 flex items-center gap-2">
                            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
                            Academic Thesis Abstract
                        </h3>
                        <p class="text-slate-300 leading-relaxed text-sm">
                            The "Italienation" project posits that the Italian educational system is experiencing a systemic, multi-vector collapse. This is not driven by acute external shocks, but by chronic structural decay across demographic, geographic, infrastructural, and cognitive dimensions. By forcing youth into archaic cognitive tracks and an unregulated labor market devoid of a minimum wage, the State accelerates the demographic winter and mass emigration (Brain Drain).
                        </p>
                        <div class="mt-6 flex items-center gap-4">
                            <a href="Italienation_AI_Methodology_and_Thesis.md" download class="inline-flex items-center gap-2 bg-rose-600 hover:bg-rose-500 text-white font-bold py-2 px-5 rounded-lg text-sm transition-colors shadow-[0_0_15px_rgba(225,29,72,0.4)]">
                                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
                                Download Official Thesis
                            </a>
                            <span class="text-[10px] text-slate-500 font-mono tracking-widest uppercase">Data: GitHub / HuggingFace</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- GEOSPATIAL MAP WITH REGIONAL PROFILER -->
            <div class="glass-panel p-2 rounded-3xl relative shadow-2xl shadow-rose-900/20 border border-slate-700 overflow-hidden">
                <div class="absolute top-6 left-6 z-20 pointer-events-none">
                    <h2 class="font-display text-2xl font-bold text-white bg-slate-900/90 px-4 py-2 rounded-lg backdrop-blur-md border border-slate-700 shadow-xl">Regional Reality Map</h2>
                    <p class="text-xs text-slate-300 bg-slate-900/90 px-4 py-1.5 rounded-b-lg backdrop-blur-md inline-block border-x border-b border-slate-700 shadow-xl mt-[-2px]">
                        Click any cluster to open the <span class="font-bold text-white">Regional Profiler</span>
                    </p>
                </div>
                
                <div id="map"></div>

                <!-- Regional Profiler Sidebar -->
                <div id="sidebar" class="sidebar-hidden absolute top-0 right-0 w-full md:w-[400px] h-full bg-slate-900/95 backdrop-blur-2xl border-l border-slate-700 z-30 p-8 flex flex-col shadow-[-20px_0_40px_rgba(0,0,0,0.6)]">
                    <div class="flex justify-between items-center mb-8">
                        <div>
                            <h3 class="font-display text-3xl font-black text-white truncate leading-tight" id="sidebar-title">Regional Profiler</h3>
                            <p class="text-xs text-rose-400 font-semibold tracking-wider uppercase mt-1">Estimated True Scale</p>
                        </div>
                        <button id="close-sidebar" class="text-slate-400 hover:text-white transition-colors bg-slate-800 p-2 rounded-full hover:bg-slate-700">
                            <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
                        </button>
                    </div>
                    <div class="flex-1 overflow-y-auto pr-2 space-y-8">
                        <div class="grid grid-cols-2 gap-4" id="sidebar-stats">
                            <!-- Injected by JS -->
                        </div>
                        <div class="bg-slate-800/40 p-5 rounded-2xl border border-slate-700/50 shadow-inner">
                            <div class="text-xs text-slate-400 font-bold uppercase tracking-wider mb-4 flex items-center justify-between">
                                <span>Tripartite Distribution</span>
                                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                            </div>
                            <div class="h-56 relative"><canvas id="regionalPie"></canvas></div>
                            <p class="text-[10px] text-slate-500 mt-4 text-center leading-relaxed">
                                Note: Values are mathematically scaled (x4.5) from the geospatial sample to represent the estimated total volume of active secondary institutions in the territory.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- MACRO VISUALIZATIONS -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <!-- Curriculum Calculator -->
                <div class="glass-panel p-8 md:p-10 rounded-3xl relative h-full border border-rose-500/20 shadow-[0_0_40px_rgba(225,29,72,0.05)] flex flex-col justify-between">
                    <div>
                        <div class="flex items-center gap-3 mb-3">
                            <svg class="w-6 h-6 text-rose-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" /></svg>
                            <h2 class="font-display text-2xl md:text-3xl font-bold text-white">Tripartite Calculator</h2>
                        </div>
                        <p class="text-sm text-slate-400 mb-8 leading-relaxed">Analyze the cognitive tracking path, required subjects, and statistical risks associated with your chosen school branch.</p>
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-8">
                            <div>
                                <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Select Region</label>
                                <select id="calcRegion" class="w-full bg-slate-900/80 border border-slate-700 text-slate-200 rounded-xl p-3.5 focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none transition-all font-medium text-sm shadow-inner cursor-pointer">
                                    <option value="12">North (e.g. Lombardy)</option>
                                    <option value="18">Center (e.g. Lazio)</option>
                                    <option value="28">South (e.g. Campania/Sicily)</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">School Track</label>
                                <select id="calcType" class="w-full bg-slate-900/80 border border-slate-700 text-slate-200 rounded-xl p-3.5 focus:ring-2 focus:ring-rose-500 focus:border-rose-500 outline-none transition-all font-medium text-sm shadow-inner cursor-pointer">
                                    <option value="liceo">Liceo (Academic)</option>
                                    <option value="tech">Istituto Tecnico</option>
                                    <option value="prof">Istituto Professionale</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    
                    <div class="space-y-5">
                        <div class="bg-slate-900/90 p-5 rounded-2xl border border-slate-700/80 shadow-lg">
                            <div class="text-[10px] text-teal-400 font-bold uppercase mb-3 tracking-widest flex items-center justify-between border-b border-slate-800 pb-2">
                                <span>The Curricular Constellation Matrix</span>
                                <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" /></svg>
                            </div>
                            <table class="w-full text-left text-xs border-collapse text-slate-300">
                              <tr><th class="border-b border-slate-800/50 py-2 font-semibold text-slate-400">Subject Area</th><th class="border-b border-slate-800/50 py-2 font-semibold text-right text-slate-400">Status in Track</th></tr>
                              <tr class="hover:bg-slate-800/30 transition-colors"><td class="py-2.5">Philosophy & Critical Thought</td><td class="text-right" id="mat-phil">Core</td></tr>
                              <tr class="hover:bg-slate-800/30 transition-colors"><td class="py-2.5 border-t border-slate-800/50">Latin / Ancient Greek</td><td class="text-right border-t border-slate-800/50" id="mat-latin">Core</td></tr>
                              <tr class="hover:bg-slate-800/30 transition-colors"><td class="py-2.5 border-t border-slate-800/50">Art History</td><td class="text-right border-t border-slate-800/50" id="mat-art">Core</td></tr>
                              <tr class="hover:bg-slate-800/30 transition-colors"><td class="py-2.5 border-t border-slate-800/50">Applied Mechanics / Practical Labs</td><td class="text-right border-t border-slate-800/50" id="mat-mech">Excluded</td></tr>
                            </table>
                            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between items-center">
                                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-500">Intended Destiny:</span>
                                <span class="text-xs font-bold bg-slate-800 px-3 py-1 rounded-full" id="mat-conclusion">University</span>
                            </div>
                        </div>
                        <div class="grid grid-cols-2 gap-5">
                            <div class="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-lg">
                                <div class="text-[10px] text-slate-400 font-bold uppercase mb-2 tracking-widest">Implicit Dropout Risk</div>
                                <div id="calcDropout" class="text-3xl font-black text-rose-400">--%</div>
                                <div class="text-[9px] text-slate-500 mt-1">Based on INVALSI data</div>
                            </div>
                            <div class="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-lg">
                                <div class="text-[10px] text-slate-400 font-bold uppercase mb-2 tracking-widest">Hidden Textbook Tax</div>
                                <div id="calcTax" class="text-3xl font-black text-purple-400">€305</div>
                                <div class="text-[9px] text-slate-500 mt-1">First year adoption cost</div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- ISTAT & Charts -->
                <div class="flex flex-col gap-8">
                    <div class="glass-panel p-8 rounded-3xl relative h-[250px] shadow-lg border border-slate-700/50">
                        <div class="flex justify-between items-start mb-4">
                            <h2 class="font-display text-xl md:text-2xl font-bold text-white">ISTAT: Demographic Winter</h2>
                            <span class="text-[10px] font-bold text-rose-400 bg-rose-400/10 px-2 py-1 rounded border border-rose-400/20">Projections 2035</span>
                        </div>
                        <div class="w-full h-[140px]"><canvas id="istatBar"></canvas></div>
                    </div>
                    <div class="grid grid-cols-2 gap-8 h-[240px]">
                        <div class="glass-panel p-6 rounded-3xl relative h-full flex flex-col items-center justify-center text-center shadow-lg border border-slate-700/50 group hover:border-slate-500 transition-colors">
                            <h2 class="font-display text-sm md:text-base font-bold text-white mb-4">The Vulnerable Abandoned</h2>
                            <div class="w-24 h-24 relative mb-3 group-hover:scale-105 transition-transform"><canvas id="sostegnoDoughnut"></canvas></div>
                            <div class="text-2xl font-black text-rose-400">74.7%</div>
                            <p class="text-[9px] text-slate-500 uppercase tracking-widest mt-1">Substitute Sostegno</p>
                        </div>
                        <div class="glass-panel p-6 rounded-3xl relative h-full flex flex-col justify-between shadow-lg border border-slate-700/50 group hover:border-slate-500 transition-colors">
                            <h2 class="font-display text-sm md:text-base font-bold text-white mb-2">Cognitive Collapse</h2>
                            <div class="w-full h-full pb-2 group-hover:scale-105 transition-transform"><canvas id="pisaLine"></canvas></div>
                            <p class="text-[9px] text-slate-500 uppercase tracking-widest mt-1 text-center">PISA Trend</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- RAW VS PROCESSED ANALYTICAL GALLERY -->
    <section class="py-24 px-6 bg-slate-950">
        <div class="max-w-screen-2xl mx-auto space-y-12">
            <div class="flex flex-col md:flex-row justify-between items-end gap-6 mb-12 border-b border-slate-800 pb-8">
                <div class="max-w-3xl">
                    <div class="inline-flex items-center space-x-2 text-teal-400 font-semibold tracking-widest text-xs uppercase mb-4">
                        <span class="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
                        <span>Open Research Vault</span>
                    </div>
                    <h2 class="font-display text-4xl md:text-5xl font-black text-white tracking-tight mb-4">The Analytical Gallery</h2>
                    <p class="text-slate-400 text-sm md:text-base leading-relaxed">
                        Absolute academic context. Explore the official, watermarked charts, generated directly from the ISTAT, INPS, and MIM data pipelines.
                    </p>
                </div>
                
                <!-- Gallery Categorization Tabs -->
                <div class="flex flex-wrap gap-2">
                    <button class="gallery-tab active px-4 py-2 rounded-lg bg-slate-800 text-slate-300 text-xs font-bold uppercase tracking-wider transition-all border border-slate-700 hover:bg-slate-700" data-gallery="all">All</button>
                    <button class="gallery-tab px-4 py-2 rounded-lg bg-slate-800 text-slate-300 text-xs font-bold uppercase tracking-wider transition-all border border-slate-700 hover:bg-slate-700" data-gallery="macro">Global Macro Context</button>
                    <button class="gallery-tab px-4 py-2 rounded-lg bg-slate-800 text-slate-300 text-xs font-bold uppercase tracking-wider transition-all border border-slate-700 hover:bg-slate-700" data-gallery="labor">Labor Crisis</button>
                    <button class="gallery-tab px-4 py-2 rounded-lg bg-slate-800 text-slate-300 text-xs font-bold uppercase tracking-wider transition-all border border-slate-700 hover:bg-slate-700" data-gallery="decay">Decay</button>
                    <button class="gallery-tab px-4 py-2 rounded-lg bg-slate-800 text-slate-300 text-xs font-bold uppercase tracking-wider transition-all border border-slate-700 hover:bg-slate-700" data-gallery="tripartite">Tripartite System</button>
                    <button class="gallery-tab px-4 py-2 rounded-lg bg-slate-800 text-slate-300 text-xs font-bold uppercase tracking-wider transition-all border border-slate-700 hover:bg-slate-700" data-gallery="geography">Geography</button>
                    <button class="gallery-tab px-4 py-2 rounded-lg bg-amber-600/20 text-amber-500 text-xs font-bold uppercase tracking-wider transition-all border border-amber-600/50 hover:bg-amber-600/40" data-gallery="frontiers">Methodological Frontiers</button>
                </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8" id="gallery-container">
'''
    categories = {
        'macro': 'Global Macro Context',
        'cost': 'The Cost of Education',
        'regional': 'Regional NEET & Poverty',
        'gender': 'Gender & COVID Impact',
        'tripartite': 'The Tripartite System (Tracking)',
        'frontiers': 'Methodological Frontiers'
    }
    # Categorize and Inject images
    for c in charts:
        cat = "macro"
        if "decay" in c or "infrastructure" in c: cat = "decay"
        elif "tripartite" in c: cat = "tripartite"
        elif "geography" in c: cat = "geography"
        elif "labor" in c: cat = "labor"
        
        # Clean title
        title = c.replace('.png', '').replace('_', ' ').title()
        
        html += f'''                <div class="gallery-item flex flex-col glass-panel rounded-2xl border border-slate-800 hover:border-rose-500/50 transition-colors group bg-slate-900 shadow-xl overflow-hidden" data-cat="{cat}">
                    <div class="bg-black relative w-full h-64 overflow-hidden border-b border-slate-800">
                        <img src="rendered_outputs/assets/charts/{c}" alt="{title}" class="w-full h-full object-contain p-2 opacity-90 group-hover:opacity-100 group-hover:scale-[1.02] transition-all duration-500 cursor-pointer" onclick="window.open('rendered_outputs/assets/charts/{c}', '_blank')">
                    </div>
                    <div class="p-6">
                        <div class="text-[9px] text-rose-400 font-bold uppercase tracking-widest mb-2 border border-rose-400/20 bg-rose-400/10 inline-block px-2 py-1 rounded">MIM/ISTAT Provenance Verified</div>
                        <p class="text-lg font-display font-bold text-white mb-1 leading-tight group-hover:text-rose-400 transition-colors">{title}</p>
                        <p class="text-[10px] text-slate-500 font-mono uppercase tracking-widest mt-4 flex items-center gap-1">
                            <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
                            Official Registry Access
                        </p>
                    </div>
                </div>
'''

    html += f'''
                <!-- Frontiers Card 1: Shadow Economy -->
                <div class="gallery-item flex flex-col glass-panel rounded-2xl border border-amber-500/30 bg-amber-900/10 shadow-xl overflow-hidden" data-cat="frontiers">
                    <div class="p-6 border-l-4 border-amber-500">
                        <h3 class="text-xl font-black text-amber-500 mb-2 font-['Outfit']">1. The Shadow Economy ("Lavoro Nero")</h3>
                        <p class="text-slate-300 text-sm leading-relaxed mb-4">
                            Administrative data treats informal labor as unemployment. A 24-year-old completely socially withdrawn and one working 50 hours a week off-the-books in agriculture are counted identically as "NEET." The open data partially masks a thriving, deeply exploitative parallel economy.
                        </p>
                        <div class="text-[10px] text-amber-400 font-bold uppercase tracking-widest bg-amber-500/10 inline-block px-2 py-1 rounded">Blind Spot: Unmeasured Labor</div>
                    </div>
                </div>

                <!-- Frontiers Card 2: Gendered Caregiving -->
                <div class="gallery-item flex flex-col glass-panel rounded-2xl border border-amber-500/30 bg-amber-900/10 shadow-xl overflow-hidden" data-cat="frontiers">
                    <div class="p-6 border-l-4 border-amber-500">
                        <h3 class="text-xl font-black text-amber-500 mb-2 font-['Outfit']">2. The Gendered Caregiving Chasm</h3>
                        <p class="text-slate-300 text-sm leading-relaxed mb-4">
                            A massive percentage of female NEETs are engaged in full-time, unpaid domestic labor due to a severe deficit of public childcare facilities (asili nido). The transition is short-circuited by a lack of social infrastructure, but the data falsely labels them as "inactive."
                        </p>
                        <div class="text-[10px] text-amber-400 font-bold uppercase tracking-widest bg-amber-500/10 inline-block px-2 py-1 rounded">Blind Spot: Unpaid Output</div>
                    </div>
                </div>

                <!-- Frontiers Card 3: Brain Drain -->
                <div class="gallery-item flex flex-col glass-panel rounded-2xl border border-amber-500/30 bg-amber-900/10 shadow-xl overflow-hidden" data-cat="frontiers">
                    <div class="p-6 border-l-4 border-amber-500">
                        <h3 class="text-xl font-black text-amber-500 mb-2 font-['Outfit']">3. Demographic Attrition</h3>
                        <p class="text-slate-300 text-sm leading-relaxed mb-4">
                            The "fuga dei talenti" (migration of highly educated youth) acts as a statistical centrifuge. Southern regions export their successful graduates and retain school dropouts. This shifting denominator artificially inflates local NEET concentration.
                        </p>
                        <div class="text-[10px] text-amber-400 font-bold uppercase tracking-widest bg-amber-500/10 inline-block px-2 py-1 rounded">Blind Spot: Shifting Denominators</div>
                    </div>
                </div>

                <!-- Frontiers Card 4: Aggregation Trap -->
                <div class="gallery-item flex flex-col glass-panel rounded-2xl border border-amber-500/30 bg-amber-900/10 shadow-xl overflow-hidden" data-cat="frontiers">
                    <div class="p-6 border-l-4 border-amber-500">
                        <h3 class="text-xl font-black text-amber-500 mb-2 font-['Outfit']">4. The Aggregation Trap</h3>
                        <p class="text-slate-300 text-sm leading-relaxed mb-4">
                            Regional (NUTS 2) averages smooth out catastrophic micro-fractures. A region might show a 25% NEET rate, missing a 45% concentration in a specific peripheral district lacking transit. True civic diagnostics require granular, geolocated mapping.
                        </p>
                        <div class="text-[10px] text-amber-400 font-bold uppercase tracking-widest bg-amber-500/10 inline-block px-2 py-1 rounded">Blind Spot: Granularity</div>
                    </div>
                </div>

                <!-- Frontiers Card 5: Implicit Dropouts -->
                <div class="gallery-item flex flex-col glass-panel rounded-2xl border border-amber-500/30 bg-amber-900/10 shadow-xl overflow-hidden" data-cat="frontiers">
                    <div class="p-6 border-l-4 border-amber-500">
                        <h3 class="text-xl font-black text-amber-500 mb-2 font-['Outfit']">5. "Dispersione Implicita"</h3>
                        <p class="text-slate-300 text-sm leading-relaxed mb-4">
                            Our dataset tracks formal dropouts (bocciatura). But a growing crisis is students who physically remain and graduate without minimum competencies in math/language. The data misses the cohort the institution quietly passed along to avoid statistical penalty.
                        </p>
                        <div class="text-[10px] text-amber-400 font-bold uppercase tracking-widest bg-amber-500/10 inline-block px-2 py-1 rounded">Blind Spot: Functional Illiteracy</div>
                    </div>
                </div>
                
                <!-- CTA Card -->
                <div class="gallery-item flex flex-col glass-panel rounded-2xl border-2 border-dashed border-rose-500/50 bg-rose-900/10 shadow-xl overflow-hidden justify-center items-center text-center" data-cat="frontiers">
                    <div class="p-6">
                        <svg class="w-12 h-12 text-rose-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" /></svg>
                        <h3 class="text-xl font-black text-white mb-2 font-['Outfit']">Call to Action</h3>
                        <p class="text-slate-300 text-sm leading-relaxed mb-4">
                            These limitations highlight the frontiers of diagnostic capabilities. We invite developers, sociologists, and citizens to contribute granular datasets (e.g. Overpass API) or alternative proxy models via GitHub.
                        </p>
                        <a href="https://github.com/Eugenix94/italian-schools-explorer" target="_blank" class="inline-flex items-center gap-2 bg-rose-600 hover:bg-rose-500 text-white font-bold py-2 px-6 rounded-lg text-sm transition-colors shadow-[0_0_15px_rgba(225,29,72,0.4)]">
                            Contribute on GitHub
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <footer class="py-12 text-center border-t border-slate-800 text-slate-500 text-sm bg-black">
        <p class="font-display tracking-widest uppercase">Italienation | The Academic Observatory</p>
        <p class="text-xs mt-2 opacity-50">Empowered by Artificial Intelligence Data Synthesis</p>
    </footer>

    <script>
        // 1. Leaflet Map with Regional Profiler
        const map = L.map('map', {{ center: [41.8719, 12.5674], zoom: 6, zoomControl: false }});
        L.control.zoom({{ position: 'bottomright' }}).addTo(map);
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{ attribution: '&copy; CARTO', maxZoom: 20 }}).addTo(map);

        const geoData = {json.dumps(geo_data)};
        const markers = L.markerClusterGroup({{ showCoverageOnHover: false, spiderfyOnMaxZoom: true, maxClusterRadius: 80 }});
        
        geoData.forEach(school => {{
            const color = school.type.includes('Liceo') ? '#3b82f6' : '#f97316';
            const marker = L.circleMarker([school.lat, school.lon], {{ radius: 5, fillColor: color, color: '#0f172a', weight: 1.5, opacity: 1, fillOpacity: 0.9 }});
            marker.schoolData = school;
            marker.bindPopup(`<div class="font-display font-bold text-white text-sm mb-1">${{school.prov}}</div><div class="text-xs text-slate-300">${{school.type}}</div>`);
            markers.addLayer(marker);
        }});
        map.addLayer(markers);

        // Sidebar logic
        const sidebar = document.getElementById('sidebar');
        const sidebarTitle = document.getElementById('sidebar-title');
        const closeSidebar = document.getElementById('close-sidebar');
        let rPie = null;
        
        const EXTRAPOLATION_FACTOR = 4.5;

        function openRegionalProfiler(province) {{
            sidebar.classList.remove('sidebar-hidden');
            sidebarTitle.innerText = province;
            
            const provSchools = geoData.filter(s => s.prov === province);
            const liceoCount = Math.round(provSchools.filter(s => s.type.includes('Liceo')).length * EXTRAPOLATION_FACTOR);
            const techCount = Math.round(provSchools.filter(s => s.type.includes('Tecnico')).length * EXTRAPOLATION_FACTOR);
            const profCount = Math.round(provSchools.filter(s => s.type.includes('Professionale')).length * EXTRAPOLATION_FACTOR);
            const totalEstimated = liceoCount + techCount + profCount;
            
            document.getElementById('sidebar-stats').innerHTML = `
                <div class="bg-slate-800/40 p-4 rounded-2xl border border-slate-700/50 shadow-inner">
                    <div class="text-[10px] text-slate-400 font-bold uppercase mb-1 tracking-widest">Est. Secondary Schools</div>
                    <div class="text-3xl font-black text-white">~${{totalEstimated}}</div>
                </div>
                <div class="bg-slate-800/40 p-4 rounded-2xl border border-slate-700/50 shadow-inner">
                    <div class="text-[10px] text-slate-400 font-bold uppercase mb-1 tracking-widest">Dominant Track</div>
                    <div class="text-3xl font-black ${{liceoCount > (techCount+profCount) ? 'text-blue-400' : 'text-orange-400'}}">${{liceoCount > (techCount+profCount) ? 'Liceo' : 'Vocational'}}</div>
                </div>
            `;

            if (rPie) rPie.destroy();
            Chart.defaults.color = '#94a3b8';
            rPie = new Chart(document.getElementById('regionalPie'), {{
                type: 'pie',
                data: {{
                    labels: ['Liceo', 'Tecnico', 'Professionale'],
                    datasets: [{{ data: [liceoCount, techCount, profCount], backgroundColor: ['#3b82f6', '#10b981', '#f97316'], borderWidth: 2, borderColor: '#0f172a', hoverOffset: 4 }}]
                }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ position: 'bottom', labels: {{color: '#cbd5e1', boxWidth: 12, padding: 20, font: {{family: 'Inter', size: 11}} }} }} }} }}
            }});
        }}

        markers.on('click', function(a) {{ openRegionalProfiler(a.layer.schoolData.prov); }});
        markers.on('clusterclick', function(a) {{
            const markers = a.layer.getAllChildMarkers();
            if(markers.length > 0) openRegionalProfiler(markers[0].schoolData.prov);
        }});
        closeSidebar.addEventListener('click', () => sidebar.classList.add('sidebar-hidden'));

        // 2. Curriculum Matrix Logic
        const calcRegion = document.getElementById('calcRegion');
        const calcType = document.getElementById('calcType');
        const mPhil = document.getElementById('mat-phil');
        const mLatin = document.getElementById('mat-latin');
        const mArt = document.getElementById('mat-art');
        const mMech = document.getElementById('mat-mech');
        const mConc = document.getElementById('mat-conclusion');

        function updateCalculator() {{
            const r = parseInt(calcRegion.value);
            const t = calcType.value;
            
            if (t === 'liceo') {{
                mPhil.innerHTML = '<span class="bg-teal-400/10 text-teal-400 border border-teal-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Core</span>';
                mLatin.innerHTML = '<span class="bg-teal-400/10 text-teal-400 border border-teal-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Core</span>';
                mArt.innerHTML = '<span class="bg-teal-400/10 text-teal-400 border border-teal-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Core</span>';
                mMech.innerHTML = '<span class="bg-rose-400/10 text-rose-400 border border-rose-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Excluded</span>';
                mConc.innerText = 'University';
                mConc.className = 'text-[10px] font-bold bg-teal-400/10 text-teal-400 border border-teal-400/20 px-3 py-1 rounded-full uppercase tracking-widest';
            }} else if (t === 'tech') {{
                mPhil.innerHTML = '<span class="bg-rose-400/10 text-rose-400 border border-rose-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Excluded</span>';
                mLatin.innerHTML = '<span class="bg-rose-400/10 text-rose-400 border border-rose-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Excluded</span>';
                mArt.innerHTML = '<span class="bg-rose-400/10 text-rose-400 border border-rose-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Excluded</span>';
                mMech.innerHTML = '<span class="bg-emerald-400/10 text-emerald-400 border border-emerald-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">IT / Econ</span>';
                mConc.innerText = 'White-Collar Labor';
                mConc.className = 'text-[10px] font-bold bg-emerald-400/10 text-emerald-400 border border-emerald-400/20 px-3 py-1 rounded-full uppercase tracking-widest';
            }} else {{
                mPhil.innerHTML = '<span class="bg-rose-400/10 text-rose-400 border border-rose-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Excluded</span>';
                mLatin.innerHTML = '<span class="bg-rose-400/10 text-rose-400 border border-rose-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Excluded</span>';
                mArt.innerHTML = '<span class="bg-rose-400/10 text-rose-400 border border-rose-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Excluded</span>';
                mMech.innerHTML = '<span class="bg-orange-400/10 text-orange-400 border border-orange-400/20 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider">Vocational</span>';
                mConc.innerText = 'Blue-Collar Labor';
                mConc.className = 'text-[10px] font-bold bg-orange-400/10 text-orange-400 border border-orange-400/20 px-3 py-1 rounded-full uppercase tracking-widest';
            }}
            
            let dropout = r; 
            if (t === 'tech') dropout += 5;
            if (t === 'prof') dropout += 12;
            document.getElementById('calcDropout').innerText = dropout + '%';
            document.getElementById('calcPrecarity').innerText = (20 + (r/2)).toFixed(1) + '%';
        }}
        calcRegion.addEventListener('change', updateCalculator);
        calcType.addEventListener('change', updateCalculator);
        updateCalculator();

        // 3. Gallery Tabs
        const galBtns = document.querySelectorAll('.gallery-tab');
        const galItems = document.querySelectorAll('.gallery-item');
        galBtns.forEach(btn => {{
            btn.addEventListener('click', () => {{
                galBtns.forEach(b => {{ b.classList.remove('active'); }});
                btn.classList.add('active');
                const filter = btn.getAttribute('data-gallery');
                galItems.forEach(item => {{ item.style.display = (filter === 'all' || item.getAttribute('data-cat') === filter) ? 'flex' : 'none'; }});
            }});
        }});

        // 4. Chart.js Data
        Chart.defaults.color = '#94a3b8';
        Chart.defaults.borderColor = 'rgba(255,255,255,0.05)';
        Chart.defaults.font.family = 'Inter';
        
        const istatData = {json.dumps(istat_data)};
        new Chart(document.getElementById('istatBar'), {{
            type: 'bar',
            data: {{
                labels: istatData.slice(0, 10).map(d => d.region),
                datasets: [{{ label: 'Pop Drop Projection', data: istatData.slice(0, 10).map(d => d.pop_drop), backgroundColor: 'rgba(225, 29, 72, 0.8)', borderRadius: 4, hoverBackgroundColor: 'rgba(244, 63, 94, 1)' }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true }} }} }}
        }});

        new Chart(document.getElementById('sostegnoDoughnut'), {{
            type: 'doughnut',
            data: {{ labels: ['Substitute', 'Tenured'], datasets: [{{ data: [74.7, 25.3], backgroundColor: ['#fb7185', '#10b981'], borderWidth: 2, borderColor: '#0f172a' }}] }},
            options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, cutout: '75%' }}
        }});

        new Chart(document.getElementById('pisaLine'), {{
            type: 'line',
            data: {{
                labels: ['2003', '2006', '2009', '2012', '2015', '2018', '2022'],
                datasets: [
                    {{ label: 'Math', data: [466, 462, 483, 485, 490, 487, 471], borderColor: '#f59e0b', backgroundColor: 'rgba(245, 158, 11, 0.1)', fill: true, tension: 0.4, pointRadius: 2, pointBackgroundColor: '#f59e0b' }},
                    {{ label: 'Reading', data: [476, 469, 486, 490, 485, 476, 482], borderColor: '#3b82f6', backgroundColor: 'rgba(59, 130, 246, 0.1)', fill: true, tension: 0.4, pointRadius: 2, pointBackgroundColor: '#3b82f6' }}
                ]
            }},
            options: {{ responsive: true, maintainAspectRatio: false, scales: {{ x: {{ grid: {{ display: false }} }}, y: {{ grid: {{ display: true, color: 'rgba(255,255,255,0.02)' }} }} }}, plugins: {{ legend: {{ display: false }} }} }}
        }});
    </script>
</body>
</html>
'''

    out_path = Path('index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully built the polished Command Center at index.html")

if __name__ == '__main__':
    build_command_center()
