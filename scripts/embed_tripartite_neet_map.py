#!/usr/bin/env python3
"""
embed_tripartite_neet_map.py

Upgrades `holistic_analysis/interactive_web_experience/index.html` (and syncs to root `index.html`)
to include Tab 2b: `🎒 Tripartite Orientation vs. NEET Area Map`.

Allows users to click any Macro-Area (`Nord-Ovest`, `Nord-Est`, `Centro`, `Sud`, `Isole`) or individual Region
to view interactive Tripartite formation splits (`% Licei vs % Tecnici vs % Professionali`), Youth NEET rates,
Grade 9 repetition severity (`bocciature`), Industrial Absorption indices, and explicit pedagogical orientation diagnostics.
"""

import os
import pandas as pd

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) if os.path.basename(os.getcwd()) == 'scripts' else os.path.abspath(".")
DATA_DIR = os.path.join(ROOT_DIR, "holistic_analysis", "data_panels")
WEB_DIR = os.path.join(ROOT_DIR, "holistic_analysis", "interactive_web_experience")

os.makedirs(WEB_DIR, exist_ok=True)

print(f"[{WEB_DIR}] Building Tripartite System vs. NEET Area Orientation Map & embedding into index.html...")

# Read Panel 15
df_trip = pd.read_csv(os.path.join(DATA_DIR, "15_tripartite_neet_area_orientation_matrix.csv"))

# Build JSON object for Macro-Areas and Regions
trip_json_entries = []

# First compute Macro-Area aggregates
for macro in ["Nord-Ovest", "Nord-Est", "Centro", "Sud", "Isole"]:
    sub = df_trip[df_trip['macro_area'] == macro]
    if len(sub) > 0:
        l_avg = sub['licei_share_pct'].mean()
        t_avg = sub['tecnici_share_pct'].mean()
        p_avg = sub['professionali_share_pct'].mean()
        n_avg = sub['neet_rate_15_29_pct'].mean()
        b_avg = sub['bocciature_grade9_pct'].mean()
        i_avg = sub['industrial_absorption_index'].mean()
        
        profile = ""
        if macro in ["Nord-Ovest", "Nord-Est"]:
            profile = f"Strong Technical-Vocational Synergy (`~{t_avg+p_avg:.1f}% combined Tecnici/Professionali share`). High industrial district density (`Index: {i_avg:.1f}/100`) directly absorbs graduating youth, maintaining low NEET rates (`{n_avg:.1f}%`)."
        elif macro == "Centro":
            profile = f"Balanced Academic-Technical Split (`{l_avg:.1f}% Licei vs {t_avg:.1f}% Tecnici`). Moderate district absorption (`Index: {i_avg:.1f}/100`) keeps transitions stable (`NEET: {n_avg:.1f}%`), though metropolitan Rome shows high academic tracking."
        else:
            profile = f"Severe Orientation & Absorption Mismatch. High Liceo concentration (`{l_avg:.1f}% share`) lacks local corporate R&D demand (`Absorption Index: {i_avg:.1f}/100`). Meanwhile, Professionali students face high Grade 9 repetition (`bocciature: {b_avg:.1f}%`), driving high implicit dropout and acute NEET traps (`NEET: {n_avg:.1f}%`)."
            
        trip_json_entries.append(f'"{macro} (Macro-Area)": {{"type": "Macro-Area", "macro": "{macro}", "licei": {l_avg:.1f}, "tecnici": {t_avg:.1f}, "professionali": {p_avg:.1f}, "neet": {n_avg:.1f}, "bocciature": {b_avg:.1f}, "absorption": {i_avg:.1f}, "profile": "{profile}"}}')

# Add individual regions
for _, r in df_trip.iterrows():
    trip_json_entries.append(f'"{r["region"]}": {{"type": "Region", "macro": "{r["macro_area"]}", "licei": {r["licei_share_pct"]:.1f}, "tecnici": {r["tecnici_share_pct"]:.1f}, "professionali": {r["professionali_share_pct"]:.1f}, "neet": {r["neet_rate_15_29_pct"]:.1f}, "bocciature": {r["bocciature_grade9_pct"]:.1f}, "absorption": {r["industrial_absorption_index"]:.1f}, "profile": "{r["orientation_profile"]}"}}')

tripartite_json_str = "{\n    " + ",\n    ".join(trip_json_entries) + "\n}"

# Read existing index.html content or recreate with all tabs
index_path = os.path.join(WEB_DIR, "index.html")
with open(index_path, "r", encoding="utf-8", errors="ignore") as f_in:
    raw_html = f_in.read()

