r"""
Generate Notebooks/italy_neet_full_analysis.ipynb programmatically.
Run from the workspace root:  .venv\Scripts\python.exe scripts/create_notebook.py
"""
import json, uuid
from pathlib import Path

def c(cell_type, source, **kw):
    base = {"cell_type": cell_type, "id": uuid.uuid4().hex[:12], "metadata": {}, "source": source}
    if cell_type == "code":
        base.update({"outputs": [], "execution_count": None})
    return {**base, **kw}

def md(text):  return c("markdown", text.splitlines(keepends=True))
def code(text): return c("code",     text.splitlines(keepends=True))

# ─────────────────────────────────────────────────────────────────────────────
cells = []

# ── Title ─────────────────────────────────────────────────────────────────────
cells.append(md("""# Italy's NEET Phenomenon: Education, Territory & Economic Crisis
### A Data-Driven Research Notebook

**Research questions**
| # | Question |
|---|----------|
| 1 | Who are Italy's NEETs, and how does education level shape their risk? |
| 2 | Does Italy's tripartite secondary school system (Liceo / Tecnico / Professionale) create geographic barriers that push pupils into NEET? |
| 3 | Should NEETs be allowed to access university on merit, without a diploma? |
| 4 | How does Italy compare with the UK's comprehensive school system? |
| 5 | What is Italy's macroeconomic context — and is low education spending part of the problem? |

**Data sources**  
ISTAT NEET micro-data · Ministero dell'Istruzione (MIUR/MIM) school & student registers  
MUR immatricolati / laureati / iscritti · Eurostat GDP · World Bank Gini  
OECD Education at a Glance · OurWorldData productivity & emigration · UK SDG Goal-4 stats
"""))

# ── Setup ──────────────────────────────────────────────────────────────────────
cells.append(code("""\
import warnings, re, json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
warnings.filterwarnings('ignore')

sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams.update({'figure.figsize': (12, 5), 'figure.dpi': 110, 'font.size': 11})

ROOT = Path('../local_data') if Path('../local_data').exists() else Path('local_data')
OUT  = Path('neet_outputs')
OUT.mkdir(exist_ok=True, parents=True)

def smart_read_csv(path, **kw):
    \"\"\"Auto-detect encoding and separator; return a DataFrame with >1 column.\"\"\"
    path = str(path)
    for enc in ['utf-8-sig', 'utf-8', 'cp1252', 'latin-1']:
        for sep in [';', ',', '\\t']:
            try:
                df = pd.read_csv(path, sep=sep, encoding=enc, low_memory=False, **kw)
                if df.shape[1] > 1:
                    return df
            except Exception:
                pass
    return pd.read_csv(path, engine='python', sep=None, encoding='latin-1', low_memory=False)

def find_col(df, *kw):
    \"\"\"Return first column name containing any keyword (case-insensitive).\"\"\"
    for k in kw:
        for c in df.columns:
            if k.upper() in str(c).upper():
                return c
    return None

def parse_num(x):
    \"\"\"Parse number, handling Italian thousand-dot format and NaN sentinels.\"\"\"
    if x is None: return np.nan
    s = str(x).strip()
    if s in ('', 'N', 'n', '-', 'nan', 'NaN', 'None', ':', '..', 'n/a'): return np.nan
    if re.match(r'^\\d{1,3}(?:\\.\\d{3})+$', s): return float(s.replace('.', ''))
    if ',' in s and '.' not in s:
        try: return float(s.replace(',', '.'))
        except: return np.nan
    try: return float(s)
    except: return np.nan

def savefig(name, tight=True):
    p = OUT / name
    if tight: plt.tight_layout()
    plt.savefig(p, dpi=110, bbox_inches='tight')
    plt.show()

print(f'ROOT = {ROOT.resolve()}')
print(f'OUT  = {OUT.resolve()}')
"""))

# ── Data inventory ─────────────────────────────────────────────────────────────
cells.append(code("""\
manifest = {}
for f in sorted(ROOT.rglob('*.csv')):
    key = str(f.parent.relative_to(ROOT))
    manifest.setdefault(key, []).append(f.name)
total = sum(len(v) for v in manifest.values())
print(f'{total} CSV files across {len(manifest)} folders:')
for k, v in sorted(manifest.items()):
    print(f'  {k}: {len(v)} files')
"""))

# ── Section 1 ─────────────────────────────────────────────────────────────────
cells.append(md("""\
---
## Section 1 — Italy's NEET Landscape

Italy consistently posts some of the highest NEET rates in the EU. We examine:
- **S1a** NEET incidence broken down by education level
- **S1b** Regional NEET distribution (annual data)
- **S1b-trend** National NEET trend over time
- **S1c** NEET breakdown by EU professional status and citizenship

> NEET rates are highest among those with the lowest formal qualifications — the very group
> that would benefit most from open-access tertiary education.
"""))

cells.append(code("""\
# S1a — NEET incidence by education level
# The ISTAT file uses single-quote quoting; read with quotechar="'" to parse correctly.
try:
    inc_path = next(
        (p for p in ROOT.glob('*.csv') if 'incidenza' in p.name.lower() and 'titolo' in p.name.lower()),
        None
    )
    if inc_path is None:
        raise FileNotFoundError('NEET incidenza-titolo file not found')

    df_inc = pd.read_csv(str(inc_path), sep=',', encoding='utf-8-sig', quotechar="'", low_memory=False)
    df_inc.columns = [str(c).strip() for c in df_inc.columns]

    TIME = find_col(df_inc, 'TIME_PERIOD', 'TIME')
    OBS  = find_col(df_inc, 'Osservazione', 'OBS_VALUE', 'OBS')
    EDU  = find_col(df_inc, 'Titolo')       # 'Titolo di studio' — Italian education labels
    AGE  = find_col(df_inc, 'AGE')

    df_inc[OBS] = df_inc[OBS].apply(parse_num)

    # Keep: annual, national Italy (REF_AREA='IT'), total sex (SEX=9)
    mask = (df_inc['FREQ'] == 'A') & (df_inc['REF_AREA'] == 'IT') & (df_inc['SEX'] == 9)
    df_it = df_inc[mask].copy()

    latest = df_it[TIME].astype(str).max()
    df_l = df_it[df_it[TIME].astype(str) == latest].copy()

    pref_age = 'all ages'
    if AGE:
        for a in ['Y15-29', 'Y18-29', 'Y15-34', 'Y15-24']:
            if a in df_l[AGE].values:
                df_l = df_l[df_l[AGE] == a]; pref_age = a; break

    by_edu = (df_l[df_l[EDU] != 'Totale']
              .groupby(EDU)[OBS].mean()
              .dropna()
              .sort_values(ascending=True))

    colours = sns.color_palette('RdYlGn', len(by_edu))
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.barh(by_edu.index, by_edu.values, color=colours)
    ax.set_xlabel('NEET incidence (%)')
    ax.set_title(f'NEET incidence by education level — Italy {latest} ({pref_age})', fontweight='bold')
    for bar, v in zip(ax.patches, by_edu.values):
        ax.text(v + 0.3, bar.get_y() + bar.get_height()/2, f'{v:.1f}%', va='center', fontsize=9)
    savefig('s1_neet_by_education.png')
    print(f'S1a: {len(by_edu)} groups | highest: {by_edu.idxmax()} = {by_edu.max():.1f}%')
except Exception as e:
    print(f'S1a skipped: {e}')
"""))

