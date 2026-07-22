import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# get the part before <main>
header_part = text.split('<main class="max-w-6xl mx-auto px-4 space-y-24 pt-8">')[0]
# get the part after <main>
main_and_footer = text.split('<main class="max-w-6xl mx-auto px-4 space-y-24 pt-8">')[1]

# inside main, keep #hero
hero_part = main_and_footer.split('<!-- ========================== -->\n<!-- §2 MANIFESTO CIVICO & ATLANTE -->')[0]
if '<!-- ========================== -->\n<!-- THE NARRATIVE MANIFESTO    -->' in hero_part:
    hero_part = hero_part.split('<!-- ========================== -->\n<!-- THE NARRATIVE MANIFESTO    -->')[0]

# get the laboratory part (the old raw data section)
lab_part_split = main_and_footer.split('<!-- ========================= -->\n<!-- §6 RAW DATA CATALOG')
if len(lab_part_split) > 1:
    lab_part = '<!-- ========================= -->\n<!-- §6 RAW DATA CATALOG' + lab_part_split[1]
else:
    # it's just '<!-- §6 RAW DATA CATALOG'
    lab_part = '<!-- §6 RAW DATA CATALOG' + main_and_footer.split('<!-- §6 RAW DATA CATALOG')[1]

new_body = """<!-- ========================== -->
<!-- THE NARRATIVE MANIFESTO    -->
<!-- ========================== -->

<!-- CHAPTER 1 -->
<section id="ch1" class="space-y-6 pt-10 border-t border-zinc-800/80">
    <div class="flex items-center gap-3">
        <span class="px-3 py-1 rounded-full bg-indigo-500/20 text-indigo-300 font-bold text-xs uppercase tracking-wider">Capitolo 1</span>
    </div>
    <h2 class="text-3xl md:text-4xl font-black tracking-tight text-white"><span class="i18n" data-it="L'Inverno Demografico e la Condanna della Culla" data-en="The Demographic Winter & Cradle Condemnation"></span></h2>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        <div class="space-y-4 text-zinc-300 text-sm md:text-base leading-relaxed">
            <p><span class="i18n" data-it="L'Italia sta affrontando una crisi demografica senza precedenti. Tra il 2014 e il 2024, la popolazione scolastica è crollata di oltre <b class='text-white'>1 milione di alunni</b>, portando alla chiusura di quasi <b class='text-white'>3.000 scuole</b> (Dati MIM/ISTAT)." data-en="Italy is facing an unprecedented demographic crisis. Between 2014 and 2024, the school population collapsed by over <b class='text-white'>1 million students</b>, leading to the closure of nearly <b class='text-white'>3,000 schools</b> (MIM/ISTAT data)."></span></p>
            <p><span class="i18n" data-it="Ma la povertà educativa inizia ancora prima: a 0-2 anni. La copertura degli asili nido comunali varia dal <b class='text-white'>41.2%</b> di Bologna al <b class='text-white'>8.9%</b> di Catania. Questo divario iniziale predetermina le competenze già al secondo anno di elementare, sancendo una 'condanna' basata puramente sul codice di avviamento postale in cui si nasce." data-en="But educational poverty starts even earlier: at 0-2 years. Municipal daycare coverage varies from <b class='text-white'>41.2%</b> in Bologna to <b class='text-white'>8.9%</b> in Catania. This initial gap predetermines skills by Grade 2, cementing a 'condemnation' based purely on the zip code of birth."></span></p>
        </div>
        <div class="glass p-6 rounded-2xl border-l-4 border-l-indigo-500">
            <h3 class="font-bold text-indigo-400 mb-2">Il Dato Chiave (Notebook 16)</h3>
            <p class="text-xs text-zinc-400">Le proiezioni ISTAT stimano un ulteriore calo di 1.5 milioni di studenti entro il 2034. Senza un ripensamento del sistema strutturale, le aree interne e periferiche del Sud rischiano la completa desertificazione delle infrastrutture educative.</p>
        </div>
    </div>
</section>

<!-- CHAPTER 2 -->
<section id="ch2" class="space-y-6 pt-16">
    <div class="flex items-center gap-3">
        <span class="px-3 py-1 rounded-full bg-amber-500/20 text-amber-300 font-bold text-xs uppercase tracking-wider">Capitolo 2</span>
    </div>
    <h2 class="text-3xl md:text-4xl font-black tracking-tight text-white"><span class="i18n" data-it="Il Bivio a 14 Anni: La Mappa della Segregazione" data-en="The Age-14 Fork: The Map of Segregation"></span></h2>
    
    <div class="space-y-4 text-zinc-300 text-sm md:text-base leading-relaxed max-w-4xl">
        <p><span class="i18n" data-it="A soli 14 anni, il sistema italiano impone una scelta irreversibile (Liceo, Tecnico o Professionale). Questa separazione precoce (Early Tracking), bandita nel modello Comprehensive britannico o scandinavo, agisce come un rigido filtro di classe. Come vediamo nella mappa qui sotto, questa separazione didattica si traduce in una segregazione urbanistica reale: i Licei (Blu) si concentrano nei centri storici ricchi, mentre gli Istituti Tecnici/Professionali (Verde/Rosso) vengono spinti nelle periferie industriali." data-en="At just 14, the Italian system forces an irreversible choice (Lyceum, Technical, or Vocational). This early tracking, banned in the British or Nordic Comprehensive model, acts as a rigid class filter. As seen in the map below, this pedagogical separation translates into real urban segregation: Lyceums (Blue) cluster in wealthy historic centers, while Technical/Vocational institutes (Green/Red) are pushed to industrial suburbs."></span></p>
    </div>

    <!-- EMBEDDED FOLIUM MAP -->
    <div class="w-full h-[600px] rounded-2xl overflow-hidden border-2 border-amber-500/40 shadow-2xl shadow-amber-500/10 relative">
        <div class="absolute top-4 left-14 z-10 bg-zinc-950/80 backdrop-blur px-3 py-2 rounded-xl border border-zinc-700 text-xs text-zinc-300 pointer-events-none">
            <div class="flex items-center gap-2"><div class="w-3 h-3 rounded-full bg-[#3b82f6]"></div> Liceo (Accademico)</div>
            <div class="flex items-center gap-2 mt-1"><div class="w-3 h-3 rounded-full bg-[#10b981]"></div> Istituto Tecnico</div>
            <div class="flex items-center gap-2 mt-1"><div class="w-3 h-3 rounded-full bg-[#ef4444]"></div> Ist. Professionale</div>
        </div>
        <iframe src="interactive_map.html" class="w-full h-full border-none" title="Mappa Geospaziale delle Scuole Italiane e Caso Catania"></iframe>
    </div>
    <p class="text-xs text-zinc-500 text-center"><span class="i18n" data-it="Mappa Interattiva: Esplora il Campione Nazionale o fai zoom su Catania per osservare la distribuzione spaziale. Generata dal Quaderno 18." data-en="Interactive Map: Explore the National Sample or zoom into Catania to observe spatial distribution. Generated by Notebook 18."></span></p>
</section>

<!-- CHAPTER 3 -->
<section id="ch3" class="space-y-6 pt-16">
    <div class="flex items-center gap-3">
        <span class="px-3 py-1 rounded-full bg-violet-500/20 text-violet-300 font-bold text-xs uppercase tracking-wider">Capitolo 3</span>
    </div>
    <h2 class="text-3xl md:text-4xl font-black tracking-tight text-white"><span class="i18n" data-it="Il Divario Curricolare: Frammentazione vs Poliedricità" data-en="The Curricular Gap: Fragmentation vs Polymathy"></span></h2>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
        <div class="space-y-4 text-zinc-300 text-sm md:text-base leading-relaxed">
            <p><span class="i18n" data-it="L'Italia soffre di una frammentazione estrema: oltre 1.100 materie legali uniche e 80+ indirizzi scolastici. Un quindicenne britannico nel sistema <b class='text-white'>Comprehensive</b> studia fianco a fianco coi suoi coetanei, potendo mescolare Arte, Fisica e Falegnameria." data-en="Italy suffers from extreme fragmentation: over 1,100 unique legal subjects and 80+ school tracks. A 15-year-old in the British <b class='text-white'>Comprehensive</b> system studies alongside peers, able to mix Art, Physics, and Carpentry."></span></p>
            <p><span class="i18n" data-it="In Italia, lo studente del Classico non toccherà mai l'Economia Aziendale, e quello del Professionale non leggerà mai Kant. Questo distrugge la <b>'Poliedricità'</b> (Polymathy Index): la capacità del capitale umano di adattarsi rapidamente ai cambiamenti tecnologici globali." data-en="In Italy, the Classical student will never touch Business Economics, and the Vocational student will never read Kant. This destroys <b>'Polymathy'</b>: the human capital's ability to adapt rapidly to global technological shifts."></span></p>
            
            <div class="glass p-4 rounded-xl border border-violet-500/30 mt-4">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-violet-400">Polymathy Index (Capacità di Ibridazione)</span>
                </div>
                <div class="space-y-3">
                    <div>
                        <div class="flex justify-between text-[11px] mb-1"><span>🇬🇧 UK Comprehensive (GCSE)</span><span class="text-emerald-400">92%</span></div>
                        <div class="w-full bg-zinc-900 h-1.5 rounded-full"><div class="bg-emerald-500 h-full rounded-full" style="width: 92%"></div></div>
                    </div>
                    <div>
                        <div class="flex justify-between text-[11px] mb-1"><span>🇮🇹 IT Liceo Scientifico</span><span class="text-violet-400">28%</span></div>
                        <div class="w-full bg-zinc-900 h-1.5 rounded-full"><div class="bg-violet-500 h-full rounded-full" style="width: 28%"></div></div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="grid grid-cols-1 gap-4">
            <div class="bg-zinc-950/80 p-5 rounded-2xl border border-red-500/30">
                <div class="text-[11px] text-red-400 font-bold uppercase mb-2">La Barriera Economica: Libri di Testo</div>
                <div class="flex items-baseline justify-between">
                    <div><span class="text-3xl font-black text-white">€310</span> <span class="text-xs text-zinc-500">Spesa Media IT 1° Anno</span></div>
                    <div><span class="text-3xl font-black text-emerald-400">£0</span> <span class="text-xs text-zinc-500">UK (Gratis / Class Sets)</span></div>
                </div>
            </div>
            <div class="bg-zinc-950/80 p-5 rounded-2xl border border-amber-500/30">
                <div class="text-[11px] text-amber-400 font-bold uppercase mb-2">Il Filtro Pedagogico: Bocciature (15 anni)</div>
                <div class="flex items-baseline justify-between">
                    <div><span class="text-3xl font-black text-white">14.8%</span> <span class="text-xs text-zinc-500">Ist. Professionali IT</span></div>
                    <div><span class="text-3xl font-black text-emerald-400"><0.5%</span> <span class="text-xs text-zinc-500">UK Comprehensive</span></div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CHAPTER 4 -->
<section id="ch4" class="space-y-6 pt-16 pb-12 border-b border-zinc-800/80">
    <div class="flex items-center gap-3">
        <span class="px-3 py-1 rounded-full bg-red-500/20 text-red-300 font-bold text-xs uppercase tracking-wider">Capitolo 4</span>
    </div>
    <h2 class="text-3xl md:text-4xl font-black tracking-tight text-white"><span class="i18n" data-it="Esiti Macro: ITS, Fuga di Talenti e Stagnazione TFP" data-en="Macro Outcomes: ITS, Talent Drain & TFP Stagnation"></span></h2>
    
    <div class="space-y-4 text-zinc-300 text-sm md:text-base leading-relaxed max-w-4xl mb-6">
        <p><span class="i18n" data-it="La frammentazione si scontra con il mercato del lavoro. Mentre il 23.1% dei giovani cade nella trappola NEET, gli ITS Academy (Istituti Tecnologici Superiori) garantiscono l'occupazione all'87% dei diplomati, superando molte lauree magistrali." data-en="Fragmentation collides with the labor market. While 23.1% of youths fall into the NEET trap, ITS Academies (Higher Technological Institutes) guarantee employment to 87% of graduates, surpassing many Master's degrees."></span></p>
        <p><span class="i18n" data-it="Ma il risultato più letale è l'emorragia territoriale: il Mezzogiorno perde strutturalmente <b>-26.000 laureati l'anno</b> verso il Nord o l'estero. Questa 'Brain Drain' condanna la Produttività Totale dei Fattori (TFP) dell'intera nazione alla stagnazione perpetua (bloccata da 25 anni), rendendo il sistema economicamente insostenibile." data-en="But the most lethal outcome is territorial hemorrhage: the South structurally loses <b>-26,000 graduates per year</b> to the North or abroad. This 'Brain Drain' condemns the nation's Total Factor Productivity (TFP) to perpetual stagnation (flat for 25 years), rendering the system economically unsustainable."></span></p>
    </div>
</section>

<!-- ============================================= -->
<!-- THE EXPERT LABORATORY (Catalogs & Code)       -->
<!-- ============================================= -->
<section id="laboratorio" class="pt-16 space-y-16">
    <div class="text-center max-w-2xl mx-auto space-y-4 mb-12">
        <h2 class="text-3xl font-black text-white">🔬 Il Laboratorio per Esperti</h2>
        <p class="text-zinc-400 text-sm">Tutte le affermazioni dei capitoli precedenti sono pubblicamente verificabili. Accedi ai cataloghi grezzi ISTAT/MIM, scarica i CSV, ri-esegui i nostri notebook o dibatti i modelli statistici sul forum di GitHub.</p>
    </div>
"""