# Check if we already have the tripartite tab button
if "Tripartite Orientation vs. NEET Area Map" not in raw_html:
    # We will inject the new button into the tabs container right after Tab 2 (geomap)
    old_btn = '<button class="tab-btn" onclick="openTab(\'tab-geomap\')">🗺️ Interactive Regional Geo-Map</button>'
    new_btns = old_btn + '\n        <button class="tab-btn" onclick="openTab(\'tab-tripmap\')">🎒 Tripartite vs. NEET Area Map</button>'
    raw_html = raw_html.replace(old_btn, new_btns)
    
    # Build the Tab Content for Tripartite vs NEET Area Map
    tripmap_tab_content = """
    <!-- TAB 2B: TRIPARTITE VS NEET AREA MAP -->
    <div id="tab-tripmap" class="tab-content">
        <h2>🎒 Tripartite School Orientation vs. NEET Area Map (Italian Secondary Tracking Observatory)</h2>
        <p>In Italy, upper secondary education is divided at age 14 into three distinct tracks (*Il Sistema Tripartito*): <strong>Licei</strong> (academic orientation), <strong>Istituti Tecnici</strong> (technical specialization), and <strong>Istituti Professionali</strong> (vocational trades). How does this tripartite formation split interact with geographical areas and youth NEET outcomes?</p>
        <p>Select any of the <strong>5 Macro-Areas</strong> or <strong>20 individual Regions</strong> below to examine the interactive tripartite enrollment split, Grade 9 repetition severity (<em>bocciature</em>), and industrial district absorption capacity:</p>
        
        <div class="map-layout">
            <div class="map-container">
                <h4 style="color: var(--accent-gold); margin-bottom: 12px; font-family: 'Outfit', sans-serif;">Select Macro-Area:</h4>
                <div style="margin-bottom: 18px; border-bottom: 1px solid var(--border-color); padding-bottom: 14px;">
                    <button class="map-btn selected" onclick="selectTrip('Nord-Ovest (Macro-Area)')">Nord-Ovest (Area)</button>
                    <button class="map-btn" onclick="selectTrip('Nord-Est (Macro-Area)')">Nord-Est (Area)</button>
                    <button class="map-btn" onclick="selectTrip('Centro (Macro-Area)')">Centro (Area)</button>
                    <button class="map-btn" onclick="selectTrip('Sud (Macro-Area)')">Sud (Area)</button>
                    <button class="map-btn" onclick="selectTrip('Isole (Macro-Area)')">Isole (Area)</button>
                </div>
                <h4 style="color: var(--accent-teal); margin-bottom: 12px; font-family: 'Outfit', sans-serif;">Or Select Individual Region:</h4>
                <div>
                    <button class="map-btn" onclick="selectTrip('Lombardia')">Lombardia</button>
                    <button class="map-btn" onclick="selectTrip('Veneto')">Veneto</button>
                    <button class="map-btn" onclick="selectTrip('Emilia-Romagna')">Emilia-Romagna</button>
                    <button class="map-btn" onclick="selectTrip('Piemonte')">Piemonte</button>
                    <button class="map-btn" onclick="selectTrip('Campania')">Campania</button>
                    <button class="map-btn" onclick="selectTrip('Sicilia')">Sicilia</button>
                    <button class="map-btn" onclick="selectTrip('Lazio')">Lazio</button>
                    <button class="map-btn" onclick="selectTrip('Puglia')">Puglia</button>
                    <button class="map-btn" onclick="selectTrip('Calabria')">Calabria</button>
                    <button class="map-btn" onclick="selectTrip('Toscana')">Toscana</button>
                    <button class="map-btn" onclick="selectTrip('Sardegna')">Sardegna</button>
                    <button class="map-btn" onclick="selectTrip('Liguria')">Liguria</button>
                    <button class="map-btn" onclick="selectTrip('Marche')">Marche</button>
                    <button class="map-btn" onclick="selectTrip('Abruzzo')">Abruzzo</button>
                    <button class="map-btn" onclick="selectTrip('Friuli-Venezia Giulia')">Friuli-Venezia Giulia</button>
                    <button class="map-btn" onclick="selectTrip('Trentino-Alto Adige')">Trentino-Alto Adige</button>
                    <button class="map-btn" onclick="selectTrip('Umbria')">Umbria</button>
                    <button class="map-btn" onclick="selectTrip('Basilicata')">Basilicata</button>
                    <button class="map-btn" onclick="selectTrip('Molise')">Molise</button>
                    <button class="map-btn" onclick="selectTrip('Valle d\\'Aosta')">Valle d'Aosta</button>
                </div>
            </div>

            <div class="region-card" style="border-color: var(--accent-gold);">
                <h3 id="trip-name" style="color: var(--accent-gold);">Nord-Ovest (Macro-Area)</h3>
                <div class="region-metric"><span>Geographic Classification:</span> <span id="trip-macro">Nord-Ovest</span></div>
                <div class="region-metric"><span>Youth NEET Rate (15-29 Yrs):</span> <span id="trip-neet" style="color: #E63946;">12.3%</span></div>
                <div class="region-metric"><span>9th-Grade Repetition Severity (Bocciature):</span> <span id="trip-bocc">7.8%</span></div>
                <div class="region-metric"><span>Industrial District Absorption Index:</span> <span id="trip-abs">82.5 / 100</span></div>
                
                <div style="margin-top: 25px; margin-bottom: 15px;">
                    <h4 style="color: var(--text-light); font-size: 1.05rem; margin-bottom: 8px;">Tripartite Enrollment Split (Age 14 Tracking):</h4>
                    <div style="display: flex; height: 28px; border-radius: 6px; overflow: hidden; font-weight: 700; font-size: 0.85rem; text-align: center; line-height: 28px; box-shadow: 0 4px 10px rgba(0,0,0,0.5);">
                        <div id="bar-licei" style="background: #48CAE4; color: #0A192F; width: 52.2%;">Licei: 52.2%</div>
                        <div id="bar-tecnici" style="background: #FFB703; color: #0A192F; width: 33.3%;">Tecnici: 33.3%</div>
                        <div id="bar-prof" style="background: #2A9D8F; color: #FFFFFF; width: 14.5%;">Prof: 14.5%</div>
                    </div>
                </div>

                <div style="background: rgba(255,183,3,0.08); border: 1px solid var(--accent-gold); padding: 18px; border-radius: 8px; margin-top: 20px;">
                    <h4 style="color: var(--accent-gold); font-family: 'Outfit', sans-serif; font-size: 1.1rem; margin-bottom: 6px;">💡 Pedagogical & Orientation Diagnostics:</h4>
                    <p id="trip-profile" style="color: var(--text-light); font-size: 0.98rem; margin: 0;">Strong Technical-Vocational Synergy (`~47.8% combined Tecnici/Professionali share`). High industrial district density directly absorbs graduating youth, maintaining low NEET rates (`12.3%`).</p>
                </div>
            </div>
        </div>

        <div class="reflection-box" style="margin-top: 30px;">
            <div class="reflection-title">🔬 Open Research Hypothesis: The Tripartite Area Paradox</div>
            <p>Notice the structural divergence between Northern areas (where <strong>Istituti Tecnici</strong> account for `>36% of students` and feed directly into high-absorption mechanical districts like Motor Valley or Veneto mechatronics) versus Southern areas (where students over-concentrate in <strong>Licei `>58%`</strong> due to lack of technical employment alternatives, yet face high university dropout and local R&D deficits). Meanwhile, Southern vocational students (<strong>Professionali</strong>) face Grade 9 repetition rates exceeding `14%` (`bocciature`), triggering early school leaving directly into the NEET pool (`NEET >27%`). We invite educational sociologists to download Panel 15 (`15_tripartite_neet_area_orientation_matrix.csv`) and run interaction regressions!</p>
        </div>
    </div>
    """
    
    # Insert right before Tab 3 (dashboard)
    tab_dashboard_marker = '<!-- TAB 3: DASHBOARD -->'
    if tab_dashboard_marker in raw_html:
        raw_html = raw_html.replace(tab_dashboard_marker, tripmap_tab_content + '\n' + tab_dashboard_marker)
    else:
        # Just append before closing container
        raw_html = raw_html.replace('<!-- TAB 4: NEW PANELS -->', tripmap_tab_content + '\n<!-- TAB 4: NEW PANELS -->')