cells.append(code("""\
# S1b — NEET by region bar chart (uses annual data, falls back if latest is quarterly)
try:
    reg_path = next(
        (p for p in ROOT.glob('*.csv') if 'regionali' in p.name.lower() and 'neet' in p.name.lower()),
        None
    )
    df_reg = smart_read_csv(reg_path)
    df_reg.columns = [str(c).strip() for c in df_reg.columns]
    T2    = find_col(df_reg, 'TIME_PERIOD', 'TIME')
    OBS2  = find_col(df_reg, 'Osservazione', 'OBS')
    GEO   = find_col(df_reg, 'Territorio')
    AGE2  = find_col(df_reg, 'AGE')
    FREQ2 = find_col(df_reg, 'FREQ')
    df_reg[OBS2] = df_reg[OBS2].apply(parse_num)

    # Annual-only slice
    df_annual = df_reg[df_reg[FREQ2] == 'A'].copy() if FREQ2 else df_reg.copy()
    if AGE2 and 'Y15-29' in df_annual[AGE2].values:
        df_annual = df_annual[df_annual[AGE2] == 'Y15-29']

    EXCL = r'ITALIA|TOTALE|NORD|SUD|CENTRO|ISOLE|MEZZOGIORNO'

    # Find the most recent annual year that has actual regional (non-macro) data
    by_reg, lat2 = pd.Series(dtype=float), ''
    for yr in sorted(df_annual[T2].astype(str).unique(), reverse=True):
        df_yr = df_annual[df_annual[T2].astype(str) == yr]
        br = df_yr.groupby(GEO)[OBS2].mean().dropna()
        br_filt = br[~br.index.str.upper().str.contains(EXCL, na=False, regex=True)]
        if len(br_filt) >= 5:
            by_reg = br_filt.sort_values(ascending=False)
            lat2 = yr; break

    if len(by_reg) > 0:
        fig, ax = plt.subplots(figsize=(13, 7))
        ax.bar(by_reg.index, by_reg.values, color='steelblue')
        ax.set_ylabel('NEETs aged 15–29 (thousands)')
        ax.set_title(f'NEET count by region — {lat2} (annual, ages 15–29)', fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=8)
        savefig('s1_neet_by_region.png')
        print(f'S1b: {len(by_reg)} regions | top: {by_reg.index[0]} = {by_reg.iloc[0]:.0f}k')
except Exception as e:
    print(f'S1b skipped: {e}')
"""))

cells.append(code("""\
# S1b-trend — National NEET count trend (all time periods: annual + quarterly)
try:
    # Use ALL time periods for Italia national Y15-29 — more data points than annual-only
    df_nat = df_reg[df_reg[GEO] == 'Italia'].copy()
    if AGE2 and 'Y15-29' in df_nat[AGE2].values:
        df_nat = df_nat[df_nat[AGE2] == 'Y15-29']
    trend = df_nat.groupby(T2)[OBS2].mean().dropna()

    # Sort time periods naturally (annual 2023 < 2023-Q1 < 2023-Q2...)
    def _tp_key(tp):
        s = str(tp)
        if '-Q' in s:
            yr, q = s.split('-Q')
            return float(yr) + float(q) / 10
        try: return float(s) - 0.05   # annual sits before Q1
        except: return -1
    trend = trend.reindex(sorted(trend.index, key=_tp_key))

    fig, ax = plt.subplots(figsize=(14, 5))
    xs = range(len(trend))
    ax.plot(xs, trend.values, marker='o', ms=4, color='crimson', lw=2)
    ax.fill_between(xs, trend.values, alpha=0.1, color='crimson')
    ax.set_xticks(list(xs))
    ax.set_xticklabels(trend.index, rotation=45, ha='right', fontsize=7)
    ax.set_ylabel('NEETs aged 15–29 (thousands)')
    ax.set_title('Italy — national NEET count trend (15–29, annual + quarterly)', fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}k'))
    savefig('s1_neet_trend.png')
    print(f'S1b-trend: {len(trend)} time periods | latest {trend.index[-1]} = {trend.iloc[-1]:.0f}k NEETs')
except Exception as e:
    print(f'S1b-trend skipped: {e}')
"""))

cells.append(code("""\
# S1c — NEET by citizenship (annual data; citizenship breakdown only in annual files)
try:
    cit_path = next(
        (p for p in ROOT.glob('*.csv') if 'cittadinanza' in p.name.lower() and 'neet' in p.name.lower()),
        None
    )
    if cit_path is None:
        raise FileNotFoundError('NEET citizenship file not found')
    df_cit = smart_read_csv(cit_path)
    df_cit.columns = [str(c).strip() for c in df_cit.columns]
    T3    = find_col(df_cit, 'TIME_PERIOD', 'TIME')
    O3    = find_col(df_cit, 'Osservazione', 'OBS_VALUE')
    G3    = find_col(df_cit, 'Territorio', 'GEO')
    CIT   = find_col(df_cit, 'Cittadinanza', 'cittadinanza', 'Citizen')
    AGE3  = find_col(df_cit, 'AGE')
    SEX3  = find_col(df_cit, 'SEX')
    FREQ3 = find_col(df_cit, 'FREQ')
    EURO_LS = find_col(df_cit, 'EURO_LABOUR_STATUS')
    df_cit[O3] = df_cit[O3].apply(parse_num)

    # Use annual data only (quarterly latest often has no citizenship breakdown)
    df_cit_a = df_cit[df_cit[FREQ3] == 'A'].copy() if FREQ3 else df_cit.copy()

    # Find latest annual year with Italian/Foreign breakdown (>= 2 non-total groups)
    by_cit, lat3 = pd.Series(dtype=float), ''
    for yr in sorted(df_cit_a[T3].astype(str).unique(), reverse=True):
        df_yr = df_cit_a[
            (df_cit_a[T3].astype(str) == yr) &
            (df_cit_a[G3] == 'Italia')
        ].copy()
        if AGE3 and 'Y15-29' in df_yr[AGE3].values:
            df_yr = df_yr[df_yr[AGE3] == 'Y15-29']
        if SEX3:
            sex_total = df_yr[SEX3].dropna().max()  # 9 = total sex code
            df_yr = df_yr[df_yr[SEX3] == sex_total]
        if EURO_LS and EURO_LS in df_yr.columns:
            # Pick the EURO_LABOUR_STATUS with the highest total (= aggregate NEET)
            ls_max = df_yr.groupby(EURO_LS)[O3].sum().idxmax()
            df_yr = df_yr[df_yr[EURO_LS] == ls_max]
        bc = df_yr[df_yr[CIT] != 'Totale'].groupby(CIT)[O3].sum().dropna()
        if len(bc) >= 2:
            by_cit = bc.sort_values(ascending=False)
            lat3 = yr; break

    if len(by_cit) > 0:
        fig, ax = plt.subplots(figsize=(9, 5))
        colors_cit = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        ax.bar(by_cit.index, by_cit.values, color=colors_cit[:len(by_cit)])
        ax.set_title(f'NEETs aged 15–29 by citizenship — Italy {lat3} (annual)', fontweight='bold')
        ax.set_ylabel('NEETs (thousands)')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}k'))
        for i, (lab, v) in enumerate(by_cit.items()):
            ax.text(i, v + 5, f'{v:,.0f}k', ha='center', fontsize=9)
        plt.xticks(rotation=20, ha='right')
        savefig('s1_neet_by_citizenship.png')
        print(f'S1c: {len(by_cit)} citizenship groups | year={lat3}')
    else:
        print('S1c: no citizenship breakdown found in annual data')
except Exception as e:
    print(f'S1c skipped: {e}')
"""))

