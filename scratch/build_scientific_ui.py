import re

with open('web/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Split around the main content
header_part = text.split('<main class="max-w-6xl mx-auto px-4 space-y-24 pt-8">')[0]
main_and_footer = text.split('<main class="max-w-6xl mx-auto px-4 space-y-24 pt-8">')[1]

# Extract hero (which acts as Title/Authors section)
hero_part = main_and_footer.split('<!-- ========================== -->\n<!-- OPEN RESEARCH SYNTHESIS    -->')[0]

# Extract lab
lab_part = '<!-- ============================================= -->\n<!-- THE EXPERT LABORATORY' + main_and_footer.split('<!-- ============================================= -->\n<!-- THE EXPERT LABORATORY')[1]

academic_body = """
<!-- ========================== -->
<!-- ACADEMIC PAPER STRUCTURE   -->
<!-- ========================== -->

<article class="max-w-4xl mx-auto space-y-16 text-zinc-300">
    
    <!-- 1. ABSTRACT & MOTIVATION -->
    <section id="abstract" class="space-y-6 scroll-mt-24">
        <div class="border-b border-zinc-700 pb-2">
            <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="1. Abstract & Motivazione" data-en="1. Abstract & Motivation"></span></h2>
        </div>
        <p class="text-base leading-relaxed text-justify">
            <span class="i18n" data-it="L'Italia affronta una doppia crisi sistemica: un <i>inverno demografico</i> che causerà la perdita di oltre 1 milione di studenti nel prossimo decennio, e un'emorragia di capitale umano caratterizzata da un tasso di NEET (Not in Education, Employment, or Training) al 23.1%. Questo studio empirico indaga le radici strutturali di tale fenomeno, ipotizzando che la causa primaria risieda nell'obsolescenza del <b>sistema educativo tripartito</b> (Licei, Tecnici, Professionali) combinato con barriere economiche d'accesso incostituzionali. L'obiettivo è fornire una sintesi open-data olistica, ispirata alle metodologie dei MOOC internazionali sull'educazione, per guidare policy evidence-based." data-en="Italy faces a dual systemic crisis: a <i>demographic winter</i> that will cause the loss of over 1 million students in the next decade, and a hemorrhage of human capital characterized by a NEET rate of 23.1%. This empirical study investigates the structural roots of this phenomenon, hypothesizing that the primary cause lies in the obsolescence of the <b>tripartite educational system</b> combined with unconstitutional economic barriers to entry. The goal is to provide a holistic open-data synthesis, inspired by international MOOC methodologies on education, to guide evidence-based policy."></span>
        </p>
    </section>

    <!-- 2. THEORETICAL FRAMEWORK -->
    <section id="framework" class="space-y-8 scroll-mt-24">
        <div class="border-b border-zinc-700 pb-2">
            <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="2. Framework Teorico" data-en="2. Theoretical Framework"></span></h2>
        </div>
        
        <div class="space-y-4">
            <h3 class="text-xl font-bold text-indigo-400"><span class="i18n" data-it="2.1 Il Triangolo OED di Goldthorpe" data-en="2.1 Goldthorpe's OED Triangle"></span></h3>
            <p class="text-base leading-relaxed text-justify">
                <span class="i18n" data-it="Ci basiamo sul modello sociologico di John H. Goldthorpe per misurare la mobilità sociale tramite il triangolo <b>OED (Origins - Education - Destinations)</b>. In Italia, lo smistamento precoce degli studenti a 14 anni (<i>Early Tracking</i>) solidifica il legame tra l'estrazione socio-economica (Origini) e i percorsi formativi (Educazione). I licei attraggono i ceti borghesi, mentre i professionali fungono da parcheggio per le classi svantaggiate, predeterminandone il futuro lavorativo o lo status di NEET (Destinazioni)." data-en="We rely on John H. Goldthorpe's sociological model to measure social mobility via the <b>OED (Origins - Education - Destinations)</b> triangle. In Italy, early tracking at age 14 solidifies the link between socio-economic extraction (Origins) and educational paths (Education). Lyceums attract the middle classes, while vocational schools act as a parking lot for disadvantaged classes, predetermining their future employment or NEET status (Destinations)."></span>
            </p>
        </div>

        <div class="space-y-4">
            <h3 class="text-xl font-bold text-amber-400"><span class="i18n" data-it="2.2 Analisi Comparata dei Sistemi Tripartiti" data-en="2.2 Comparative Analysis of Tripartite Systems"></span></h3>
            <p class="text-base leading-relaxed text-justify">
                <span class="i18n" data-it="Sebbene anche nazioni come la Germania e la Svizzera (area DACH) utilizzino il sistema tripartito, esse vantano tassi di NEET inferiori all'8%. La devianza italiana (23.1%) si spiega con l'assenza di un <b>Dual System (VET)</b> integrato col mondo del lavoro e col massiccio definanziamento degli Istituti Professionali. Al contrario, nazioni come il Regno Unito hanno abolito il <i>tripartism</i> negli anni '60 in favore del sistema <b>Comprehensive</b> fino a 16 anni, uniformando il capitale culturale di base." data-en="Although nations like Germany and Switzerland (DACH area) also use the tripartite system, they boast NEET rates below 8%. The Italian deviance (23.1%) is explained by the absence of a <b>Dual System (VET)</b> integrated with the labor market and the massive defunding of Vocational Institutes. Conversely, nations like the UK abolished tripartism in the 1960s in favor of the <b>Comprehensive</b> system up to age 16, standardizing foundational cultural capital."></span>
            </p>
        </div>
    </section>

    <!-- 3. EMPIRICAL EVIDENCE -->
    <section id="evidence" class="space-y-8 scroll-mt-24">
        <div class="border-b border-zinc-700 pb-2">
            <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="3. Evidenze Empiriche" data-en="3. Empirical Evidence"></span></h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
            <div class="space-y-4">
                <h3 class="text-lg font-bold text-red-400"><span class="i18n" data-it="3.1 Dropout e Fuga di Talenti" data-en="3.1 Dropout and Brain Drain"></span></h3>
                <p class="text-sm text-justify leading-relaxed">
                    <span class="i18n" data-it="I tassi di bocciatura sfiorano il 15% nei professionali già al primo anno. Questa pedagogia punitiva, accoppiata alla segregazione geografica, alimenta un drammatico <i>Brain Drain</i>: il Sud Italia perde oltre 26.000 laureati all'anno." data-en="Repetition rates reach 15% in vocational schools in the first year alone. This punitive pedagogy, coupled with geographic segregation, fuels a dramatic <i>Brain Drain</i>: Southern Italy loses over 26,000 graduates annually."></span>
                </p>
                <img src="https://raw.githubusercontent.com/Eugenix94/Italienation/main/archive/data_processed/charts/neet_analysis/s4_dropout_trend.png" alt="Dropout Trend" class="rounded border border-zinc-700 w-full">
            </div>
            
            <div class="space-y-4">
                <h3 class="text-lg font-bold text-violet-400"><span class="i18n" data-it="3.2 Barriere Economiche e Costo Libri" data-en="3.2 Economic Barriers and Book Costs"></span></h3>
                <p class="text-sm text-justify leading-relaxed">
                    <span class="i18n" data-it="L'Italia viola il principio costituzionale della gratuità dell'istruzione imponendo l'acquisto privato dei testi (al contrario del sistema a comodato d'uso britannico). Il costo medio al primo anno di superiori supera i €310." data-en="Italy violates the constitutional principle of free education by mandating private textbook purchases (unlike the British class-set loan system). The average cost in the first year of upper secondary exceeds €310."></span>
                </p>
                <img src="https://raw.githubusercontent.com/Eugenix94/Italienation/main/archive/data_processed/charts/textbooks/lb_02_total_annual_cost.png" alt="Book Costs" class="rounded border border-zinc-700 w-full">
            </div>
        </div>
    </section>

    <!-- 4. GEOSPATIAL CASE STUDY -->
    <section id="spatial" class="space-y-8 scroll-mt-24">
        <div class="border-b border-zinc-700 pb-2">
            <h2 class="text-2xl font-bold text-white uppercase tracking-wider"><span class="i18n" data-it="4. Caso Studio Geospaziale" data-en="4. Geospatial Case Study"></span></h2>
        </div>
        <p class="text-base leading-relaxed text-justify">
            <span class="i18n" data-it="L'applicazione del framework OED si materializza nello spazio urbano. Mappando i dataset geolocalizzati (Folium JS), emerge la polarizzazione tra centro e periferia: i Licei dominano i quartieri abbienti, mentre gli istituti Tecnici e Professionali sono reclusi nelle aree industriali limitrofe. Esplora la mappa interattiva sottostante:" data-en="The application of the OED framework materializes in urban space. By mapping geolocated datasets (Folium JS), polarization between the center and the periphery emerges: Lyceums dominate wealthy neighborhoods, while Technical and Vocational institutes are confined to adjacent industrial areas. Explore the interactive map below:"></span>
        </p>
        <div class="h-[450px] w-full rounded-lg overflow-hidden border border-zinc-700 shadow-2xl">
            <iframe src="interactive_map.html" class="w-full h-full border-none" title="Geospatial Map"></iframe>
        </div>
    </section>

    <!-- 5. FUTURE EXPANSION: THE HF BLIND SPOTS -->
    <section id="future" class="space-y-6 scroll-mt-24 bg-zinc-900/50 p-8 rounded-xl border border-zinc-800">
        <h2 class="text-xl font-bold text-cyan-400 uppercase tracking-wider"><span class="i18n" data-it="5. Direttrici di Sviluppo (I Punti Ciechi)" data-en="5. Development Vectors (The Blind Spots)"></span></h2>
        <p class="text-base leading-relaxed text-justify">
            <span class="i18n" data-it="Per completare l'indagine empirica, l'osservatorio sta integrando nuovi archivi raw prelevati da HuggingFace. Le prossime validazioni scientifiche copriranno i 'Blind Spots' strutturali:" data-en="To complete the empirical investigation, the observatory is integrating new raw archives retrieved from HuggingFace. Upcoming scientific validations will cover structural 'Blind Spots':"></span>
        </p>
        <ul class="list-disc list-inside space-y-2 text-zinc-400">
            <li><strong class="text-zinc-200">Valutazione INVALSI:</strong> Misurazione oggettiva del gap di competenze (Scores).</li>
            <li><strong class="text-zinc-200">Edilizia Scolastica:</strong> Impatto della fatiscenza infrastrutturale al Sud.</li>
            <li><strong class="text-zinc-200">Personale Docente:</strong> Analisi del tasso di turnover e precariato.</li>
        </ul>
    </section>

</article>
"""

# update navbar to match scientific sections
nav_replacement = """        <nav class="desk-nav hidden sm:flex items-center gap-1 overflow-x-auto text-xs py-1" id="dNav">
            <a href="#hero" class="active"><span class="i18n" data-it="1. Abstract" data-en="1. Abstract"></span></a>
            <a href="#framework"><span class="i18n" data-it="2. Framework" data-en="2. Framework"></span></a>
            <a href="#evidence"><span class="i18n" data-it="3. Evidenze" data-en="3. Evidence"></span></a>
            <a href="#spatial"><span class="i18n" data-it="4. Caso Spaziale" data-en="4. Spatial Case"></span></a>
            <a href="#laboratorio"><span class="i18n" data-it="5. Metodologia" data-en="5. Methodology"></span></a>
        </nav>"""
header_part = re.sub(r'<nav class="desk-nav.*?id="dNav">.*?</nav>', nav_replacement, header_part, flags=re.DOTALL)

mob_nav_replacement = """<nav class="bottom-nav flex items-center justify-around sm:hidden" id="bNav">
    <a href="#hero" class="active"><span class="text-lg">📄</span></a>
    <a href="#evidence"><span class="text-lg">📊</span></a>
    <a href="#spatial"><span class="text-lg">🗺️</span></a>
    <a href="#laboratorio"><span class="text-lg">🔬</span></a>
</nav>"""
lab_part = re.sub(r'<nav class="bottom-nav.*?id="bNav">.*?</nav>', mob_nav_replacement, lab_part, flags=re.DOTALL)

# Also rename "THE EXPERT LABORATORY" to "5. OPEN DATA & METHODOLOGY" in the UI
lab_part = lab_part.replace('Il Laboratorio per Esperti', '5. Open Data & Methodology Repository')
lab_part = lab_part.replace('The Expert Laboratory', '5. Open Data & Methodology Repository')


final_html = header_part + '<main class="max-w-6xl mx-auto px-4 space-y-24 pt-8">' + hero_part + academic_body + lab_part

with open('web/index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)
print("Scientific Academic layout applied.")
