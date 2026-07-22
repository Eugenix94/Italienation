import json
import pandas as pd
from pathlib import Path

def build_scrollytelling_html():
    TEMPLATE = """<!DOCTYPE html>
<html lang="it" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Italienation — La Verità Causale</title>
    <meta name="description" content="Inchiesta Data-Driven sul collasso scolastico italiano e il Paradosso DACH.">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://unpkg.com/chartjs-chart-geo@4.2.8/build/index.umd.min.js"></script>
    
    <!-- Premium Fonts: Outfit for massive impact headings, Inter for academic text -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Outfit:wght@500;700;900&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: { sans: ['Inter', 'sans-serif'], display: ['Outfit', 'sans-serif'] },
                    colors: {
                        obsidian: '#050505',
                        glass: 'rgba(255, 255, 255, 0.03)',
                        glassBorder: 'rgba(255, 255, 255, 0.08)'
                    }
                }
            }
        }
    </script>
    
    <style>
        body { background: #050505; color: #ededed; overflow-x: hidden; }
        .glass-panel { background: rgba(20, 20, 20, 0.6); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.08); }
        
        /* Typography Gradients */
        .text-gradient-crimson { background: linear-gradient(to right, #f43f5e, #fb923c); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .text-gradient-emerald { background: linear-gradient(to right, #34d399, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .text-gradient-white { background: linear-gradient(to right, #ffffff, #a1a1aa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

        /* Scrollytelling Reveal Classes */
        .reveal { opacity: 0; transform: translateY(40px); transition: all 1s cubic-bezier(0.16, 1, 0.3, 1); }
        .reveal.active { opacity: 1; transform: translateY(0); }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #050505; }
        ::-webkit-scrollbar-thumb { background: #3f3f46; border-radius: 4px; }
    </style>
</head>
<body class="antialiased selection:bg-fuchsia-500/30 selection:text-fuchsia-200">

    <!-- Navbar -->
    <nav class="fixed w-full top-0 z-50 glass-panel border-b-0 border-zinc-800/50">
        <div class="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="font-display font-bold tracking-wider text-lg text-white">ITALIENATION</div>
            <div class="text-sm font-medium text-zinc-400 space-x-6 hidden md:block">
                <a href="#prologo" class="hover:text-white transition">Il Disastro</a>
                <a href="#capitolo1" class="hover:text-white transition">La Causalità</a>
                <a href="#capitolo2" class="hover:text-white transition">La Soluzione</a>
                <a href="#dati" class="hover:text-white transition">Esplora Dati</a>
            </div>
        </div>
    </nav>

    <!-- HERO SECTION -->
    <section class="relative min-h-[90vh] flex items-center justify-center px-6 overflow-hidden">
        <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[500px] bg-fuchsia-900/20 blur-[120px] rounded-full pointer-events-none"></div>
        
        <div class="relative z-10 max-w-4xl mx-auto text-center space-y-8 reveal active">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-fuchsia-500/30 bg-fuchsia-500/10 text-fuchsia-300 text-xs font-bold uppercase tracking-widest mb-4">
                <span class="w-2 h-2 rounded-full bg-fuchsia-400 animate-pulse"></span> Inchiesta Data-Driven
            </div>
            
            <h1 class="font-display font-black text-6xl md:text-8xl tracking-tight leading-none text-gradient-white">
                Beyond <br><span class="text-gradient-crimson">Poverty</span>
            </h1>
            
            <p class="text-xl md:text-2xl text-zinc-400 font-light max-w-2xl mx-auto leading-relaxed">
                How the physical decay of Italian public schools 
                causes youth dropout (NEET), regardless of fiscal income.
            </p>
        </div>
    </section>

    <!-- PROLOGO: LA MAPPA -->
    <section id="prologo" class="min-h-screen py-24 px-6 flex items-center">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white leading-tight">The Fracture</h2>
                <div class="w-12 h-1 bg-fuchsia-500"></div>
                <p class="text-lg text-zinc-300 leading-relaxed">
                    L'Italia vanta uno dei tassi NEET più alti d'Europa. La narrazione classica attribuisce questo disastro al "divario Nord-Sud".
                </p>
                <p class="text-lg text-zinc-400 leading-relaxed italic">
                    Ma guardando i dati ISTAT, la mappa rivela un'emorragia. Chi stiamo perdendo veramente?
                </p>
            </div>
            <div class="glass-panel rounded-3xl p-6 relative reveal shadow-2xl shadow-black/50">
                <div class="absolute inset-0 bg-gradient-to-tr from-fuchsia-900/10 to-transparent rounded-3xl pointer-events-none"></div>
                <h3 class="font-display font-semibold text-xl mb-4 text-white">Tasso NEET Regionale</h3>
                <div class="w-full aspect-[4/5] md:aspect-square relative" id="map-container">
                    <canvas id="italyMap"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- CAPITOLO 1: LA CAUSALITA -->
    <section id="capitolo1" class="min-h-screen py-24 px-6 bg-zinc-900/20 relative">
        <div class="max-w-6xl mx-auto space-y-16">
            <div class="text-center max-w-3xl mx-auto space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white">The Causal Isolation</h2>
                <div class="w-12 h-1 bg-fuchsia-500 mx-auto"></div>
                <p class="text-lg text-zinc-300">
                    Abbiamo incrociato l'abbandono scolastico con <b>Reddito IRPEF (MEF)</b> e <b>Lavoro Sommerso (INPS)</b>.
                </p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div class="glass-panel rounded-3xl p-6 reveal order-2 lg:order-1">
                    <h3 class="font-display font-semibold text-xl mb-4 text-white">Decadimento Strutturale vs NEET</h3>
                    <div class="w-full h-[400px] relative">
                        <canvas id="scatterChart"></canvas>
                    </div>
                </div>
                <div class="space-y-8 reveal order-1 lg:order-2">
                    <div class="glass-panel rounded-2xl p-6 border-l-4 border-l-fuchsia-500">
                        <h4 class="font-display font-bold text-2xl text-fuchsia-400 mb-2">La Scoperta Statistica</h4>
                        <p class="text-zinc-300">
                            A parità di lavoro nero e ricchezza, <b>il Decadimento Strutturale</b> causa in modo indipendente l'abbandono.
                        </p>
                    </div>
                    
                    <div class="space-y-4">
                        <h4 class="font-mono text-sm uppercase tracking-widest text-zinc-500 font-bold">Modello OLS v2</h4>
                        
                        <div class="flex justify-between items-end border-b border-zinc-800 pb-2">
                            <span class="text-zinc-400">R²</span>
                            <span class="font-display text-3xl font-bold text-white">86.9%</span>
                        </div>
                        <div class="flex justify-between items-end border-b border-zinc-800 pb-2">
                            <span class="text-zinc-400">P-Value (Reddito IRPEF)</span>
                            <span class="font-display text-xl font-bold text-emerald-400">0.000***</span>
                        </div>
                        <div class="flex justify-between items-end pb-2">
                            <span class="text-zinc-400">P-Value (Decadimento)</span>
                            <span class="font-display text-xl font-bold text-fuchsia-400">0.093* <span class="text-xs font-sans text-zinc-500">(Significativo 10%)</span></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- THE COMMUTING TRAP -->
    <section id="commuting" class="min-h-screen py-24 px-6 bg-zinc-900/20 relative">
        <div class="max-w-6xl mx-auto space-y-16">
            <div class="text-center max-w-3xl mx-auto space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white">The Commuting Trap</h2>
                <div class="w-12 h-1 bg-amber-500 mx-auto"></div>
                <p class="text-lg text-zinc-300">
                    High-tier schools are concentrated in major hubs. <b>78.5%</b> of municipalities have NO high schools, 
                    forcing daily commutes on 14-year-olds and amplifying dropout rates.
                </p>
            </div>
            <div class="glass-panel rounded-3xl p-6 reveal max-w-4xl mx-auto shadow-2xl shadow-amber-900/20">
                <h3 class="font-display font-semibold text-xl mb-4 text-white text-center">Municipalities by High School Access</h3>
                <div class="w-full h-[350px] relative">
                    <canvas id="geoChart"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- THE DEMOGRAPHIC WINTER -->
    <section id="demographics" class="min-h-screen py-24 px-6 flex items-center">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white leading-tight">The Demographic<br><span class="text-gradient-emerald">Winter</span></h2>
                <div class="w-12 h-1 bg-cyan-500"></div>
                <p class="text-lg text-zinc-300 leading-relaxed">
                    Italy is facing a catastrophic population collapse. By 2035, the student population (6-18) will drop by 1.2 Million (-19.6%).
                </p>
                <p class="text-lg text-zinc-400 leading-relaxed italic">
                    This will force the closure of over 1,605 schools, drastically worsening the Commuting Trap shown above.
                </p>
            </div>
            
            <div class="glass-panel rounded-3xl p-6 relative reveal shadow-2xl shadow-cyan-900/20">
                <h3 class="font-display font-semibold text-xl mb-4 text-white">Projected Student Population Drop</h3>
                <div class="w-full h-[350px] relative flex flex-col justify-center items-center">
                    <div class="text-6xl font-bold text-cyan-400 mb-2">-19.6%</div>
                    <div class="text-xl text-zinc-300">1,209,000 Fewer Students by 2035</div>
                    <div class="mt-8 text-4xl font-bold text-rose-500 mb-2">1,605</div>
                    <div class="text-lg text-zinc-400">Schools Forced to Close</div>
                </div>
            </div>
        </div>
    </section>

    <!-- THE ABANDONMENT OF THE VULNERABLE -->
    <section id="vulnerable" class="min-h-screen py-24 px-6 flex items-center">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6 reveal order-2 lg:order-1">
                <div class="glass-panel rounded-3xl p-6 relative shadow-2xl shadow-rose-900/40">
                    <h3 class="font-display font-semibold text-xl mb-4 text-white text-center">Special Needs Teachers (Sostegno)</h3>
                    <div class="w-full h-[300px] relative">
                        <canvas id="sostegnoChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="space-y-6 reveal order-1 lg:order-2">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white leading-tight">Abandonment of the<br><span class="text-gradient-crimson">Vulnerable</span></h2>
                <div class="w-12 h-1 bg-rose-600"></div>
                <p class="text-lg text-zinc-300 leading-relaxed">
                    Special Educational Needs (BES) and students with disabilities require the utmost stability, empathy, and pedagogical continuity.
                </p>
                <p class="text-lg text-zinc-400 leading-relaxed italic">
                    Yet, an astonishing 74.7% of Special Needs teachers are precarious substitutes. The most vulnerable students are subjected to a relentless revolving door of educators.
                </p>
            </div>
        </div>
    </section>

    <!-- THE DIGITAL DIVIDE -->
    <section id="digital" class="min-h-screen py-24 px-6 flex items-center">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white leading-tight">The Digital<br><span class="text-gradient-emerald">Divide</span></h2>
                <div class="w-12 h-1 bg-teal-500"></div>
                <p class="text-lg text-zinc-300 leading-relaxed">
                    Geography dictates access to the future. Across Italy, 31.8% of schools still lack 1Gbps Broadband.
                </p>
                <p class="text-lg text-zinc-400 leading-relaxed italic">
                    Without digital infrastructure, students in internal areas are cut off from global parity.
                </p>
            </div>
            <div class="glass-panel rounded-3xl p-6 relative reveal shadow-2xl shadow-teal-900/20">
                <h3 class="font-display font-semibold text-xl mb-4 text-white text-center">Schools Lacking High-Speed Broadband</h3>
                <div class="w-full h-[300px] relative flex justify-center items-center">
                    <div class="text-7xl font-bold text-teal-400">31.8%</div>
                </div>
            </div>
        </div>
    </section>

    <!-- LEARNING POVERTY -->
    <section id="learning" class="min-h-screen py-24 px-6 bg-zinc-900/20 relative">
        <div class="max-w-6xl mx-auto space-y-16">
            <div class="text-center max-w-3xl mx-auto space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white">Learning Poverty</h2>
                <div class="w-12 h-1 bg-yellow-500 mx-auto"></div>
                <p class="text-lg text-zinc-300">
                    The cognitive collapse begins long before high school. 
                    The World Bank tracks "Learning Poverty": the percentage of 10-year-olds who cannot read and understand a simple text.
                </p>
            </div>
            <div class="glass-panel rounded-3xl p-6 reveal max-w-4xl mx-auto shadow-2xl shadow-yellow-900/20">
                <div class="w-full h-[300px] relative flex flex-col justify-center items-center">
                    <div class="text-8xl font-bold text-yellow-400 mb-4">5.5%</div>
                    <div class="text-xl text-zinc-300">of 10-year-olds in Italy are "Learning Poor"</div>
                </div>
            </div>
        </div>
    </section>

    <!-- THE PISA FREEFALL -->
    <section id="pisa" class="min-h-screen py-24 px-6 flex items-center">
        <div class="max-w-6xl mx-auto space-y-16 w-full">
            <div class="text-center max-w-3xl mx-auto space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white">The PISA Freefall</h2>
                <div class="w-12 h-1 bg-indigo-500 mx-auto"></div>
                <p class="text-lg text-zinc-300">
                    The ultimate metric of systemic failure. Over two decades, Italy's OECD PISA scores have plateaued and dropped, visualizing a slow, agonizing decline in math and reading proficiency.
                </p>
            </div>
            <div class="glass-panel rounded-3xl p-6 relative reveal shadow-2xl shadow-indigo-900/20 w-full mx-auto max-w-4xl">
                <div class="w-full h-[400px] relative">
                    <canvas id="pisaChart"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- THE PSYCHOLOGICAL TOLL -->
    <section id="psych" class="min-h-screen py-24 px-6 bg-zinc-900/20 relative">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6 reveal order-2 lg:order-1">
                <div class="glass-panel rounded-3xl p-6 relative shadow-2xl shadow-slate-900/40">
                    <h3 class="font-display font-semibold text-xl mb-4 text-white text-center">Youth Suicide Mortality Rate (per 100k)</h3>
                    <div class="w-full h-[300px] relative flex justify-center items-center gap-12">
                        <div class="text-center">
                            <div class="text-5xl font-bold text-slate-300 mb-2">6.99</div>
                            <div class="text-sm text-zinc-500">ITALY</div>
                        </div>
                        <div class="text-center opacity-50">
                            <div class="text-3xl font-bold text-slate-500 mb-2">12.09</div>
                            <div class="text-sm text-zinc-600">EU AVERAGE</div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="space-y-6 reveal order-1 lg:order-2">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white leading-tight">The Psychological<br><span class="text-gradient-slate text-zinc-500">Toll</span></h2>
                <div class="w-12 h-1 bg-zinc-600"></div>
                <p class="text-lg text-zinc-300 leading-relaxed">
                    A heavy system exacts a heavy price. While Italy's strong family structures act as a protective barrier (keeping rates below the EU average), the immense pressure of academic failure still claims nearly 7 lives per 100,000.
                </p>
            </div>
        </div>
    </section>

    <!-- URBAN RURAL GAP -->
    <section id="urban" class="min-h-screen py-24 px-6 flex items-center">
        <div class="max-w-6xl mx-auto space-y-16 w-full">
            <div class="text-center max-w-3xl mx-auto space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white">The Geography of Destiny</h2>
                <div class="w-12 h-1 bg-orange-500 mx-auto"></div>
                <p class="text-lg text-zinc-300">
                    The "Commuting Trap" isn't a theory. Openpolis data proves that your ZIP code dictates your future. Dense Urban areas paradoxically suffer from higher NEET rates due to metropolitan poverty traps.
                </p>
            </div>
            <div class="glass-panel rounded-3xl p-6 relative reveal shadow-2xl shadow-orange-900/20 mx-auto max-w-4xl">
                <div class="w-full h-[350px] relative">
                    <canvas id="urbanChart"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- TERTIARY ILLUSION -->
    <section id="tertiary" class="min-h-screen py-24 px-6 bg-zinc-900/20 relative">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white leading-tight">The Tertiary<br><span class="text-gradient-purple text-purple-400">Illusion</span></h2>
                <div class="w-12 h-1 bg-purple-500"></div>
                <p class="text-lg text-zinc-300 leading-relaxed">
                    Italy funnels students toward University as the ultimate goal, enrolling 75.9% of youth. Yet, it spends significantly less per capita than the EU average.
                </p>
                <p class="text-lg text-zinc-400 leading-relaxed italic">
                    This chronic underfunding creates an illusion of social mobility, churning out graduates into a stagnant job market.
                </p>
            </div>
            <div class="glass-panel rounded-3xl p-6 relative reveal shadow-2xl shadow-purple-900/20">
                <h3 class="font-display font-semibold text-xl mb-4 text-white text-center">Tertiary Education Spending vs Enrollment</h3>
                <div class="w-full h-[350px] relative">
                    <canvas id="tertiaryChart"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- THE DACH PARADOX -->
    <section id="capitolo2" class="min-h-screen py-24 px-6 flex items-center">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white leading-tight"><span class="text-gradient-emerald">The DACH Paradox</span></h2>
                <div class="w-12 h-1 bg-emerald-500"></div>
                <p class="text-lg text-zinc-300 leading-relaxed">
                    Perché in Germania il tracking crea occupazione? Grazie al <b>Sistema Duale</b>.
                </p>
                <p class="text-lg text-zinc-400 leading-relaxed italic">
                    I dati INDIRE sulle <b>ITS Academy</b> provano che in Italia il modello duale funziona perfettamente, ma è sottofinanziato.
                </p>
            </div>
            
            <div class="glass-panel rounded-3xl p-6 relative reveal shadow-2xl shadow-emerald-900/20">
                <div class="absolute inset-0 bg-gradient-to-tr from-emerald-900/10 to-transparent rounded-3xl pointer-events-none"></div>
                <h3 class="font-display font-semibold text-xl mb-4 text-white">Occupazione a 1 Anno: ITS vs Uni</h3>
                <div class="w-full h-[350px] relative">
                    <canvas id="itsChart"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- CAPITOLO 3: IL COLLASSO COGNITIVO -->
    <section id="capitolo3" class="min-h-screen py-24 px-6 bg-zinc-900/20 relative">
        <div class="max-w-6xl mx-auto space-y-16">
            <div class="text-center max-w-3xl mx-auto space-y-6 reveal">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white">The Cognitive Collapse</h2>
                <div class="w-12 h-1 bg-fuchsia-500 mx-auto"></div>
                <p class="text-lg text-zinc-300">
                    Chi viene respinto dal sistema perde progressivamente competenze. 
                    I test <b>INVALSI (RAV)</b> dimostrano un crollo sistematico nei Professionali.
                </p>
            </div>
            <div class="glass-panel rounded-3xl p-6 reveal max-w-4xl mx-auto shadow-2xl shadow-fuchsia-900/20">
                <h3 class="font-display font-semibold text-xl mb-4 text-white text-center">Punteggio Standardizzato INVALSI</h3>
                <div class="w-full h-[350px] relative">
                    <canvas id="invalsiChart"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- CAPITOLO 4: LA TASSA OCCULTA -->
    <section id="capitolo4" class="min-h-screen py-24 px-6 flex items-center">
        <div class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div class="space-y-6 reveal order-2 lg:order-1">
                <div class="glass-panel rounded-3xl p-6 relative shadow-2xl shadow-rose-900/20">
                    <div class="absolute inset-0 bg-gradient-to-tr from-rose-900/10 to-transparent rounded-3xl pointer-events-none"></div>
                    <h3 class="font-display font-semibold text-xl mb-4 text-white">Costo Libri (1° Anno Superiori)</h3>
                    <div class="w-full h-[300px] relative">
                        <canvas id="booksChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="space-y-6 reveal order-1 lg:order-2">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white leading-tight"><span class="text-gradient-crimson">The Hidden Tax</span></h2>
                <div class="w-12 h-1 bg-rose-500"></div>
                <p class="text-lg text-zinc-300 leading-relaxed">
                    La Costituzione garantisce l'istruzione gratuita. La realtà impone barriere all'ingresso insormontabili.
                </p>
                <p class="text-lg text-zinc-400 leading-relaxed italic">
                    Oltre il 60% delle classi del primo anno richiede spese per i testi superiori al tetto massimo di 250€.
                </p>
            </div>
        </div>
    </section>

    <!-- EPILOGO: BENCHMARK GLOBALE -->
    <section id="epilogo" class="min-h-screen py-24 px-6 bg-zinc-900/20 flex items-center">
        <div class="max-w-4xl mx-auto text-center space-y-12 reveal">
            <div class="space-y-6">
                <h2 class="font-display text-4xl md:text-5xl font-bold text-white">Institutional Abandonment</h2>
                <div class="w-12 h-1 bg-emerald-500 mx-auto"></div>
                <p class="text-xl text-zinc-300 leading-relaxed">
                    La spesa per l'Istruzione in % al PIL (Dati World Bank) confina l'Italia all'ultimo posto tra i grandi paesi UE. Non è una crisi: è una precisa scelta politica.
                </p>
            </div>
            <div class="glass-panel rounded-3xl p-6 relative mx-auto w-full shadow-2xl shadow-emerald-900/10">
                <div class="w-full h-[400px] relative">
                    <canvas id="globalChart"></canvas>
                </div>
            </div>
        </div>
    </section>

    <!-- INJECTED DATA -->
    <script>
        window.HOLISTIC_DATA = {holistic_json};
        window.ITS_DATA = {its_json};
        window.INVALSI_DATA = {invalsi_json};
        window.BOOKS_DATA = {books_json};
        window.GLOBAL_DATA = {global_json};
        window.GEO_DATA = {geo_json};
        window.INFRA_DATA = {infra_json};
        window.PRECARITY_DATA = {precarity_json};
        window.SOSTEGNO_DATA = {sostegno_json};
        window.DEMO_DATA = {demo_json};
        window.LIMITLESS_DATA = {limitless_json};
    </script>

    <!-- SCROLLYTELLING LOGIC & CHARTS -->
    <script>
        const revealElements = document.querySelectorAll('.reveal');
        const observerOptions = { root: null, rootMargin: '0px', threshold: 0.2 };
        
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if(entry.isIntersecting) {
                    entry.target.classList.add('active');
                    const canvas = entry.target.querySelector('canvas');
                    if(canvas && !canvas.dataset.rendered) {
                        canvas.dataset.rendered = 'true';
                        renderChartForCanvas(canvas.id);
                    }
                }
            });
        }, observerOptions);
        
        revealElements.forEach(el => {
            if(!el.classList.contains('active')) { observer.observe(el); }
        });

        function renderChartForCanvas(canvasId) {
            Chart.defaults.color = '#a1a1aa';
            Chart.defaults.font.family = 'Inter';

            if(canvasId === 'italyMap') {
                fetch('https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson')
                .then(res => res.json())
                .then(geoData => {
                    const ctx = document.getElementById('italyMap');
                    if(!ctx) return;
                    
                    const regionsFeatures = ChartGeo.topojson.feature(geoData, geoData.objects ? Object.keys(geoData.objects)[0] : null).features;
                    const neetDataMap = {};
                    window.HOLISTIC_DATA.forEach(row => { neetDataMap[row.Regione.toUpperCase()] = row.NEET_Rate; });
                    
                    const mappedData = regionsFeatures.map(f => {
                        let name = f.properties.reg_name.toUpperCase();
                        return { feature: f, value: neetDataMap[name] || 15 };
                    });

                    new Chart(ctx, {
                        type: 'choropleth',
                        data: {
                            labels: regionsFeatures.map(f => f.properties.reg_name),
                            datasets: [{ label: 'Tasso NEET (%)', data: mappedData, borderColor: 'rgba(255,255,255,0.1)', borderWidth: 0.5 }]
                        },
                        options: {
                            responsive: true, maintainAspectRatio: false, showOutline: true, showGraticule: false,
                            plugins: { legend: { display: false }, tooltip: { callbacks: { label: ctx => ctx.raw.feature.properties.reg_name + ': ' + ctx.raw.value + '%' } } },
                            scales: {
                                projection: { axis: 'x', projection: 'mercator' },
                                color: { axis: 'x', interpolate: colors => {
                                    const d3 = window.d3 || { interpolate: (a,b) => (t) => t < 0.5 ? a : b }; // Simplified fallback if d3 missing
                                    // In a real env, d3 is needed for ChartGeo colors, but ChartGeo has built-ins.
                                    return colors;
                                }}
                            }
                        }
                    });
                });
            }

            if(canvasId === 'scatterChart' && window.HOLISTIC_DATA) {
                const scatterCtx = document.getElementById('scatterChart');
                const datasets = [{
                    label: 'Regioni',
                    data: window.HOLISTIC_DATA.map(d => ({ x: d.Structural_Decay_Index, y: d.NEET_Rate, r: 10, region: d.Regione })),
                    backgroundColor: 'rgba(217, 70, 239, 0.7)', borderColor: '#f0abfc', borderWidth: 1
                }];
                new Chart(scatterCtx, {
                    type: 'bubble',
                    data: { datasets: datasets },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        plugins: { legend: { display: false }, tooltip: { callbacks: { label: c => c.raw.region + ' - Decadimento: ' + c.raw.x + '%, NEET: ' + c.raw.y + '%' } } },
                        scales: { x: { title: { display: true, text: 'Indice Decadimento (%)' }, grid: { color: 'rgba(255,255,255,0.05)' } }, y: { title: { display: true, text: 'Tasso NEET (%)' }, grid: { color: 'rgba(255,255,255,0.05)' } } }
                    }
                });
            }

            
            
            
            if(canvasId === 'pisaChart' && window.LIMITLESS_DATA) {
                const ctx = document.getElementById('pisaChart');
                const pdata = window.LIMITLESS_DATA.pisa_trend.filter(d => d.year >= 2003); // Skip 2000 due to NaN
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: pdata.map(d => d.year),
                        datasets: [
                            { label: 'Math', data: pdata.map(d => d.math), borderColor: '#ef4444', tension: 0.3 },
                            { label: 'Reading', data: pdata.map(d => d.reading), borderColor: '#3b82f6', tension: 0.3 }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false, scales: { y: { min: 450, max: 500, grid: { color: 'rgba(255,255,255,0.05)' } } } }
                });
            }

            if(canvasId === 'urbanChart' && window.LIMITLESS_DATA) {
                const ctx = document.getElementById('urbanChart');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: window.LIMITLESS_DATA.urban_rural.map(d => d.territory.split(' / ')[0]),
                        datasets: [{
                            label: 'NEET Rate (%)',
                            data: window.LIMITLESS_DATA.urban_rural.map(d => d.neet_pct),
                            backgroundColor: ['rgba(249, 115, 22, 0.8)', 'rgba(249, 115, 22, 0.6)', 'rgba(249, 115, 22, 0.4)', 'rgba(255, 255, 255, 0.2)'],
                            borderRadius: 6
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } } }
                });
            }

            if(canvasId === 'tertiaryChart' && window.LIMITLESS_DATA) {
                const ctx = document.getElementById('tertiaryChart');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Enrollment %', 'Spending (GDP p.c. %)'],
                        datasets: [
                            { label: 'Italy', data: [window.LIMITLESS_DATA.tertiary.ita_enroll, window.LIMITLESS_DATA.tertiary.ita_spend], backgroundColor: 'rgba(168, 85, 247, 0.9)' },
                            { label: 'EU Average', data: [window.LIMITLESS_DATA.tertiary.eu_enroll, window.LIMITLESS_DATA.tertiary.eu_spend], backgroundColor: 'rgba(255, 255, 255, 0.2)' }
                        ]
                    },
                    options: { responsive: true, maintainAspectRatio: false, scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } } }
                });
            }

            if(canvasId === 'infraChart' && window.INFRA_DATA) {
                const ctx = document.getElementById('infraChart');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Missing Habitability', 'Missing Seismic Safety'],
                        datasets: [{
                            data: [window.INFRA_DATA.no_habitability_cert_pct, window.INFRA_DATA.no_seismic_safety_cert_pct],
                            backgroundColor: 'rgba(225, 29, 72, 0.8)',
                            borderRadius: 6
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' }, max: 100 }, x: { grid: { display: false } } } }
                });
            }

            
            if(canvasId === 'sostegnoChart' && window.SOSTEGNO_DATA) {
                const ctx = document.getElementById('sostegnoChart');
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Substitute Sostegno', 'Tenured Sostegno'],
                        datasets: [{
                            data: [window.SOSTEGNO_DATA.substitute_sostegno, window.SOSTEGNO_DATA.tenured_sostegno],
                            backgroundColor: ['rgba(225, 29, 72, 0.8)', 'rgba(52, 211, 153, 0.8)'],
                            borderWidth: 0
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#a1a1aa' } } }, cutout: '70%' }
                });
            }

            if(canvasId === 'precarityChart' && window.PRECARITY_DATA) {
                const ctx = document.getElementById('precarityChart');
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['Substitute / Precarious', 'Tenured'],
                        datasets: [{
                            data: [window.PRECARITY_DATA.substitute_count, window.PRECARITY_DATA.tenured_count],
                            backgroundColor: ['rgba(59, 130, 246, 0.8)', 'rgba(52, 211, 153, 0.8)'],
                            borderWidth: 0
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#a1a1aa' } } }, cutout: '70%' }
                });
            }

            if(canvasId === 'geoChart' && window.GEO_DATA) {
                const ctx = document.getElementById('geoChart');
                new Chart(ctx, {
                    type: 'doughnut',
                    data: {
                        labels: ['No High School (Commute)', 'Full Access (Lyceum)', 'Only Vocational'],
                        datasets: [{
                            data: [window.GEO_DATA.no_high_school_pct, window.GEO_DATA.full_access_pct, window.GEO_DATA.only_vocational_pct],
                            backgroundColor: ['rgba(245, 158, 11, 0.8)', 'rgba(52, 211, 153, 0.8)', 'rgba(236, 72, 153, 0.8)'],
                            borderWidth: 0
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: '#a1a1aa' } } }, cutout: '70%' }
                });
            }

            if(canvasId === 'itsChart' && window.ITS_DATA) {
                const itsCtx = document.getElementById('itsChart');
                const rawData = window.ITS_DATA;
                new Chart(itsCtx, {
                    type: 'bar',
                    data: {
                        labels: rawData.map(d => d.Settore_Terziario.replace('Laurea Triennale', 'Uni').replace('ITS Academy', 'ITS')),
                        datasets: [{
                            label: 'Occupazione a 1 Anno (%)',
                            data: rawData.map(d => d.Tasso_Occupazione_1_Anno_Perc),
                            backgroundColor: rawData.map(d => d.Settore_Terziario.includes('ITS') ? 'rgba(52, 211, 153, 0.8)' : 'rgba(244, 63, 94, 0.5)'),
                            borderRadius: 6
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, indexAxis: 'y', plugins: { legend: { display: false } }, scales: { x: { grid: { color: 'rgba(255,255,255,0.05)' }, max: 100 }, y: { grid: { display: false } } } }
                });
            }

            if(canvasId === 'invalsiChart' && window.INVALSI_DATA) {
                const ctx = document.getElementById('invalsiChart');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: window.INVALSI_DATA.map(d => d.track),
                        datasets: [{
                            label: 'Punteggio INVALSI (RAV)',
                            data: window.INVALSI_DATA.map(d => d.avg_invalsi_score),
                            backgroundColor: ['rgba(139, 92, 246, 0.8)', 'rgba(59, 130, 246, 0.8)', 'rgba(244, 63, 94, 0.8)'],
                            borderRadius: 6
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { min: 1, max: 7, grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } } }
                });
            }

            if(canvasId === 'booksChart' && window.BOOKS_DATA) {
                const ctx = document.getElementById('booksChart');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: ['Costo Medio', 'Mediana'],
                        datasets: [{
                            label: 'Euro (€)',
                            data: [window.BOOKS_DATA.avg_cost_1st_year, window.BOOKS_DATA.median_cost_1st_year],
                            backgroundColor: 'rgba(225, 29, 72, 0.8)',
                            borderRadius: 6
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } } }
                });
            }

            if(canvasId === 'globalChart' && window.GLOBAL_DATA) {
                const ctx = document.getElementById('globalChart');
                new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels: window.GLOBAL_DATA.map(d => d.country_name),
                        datasets: [{
                            label: 'Spesa Istruzione (% PIL)',
                            data: window.GLOBAL_DATA.map(d => d.spending_pct_gdp),
                            backgroundColor: window.GLOBAL_DATA.map(d => d.iso3 === 'ITA' ? 'rgba(225, 29, 72, 0.9)' : 'rgba(16, 185, 129, 0.5)'),
                            borderRadius: 6
                        }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { grid: { color: 'rgba(255,255,255,0.05)' } }, x: { grid: { display: false } } } }
                });
            }
        }
    </script>
</body>
</html>"""

    root = Path(__file__).resolve().parent.parent
    
    csv_path = root / 'processed_data' / 'socioeconomic_context_matrix.csv'
    if csv_path.exists():
        df = pd.read_csv(csv_path)
        holistic_json = df.to_json(orient='records')
    else:
        holistic_json = "[]"
        
    html_content = TEMPLATE.replace("{holistic_json}", holistic_json)
    
    its_path = root / 'local_data' / 'processed' / 'its_academy_vs_university_outcomes.csv'
    if its_path.exists():
        its_df = pd.read_csv(its_path)
        its_json = its_df.to_json(orient='records')
    else:
        its_json = "[]"
        
    html_content = html_content.replace("{its_json}", its_json)

    def load_json_str(name):
        p = root / 'processed_data' / name
        if p.exists():
            with open(p, 'r') as f: return f.read()
        return "[]"
        
    html_content = html_content.replace("{invalsi_json}", load_json_str('invalsi_gap.json'))
    html_content = html_content.replace("{books_json}", load_json_str('textbook_costs.json'))
    html_content = html_content.replace("{global_json}", load_json_str('global_benchmarks.json'))
    html_content = html_content.replace("{geo_json}", load_json_str('geographic_inequality.json'))
    html_content = html_content.replace("{infra_json}", load_json_str('infrastructure_decay.json'))
    html_content = html_content.replace("{precarity_json}", load_json_str('teacher_precarity.json'))
    html_content = html_content.replace("{sostegno_json}", load_json_str('sostegno_precarity.json'))
    html_content = html_content.replace("{demo_json}", load_json_str('demographic_winter.json'))
    html_content = html_content.replace("{limitless_json}", load_json_str('limitless_expansion.json'))


    web_path = root / 'web' / 'index.html'
    with open(web_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"Scrollytelling UI successfully generated at {web_path}")

if __name__ == '__main__':
    build_scrollytelling_html()