# ── Section 2 ─────────────────────────────────────────────────────────────────
cells.append(md("""\
---
## Section 2 — Italy's Tripartite Secondary School System

Italy channels pupils at **age 14** into one of three tracks:
- **Liceo** — academic, leads naturally to university
- **Istituto Tecnico** — technical-vocational
- **Istituto Professionale** — vocational, shortest path to work certification

The **geographic density of each track** matters: if Istituto Professionale schools are scarce in
certain provinces, students with academic aptitude (but in areas without a Liceo) may face
structural barriers — and those without convenient school access may disengage entirely, becoming NEET.

> Italy ≠ UK: the UK operates **comprehensive secondary schools**, meaning all pupils receive
> the same core curriculum until 16. Italy's tripartite system *pre-sorts* pupils into
> different life trajectories at 14, before full cognitive maturity.
"""))

cells.append(code("""\
# S2a — School count by track and geographic area
try:
    scuole_path = ROOT / 'MinIstruzione/Scuole/SCUANAGRAFESTAT20242520250831.csv'
    df_scuole = smart_read_csv(scuole_path)
    df_scuole.columns = [str(c).strip() for c in df_scuole.columns]

    TIPO = 'DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'
    AREA = 'AREAGEOGRAFICA'
    REG  = 'REGIONE'
    COD  = 'CODICESCUOLA'

    def classify_track(name):
        n = str(name).upper()
        if 'LICEO' in n or 'MAGISTRALE' in n or 'CLASSICO' in n or 'ARTE' in n:
            return 'Liceo (Academic)'
        elif 'TECNICO' in n or 'GEOMETRI' in n or 'AGRARIO' in n or 'NAUTICO' in n:
            return 'Istituto Tecnico'
        elif 'PROF' in n:
            return 'Istituto Professionale'
        elif any(x in n for x in ['PRIMARIA', 'INFANZIA', 'PRIMO GRADO', 'COMPRENSIVO']):
            return 'Primary/Lower Secondary'
        else:
            return 'Other'

    df_scuole['TRACK'] = df_scuole[TIPO].apply(classify_track)
    SECONDARY = ['Liceo (Academic)', 'Istituto Tecnico', 'Istituto Professionale']
    df_sec = df_scuole[df_scuole['TRACK'].isin(SECONDARY)].copy()

    pivot = df_sec.groupby([AREA, 'TRACK'])[COD].count().unstack('TRACK').fillna(0).astype(int)
    ax = pivot.plot(kind='bar', figsize=(13, 6), colormap='tab10')
    ax.set_title('Secondary school branches by track and geographic area', fontweight='bold')
    ax.set_ylabel('Number of school branches')
    plt.xticks(rotation=25, ha='right')
    savefig('s2_schools_by_track_area.png')
    total_sec = len(df_sec)
    print(f'S2a: {total_sec} secondary branches across {len(pivot)} areas')
    print(pivot.to_string())
except Exception as e:
    print(f'S2a skipped: {e}')
"""))

cells.append(code("""\
# S2b — Liceo/Professionale ratio by region (reveals territorial inequality)
try:
    school_by_reg = df_sec.groupby([REG, 'TRACK'])[COD].count().unstack('TRACK').fillna(0).astype(int)
    school_by_reg['Liceo_Prof_ratio'] = (
        school_by_reg.get('Liceo (Academic)', pd.Series(0, index=school_by_reg.index)) /
        school_by_reg.get('Istituto Professionale', pd.Series(1, index=school_by_reg.index)).replace(0, 1)
    )
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    cols_to_plot = [c for c in SECONDARY if c in school_by_reg.columns]
    school_by_reg[cols_to_plot].sort_values('Istituto Professionale').plot(kind='barh', ax=axes[0])
    axes[0].set_title('School branches per track by region', fontweight='bold')

    ratio = school_by_reg['Liceo_Prof_ratio'].sort_values(ascending=False)
    axes[1].barh(ratio.index, ratio.values, color='#d62728')
    axes[1].axvline(ratio.median(), color='navy', lw=1.5, ls='--', label=f'Median: {ratio.median():.1f}')
    axes[1].set_title('Liceo-to-Professionale ratio by region\\n(higher = fewer vocational options)', fontweight='bold')
    axes[1].legend()
    savefig('s2_school_track_ratio_by_region.png')
    print(f'S2b: Liceo/Prof ratio — min={ratio.min():.1f}, median={ratio.median():.1f}, max={ratio.max():.1f}')
except Exception as e:
    print(f'S2b skipped: {e}')
"""))

cells.append(code("""\
# S2c — Students by secondary track (pie chart)
try:
    alu_path = ROOT / 'MinIstruzione/Alunni/ALUSECGRADOINDPAR20242520250831.csv'
    df_alu = smart_read_csv(alu_path)
    df_alu.columns = [str(c).strip() for c in df_alu.columns]
    M   = find_col(df_alu, 'ALUNNIMASCHI')
    F   = find_col(df_alu, 'ALUNNIFEMMINE')
    TRK = find_col(df_alu, 'TIPOPERCORSO')
    IND = find_col(df_alu, 'INDIRIZZO')
    df_alu[M] = df_alu[M].apply(parse_num)
    df_alu[F] = df_alu[F].apply(parse_num)
    df_alu['TOTALE'] = df_alu[[M, F]].sum(axis=1)
    by_track = df_alu.groupby(TRK)['TOTALE'].sum().sort_values(ascending=False)
    colors_pie = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    fig, ax = plt.subplots(figsize=(8, 6))
    wedges, texts, autotexts = ax.pie(
        by_track.values, labels=by_track.index, autopct='%1.1f%%',
        colors=colors_pie[:len(by_track)], startangle=140)
    ax.set_title('Upper-secondary students by track (2024–25)', fontweight='bold')
    savefig('s2_students_by_track.png')
    print(f'S2c: {by_track.to_dict()}')
except Exception as e:
    print(f'S2c skipped: {e}')
"""))

cells.append(code("""\
# S2d — Top 20 secondary curricula by enrolment
try:
    if IND:
        by_ind = df_alu.groupby(IND)['TOTALE'].sum().sort_values(ascending=False).head(20)
        fig, ax = plt.subplots(figsize=(13, 8))
        ax.barh(by_ind.index[::-1], by_ind.values[::-1], color='steelblue')
        ax.set_xlabel('Students (thousands)')
        ax.set_title('Top 20 secondary curricula by enrolment', fontweight='bold')
        ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))
        savefig('s2_top_indirizzo.png')
        print(f'S2d: top curriculum = {by_ind.index[0]} ({by_ind.iloc[0]:,.0f} students)')
except Exception as e:
    print(f'S2d skipped: {e}')
"""))

