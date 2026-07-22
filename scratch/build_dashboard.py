import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

header_part = text.split('<main class="max-w-6xl mx-auto px-4 space-y-24 pt-8">')[0]
main_and_footer = text.split('<main class="max-w-6xl mx-auto px-4 space-y-24 pt-8">')[1]

# Extract hero
hero_part = main_and_footer.split('<!-- ========================== -->\n<!-- THE NARRATIVE MANIFESTO    -->')[0]

# Extract laboratory
lab_part = '<!-- ============================================= -->\n<!-- THE EXPERT LABORATORY' + main_and_footer.split('<!-- ============================================= -->\n<!-- THE EXPERT LABORATORY')[1]

new_dashboard = """<!-- ========================== -->
<!-- OPEN RESEARCH SYNTHESIS    -->
<!-- ========================== -->

<section id="synthesis-dashboard" class="space-y-12 pt-8 border-t border-zinc-800/80">
    <div class="text-center space-y-4 max-w-3xl mx-auto">
        <h2 class="text-3xl md:text-5xl font-black tracking-tight text-white"><span class="i18n" data-it="Sintesi della Ricerca Aperta" data-en="Open Research Synthesis"></span></h2>
        <p class="text-zinc-400 text-sm md:text-base leading-relaxed"><span class="i18n" data-it="Un'esplorazione olistica e multidimensionale del fenomeno Italienation. Dalle teorie sociologiche di Goldthorpe alle evidenze macroeconomiche sui NEET." data-en="A holistic, multidimensional exploration of the Italienation phenomenon. From Goldthorpe's sociological theories to macroeconomic evidence on NEETs."></span></p>
    </div>

    <!-- BENTO BOX GRID -->
    <div class="grid grid-cols-1 md:grid-cols-12 gap-6 auto-rows-[auto]">
        
        <!-- CARD 1: GOLDTHORPE OED (Span 8) -->
        <div id="goldthorpe" class="md:col-span-8 glass p-6 rounded-3xl border border-indigo-500/30 flex flex-col justify-between space-y-6 hover:border-indigo-500/60 transition">
            <div class="space-y-2">
                <div class="flex items-center gap-2 mb-2">
                    <span class="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 font-bold text-xs uppercase tracking-wider">Sociologia</span>
                </div>
                <h3 class="text-2xl font-black text-white"><span class="i18n" data-it="Il Triangolo OED di Goldthorpe: L'Educazione come Destino" data-en="Goldthorpe's OED Triangle: Education as Destiny"></span></h3>
                <p class="text-zinc-300 text-sm leading-relaxed"><span class="i18n" data-it="John H. Goldthorpe (Oxford) utilizza il triangolo <b>OED</b> (Origins, Education, Destinations) per misurare la mobilità sociale. In Italia, la scelta precoce a 14 anni (Early Tracking) agisce da cinghia di trasmissione fortissima tra le <b>Origini (O)</b> di classe e l'<b>Educazione (E)</b>. A differenza del Regno Unito, dove il sistema <i>Comprehensive</i> tenta di rompere il legame O-E posticipando le scelte, l'Italia utilizza la segregazione in Istituti Professionali per cristallizzare le <b>Destinazioni (D)</b> sociali, rendendo il sistema impermeabile all'ascensore sociale." data-en="John H. Goldthorpe (Oxford) uses the <b>OED</b> triangle (Origins, Education, Destinations) to measure social mobility. In Italy, early tracking at age 14 acts as a powerful transmission belt between class <b>Origins (O)</b> and <b>Education (E)</b>. Unlike the UK, where the <i>Comprehensive</i> system attempts to break the O-E link by delaying choices, Italy uses segregation into Vocational institutes to crystallize social <b>Destinations (D)</b>, rendering the system impervious to upward mobility."></span></p>
            </div>
            
            <div class="bg-zinc-950/80 p-5 rounded-2xl border border-zinc-800 flex justify-center items-center gap-4 sm:gap-12 relative overflow-hidden">
                <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0IiBoZWlnaHQ9IjQiPjxyZWN0IHdpZHRoPSI0IiBoZWlnaHQ9IjQiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iMC4wNSIvPjwvc3ZnPg==')] opacity-20 pointer-events-none"></div>
                <div class="text-center z-10">
                    <div class="w-16 h-16 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-black text-2xl mx-auto mb-2 border border-indigo-500/40">O</div>
                    <div class="text-[10px] font-bold text-zinc-400 uppercase">Origins (Classe)</div>
                </div>
                <div class="text-indigo-500 font-black text-2xl z-10">→</div>
                <div class="text-center z-10">
                    <div class="w-16 h-16 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center font-black text-2xl mx-auto mb-2 border border-amber-500/40">E</div>
                    <div class="text-[10px] font-bold text-zinc-400 uppercase">Education (Tripartita)</div>
                </div>
                <div class="text-indigo-500 font-black text-2xl z-10">→</div>
                <div class="text-center z-10">
                    <div class="w-16 h-16 rounded-full bg-red-500/20 text-red-400 flex items-center justify-center font-black text-2xl mx-auto mb-2 border border-red-500/40">D</div>
                    <div class="text-[10px] font-bold text-zinc-400 uppercase">Destinations (Lavoro/NEET)</div>
                </div>
            </div>
        </div>

        <!-- CARD 2: INTERNATIONAL COMPARISON (Span 4) -->
        <div id="international" class="md:col-span-4 glass p-6 rounded-3xl border border-amber-500/30 space-y-4 flex flex-col justify-between hover:border-amber-500/60 transition">
            <div class="space-y-2">
                <div class="flex items-center gap-2 mb-2">
                    <span class="px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 font-bold text-xs uppercase tracking-wider">Comparazione Globale</span>
                </div>
                <h3 class="text-xl font-black text-white leading-tight"><span class="i18n" data-it="L'Anomalia Tripartita: IT vs DACH vs UK" data-en="The Tripartite Anomaly: IT vs DACH vs UK"></span></h3>
                <p class="text-zinc-400 text-xs sm:text-sm leading-relaxed"><span class="i18n" data-it="Anche nazioni DACH (Germania, Svizzera) usano l'Early Tracking, ma possiedono un robusto <b>Dual System (VET)</b> che integra l'apprendistato, azzerando i NEET (8.8%). L'Italia mantiene la segregazione tripartita ma senza fondi per i Professionali, creando una fabbrica di NEET (23.1%). Il Regno Unito, invece, usa il modello <b>Comprehensive</b> fino a 16 anni per unificare il capitale culturale." data-en="DACH nations (Germany, Switzerland) also use Early Tracking, but possess a robust <b>Dual System (VET)</b> integrating apprenticeships, minimizing NEETs (8.8%). Italy maintains tripartite segregation but underfunds Vocational schools, creating a NEET factory (23.1%). The UK, conversely, uses the <b>Comprehensive</b> model up to age 16 to unify cultural capital."></span></p>
            </div>
            <div class="space-y-2">
                <div class="bg-zinc-950/80 p-3 rounded-xl border border-zinc-800 flex justify-between items-center">
                    <span class="text-xs text-zinc-300">🇩🇪 DACH (Dual System)</span>
                    <span class="text-emerald-400 font-black text-sm">NEET ~8%</span>
                </div>
                <div class="bg-zinc-950/80 p-3 rounded-xl border border-zinc-800 flex justify-between items-center">
                    <span class="text-xs text-zinc-300">🇬🇧 UK (Comprehensive)</span>
                    <span class="text-amber-400 font-black text-sm">NEET 12.6%</span>
                </div>
                <div class="bg-zinc-950/80 p-3 rounded-xl border border-red-500/30 flex justify-between items-center">
                    <span class="text-xs text-zinc-300 font-bold">🇮🇹 IT (Underfunded Tripartite)</span>
                    <span class="text-red-400 font-black text-sm">NEET 23.1%</span>
                </div>
            </div>
        </div>

        <!-- CARD 3: THE MAP (Span 12) -->
        <div id="geospatial" class="md:col-span-12 glass p-6 rounded-3xl border border-emerald-500/30 space-y-4 hover:border-emerald-500/60 transition">
            <div class="flex items-center justify-between">
                <span class="px-3 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-bold text-xs uppercase tracking-wider">Spazio Urbano & Segregazione</span>
                <span class="text-xs text-zinc-500 font-mono">Folium JS Engine</span>
            </div>
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div class="lg:col-span-1 space-y-4">
                    <h3 class="text-2xl font-black text-white leading-tight"><span class="i18n" data-it="La Materializzazione Geografica del Tripartitismo" data-en="The Geographic Materialization of Tripartism"></span></h3>
                    <p class="text-zinc-300 text-sm leading-relaxed"><span class="i18n" data-it="Il framework di Goldthorpe diventa fisico nella geografia urbana. Esplora il caso studio di Catania: i <b>Licei</b> (Blu) dominano i quartieri centrali ad alto reddito, mentre gli <b>Istituti Professionali</b> (Rosso) sono confinati nelle periferie industriali sud. La pedagogia determina l'urbanistica." data-en="Goldthorpe's framework becomes physical in urban geography. Explore the Catania case study: <b>Lyceums</b> (Blue) dominate wealthy central districts, while <b>Vocational Institutes</b> (Red) are confined to southern industrial suburbs. Pedagogy dictates urbanism."></span></p>
                </div>
                <div class="lg:col-span-2 relative h-[400px] rounded-2xl overflow-hidden border border-zinc-700/50">
                    <iframe src="interactive_map.html" class="w-full h-full border-none" title="Mappa Geospaziale delle Scuole Italiane e Caso Catania"></iframe>
                </div>
            </div>
        </div>

        <!-- CARD 4: DROPOUT & BRAIN DRAIN (Span 6) -->
        <div class="md:col-span-6 glass p-6 rounded-3xl border border-red-500/30 space-y-4 hover:border-red-500/60 transition flex flex-col">
            <div class="flex items-center gap-2 mb-2">
                <span class="px-3 py-1 rounded-full bg-red-500/20 text-red-300 font-bold text-xs uppercase tracking-wider">Evidence Lab</span>
            </div>
            <h3 class="text-xl font-black text-white leading-tight"><span class="i18n" data-it="Trappola Dropout & Fuga di Talenti" data-en="Dropout Trap & Talent Flight"></span></h3>
            <p class="text-zinc-300 text-sm leading-relaxed"><span class="i18n" data-it="Nei professionali il tasso di bocciatura supera il 14.8%. Questo alimenta direttamente la perdita sistemica di capitale umano (Brain Drain) verso il Nord o l'estero (-26k laureati/anno dal Sud)." data-en="Vocational repetition rates exceed 14.8%. This directly fuels the systemic loss of human capital (Brain Drain) towards the North or abroad (-26k graduates/year from the South)."></span></p>
            <div class="grid grid-cols-2 gap-4 mt-auto pt-4">
                <img src="https://raw.githubusercontent.com/Eugenix94/Italienation/main/archive/data_processed/charts/neet_analysis/s4_dropout_trend.png" alt="Dropout Trend" class="rounded-xl border border-zinc-800 w-full hover:scale-105 transition duration-300 cursor-pointer">
                <img src="https://raw.githubusercontent.com/Eugenix94/Italienation/main/archive/data_processed/charts/neet_analysis/s5_brain_drain.png" alt="Brain Drain" class="rounded-xl border border-zinc-800 w-full hover:scale-105 transition duration-300 cursor-pointer">
            </div>
        </div>

        <!-- CARD 5: ECONOMIC BARRIERS (Span 6) -->
        <div class="md:col-span-6 glass p-6 rounded-3xl border border-violet-500/30 space-y-4 hover:border-violet-500/60 transition flex flex-col">
            <div class="flex items-center gap-2 mb-2">
                <span class="px-3 py-1 rounded-full bg-violet-500/20 text-violet-300 font-bold text-xs uppercase tracking-wider">Barriere Occulte</span>
            </div>
            <h3 class="text-xl font-black text-white leading-tight"><span class="i18n" data-it="Costi di Ingresso: Il Mercato dei Libri" data-en="Entry Costs: The Textbook Market"></span></h3>
            <p class="text-zinc-300 text-sm leading-relaxed"><span class="i18n" data-it="A differenza del Regno Unito (Class Sets gratuiti), l'Italia impone l'acquisto privato dei libri. Il costo annuo al primo anno superiore supera mediamente i €310, erigendo una barriera di censo incostituzionale all'ingresso dell'istruzione superiore." data-en="Unlike the UK (free Class Sets), Italy forces private textbook purchases. The annual cost in the first year of upper secondary averages over €310, erecting an unconstitutional wealth barrier to entry."></span></p>
            <div class="mt-auto pt-4 flex justify-center">
                <img src="https://raw.githubusercontent.com/Eugenix94/Italienation/main/archive/data_processed/charts/textbooks/lb_02_total_annual_cost.png" alt="Textbook Annual Cost" class="rounded-xl border border-zinc-800 max-h-[180px] hover:scale-105 transition duration-300 cursor-pointer">
            </div>
        </div>

    </div>
</section>
"""