# Update Navigation
nav_replacement = """        <nav class="desk-nav hidden sm:flex items-center gap-1 overflow-x-auto text-xs py-1" id="dNav">
            <a href="#hero" class="active"><span class="i18n" data-it="🏠 Home" data-en="🏠 Home"></span></a>
            <a href="#ch1"><span class="i18n" data-it="Cap 1. Crisi" data-en="Ch 1. Crisis"></span></a>
            <a href="#ch2"><span class="i18n" data-it="Cap 2. Mappa" data-en="Ch 2. Map"></span></a>
            <a href="#ch3"><span class="i18n" data-it="Cap 3. Curricolo" data-en="Ch 3. Curriculum"></span></a>
            <a href="#ch4"><span class="i18n" data-it="Cap 4. Produttività" data-en="Ch 4. Productivity"></span></a>
            <a href="#laboratorio"><span class="i18n" data-it="🔬 Laboratorio" data-en="🔬 Lab"></span></a>
        </nav>"""
header_part = re.sub(r'<nav class="desk-nav.*?id="dNav">.*?</nav>', nav_replacement, header_part, flags=re.DOTALL)

mob_nav_replacement = """<nav class="bottom-nav flex items-center justify-around sm:hidden" id="bNav">
    <a href="#hero" class="active"><span class="text-lg">🏠</span></a>
    <a href="#ch1"><span class="text-lg">📉</span></a>
    <a href="#ch2"><span class="text-lg">🗺️</span></a>
    <a href="#ch3"><span class="text-lg">📚</span></a>
    <a href="#ch4"><span class="text-lg">🏭</span></a>
    <a href="#laboratorio"><span class="text-lg">🔬</span></a>
</nav>"""
lab_part = re.sub(r'<nav class="bottom-nav.*?id="bNav">.*?</nav>', mob_nav_replacement, lab_part, flags=re.DOTALL)

final_html = header_part + '<main class="max-w-6xl mx-auto px-4 space-y-24 pt-8">' + hero_part + new_body + lab_part

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)
print('Rewrite completed perfectly!')