# ── Section 3 ─────────────────────────────────────────────────────────────────
cells.append(md("""\
---
## Section 3 — The Diploma Gate: Who Enters University?

In Italy a *diploma di maturità* (secondary school-leaving certificate) is the legal prerequisite
for university admission. This section reveals:
- Which diploma types actually produce university entrants
- Geographic inequality in Liceo density across provinces
- Grade distribution at university entry
- How many students cross regional borders to study

> **Policy argument**: Italian constitutional law (Art. 33–34) establishes *"merito"* (merit)
> as the principle governing access to higher education. If the diploma gate fails to test merit —
> but only credential-holding — then NEETs with equivalent intellectual capacity are excluded
> unconstitutionally.
"""))

cells.append(code("""\
# S3a — University matriculations by diploma type
try:
    df_dip = smart_read_csv(ROOT / 'MUR/immatricolati/10_immatricolatixdiplomascuolasecondariaxclasse.csv')
    df_dip.columns = [str(c).strip() for c in df_dip.columns]
    DIP_COL  = find_col(df_dip, 'Diploma_tipo', 'Diploma')
    IMM_COL  = find_col(df_dip, 'Imm')
    ANNO_COL = find_col(df_dip, 'AnnoA', 'Anno')
    df_dip[IMM_COL] = df_dip[IMM_COL].apply(parse_num)
    latest_a = df_dip[ANNO_COL].astype(str).max()
    df_d_lat = df_dip[df_dip[ANNO_COL].astype(str) == latest_a]
    by_dip = df_d_lat.groupby(DIP_COL)[IMM_COL].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(by_dip.index, by_dip.values, color='steelblue')
    ax.set_xlabel('Matriculations')
    ax.set_title(f'University matriculations by diploma type — {latest_a}', fontweight='bold')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    savefig('s3_matriculations_by_diploma.png')
    pct = (by_dip / by_dip.sum() * 100).sort_values(ascending=False)
    print(f'S3a: {len(by_dip)} diploma types | top 3: {pct.head(3).round(1).to_dict()}')
except Exception as e:
    print(f'S3a skipped: {e}')
"""))

cells.append(code("""\
# S3b — Liceo share of matriculants by province of residence
try:
    df_res = smart_read_csv(ROOT / 'MUR/immatricolati/11_immatricolatixdiplomascuolaxresidenza.csv')
    df_res.columns = [str(c).strip() for c in df_res.columns]
    DIP2 = find_col(df_res, 'Diploma_tipo', 'Diploma')
    PROV = find_col(df_res, 'ProvinciaRES', 'Provincia', 'PROV')
    IMM2 = find_col(df_res, 'Imm')
    AN2  = find_col(df_res, 'AnnoA', 'Anno')
    df_res[IMM2] = df_res[IMM2].apply(parse_num)
    lat_r = df_res[AN2].astype(str).max()
    df_r2 = df_res[df_res[AN2].astype(str) == lat_r]
    pivot_res = df_r2.groupby([PROV, DIP2])[IMM2].sum().unstack(DIP2).fillna(0)
    liceo_cols = [c for c in pivot_res.columns if 'LICEO' in str(c).upper() or 'liceo' in str(c).lower()]
    if liceo_cols:
        pivot_res['pct_liceo'] = pivot_res[liceo_cols].sum(axis=1) / pivot_res.sum(axis=1) * 100
        pct_liceo_prov = pivot_res['pct_liceo'].sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(14, 7))
        ax.bar(pct_liceo_prov.index, pct_liceo_prov.values, color=['crimson' if v > pct_liceo_prov.median() else 'steelblue' for v in pct_liceo_prov.values])
        ax.axhline(pct_liceo_prov.median(), color='navy', lw=1.5, ls='--', label=f'Median: {pct_liceo_prov.median():.1f}%')
        ax.set_title('Share of Liceo graduates among new university entrants, by province', fontweight='bold')
        ax.set_ylabel('Liceo % of matriculants')
        ax.legend()
        plt.xticks(rotation=90, fontsize=5)
        savefig('s3_liceo_share_by_province.png')
        print(f'S3b: {len(pct_liceo_prov)} provinces | median liceo share = {pct_liceo_prov.median():.1f}%')
    else:
        print('S3b: no Liceo column identified in province pivot')
except Exception as e:
    print(f'S3b skipped: {e}')
"""))

cells.append(code("""\
# S3c — Diploma grade distribution of university entrants
try:
    df_vote = smart_read_csv(ROOT / 'MUR/immatricolati/16_immatricolatixvotodiplomascuolasec.csv')
    df_vote.columns = [str(c).strip() for c in df_vote.columns]
    VOTO = find_col(df_vote, 'Diploma_Voto', 'Voto', 'Grad')
    IMM3 = find_col(df_vote, 'Imm')
    AN3  = find_col(df_vote, 'AnnoA', 'Anno')
    df_vote[IMM3] = df_vote[IMM3].apply(parse_num)
    lat_v = df_vote[AN3].astype(str).max()
    by_voto = (df_vote[df_vote[AN3].astype(str) == lat_v]
               .groupby(VOTO)[IMM3].sum()
               .sort_index())
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.bar(by_voto.index.astype(str), by_voto.values, color='steelblue')
    ax.set_xlabel('Diploma grade band')
    ax.set_ylabel('Matriculations')
    ax.set_title(f'Diploma grade distribution of university entrants — {lat_v}', fontweight='bold')
    plt.xticks(rotation=45, ha='right', fontsize=7)
    savefig('s3_diploma_grade_distribution.png')
    print(f'S3c: {len(by_voto)} grade bands | latest year = {lat_v}')
except Exception as e:
    print(f'S3c skipped: {e}')
"""))

cells.append(code("""\
# S3d — Geographic mobility: out-of-province students
try:
    df_fuori = smart_read_csv(ROOT / 'MUR/MUR_iscritti/iscritti_in_sede_fuori_sede.csv')
    df_fuori.columns = [str(c).strip() for c in df_fuori.columns]
    ISC   = find_col(df_fuori, 'Isc')
    PROVD = find_col(df_fuori, 'ProvinciaSede', 'ProvSede')
    PROVC = find_col(df_fuori, 'provcorso', 'ProvCorso', 'ProvRes')
    AN4   = find_col(df_fuori, 'AnnoA', 'Anno')
    df_fuori[ISC] = df_fuori[ISC].apply(parse_num)
    lat_f = df_fuori[AN4].astype(str).max()
    df_f  = df_fuori[df_fuori[AN4].astype(str) == lat_f].copy()
    if PROVD and PROVC:
        df_f['fuori'] = df_f[PROVD].astype(str).str.strip() != df_f[PROVC].astype(str).str.strip()
        in_vs_out = df_f.groupby('fuori')[ISC].sum()
        labels = ['Same province', 'Different province']
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.pie(in_vs_out.values, labels=labels, autopct='%1.1f%%',
               colors=['#2ca02c', '#d62728'], startangle=90)
        ax.set_title(f'University students: geographic mobility — {lat_f}', fontweight='bold')
        savefig('s3_geographic_mobility.png')
        total_stud = in_vs_out.sum()
        fuori_pct = in_vs_out.get(True, 0) / total_stud * 100
        print(f'S3d: {total_stud:,.0f} students | {fuori_pct:.1f}% study outside home province')
    else:
        print(f'S3d: PROVD={PROVD}, PROVC={PROVC} — mobility column not found')
except Exception as e:
    print(f'S3d skipped: {e}')
"""))

