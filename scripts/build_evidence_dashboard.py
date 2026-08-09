import json
import os
from pathlib import Path

def build_dashboard():
    with open('processed_data/50_cases.json', 'r') as f:
        cases = json.load(f)

    # Base HTML Shell with Tailwind and Inter font
    html = '''<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Italienation | The Evidence Repository</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Outfit:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #0f172a; color: #f8fafc; overflow-x: hidden; }
        h1, h2, h3, .font-display { font-family: 'Outfit', sans-serif; }
        .glass-panel { background: rgba(30, 41, 59, 0.6); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.05); }
        .card-hover:hover { transform: translateY(-4px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.3); border-color: rgba(255, 255, 255, 0.15); }
        .transition-all { transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 300ms; }
    </style>
</head>
<body class="antialiased min-h-screen selection:bg-teal-500/30 selection:text-teal-200">

    <!-- HEADER -->
    <header class="py-24 px-6 border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto space-y-6">
            <div class="inline-flex items-center space-x-2 text-teal-400 font-semibold tracking-widest text-sm uppercase mb-4">
                <span class="w-2 h-2 rounded-full bg-teal-400 animate-pulse"></span>
                <span>Open Data Repository</span>
            </div>
            <h1 class="font-display text-5xl md:text-7xl font-bold text-white tracking-tight">
                Italienation
            </h1>
            <p class="text-xl text-slate-400 max-w-2xl leading-relaxed">
                The absolute empirical truth of the Italian educational collapse. No narratives. No rhetoric. Just raw data pulled directly from the World Bank, OECD, Eurostat, Openpolis, and the HuggingFace Open Data Registers.
            </p>
            <div class="flex flex-wrap gap-4 pt-6" id="filters">
                <button class="filter-btn active px-6 py-2 rounded-full bg-teal-600 text-white font-medium hover:bg-teal-500 transition-all" data-filter="all">All Evidence</button>
                <button class="filter-btn px-6 py-2 rounded-full bg-slate-800 text-slate-300 font-medium hover:bg-slate-700 transition-all border border-slate-700" data-filter="Geographic & Demographic">Demographics</button>
                <button class="filter-btn px-6 py-2 rounded-full bg-slate-800 text-slate-300 font-medium hover:bg-slate-700 transition-all border border-slate-700" data-filter="Physical Decay">Physical Decay</button>
                <button class="filter-btn px-6 py-2 rounded-full bg-slate-800 text-slate-300 font-medium hover:bg-slate-700 transition-all border border-slate-700" data-filter="The Human Capital Crisis">Human Capital</button>
                <button class="filter-btn px-6 py-2 rounded-full bg-slate-800 text-slate-300 font-medium hover:bg-slate-700 transition-all border border-slate-700" data-filter="Cognitive Failure">Cognitive Failure</button>
                <button class="filter-btn px-6 py-2 rounded-full bg-slate-800 text-slate-300 font-medium hover:bg-slate-700 transition-all border border-slate-700" data-filter="The Economic Paradox">Economic Paradox</button>
            </div>
        </div>
    </header>

    <!-- GRID -->
    <main class="py-16 px-6">
        <div class="max-w-7xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6" id="evidence-grid">
'''
    
    # Generate Cards
    colors = {
        "Geographic & Demographic": "text-emerald-400 bg-emerald-400/10 border-emerald-400/20",
        "Physical Decay": "text-rose-400 bg-rose-400/10 border-rose-400/20",
        "The Human Capital Crisis": "text-indigo-400 bg-indigo-400/10 border-indigo-400/20",
        "Cognitive Failure": "text-amber-400 bg-amber-400/10 border-amber-400/20",
        "The Economic Paradox": "text-purple-400 bg-purple-400/10 border-purple-400/20"
    }

    for case in cases:
        pillar = case['pillar']
        c_class = colors.get(pillar, "text-slate-400 bg-slate-400/10 border-slate-400/20")
        
        card = f'''                <!-- CARD {case['id']} -->
                <div class="glass-panel rounded-3xl p-8 flex flex-col justify-between h-full card-hover transition-all evidence-card" data-category="{pillar}">
                    <div class="space-y-6">
                        <div class="inline-block px-3 py-1 rounded-full text-xs font-semibold border {c_class}">
                            {pillar}
                        </div>
                        <h3 class="font-display text-xl font-bold text-white leading-tight">{case['title']}</h3>
                        <div class="font-display text-5xl font-black text-white tracking-tighter">
                            {case['metric']}
                        </div>
                        <p class="text-sm text-slate-400 leading-relaxed">
                            {case['description']}
                        </p>
                    </div>
                    <div class="pt-8 mt-auto">
                        <div class="flex items-center justify-between border-t border-slate-800 pt-4">
                            <span class="text-xs text-slate-500 truncate max-w-[150px]" title="{case['source_name']}">{case['source_name']}</span>
                            <a href="{case['source_url']}" target="_blank" rel="noopener noreferrer" class="text-xs font-semibold text-teal-400 hover:text-teal-300 transition-colors flex items-center gap-1 group">
                                Verify Source
                                <svg class="w-3 h-3 group-hover:translate-x-0.5 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
'''
        html += card

    html += '''            </div>
        </div>
    </main>

    <footer class="py-12 text-center border-t border-slate-800 text-slate-500 text-sm">
        <p>Italienation | Built on Open Data</p>
    </footer>

    <!-- Filter Logic -->
    <script>
        const buttons = document.querySelectorAll('.filter-btn');
        const cards = document.querySelectorAll('.evidence-card');

        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                // Update active state
                buttons.forEach(b => {
                    b.classList.remove('bg-teal-600', 'text-white');
                    b.classList.add('bg-slate-800', 'text-slate-300');
                });
                btn.classList.remove('bg-slate-800', 'text-slate-300');
                btn.classList.add('bg-teal-600', 'text-white');

                const filter = btn.getAttribute('data-filter');

                cards.forEach(card => {
                    if (filter === 'all' || card.getAttribute('data-category') === filter) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    </script>
</body>
</html>
'''

    out_path = Path('rendered_outputs/index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully built the 50-Evidence Interactive Dashboard at web/index.html")

if __name__ == '__main__':
    build_dashboard()