# update navbar
nav_replacement = """        <nav class="desk-nav hidden sm:flex items-center gap-1 overflow-x-auto text-xs py-1" id="dNav">
            <a href="#hero" class="active"><span class="i18n" data-it="🏠 Home" data-en="🏠 Home"></span></a>
            <a href="#goldthorpe"><span class="i18n" data-it="📊 OED & Sociologia" data-en="📊 OED & Sociology"></span></a>
            <a href="#international"><span class="i18n" data-it="🌍 Globale" data-en="🌍 Global"></span></a>
            <a href="#geospatial"><span class="i18n" data-it="🗺️ Spazio Urbano" data-en="🗺️ Urban Space"></span></a>
            <a href="#laboratorio"><span class="i18n" data-it="🔬 Laboratorio" data-en="🔬 Lab"></span></a>
        </nav>"""
header_part = re.sub(r'<nav class="desk-nav.*?id="dNav">.*?</nav>', nav_replacement, header_part, flags=re.DOTALL)

mob_nav_replacement = """<nav class="bottom-nav flex items-center justify-around sm:hidden" id="bNav">
    <a href="#hero" class="active"><span class="text-lg">🏠</span></a>
    <a href="#goldthorpe"><span class="text-lg">📊</span></a>
    <a href="#geospatial"><span class="text-lg">🗺️</span></a>
    <a href="#laboratorio"><span class="text-lg">🔬</span></a>
</nav>"""
lab_part = re.sub(r'<nav class="bottom-nav.*?id="bNav">.*?</nav>', mob_nav_replacement, lab_part, flags=re.DOTALL)


final_html = header_part + '<main class="max-w-6xl mx-auto px-4 space-y-24 pt-8">' + hero_part + new_dashboard + lab_part

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)
print("Dashboard completely applied.")