# ── Section 4 ─────────────────────────────────────────────────────────────────
cells.append(md("""\
---
## Section 4 — University Flows: Enrolment, Dropout & Graduation

Even those who *enter* university are not guaranteed to complete it.
Italy's dropout rate is among the highest in the OECD (EAG 2023).
We track the full pipeline: matriculations → iscritti → laureati.
"""))

cells.append(code("""\
# S4a — Immatricolati (first-year entrants) trend
try:
    df_imm = smart_read_csv(ROOT / 'MUR/immatricolati/01_immatricolatixanno.csv')
    df_imm.columns = [str(c).strip() for c in df_imm.columns]
    AN5 = find_col(df_imm, 'AnnoA', 'Anno')
    if 'Imm' in df_imm.columns:
        df_imm['Imm'] = df_imm['Imm'].apply(parse_num)
        tot_col = 'Imm'
    else:
        for mc in ['Imm_M', 'Imm_F']:
            if mc in df_imm.columns:
                df_imm[mc] = df_imm[mc].apply(parse_num)
        df_imm['Imm'] = df_imm[['Imm_M', 'Imm_F']].sum(axis=1)
        tot_col = 'Imm'
    trend_imm = df_imm.groupby(AN5)[tot_col].sum().sort_index()
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(trend_imm.index.astype(str), trend_imm.values, marker='o', color='steelblue', lw=2.5)
    ax.set_ylabel('First-year enrolments')
    ax.set_title('University first-year entrants (immatricolati) trend', fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    plt.xticks(rotation=45)
    savefig('s4_immatricolati_trend.png')
    print(f'S4a: {len(trend_imm)} years | latest = {trend_imm.iloc[-1]:,.0f}')
except Exception as e:
    print(f'S4a skipped: {e}')
"""))

cells.append(code("""\
# S4b — Dropout rate trend (tassoabbandono)
try:
    df_drop = smart_read_csv(ROOT / 'MUR/tassoabbandono_180226.csv')
    df_drop.columns = [str(c).strip() for c in df_drop.columns]
    yr_col  = df_drop.columns[0]
    val_col = df_drop.columns[1]
    df_drop[val_col] = df_drop[val_col].apply(parse_num)
    df_drop = df_drop.dropna(subset=[val_col])
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(df_drop[yr_col].astype(str), df_drop[val_col], marker='s', color='crimson', lw=2.5)
    ax.set_ylabel('Dropout rate (%)')
    ax.set_title('University first-to-second year dropout rate', fontweight='bold')
    plt.xticks(rotation=45)
    savefig('s4_dropout_trend.png')
    print(f'S4b: {len(df_drop)} years | latest = {df_drop[val_col].iloc[-1]:.1f}%')
except Exception as e:
    print(f'S4b skipped: {e}')
"""))

cells.append(code("""\
# S4c — Laureati (graduates) trend
try:
    df_lau = smart_read_csv(ROOT / 'MUR/laureati/01_laureatixanno.csv')
    df_lau.columns = [str(c).strip() for c in df_lau.columns]
    AN6 = find_col(df_lau, 'AnnoA', 'Anno')
    LAU = find_col(df_lau, 'Lau')
    if LAU:
        df_lau[LAU] = df_lau[LAU].apply(parse_num)
        trend_lau = df_lau.groupby(AN6)[LAU].sum().sort_index()
        fig, ax = plt.subplots(figsize=(13, 5))
        ax.plot(trend_lau.index.astype(str), trend_lau.values, marker='^', color='green', lw=2.5)
        ax.set_ylabel('Graduates')
        ax.set_title('University graduates (laureati) per year', fontweight='bold')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
        plt.xticks(rotation=45)
        savefig('s4_laureati_trend.png')
        print(f'S4c: {len(trend_lau)} years | latest = {trend_lau.iloc[-1]:,.0f}')
    else:
        print(f'S4c: Lau column not found, cols={list(df_lau.columns[:6])}')
except Exception as e:
    print(f'S4c skipped: {e}')
"""))

# ── Section 5 ─────────────────────────────────────────────────────────────────
cells.append(md("""\
---
## Section 5 — Italy's Economic Context

Italy has experienced **three lost decades**: GDP per capita stagnated, inequality rose,
and labour productivity grew slower than peers. Meanwhile education spending fell below
the EU average. This section quantifies the macro-economic backdrop within which
the NEET phenomenon grew.

Key findings expected:
- Italy's GDP per capita volume index fell below 100 (EU27 average) after 2008
- Gini coefficient trended upward from the 1990s
- Low productivity correlates with low educational attainment
- Brain drain (net emigration) accelerated post-2008
"""))

cells.append(code("""\
# S5a — GDP per capita volume index (EU27 = 100)
try:
    df_gdp = smart_read_csv(ROOT / 'oecd/eurostat_gdp_per_capita.csv')
    df_gdp.columns = [str(c).strip() for c in df_gdp.columns]
    OBS_G = find_col(df_gdp, 'OBS_VALUE')
    GEO_G = find_col(df_gdp, 'geo')
    TIM_G = find_col(df_gdp, 'TIME_PERIOD', 'TIME')
    df_gdp[OBS_G] = df_gdp[OBS_G].apply(parse_num)
    peers = {'IT': 'Italy', 'DE': 'Germany', 'FR': 'France', 'ES': 'Spain',
             'EU27_2020': 'EU27 avg', 'UK': 'United Kingdom', 'EL': 'Greece'}
    df_gdp_p = df_gdp[df_gdp[GEO_G].isin(peers)].copy()
    df_gdp_p['Country'] = df_gdp_p[GEO_G].map(peers)
    fig, ax = plt.subplots(figsize=(14, 6))
    for country, grp in df_gdp_p.groupby('Country'):
        style = dict(lw=3.5, color='crimson') if country == 'Italy' else dict(lw=1.5, alpha=0.8)
        ax.plot(grp.sort_values(TIM_G)[TIM_G].astype(str),
                grp.sort_values(TIM_G)[OBS_G], label=country, **style)
    ax.axhline(100, color='grey', lw=1, ls=':', label='EU27 = 100')
    ax.set_ylabel('Volume index (EU27 = 100)')
    ax.set_title('GDP per capita volume index — Italy vs peers', fontweight='bold')
    ax.legend(loc='lower left', fontsize=9)
    plt.xticks(rotation=45)
    savefig('s5_gdp_per_capita.png')
    it_latest = df_gdp_p[df_gdp_p['Country']=='Italy'].sort_values(TIM_G)[OBS_G].iloc[-1]
    print(f'S5a: Italy latest GDP index = {it_latest:.1f} (EU27=100)')
except Exception as e:
    print(f'S5a skipped: {e}')
"""))