# Now inject the tripartiteData JS script and selectTrip function right above closing </script>
js_injection = f"""const tripartiteData = {tripartite_json_str};

function selectTrip(name) {{
    const data = tripartiteData[name];
    if (!data) return;
    
    document.getElementById('trip-name').innerText = name;
    document.getElementById('trip-macro').innerText = data.macro;
    document.getElementById('trip-neet').innerText = data.neet + '%';
    document.getElementById('trip-bocc').innerText = data.bocciature + '%';
    document.getElementById('trip-abs').innerText = data.absorption + ' / 100';
    document.getElementById('trip-profile').innerText = data.profile;
    
    const bL = document.getElementById('bar-licei');
    const bT = document.getElementById('bar-tecnici');
    const bP = document.getElementById('bar-prof');
    
    bL.style.width = data.licei + '%';
    bL.innerText = 'Licei: ' + data.licei + '%';
    
    bT.style.width = data.tecnici + '%';
    bT.innerText = 'Tecnici: ' + data.tecnici + '%';
    
    bP.style.width = data.professionali + '%';
    bP.innerText = 'Prof: ' + data.professionali + '%';
    
    const tripBtns = document.querySelectorAll('#tab-tripmap .map-btn');
    tripBtns.forEach(b => b.classList.remove('selected'));
    event.currentTarget.classList.add('selected');
}}
</script>"""

if "const tripartiteData =" not in raw_html:
    raw_html = raw_html.replace("</script>", js_injection)

with open(index_path, "w", encoding="utf-8") as f_out:
    f_out.write(raw_html)
print(f"[SUCCESS] Updated {index_path} with Tab 2b: Tripartite Orientation vs. NEET Area Map.")

# Sync to root index.html
root_index_path = os.path.join(ROOT_DIR, "index.html")
html_content_root = raw_html.replace('src="universal_synthesis_master_dashboard.png"', 'src="holistic_analysis/interactive_web_experience/universal_synthesis_master_dashboard.png"')
with open(root_index_path, "w", encoding="utf-8") as f_root:
    f_root.write(html_content_root)
print(f"[SUCCESS] Synchronized Tripartite Area Map to root index.html: {root_index_path}")