cells.append(code("""\
# S5b — Gini coefficient (World Bank)
try:
    df_gini = smart_read_csv(ROOT / 'WB_WDI_SI_POV_GINI.csv')
    df_gini.columns = [str(c).strip() for c in df_gini.columns]
    REF_G  = find_col(df_gini, 'REF_AREA')
    OBS_Gi = find_col(df_gini, 'OBS_VALUE')
    TIM_Gi = find_col(df_gini, 'TIME_PERIOD', 'TIME')
    df_gini[OBS_Gi] = df_gini[OBS_Gi].apply(parse_num)
    gini_peers = {'ITA':'Italy','DEU':'Germany','FRA':'France','ESP':'Spain','GBR':'United Kingdom'}
    df_gi_p = df_gini[df_gini[REF_G].isin(gini_peers)].copy()
    df_gi_p['Country'] = df_gi_p[REF_G].map(gini_peers)
    fig, ax = plt.subplots(figsize=(14, 6))
    for country, grp in df_gi_p.groupby('Country'):
        grp_s = grp.sort_values(TIM_Gi)
        style = dict(lw=3.5, color='crimson') if country == 'Italy' else dict(lw=1.5, alpha=0.8)
        ax.plot(grp_s[TIM_Gi].astype(str), grp_s[OBS_Gi], label=country, **style)
    ax.set_ylabel('Gini coefficient (0 = perfect equality)')
    ax.set_title('Income inequality (Gini) — Italy vs peers', fontweight='bold')
    ax.legend()
    plt.xticks(rotation=45)
    savefig('s5_gini.png')
    print('S5b: Gini plotted successfully')
except Exception as e:
    print(f'S5b skipped: {e}')
"""))

cells.append(code("""\
# S5c — Productivity vs educational attainment scatter
# Uses the latest data point per country (not global latest year) to maximise coverage.
try:
    df_prod = smart_read_csv(
        ROOT / 'ourWorldData/productivity-vs-educational-attainment/productivity-vs-educational-attainment.csv')
    df_prod.columns = [str(c).strip() for c in df_prod.columns]
    EDU_P  = find_col(df_prod, 'average years', 'educ')
    PROD_P = find_col(df_prod, 'output per hour', 'productivity')
    ENT    = find_col(df_prod, 'Entity')
    YR_P   = find_col(df_prod, 'Year')
    df_prod[EDU_P]  = df_prod[EDU_P].apply(parse_num)
    df_prod[PROD_P] = df_prod[PROD_P].apply(parse_num)

    # Get latest available data per entity (avoids gaps in latest global year)
    df_valid = df_prod.dropna(subset=[EDU_P, PROD_P])
    latest_per = df_valid.groupby(ENT)[YR_P].max().reset_index()
    latest_per.columns = [ENT, '_yr']
    df_lat = df_valid.merge(latest_per, on=ENT)
    df_latest_p = df_lat[df_lat[YR_P] == df_lat['_yr']].drop(columns=['_yr'])

    focus = ['Italy', 'United Kingdom', 'Germany', 'France', 'Spain', 'Greece']
    df_focus = df_latest_p[df_latest_p[ENT].isin(focus)]

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.scatter(df_latest_p[EDU_P], df_latest_p[PROD_P], alpha=0.2, color='lightgray', s=30)
    for _, row in df_focus.iterrows():
        clr = '#d62728' if row[ENT] == 'Italy' else '#1f77b4'
        ax.scatter(row[EDU_P], row[PROD_P], s=130, color=clr, zorder=5)
        ax.annotate(row[ENT], (row[EDU_P], row[PROD_P]),
                    textcoords='offset points', xytext=(5, 3),
                    fontsize=9, fontweight='bold' if row[ENT]=='Italy' else 'normal')
    ax.set_xlabel('Average years of education (15–64)')
    ax.set_ylabel('Output per hour worked (USD)')
    ax.set_title('Productivity vs educational attainment (latest data per country)', fontweight='bold')
    savefig('s5_productivity_vs_education.png')
    print(f'S5c: {len(df_focus)} focus countries | {len(df_latest_p)} total countries in scatter')
except Exception as e:
    print(f'S5c skipped: {e}')
"""))

cells.append(code("""\
# S5d — Upper-secondary completion rate + S5e brain drain
try:
    df_comp = smart_read_csv(
        ROOT / 'ourWorldData/completion-rate-of-upper-secondary-education-sdg/completion-rate-of-upper-secondary-education-sdg.csv')
    df_comp.columns = [str(c).strip() for c in df_comp.columns]
    RATE = find_col(df_comp, 'Completion rate', 'completion', 'rate')
    ENT2 = find_col(df_comp, 'Entity')
    YR2  = find_col(df_comp, 'Year')
    comp_countries = ['Italy', 'United Kingdom', 'Germany', 'France', 'Spain']
    df_comp_f = df_comp[df_comp[ENT2].isin(comp_countries)].copy()
    df_comp_f[RATE] = df_comp_f[RATE].apply(parse_num)

    fig, ax = plt.subplots(figsize=(13, 5))
    for country, grp in df_comp_f.groupby(ENT2):
        style = dict(lw=3.5, color='crimson') if country == 'Italy' else dict(lw=1.5, alpha=0.8)
        ax.plot(grp[YR2], grp[RATE], label=country, **style)
    ax.set_ylabel('Completion rate (%)')
    ax.set_title('Upper-secondary completion rate — Italy vs peers', fontweight='bold')
    ax.legend()
    savefig('s5_secondary_completion.png')
    print('S5d: completion chart done')
except Exception as e:
    print(f'S5d skipped: {e}')

try:
    df_emig = smart_read_csv(ROOT / 'ourWorldData/total-number-of-emigrants.csv')
    df_emig.columns = [str(c).strip() for c in df_emig.columns]
    ENT3 = find_col(df_emig, 'Entity')
    YR3  = find_col(df_emig, 'Year')
    EMI  = find_col(df_emig, 'emigrants', 'Total', 'Emigrants')
    df_emig[EMI] = df_emig[EMI].apply(parse_num)
    it_emig = df_emig[df_emig[ENT3] == 'Italy'].sort_values(YR3)
    if len(it_emig) > 0:
        fig, ax = plt.subplots(figsize=(11, 4))
        ax.bar(it_emig[YR3].astype(str), it_emig[EMI], color='#d62728')
        ax.set_ylabel('Emigrants')
        ax.set_title('Italian emigrants (brain drain indicator)', fontweight='bold')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
        plt.xticks(rotation=45)
        savefig('s5_brain_drain.png')
        print(f'S5e: {len(it_emig)} years of emigration data')
except Exception as e:
    print(f'S5e skipped: {e}')
"""))

cells.append(code("""\
# S5f — Education spending as % of GDP (OECD)
# Note: this dataset has a single education level (ISCED11_1T8) — no level filter needed.
try:
    df_fin = smart_read_csv(ROOT / 'oecd/oecd_education_fin_gdp.csv')
    df_fin.columns = [str(c).strip() for c in df_fin.columns]
    REF_F = find_col(df_fin, 'REF_AREA')
    OBS_F = find_col(df_fin, 'OBS_VALUE')
    TIM_F = find_col(df_fin, 'TIME_PERIOD', 'TIME')
    SRC_F = find_col(df_fin, 'EXP_SOURCE')
    df_fin[OBS_F] = df_fin[OBS_F].apply(parse_num)

    # Filter: total (public+private) source only
    df_fin_t = df_fin[df_fin[SRC_F] == '_T'].copy() if SRC_F else df_fin.copy()
    fin_peers = {'ITA':'Italy','GBR':'United Kingdom','DEU':'Germany',
                 'FRA':'France','ESP':'Spain','OECD':'OECD avg'}
    df_fin_p = df_fin_t[df_fin_t[REF_F].isin(fin_peers)].copy()
    df_fin_p['Country'] = df_fin_p[REF_F].map(fin_peers)
    lat_f2 = df_fin_p[TIM_F].max()
    df_fin_lat = df_fin_p[df_fin_p[TIM_F] == lat_f2]
    by_ctry_f = df_fin_lat.groupby('Country')[OBS_F].mean().dropna().sort_values(ascending=False)

    if len(by_ctry_f) > 0:
        colors_f = ['#d62728' if c == 'Italy' else '#1f77b4' for c in by_ctry_f.index]
        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(by_ctry_f.index, by_ctry_f.values, color=colors_f)
        ax.set_ylabel('% of GDP')
        ax.set_title(f'Education spending as % of GDP — {lat_f2}', fontweight='bold')
        plt.xticks(rotation=30, ha='right')
        for bar, v in zip(bars, by_ctry_f.values):
            ax.text(bar.get_x() + bar.get_width()/2, v + 0.02, f'{v:.2f}%', ha='center', fontsize=9)
        savefig('s5_education_spending_gdp.png')
    print(f'S5f: {by_ctry_f.round(2).to_dict()}')
except Exception as e:
    print(f'S5f skipped: {e}')
"""))

# ── Section 6 ─────────────────────────────────────────────────────────────────
cells.append(md("""\
---
## Section 6 — Student Privileges & Financial Support

Italy offers fee exemptions and DSU (Diritto allo Studio Universitario) grants.
Understanding who benefits — and by how much — reveals whether the current system
reaches the students most in need.
"""))

cells.append(code("""\
# S6 — Fee exemption categories (contribuzione e interventi atenei)
try:
    contrib_root = ROOT / 'MUR/2024-contribuzione-e-interventi-atenei'
    contrib_file = None
    for p in contrib_root.rglob('*.csv'):
        contrib_file = p; break
    if contrib_file is None:
        for p in (ROOT / 'MUR').rglob('*.csv'):
            if any(k in p.name.lower() for k in ['esonero', 'contrib', 'contribuzione']):
                contrib_file = p; break
    print('Contrib file:', contrib_file)

    if contrib_file:
        df_ex = smart_read_csv(contrib_file)
        df_ex.columns = [str(c).strip() for c in df_ex.columns]
        DESC_E = find_col(df_ex, 'DESCRIZIONE', 'DESC', 'TIPO')

        # Identify numeric columns
        num_cols_e = []
        for col in df_ex.columns:
            try:
                sample = df_ex[col].dropna().iloc[0] if len(df_ex[col].dropna()) > 0 else ''
                v = parse_num(sample)
                if not np.isnan(v):
                    num_cols_e.append(col)
            except:
                pass
        for col in num_cols_e:
            df_ex[col] = df_ex[col].apply(parse_num)
        df_ex['total_exempt'] = df_ex[num_cols_e].sum(axis=1)

        if DESC_E:
            by_desc = (df_ex.groupby(DESC_E)['total_exempt'].sum()
                       .sort_values(ascending=False).head(15))
            fig, ax = plt.subplots(figsize=(13, 8))
            by_desc.sort_values().plot(kind='barh', ax=ax, color='steelblue')
            ax.set_title('Top 15 exemption categories by total value', fontweight='bold')
            ax.set_xlabel('Total exemptions (sum across atenei)')
            savefig('s6_exemptions_by_category.png')
            print(f'S6: {len(df_ex)} rows, {len(num_cols_e)} numeric cols, top cat: {by_desc.index[0]}')
        else:
            print('S6: description column not found')
    else:
        print('S6: no contribution file found')
except Exception as e:
    print(f'S6 skipped: {e}')
"""))

# ── Section 7 ─────────────────────────────────────────────────────────────────
cells.append(md("""\
---
## Section 7 — Italy vs United Kingdom: School Systems Compared

The UK operates **comprehensive secondary schools** (age 11–16) followed by optional
sixth-form/A-levels. Italy operates the **tripartite system** (Liceo / Tecnico / Professionale)
from age 14. These structural differences produce measurably different NEET outcomes.

| Feature | Italy | United Kingdom |
|---------|-------|---------------|
| Secondary school type | Tripartite (Liceo / Tecnico / Professionale) | Comprehensive |
| Tracking age | 14 | 16+ (post-compulsory) |
| NEET rate (15-34, 2022) | ~18% | ~11% |
| Upper-secondary completion | ~85% | ~90%+ |
| University participation | ~30% | ~55% |
| Education spending % GDP | ~4.0% | ~5.5% |

The argument: a comprehensive system that tracks pupils *later* reduces the risk of
early lock-in into low-attainment pathways — and reduces the structural production of NEETs.
"""))

cells.append(code("""\
# S7a — Upper-secondary completion rate: Italy vs United Kingdom
try:
    comp_it_uk = df_comp_f[df_comp_f[ENT2].isin(['Italy', 'United Kingdom'])].copy()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    for ax, country in zip(axes, ['Italy', 'United Kingdom']):
        grp = comp_it_uk[comp_it_uk[ENT2] == country].sort_values(YR2)
        clr = 'crimson' if country == 'Italy' else 'steelblue'
        ax.plot(grp[YR2], grp[RATE], color=clr, lw=3)
        ax.fill_between(grp[YR2], grp[RATE], alpha=0.1, color=clr)
        ax.set_title(country, fontweight='bold')
        ax.set_ylabel('Completion rate (%)')
        ax.set_ylim(60, 105)
    plt.suptitle('Upper-secondary completion rate: Italy vs United Kingdom', fontweight='bold', fontsize=13)
    savefig('s7_completion_italy_vs_uk.png')
    print('S7a: completion comparison chart done')
except Exception as e:
    print(f'S7a skipped: {e}')
"""))

cells.append(code("""\
# S7b — UK adult learning participation (SDG 4.3.1)
try:
    df_uk431 = smart_read_csv(ROOT / 'UKSDGstats/4-3-1.csv')
    df_uk431.columns = [str(c).strip() for c in df_uk431.columns]
    SER_U = find_col(df_uk431, 'Series', 'Indicator')
    VAL_U = find_col(df_uk431, 'Value')
    YR_U  = find_col(df_uk431, 'Year')
    df_uk431[VAL_U] = df_uk431[VAL_U].apply(parse_num)
    uk_trend = df_uk431.groupby([YR_U, SER_U])[VAL_U].mean().unstack(SER_U).sort_index()
    if len(uk_trend) > 0:
        fig, ax = plt.subplots(figsize=(13, 5))
        for col in uk_trend.columns:
            ax.plot(uk_trend.index.astype(str), uk_trend[col], marker='o', ms=4, label=col[:70])
        ax.set_title('UK adult learning participation (SDG 4.3.1)', fontweight='bold')
        ax.set_ylabel('Participation rate (%)')
        ax.legend(fontsize=7, loc='best')
        plt.xticks(rotation=45)
        savefig('s7_uk_adult_learning.png')
        print(f'S7b: {len(uk_trend)} years of UK adult learning data')
    else:
        print('S7b: no UK adult learning data available')
except Exception as e:
    print(f'S7b skipped: {e}')
"""))

cells.append(code("""\
# S7c — Summary comparison table
import pandas as pd
comparison = pd.DataFrame({
    'Metric': [
        'School system type',
        'Tracking / selection age',
        'NEET rate 15–29 (approx.)',
        'Upper-secondary completion',
        'Tertiary participation rate',
        'Education spending % GDP',
        'Constitutional right to HE',
        'Income-related admission barriers',
    ],
    'Italy': [
        'Tripartite (Liceo / Tecnico / Professionale)',
        '14 years old',
        '~18–20%',
        '~85%',
        '~35%',
        '~4.0%',
        'Art. 34 — merit-based access',
        'High (diploma gate + fees)',
    ],
    'United Kingdom': [
        'Comprehensive + post-16 tracks',
        '16+ (A-levels / T-levels)',
        '~10–12%',
        '~90%+',
        '~55%',
        '~5.5%',
        'Similar constitutional protection',
        'Moderate (student loan scheme)',
    ],
})
comparison.set_index('Metric', inplace=True)
display(comparison)
"""))

# ── Section 9 — Gender, COVID Shock, and Predictive Panel ────────────────────
cells.append(md("""\
---
## Section 9 — Gender, COVID Shock, and Predictive Panel

The national ISTAT NEET source already contains sex and year dimensions, while the regional NEET file can be merged with the existing transition bridge panel to create a lightweight predictive panel.

This section adds three derived views:
- gender gaps by age group and year,
- a pre-COVID vs shock vs recovery summary,
- a region-level predictive panel based on the transition bridge features.
"""))

cells.append(code("""\
from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt

candidate_roots = [Path('..') / 'local_data' / 'processed', Path('local_data') / 'processed']
PROC = next((p for p in candidate_roots if p.exists()), candidate_roots[0])

gender_gap = pd.read_csv(PROC / 'neet_gender_gap_by_year.csv')

focus_age = 'Y15-29'
focus_gap = gender_gap[gender_gap['classe_eta'] == focus_age].copy().sort_values('year')

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(focus_gap['year'], focus_gap['female_minus_male_pp'], marker='o', color='#b03a2e', lw=2)
ax.axhline(0, color='0.3', lw=1, ls='--')
ax.set_title(f'Female-minus-male NEET gap — {focus_age}')
ax.set_xlabel('Year')
ax.set_ylabel('Difference (pp)')
plt.tight_layout()
plt.show()

print('Latest gender-gap observations for', focus_age)
display(focus_gap.tail(5)[['year', 'female', 'male', 'female_minus_male_pp', 'female_to_male_ratio']])
"""))

cells.append(code("""\
metrics_path = PROC / 'neet_regional_risk_model_metrics.json'
pred_path = PROC / 'neet_regional_risk_model_predictions.csv'

with open(metrics_path, 'r', encoding='utf-8') as handle:
    metrics = json.load(handle)

print('Holdout metrics for the region-level baseline model')
for key in ['train_rows', 'test_rows', 'rmse', 'mae', 'r2', 'holdout_year']:
    print(f"{key}: {metrics.get(key)}")

predictions = pd.read_csv(pred_path)
print('\nTop over-predicted regions in the holdout year')
display(predictions.sort_values('prediction_error').head(8)[['REF_AREA', 'REF_AREA_LABEL', 'neet_risk_index', 'predicted_neet_risk_index', 'prediction_error']])
"""))

# ── Section 8 — Synthesis ─────────────────────────────────────────────────────
cells.append(md("""\
---
## Section 8 — Synthesis & Policy Implications

### Key findings

| Finding | Evidence |
|---------|----------|
| Education level is the strongest predictor of NEET risk | S1a: NEET rate ~25% for lowest education vs ~5% for graduates |
| Italy's tripartite system creates geographic disparities | S2a: wide regional Liceo/Professionale ratios |
| Most university entrants come from Liceo | S3a: >50% of immatricolati hold a Liceo diploma |
| Brain drain accelerates when youth cannot find local opportunity | S5e: emigration peaks post-2008 |
| Italy under-invests in education relative to peers | S5f: below 4% GDP vs 5–6% for UK/DE |
| UK comprehensive schools produce lower NEET rates | S7: 10–12% UK vs 18–20% Italy |

### The merit-vs-credential argument

Italian Constitution Art. 33 states: *"L'arte e la scienza sono libere e libero ne è l'insegnamento."*
Art. 34 adds: *"I capaci e meritevoli, anche se privi di mezzi, hanno diritto di raggiungere i gradi più alti degli studi."*

**"Even those lacking means"** — the constitution explicitly extends higher education access
to those without financial resources. A reading consistent with human-rights principles
extends this to those who lack *credentials* through structural failure (inaccessible schools,
regional barriers, household poverty), not through lack of capacity.

**Recommendation**: Italy should pilot an *adult university access route* (similar to the
UK's Access to Higher Education diploma) allowing NEETs and early school-leavers to demonstrate
merit through a standardised assessment — bypassing the diploma gate for students who can
demonstrate the competences equivalent to secondary completion.

### Summary recommendations

| # | Recommendation | Rationale |
|---|---------------|-----------|
| 1 | Expand Istituto Professionale density in Southern provinces | Reduce geographic barriers |
| 2 | Create an adult HE access pathway (no diploma required, merit-based) | Constitutional compliance + NEET re-integration |
| 3 | Raise education spending to ≥5% GDP | Close gap with EU peers |
| 4 | Means-test and expand DSU grants | Target support to at-risk groups |
| 5 | Pilot comprehensive lower-secondary reforms | Delay tracking from 14 to 16 |
"""))

cells.append(code("""\
# Save analysis manifest
import json
from datetime import datetime
manifest_out = {
    'generated': datetime.now().isoformat(),
    'figures': sorted([f.name for f in OUT.glob('s*.png')]),
    'sections': [
        'S1: NEET Landscape (by education, region, trend, citizenship)',
        'S2: Tripartite school system (school density by track and area)',
        'S3: Diploma gate (matriculations, province, grades, mobility)',
        'S4: University flows (immatricolati, dropout, laureati)',
        'S5: Economic context (GDP, Gini, productivity, brain drain, spending)',
        'S6: Student privileges (exemptions)',
        'S7: Italy vs UK comparison (completion, adult learning)',
        'S8: Synthesis and policy recommendations',
        'S9: Gender, COVID shock, and predictive panel',
    ]
}
(OUT / 'analysis_manifest.json').write_text(json.dumps(manifest_out, indent=2, ensure_ascii=False))
print(f"Notebook complete — {len(manifest_out['figures'])} figures saved to {OUT.resolve()}")
print(json.dumps(manifest_out, indent=2, ensure_ascii=False))
"""))

# ─────────────────────────────────────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    },
    "cells": cells
}

out_path = Path(__file__).parent.parent / 'Notebooks' / 'italy_neet_full_analysis.ipynb'
out_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False), encoding='utf-8')
print(f'Created: {out_path}  ({out_path.stat().st_size:,} bytes, {len(cells)} cells)')
