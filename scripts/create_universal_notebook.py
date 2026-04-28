r"""
Generate Notebooks/italy_universal_interactive.ipynb
A single comprehensive, interactive Jupyter notebook covering all aspects of
the Italian NEET / education / economic case study.

Run from the workspace root:
    python scripts/create_universal_notebook.py
"""
import json
import uuid
from pathlib import Path


def c(cell_type, source, **kw):
    base = {
        "cell_type": cell_type,
        "id": uuid.uuid4().hex[:12],
        "metadata": {},
        "source": source,
    }
    if cell_type == "code":
        base.update({"outputs": [], "execution_count": None})
    return {**base, **kw}


def md(text):
    return c("markdown", text.splitlines(keepends=True))


def code(text):
    return c("code", text.splitlines(keepends=True))


cells = []

# ── Title & Overview ────────────────────────────────────────────────────────────
cells.append(md("""\
# 🇮🇹 Italy's NEET Crisis — Universal Interactive Notebook
### A Comprehensive, Cross-Dimensional Study of Education, Territory & Economic Stagnation

> **How to use this notebook**  
> Every section contains **interactive widgets** (dropdowns, sliders, multi-selects).  
> Run all cells first (`Kernel › Restart & Run All`), then explore by changing the widget values.  
> Charts update instantly — no re-running required.

---

**Research questions**

| # | Question |
|---|----------|
| 1 | Who are Italy's NEETs and how does education level shape their risk? |
| 2 | Does Italy's tripartite secondary school system create geographic barriers? |
| 3 | Should NEETs access university on merit, without a diploma? |
| 4 | How does Italy compare with the UK's comprehensive school system? |
| 5 | What is Italy's macroeconomic context — and is low education spending part of the problem? |
| 6 | How do textbook costs and publisher concentration lock families into poverty? |
| 7 | What does the full university pipeline (enrolment → dropout → graduation) look like? |

**Data sources**  
ISTAT NEET micro-data · Ministero dell'Istruzione (MIM) school & student registers  
MUR immatricolati / laureati / iscritti · Eurostat GDP · World Bank Gini  
OECD Education at a Glance · OurWorldData productivity & emigration  
UK SDG Goal-4 stats · MinIstruzione Libri di Testo

---
"""))

# ── 0. Setup ────────────────────────────────────────────────────────────────────
cells.append(code("""\
# ── 0. Imports & helpers ──────────────────────────────────────────────────────
import warnings, re, json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams.update({'figure.figsize': (13, 5), 'figure.dpi': 110, 'font.size': 11})

# ── ipywidgets (graceful fallback if not installed) ───────────────────────────
try:
    import ipywidgets as widgets
    from ipywidgets import interact, interactive_output, HBox, VBox
    from IPython.display import display, clear_output
    _WIDGETS = True
except ImportError:
    _WIDGETS = False
    print("ipywidgets not installed — interactive controls disabled; charts still render.")

# ── Paths ─────────────────────────────────────────────────────────────────────
ROOT = Path('../local_data') if Path('../local_data').exists() else Path('local_data')
OUT  = Path('neet_outputs')
OUT.mkdir(exist_ok=True, parents=True)

print(f'ROOT resolved → {ROOT.resolve()}')
print(f'Output dir   → {OUT.resolve()}')
print(f'Interactive widgets: {_WIDGETS}')
"""))

cells.append(code("""\
# ── Utility functions ─────────────────────────────────────────────────────────

def smart_read_csv(path, **kw):
    \"\"\"Auto-detect encoding + separator; always returns a multi-column DataFrame.\"\"\"
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
    \"\"\"Return first column whose name contains any keyword (case-insensitive).\"\"\"
    for k in kw:
        for col in df.columns:
            if k.upper() in str(col).upper():
                return col
    return None


def parse_num(x):
    \"\"\"Parse numbers, handling Italian thousand-dot format and NaN sentinels.\"\"\"
    if x is None:
        return np.nan
    s = str(x).strip()
    if s in ('', 'N', 'n', '-', 'nan', 'NaN', 'None', ':', '..', 'n/a', 'b', ':'):
        return np.nan
    if re.match(r'^\\d{1,3}(?:\\.\\d{3})+$', s):
        return float(s.replace('.', ''))
    if ',' in s and '.' not in s:
        try:
            return float(s.replace(',', '.'))
        except Exception:
            return np.nan
    try:
        return float(s)
    except Exception:
        return np.nan


def savefig(name, tight=True):
    p = OUT / name
    if tight:
        plt.tight_layout()
    plt.savefig(p, dpi=110, bbox_inches='tight')
    plt.show()


def _tp_key(tp):
    \"\"\"Sort key for ISTAT time-period strings (annual < quarterly).\"\"\"
    s = str(tp)
    if '-Q' in s:
        yr, q = s.split('-Q')
        return float(yr) + float(q) / 10
    try:
        return float(s) - 0.05
    except Exception:
        return -1


print('Utilities loaded.')
"""))

# ── Data Inventory ───────────────────────────────────────────────────────────
cells.append(md("""\
---
## 📂 Data Inventory

The cell below scans all CSV files that are available locally.  
Use the interactive widget to inspect any folder in more detail.
"""))

cells.append(code("""\
# ── Data inventory ────────────────────────────────────────────────────────────
manifest = {}
for f in sorted(ROOT.rglob('*.csv')):
    key = str(f.parent.relative_to(ROOT))
    manifest.setdefault(key, []).append(f.name)

total = sum(len(v) for v in manifest.values())
print(f'{total} CSV files across {len(manifest)} folders:')
for k, v in sorted(manifest.items()):
    print(f'  {k}: {len(v)} file(s)')
"""))

cells.append(code("""\
# ── Interactive: browse a data folder ────────────────────────────────────────
if _WIDGETS and manifest:
    folder_dd = widgets.Dropdown(
        options=sorted(manifest.keys()),
        description='Folder:',
        layout=widgets.Layout(width='60%'),
    )
    out_inv = widgets.Output()

    def _show_folder(folder):
        with out_inv:
            clear_output(wait=True)
            files = manifest.get(folder, [])
            print(f'Folder: {folder}  ({len(files)} files)')
            for f in files:
                fp = ROOT / folder / f
                try:
                    df = smart_read_csv(fp, nrows=3)
                    print(f'  {f} — {df.shape[1]} cols, sample cols: {list(df.columns[:5])}')
                except Exception as e:
                    print(f'  {f} — could not preview ({e})')

    widgets.interactive(_show_folder, folder=folder_dd)
    display(VBox([folder_dd, out_inv]))
    _show_folder(folder_dd.value)
else:
    for folder, files in sorted(manifest.items()):
        print(f'{folder}: {files[:3]}{"…" if len(files)>3 else ""}')
"""))

# ── Section 1: NEET Landscape ────────────────────────────────────────────────
cells.append(md("""\
---
## Section 1 — Italy's NEET Landscape

Italy consistently posts some of the highest NEET rates in the EU. We examine:
- **S1a** NEET incidence broken down by education level  
- **S1b** Regional NEET distribution  
- **S1c** National NEET trend (annual + quarterly)  
- **S1d** NEET breakdown by citizenship  

> NEETs with the lowest qualifications are most at risk — the very group that would benefit  
> most from open-access tertiary education.

Use the **year slider** and **age-group dropdown** in each sub-section to explore the data.
"""))

cells.append(code("""\
# ── Load NEET core datasets ──────────────────────────────────────────────────
_neet_inc = _neet_reg = _neet_cit = None

# Incidenza per titolo di studio
try:
    inc_path = next(
        (p for p in ROOT.glob('*.csv')
         if 'incidenza' in p.name.lower() and 'titolo' in p.name.lower()), None)
    if inc_path:
        _neet_inc = pd.read_csv(
            str(inc_path), sep=',', encoding='utf-8-sig', quotechar="'", low_memory=False)
        _neet_inc.columns = [str(c).strip() for c in _neet_inc.columns]
        _TIME_I = find_col(_neet_inc, 'TIME_PERIOD', 'TIME')
        _OBS_I  = find_col(_neet_inc, 'Osservazione', 'OBS_VALUE', 'OBS')
        _EDU_I  = find_col(_neet_inc, 'Titolo')
        _AGE_I  = find_col(_neet_inc, 'AGE')
        _neet_inc[_OBS_I] = _neet_inc[_OBS_I].apply(parse_num)
        print(f'Incidenza dataset: {_neet_inc.shape}')
except Exception as e:
    print(f'Incidenza load failed: {e}')

# Dati regionali
try:
    reg_path = next(
        (p for p in ROOT.glob('*.csv')
         if 'regionali' in p.name.lower() and 'neet' in p.name.lower()), None)
    if reg_path:
        _neet_reg = smart_read_csv(reg_path)
        _neet_reg.columns = [str(c).strip() for c in _neet_reg.columns]
        _TIME_R  = find_col(_neet_reg, 'TIME_PERIOD', 'TIME')
        _OBS_R   = find_col(_neet_reg, 'Osservazione', 'OBS')
        _GEO_R   = find_col(_neet_reg, 'Territorio')
        _AGE_R   = find_col(_neet_reg, 'AGE')
        _FREQ_R  = find_col(_neet_reg, 'FREQ')
        _neet_reg[_OBS_R] = _neet_reg[_OBS_R].apply(parse_num)
        print(f'Regional dataset: {_neet_reg.shape}')
except Exception as e:
    print(f'Regional load failed: {e}')

# Cittadinanza
try:
    cit_path = next(
        (p for p in ROOT.glob('*.csv')
         if 'cittadinanza' in p.name.lower() and 'neet' in p.name.lower()), None)
    if cit_path:
        _neet_cit = smart_read_csv(cit_path)
        _neet_cit.columns = [str(c).strip() for c in _neet_cit.columns]
        _TIME_C  = find_col(_neet_cit, 'TIME_PERIOD', 'TIME')
        _OBS_C   = find_col(_neet_cit, 'Osservazione', 'OBS_VALUE')
        _GEO_C   = find_col(_neet_cit, 'Territorio', 'GEO')
        _CIT_C   = find_col(_neet_cit, 'Cittadinanza', 'Citizen')
        _AGE_C   = find_col(_neet_cit, 'AGE')
        _SEX_C   = find_col(_neet_cit, 'SEX')
        _FREQ_C  = find_col(_neet_cit, 'FREQ')
        _ELS_C   = find_col(_neet_cit, 'EURO_LABOUR_STATUS')
        _neet_cit[_OBS_C] = _neet_cit[_OBS_C].apply(parse_num)
        print(f'Citizenship dataset: {_neet_cit.shape}')
except Exception as e:
    print(f'Citizenship load failed: {e}')

print('NEET datasets loaded.')
"""))

cells.append(code("""\
# ── S1a — NEET incidence by education level (interactive year) ────────────────
def plot_neet_by_edu(year=None):
    if _neet_inc is None:
        print('S1a: NEET incidence dataset not available.')
        return
    df = _neet_inc.copy()
    df_it = df[(df['FREQ'] == 'A') & (df['REF_AREA'] == 'IT') & (df['SEX'] == 9)]
    years = sorted(df_it[_TIME_I].astype(str).unique())
    if year is None or year not in years:
        year = years[-1]
    if _AGE_I:
        for a in ['Y15-29', 'Y18-29', 'Y15-34', 'Y15-24']:
            if a in df_it[_AGE_I].values:
                df_it = df_it[df_it[_AGE_I] == a]; break
    df_l = df_it[df_it[_TIME_I].astype(str) == year]
    by_edu = (df_l[df_l[_EDU_I] != 'Totale']
              .groupby(_EDU_I)[_OBS_I].mean()
              .dropna()
              .sort_values())
    if by_edu.empty:
        print(f'S1a: no data for {year}'); return
    colours = sns.color_palette('RdYlGn', len(by_edu))
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.barh(by_edu.index, by_edu.values, color=colours)
    ax.set_xlabel('NEET incidence (%)')
    ax.set_title(f'NEET incidence by education level — Italy {year}', fontweight='bold')
    for bar, v in zip(ax.patches, by_edu.values):
        ax.text(v + 0.3, bar.get_y() + bar.get_height() / 2,
                f'{v:.1f}%', va='center', fontsize=9)
    savefig('s1_neet_by_education.png')

if _WIDGETS and _neet_inc is not None:
    df_it_c = _neet_inc[(_neet_inc['FREQ'] == 'A') &
                         (_neet_inc['REF_AREA'] == 'IT') &
                         (_neet_inc['SEX'] == 9)]
    yrs = sorted(df_it_c[_TIME_I].astype(str).unique())
    interact(plot_neet_by_edu, year=widgets.Dropdown(options=yrs, value=yrs[-1],
             description='Year:', style={'description_width': 'initial'}))
else:
    plot_neet_by_edu()
"""))

cells.append(code("""\
# ── S1b — NEET by region (interactive year + age group) ─────────────────────
EXCL = r'ITALIA|TOTALE|NORD|SUD|CENTRO|ISOLE|MEZZOGIORNO'

def plot_neet_by_region(year=None, age='Y15-29'):
    if _neet_reg is None:
        print('S1b: regional dataset not available.')
        return
    df = (_neet_reg[_neet_reg[_FREQ_R] == 'A'].copy()
          if _FREQ_R else _neet_reg.copy())
    if _AGE_R and age in df[_AGE_R].values:
        df = df[df[_AGE_R] == age]
    years = sorted(df[_TIME_R].astype(str).unique(), reverse=True)
    if year is None or year not in years:
        year = years[0]
    df_yr = df[df[_TIME_R].astype(str) == year]
    by_reg = (df_yr.groupby(_GEO_R)[_OBS_R].mean().dropna())
    by_reg = by_reg[~by_reg.index.str.upper().str.contains(EXCL, na=False, regex=True)]
    by_reg = by_reg.sort_values(ascending=False)
    if by_reg.empty:
        print(f'S1b: no regional data for {year} / {age}'); return
    fig, ax = plt.subplots(figsize=(14, 6))
    clrs = ['crimson' if v > by_reg.median() else 'steelblue' for v in by_reg.values]
    ax.bar(by_reg.index, by_reg.values, color=clrs)
    ax.axhline(by_reg.median(), color='navy', ls='--', lw=1.5,
               label=f'Median: {by_reg.median():.0f}')
    ax.set_ylabel('NEETs (thousands)')
    ax.set_title(f'NEET count by region — {year} (ages {age})', fontweight='bold')
    ax.legend()
    plt.xticks(rotation=45, ha='right', fontsize=8)
    savefig('s1_neet_by_region.png')

if _WIDGETS and _neet_reg is not None:
    df_ann = (_neet_reg[_neet_reg[_FREQ_R] == 'A'] if _FREQ_R else _neet_reg)
    yrs_r  = sorted(df_ann[_TIME_R].astype(str).unique(), reverse=True)
    ages_r = sorted(df_ann[_AGE_R].dropna().unique()) if _AGE_R else ['Y15-29']
    interact(plot_neet_by_region,
             year=widgets.Dropdown(options=yrs_r, value=yrs_r[0],
                                   description='Year:',
                                   style={'description_width': 'initial'}),
             age=widgets.Dropdown(options=ages_r,
                                  value='Y15-29' if 'Y15-29' in ages_r else ages_r[0],
                                  description='Age group:',
                                  style={'description_width': 'initial'}))
else:
    plot_neet_by_region()
"""))

cells.append(code("""\
# ── S1c — National NEET trend (all time periods) ─────────────────────────────
def plot_neet_trend(age='Y15-29', show_quarterly=True):
    if _neet_reg is None:
        print('S1c: regional dataset not available.'); return
    df = _neet_reg[_neet_reg[_GEO_R] == 'Italia'].copy()
    if _AGE_R and age in df[_AGE_R].values:
        df = df[df[_AGE_R] == age]
    if not show_quarterly and _FREQ_R:
        df = df[df[_FREQ_R] == 'A']
    trend = df.groupby(_TIME_R)[_OBS_R].mean().dropna()
    trend = trend.reindex(sorted(trend.index, key=_tp_key))
    if trend.empty:
        print('S1c: no trend data'); return
    fig, ax = plt.subplots(figsize=(15, 5))
    xs = range(len(trend))
    ax.plot(xs, trend.values, marker='o', ms=4, color='crimson', lw=2)
    ax.fill_between(xs, trend.values, alpha=0.12, color='crimson')
    ax.set_xticks(list(xs))
    ax.set_xticklabels(trend.index, rotation=45, ha='right', fontsize=7)
    ax.set_ylabel('NEETs (thousands)')
    ax.set_title(f'Italy — national NEET trend ({age})', fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}k'))
    savefig('s1_neet_trend.png')

if _WIDGETS and _neet_reg is not None:
    ages_t = sorted(_neet_reg[_AGE_R].dropna().unique()) if _AGE_R else ['Y15-29']
    interact(plot_neet_trend,
             age=widgets.Dropdown(options=ages_t,
                                  value='Y15-29' if 'Y15-29' in ages_t else ages_t[0],
                                  description='Age group:',
                                  style={'description_width': 'initial'}),
             show_quarterly=widgets.Checkbox(value=True, description='Include quarterly data'))
else:
    plot_neet_trend()
"""))

cells.append(code("""\
# ── S1d — NEET by citizenship (interactive year) ─────────────────────────────
def plot_neet_by_citizenship(year=None):
    if _neet_cit is None:
        print('S1d: citizenship dataset not available.'); return
    df = (_neet_cit[_neet_cit[_FREQ_C] == 'A'].copy()
          if _FREQ_C else _neet_cit.copy())
    years_c = sorted(df[_TIME_C].astype(str).unique(), reverse=True)
    if year is None or year not in years_c:
        year = years_c[0]
    for yr in years_c if year == years_c[0] else [year]:
        df_yr = df[(df[_TIME_C].astype(str) == yr) & (df[_GEO_C] == 'Italia')].copy()
        if _AGE_C and 'Y15-29' in df_yr[_AGE_C].values:
            df_yr = df_yr[df_yr[_AGE_C] == 'Y15-29']
        if _SEX_C:
            sex_tot = df_yr[_SEX_C].dropna().max()
            df_yr = df_yr[df_yr[_SEX_C] == sex_tot]
        if _ELS_C and _ELS_C in df_yr.columns:
            ls_max = df_yr.groupby(_ELS_C)[_OBS_C].sum().idxmax()
            df_yr = df_yr[df_yr[_ELS_C] == ls_max]
        by_cit = df_yr[df_yr[_CIT_C] != 'Totale'].groupby(_CIT_C)[_OBS_C].sum().dropna()
        if len(by_cit) >= 2:
            by_cit = by_cit.sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(9, 5))
            colors_c = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            ax.bar(by_cit.index, by_cit.values, color=colors_c[:len(by_cit)])
            ax.set_title(f'NEETs 15–29 by citizenship — Italy {yr}', fontweight='bold')
            ax.set_ylabel('NEETs (thousands)')
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}k'))
            for i, (lab, v) in enumerate(by_cit.items()):
                ax.text(i, v + 2, f'{v:,.0f}k', ha='center', fontsize=9)
            plt.xticks(rotation=20, ha='right')
            savefig('s1_neet_by_citizenship.png')
            return
    print(f'S1d: no citizenship breakdown for {year}')

if _WIDGETS and _neet_cit is not None:
    df_c = (_neet_cit[_neet_cit[_FREQ_C] == 'A'] if _FREQ_C else _neet_cit)
    yrs_c = sorted(df_c[_TIME_C].astype(str).unique(), reverse=True)
    interact(plot_neet_by_citizenship,
             year=widgets.Dropdown(options=yrs_c, value=yrs_c[0],
                                   description='Year:',
                                   style={'description_width': 'initial'}))
else:
    plot_neet_by_citizenship()
"""))

# ── Section 2: School System ─────────────────────────────────────────────────
cells.append(md("""\
---
## Section 2 — Italy's Tripartite Secondary School System

Italy channels pupils at **age 14** into one of three tracks:
- **Liceo** — academic, leads naturally to university
- **Istituto Tecnico** — technical-vocational
- **Istituto Professionale** — vocational, shortest path to work certification

The geographic density of each track determines opportunity:  
if Liceo schools are scarce in a province, students with academic potential may disengage.

> Italy ≠ UK: the UK uses **comprehensive secondary schools** — pupils receive the same  
> core curriculum until 16. Italy pre-sorts pupils at 14.
"""))

cells.append(code("""\
# ── Load school & student data ────────────────────────────────────────────────
_df_scuole = _df_alu = None

try:
    scuole_path = ROOT / 'MinIstruzione/Scuole/SCUANAGRAFESTAT20242520250831.csv'
    _df_scuole = smart_read_csv(scuole_path)
    _df_scuole.columns = [str(c).strip() for c in _df_scuole.columns]
    TIPO_S = 'DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'
    AREA_S = 'AREAGEOGRAFICA'
    REG_S  = 'REGIONE'
    COD_S  = 'CODICESCUOLA'

    def classify_track(name):
        n = str(name).upper()
        if any(x in n for x in ['LICEO', 'MAGISTRALE', 'CLASSICO', 'ARTE']):
            return 'Liceo (Academic)'
        if any(x in n for x in ['TECNICO', 'GEOMETRI', 'AGRARIO', 'NAUTICO']):
            return 'Istituto Tecnico'
        if 'PROF' in n:
            return 'Istituto Professionale'
        if any(x in n for x in ['PRIMARIA', 'INFANZIA', 'PRIMO GRADO', 'COMPRENSIVO']):
            return 'Primary / Lower Secondary'
        return 'Other'

    _df_scuole['TRACK'] = _df_scuole[TIPO_S].apply(classify_track)
    print(f'Schools dataset: {_df_scuole.shape}')
except Exception as e:
    print(f'Schools load failed: {e}')

try:
    alu_path = ROOT / 'MinIstruzione/Alunni/ALUSECGRADOINDPAR20242520250831.csv'
    _df_alu = smart_read_csv(alu_path)
    _df_alu.columns = [str(c).strip() for c in _df_alu.columns]
    _M_ALU  = find_col(_df_alu, 'ALUNNIMASCHI')
    _F_ALU  = find_col(_df_alu, 'ALUNNIFEMMINE')
    _TRK_ALU = find_col(_df_alu, 'TIPOPERCORSO')
    _IND_ALU = find_col(_df_alu, 'INDIRIZZO')
    _REG_ALU = find_col(_df_alu, 'REGIONE')
    for col in [_M_ALU, _F_ALU]:
        if col:
            _df_alu[col] = _df_alu[col].apply(parse_num)
    _df_alu['TOTALE'] = _df_alu[[_M_ALU, _F_ALU]].sum(axis=1)
    print(f'Students dataset: {_df_alu.shape}')
except Exception as e:
    print(f'Students load failed: {e}')
"""))

cells.append(code("""\
# ── S2a — School count by track and geographic area (interactive area filter) ─
SECONDARY = ['Liceo (Academic)', 'Istituto Tecnico', 'Istituto Professionale']

def plot_schools_by_track(area_filter='All'):
    if _df_scuole is None:
        print('S2a: school dataset not available.'); return
    df_sec = _df_scuole[_df_scuole['TRACK'].isin(SECONDARY)].copy()
    if area_filter != 'All' and AREA_S in df_sec.columns:
        df_sec = df_sec[df_sec[AREA_S] == area_filter]
    pivot = df_sec.groupby([AREA_S, 'TRACK'])[COD_S].count().unstack('TRACK').fillna(0).astype(int)
    if pivot.empty:
        print(f'S2a: no data for area={area_filter}'); return
    ax = pivot.plot(kind='bar', figsize=(14, 6), colormap='tab10')
    ax.set_title(f'Secondary school branches by track — area: {area_filter}', fontweight='bold')
    ax.set_ylabel('Number of school branches')
    plt.xticks(rotation=25, ha='right')
    savefig('s2_schools_by_track_area.png')

if _WIDGETS and _df_scuole is not None and AREA_S in _df_scuole.columns:
    areas = ['All'] + sorted(_df_scuole[AREA_S].dropna().unique().tolist())
    interact(plot_schools_by_track,
             area_filter=widgets.Dropdown(options=areas, value='All',
                                          description='Geographic area:',
                                          style={'description_width': 'initial'}))
else:
    plot_schools_by_track()
"""))

cells.append(code("""\
# ── S2b — Liceo/Professionale ratio by region ─────────────────────────────────
def plot_liceo_ratio(sort_by='ratio'):
    if _df_scuole is None:
        print('S2b: school dataset not available.'); return
    df_sec = _df_scuole[_df_scuole['TRACK'].isin(SECONDARY)].copy()
    sbr = df_sec.groupby([REG_S, 'TRACK'])[COD_S].count().unstack('TRACK').fillna(0).astype(int)
    sbr['ratio'] = (
        sbr.get('Liceo (Academic)', pd.Series(0, index=sbr.index)) /
        sbr.get('Istituto Professionale', pd.Series(1, index=sbr.index)).replace(0, 1)
    )
    ratio = sbr['ratio']
    if sort_by == 'ratio':
        ratio = ratio.sort_values(ascending=False)
    else:
        ratio = ratio.sort_index()
    fig, ax = plt.subplots(figsize=(14, 6))
    clrs = ['crimson' if v > ratio.median() else 'steelblue' for v in ratio.values]
    ax.barh(ratio.index, ratio.values, color=clrs)
    ax.axvline(ratio.median(), color='navy', lw=1.5, ls='--',
               label=f'Median: {ratio.median():.1f}')
    ax.set_title('Liceo-to-Professionale ratio by region\\n(higher = fewer vocational options)',
                 fontweight='bold')
    ax.legend()
    savefig('s2_school_track_ratio_by_region.png')

if _WIDGETS and _df_scuole is not None:
    interact(plot_liceo_ratio,
             sort_by=widgets.ToggleButtons(options=['ratio', 'region name'],
                                           description='Sort by:',
                                           style={'description_width': 'initial'}))
else:
    plot_liceo_ratio()
"""))

cells.append(code("""\
# ── S2c — Students by secondary track (interactive: total vs by region) ────────
def plot_students_by_track(breakdown='National total', region='All'):
    if _df_alu is None:
        print('S2c: student dataset not available.'); return
    df = _df_alu.copy()
    if region != 'All' and _REG_ALU and region in df[_REG_ALU].values:
        df = df[df[_REG_ALU] == region]
    if breakdown == 'National total' or not _TRK_ALU:
        by_track = df.groupby(_TRK_ALU)['TOTALE'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(9, 6))
        wedges, texts, autotexts = ax.pie(
            by_track.values, labels=by_track.index, autopct='%1.1f%%',
            colors=sns.color_palette('tab10', len(by_track)), startangle=140)
        title_sfx = f' — {region}' if region != 'All' else ''
        ax.set_title(f'Upper-secondary students by track (2024–25){title_sfx}', fontweight='bold')
    else:
        by_track = df.groupby(_TRK_ALU)['TOTALE'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(by_track.index, by_track.values, color=sns.color_palette('tab10', len(by_track)))
        ax.set_ylabel('Students')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))
        ax.set_title('Students by track', fontweight='bold')
        plt.xticks(rotation=25, ha='right')
    savefig('s2_students_by_track.png')

if _WIDGETS and _df_alu is not None:
    regs = ['All'] + (sorted(_df_alu[_REG_ALU].dropna().unique().tolist()) if _REG_ALU else [])
    interact(plot_students_by_track,
             breakdown=widgets.ToggleButtons(options=['National total', 'Bar chart'],
                                             description='View:',
                                             style={'description_width': 'initial'}),
             region=widgets.Dropdown(options=regs, value='All',
                                     description='Region:',
                                     style={'description_width': 'initial'}))
else:
    plot_students_by_track()
"""))

# ── Section 3: Higher Education ──────────────────────────────────────────────
cells.append(md("""\
---
## Section 3 — The Diploma Gate: University Entry & Flows

In Italy a *diploma di maturità* is the legal prerequisite for university admission.

- **S3a** Matriculations by diploma type  
- **S3b** Liceo share by province of residence  
- **S3c** Diploma grade distribution  
- **S3d** Geographic mobility (in-province vs out-of-province students)  
- **S3e** University enrolment trend  
- **S3f** Dropout rate trend  
- **S3g** Graduation (laureati) trend  

> Italian constitutional Art. 33–34 establishes *merito* as the access principle.  
> If the diploma gate tests credential-holding rather than merit, NEETs with equivalent  
> intellectual capacity are excluded unconstitutionally.
"""))

cells.append(code("""\
# ── Load higher-education datasets ────────────────────────────────────────────
_df_imm = _df_drop = _df_lau = _df_dip = _df_vote = _df_fuori = _df_iscr_reg = None

def _try_load(path, label):
    try:
        df = smart_read_csv(ROOT / path)
        df.columns = [str(c).strip() for c in df.columns]
        print(f'{label}: {df.shape}')
        return df
    except Exception as e:
        print(f'{label} load failed: {e}')
        return None

_df_imm       = _try_load('MUR/immatricolati/01_immatricolatixanno.csv', 'Immatricolati')
_df_drop      = _try_load('MUR/tassoabbandono_180226.csv', 'Dropout')
_df_lau       = _try_load('MUR/laureati/01_laureatixanno.csv', 'Laureati')
_df_dip       = _try_load('MUR/immatricolati/10_immatricolatixdiplomascuolasecondariaxclasse.csv',
                           'Diploma type')
_df_vote      = _try_load('MUR/immatricolati/16_immatricolatixvotodiplomascuolasec.csv',
                           'Diploma grade')
_df_fuori     = _try_load('MUR/MUR_iscritti/iscritti_in_sede_fuori_sede.csv', 'Mobility')
_df_iscr_reg  = _try_load('MUR/MUR_iscritti/iscritti_per_regione.csv', 'Enrolment by region')
"""))

cells.append(code("""\
# ── S3a — Matriculations by diploma type ──────────────────────────────────────
def plot_matriculations_by_diploma(year=None, top_n=15):
    if _df_dip is None:
        print('S3a: diploma dataset not available.'); return
    DIP_COL  = find_col(_df_dip, 'Diploma_tipo', 'Diploma')
    IMM_COL  = find_col(_df_dip, 'Imm')
    ANNO_COL = find_col(_df_dip, 'AnnoA', 'Anno')
    for col in [DIP_COL, IMM_COL, ANNO_COL]:
        if col is None:
            print(f'S3a: required column not found'); return
    _df_dip[IMM_COL] = _df_dip[IMM_COL].apply(parse_num)
    years = sorted(_df_dip[ANNO_COL].astype(str).unique())
    if year is None or year not in years:
        year = years[-1]
    by_dip = (_df_dip[_df_dip[ANNO_COL].astype(str) == year]
              .groupby(DIP_COL)[IMM_COL].sum()
              .sort_values(ascending=True)
              .tail(top_n))
    fig, ax = plt.subplots(figsize=(12, max(4, len(by_dip) * 0.45)))
    ax.barh(by_dip.index, by_dip.values, color='steelblue')
    ax.set_xlabel('Matriculations')
    ax.set_title(f'University matriculations by diploma type — {year} (top {top_n})',
                 fontweight='bold')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    savefig('s3_matriculations_by_diploma.png')

if _WIDGETS and _df_dip is not None:
    ANNO_C2 = find_col(_df_dip, 'AnnoA', 'Anno')
    yrs_d = sorted(_df_dip[ANNO_C2].astype(str).unique()) if ANNO_C2 else ['latest']
    interact(plot_matriculations_by_diploma,
             year=widgets.Dropdown(options=yrs_d, value=yrs_d[-1],
                                   description='Year:',
                                   style={'description_width': 'initial'}),
             top_n=widgets.IntSlider(min=5, max=30, step=1, value=15,
                                     description='Top N types:',
                                     style={'description_width': 'initial'}))
else:
    plot_matriculations_by_diploma()
"""))

cells.append(code("""\
# ── S3b-c — Diploma grade distribution + Geographic mobility ─────────────────
try:
    # Grade distribution
    if _df_vote is not None:
        VOTO    = find_col(_df_vote, 'Diploma_Voto', 'Voto', 'Grad')
        IMM3    = find_col(_df_vote, 'Imm')
        AN3     = find_col(_df_vote, 'AnnoA', 'Anno')
        _df_vote[IMM3] = _df_vote[IMM3].apply(parse_num)
        lat_v   = _df_vote[AN3].astype(str).max()
        by_voto = (_df_vote[_df_vote[AN3].astype(str) == lat_v]
                   .groupby(VOTO)[IMM3].sum().sort_index())
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.bar(by_voto.index.astype(str), by_voto.values, color='steelblue')
        ax.set_xlabel('Diploma grade band')
        ax.set_ylabel('Matriculations')
        ax.set_title(f'Diploma grade distribution of university entrants — {lat_v}',
                     fontweight='bold')
        plt.xticks(rotation=45, ha='right', fontsize=7)
        savefig('s3_diploma_grade_distribution.png')
        print(f'S3b: {len(by_voto)} grade bands')
except Exception as e:
    print(f'S3b skipped: {e}')

try:
    # Mobility
    if _df_fuori is not None:
        ISC_F  = find_col(_df_fuori, 'Isc')
        PROVD  = find_col(_df_fuori, 'ProvinciaSede', 'ProvSede')
        PROVC  = find_col(_df_fuori, 'provcorso', 'ProvCorso', 'ProvRes')
        AN4    = find_col(_df_fuori, 'AnnoA', 'Anno')
        _df_fuori[ISC_F] = _df_fuori[ISC_F].apply(parse_num)
        lat_f  = _df_fuori[AN4].astype(str).max()
        df_f   = _df_fuori[_df_fuori[AN4].astype(str) == lat_f].copy()
        if PROVD and PROVC:
            df_f['fuori'] = (df_f[PROVD].astype(str).str.strip() !=
                             df_f[PROVC].astype(str).str.strip())
            in_vs_out = df_f.groupby('fuori')[ISC_F].sum()
            labels    = ['Same province', 'Different province']
            fig, ax   = plt.subplots(figsize=(7, 5))
            ax.pie(in_vs_out.values, labels=labels, autopct='%1.1f%%',
                   colors=['#2ca02c', '#d62728'], startangle=90)
            ax.set_title(f'University students geographic mobility — {lat_f}', fontweight='bold')
            savefig('s3_geographic_mobility.png')
            fuori_pct = in_vs_out.get(True, 0) / in_vs_out.sum() * 100
            print(f'S3c: {fuori_pct:.1f}% study outside home province')
except Exception as e:
    print(f'S3c skipped: {e}')
"""))

cells.append(code("""\
# ── S3d — University pipeline: immatricolati → dropout → laureati ─────────────
def plot_uni_pipeline(metric='all'):
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Immatricolati
    ax = axes[0]
    if _df_imm is not None:
        AN5 = find_col(_df_imm, 'AnnoA', 'Anno')
        if 'Imm' not in _df_imm.columns:
            _df_imm['Imm'] = _df_imm[['Imm_M','Imm_F']].apply(parse_num).sum(axis=1) if 'Imm_M' in _df_imm.columns else np.nan
        else:
            _df_imm['Imm'] = _df_imm['Imm'].apply(parse_num)
        trend_imm = _df_imm.groupby(AN5)['Imm'].sum().sort_index().dropna()
        ax.plot(trend_imm.index.astype(str), trend_imm.values, marker='o', color='steelblue', lw=2)
        ax.set_title('First-year enrolments\\n(immatricolati)', fontweight='bold')
        ax.set_ylabel('Students')
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=7)
    else:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)

    # Dropout
    ax = axes[1]
    if _df_drop is not None:
        yr_c  = _df_drop.columns[0]
        val_c = _df_drop.columns[1]
        _df_drop[val_c] = _df_drop[val_c].apply(parse_num)
        drop_clean = _df_drop.dropna(subset=[val_c])
        ax.plot(drop_clean[yr_c].astype(str), drop_clean[val_c], marker='s', color='crimson', lw=2)
        ax.set_title('1st→2nd year dropout rate', fontweight='bold')
        ax.set_ylabel('Dropout rate (%)')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=7)
    else:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)

    # Laureati
    ax = axes[2]
    if _df_lau is not None:
        AN6 = find_col(_df_lau, 'AnnoA', 'Anno')
        LAU = find_col(_df_lau, 'Lau')
        if LAU:
            _df_lau[LAU] = _df_lau[LAU].apply(parse_num)
            trend_lau = _df_lau.groupby(AN6)[LAU].sum().sort_index().dropna()
            ax.plot(trend_lau.index.astype(str), trend_lau.values, marker='^', color='green', lw=2)
            ax.set_title('Graduates (laureati)', fontweight='bold')
            ax.set_ylabel('Graduates')
            ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=7)
    else:
        ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)

    plt.suptitle('University Pipeline — Italy', fontsize=13, fontweight='bold', y=1.01)
    savefig('s3_uni_pipeline.png')

plot_uni_pipeline()
"""))

# ── Section 4: Economic Context ──────────────────────────────────────────────
cells.append(md("""\
---
## Section 4 — Italy's Economic Context

Italy has experienced **three lost decades**: GDP per capita stagnated, inequality rose,  
and labour productivity grew slower than peers.

Key datasets:
- GDP per capita volume index (Eurostat, EU27 = 100)
- Gini coefficient (World Bank)
- Productivity vs educational attainment (OurWorldData)
- Upper-secondary completion rates
- Brain drain — net emigration
- Education spending as % of GDP

Use the **country multi-select** in each chart to customise your comparison.
"""))

cells.append(code("""\
# ── Load economic context datasets ────────────────────────────────────────────
_df_gdp = _df_gini = _df_emig = _df_comp = _df_prod = None

try:
    _df_gdp = smart_read_csv(ROOT / 'oecd/eurostat_gdp_per_capita.csv')
    _df_gdp.columns = [str(c).strip() for c in _df_gdp.columns]
    _OBS_G = find_col(_df_gdp, 'OBS_VALUE')
    _GEO_G = find_col(_df_gdp, 'geo')
    _TIM_G = find_col(_df_gdp, 'TIME_PERIOD', 'TIME')
    _df_gdp[_OBS_G] = _df_gdp[_OBS_G].apply(parse_num)
    print(f'GDP dataset: {_df_gdp.shape}')
except Exception as e:
    print(f'GDP load failed: {e}')

try:
    _df_gini = smart_read_csv(ROOT / 'WB_WDI_SI_POV_GINI.csv')
    _df_gini.columns = [str(c).strip() for c in _df_gini.columns]
    _REF_Gi  = find_col(_df_gini, 'REF_AREA')
    _OBS_Gi  = find_col(_df_gini, 'OBS_VALUE')
    _TIM_Gi  = find_col(_df_gini, 'TIME_PERIOD', 'TIME')
    _df_gini[_OBS_Gi] = _df_gini[_OBS_Gi].apply(parse_num)
    print(f'Gini dataset: {_df_gini.shape}')
except Exception as e:
    print(f'Gini load failed: {e}')

try:
    _df_emig = smart_read_csv(ROOT / 'ourWorldData/total-number-of-emigrants.csv')
    _df_emig.columns = [str(c).strip() for c in _df_emig.columns]
    print(f'Emigration dataset: {_df_emig.shape}')
except Exception as e:
    print(f'Emigration load failed: {e}')

try:
    comp_dir = ROOT / 'ourWorldData/completion-rate-of-upper-secondary-education-sdg'
    comp_csv = list(comp_dir.glob('*.csv'))
    if comp_csv:
        _df_comp = smart_read_csv(comp_csv[0])
        _df_comp.columns = [str(c).strip() for c in _df_comp.columns]
        print(f'Completion dataset: {_df_comp.shape}')
except Exception as e:
    print(f'Completion load failed: {e}')

try:
    prod_dir = ROOT / 'ourWorldData/productivity-vs-educational-attainment'
    prod_csv = list(prod_dir.glob('*.csv'))
    if prod_csv:
        _df_prod = smart_read_csv(prod_csv[0])
        _df_prod.columns = [str(c).strip() for c in _df_prod.columns]
        print(f'Productivity dataset: {_df_prod.shape}')
except Exception as e:
    print(f'Productivity load failed: {e}')
"""))

cells.append(code("""\
# ── S4a — GDP per capita volume index (interactive country selection) ──────────
GDP_PEERS = {
    'IT': 'Italy', 'DE': 'Germany', 'FR': 'France', 'ES': 'Spain',
    'EU27_2020': 'EU27 avg', 'GB': 'United Kingdom', 'EL': 'Greece',
    'PL': 'Poland', 'PT': 'Portugal', 'NL': 'Netherlands',
}

def plot_gdp(countries=None):
    if _df_gdp is None:
        print('S4a: GDP dataset not available.'); return
    if countries is None:
        countries = ['Italy', 'Germany', 'France', 'Spain', 'EU27 avg', 'Greece']
    code_to_name = {v: v for v in GDP_PEERS.values()}
    name_to_code = {v: k for k, v in GDP_PEERS.items()}
    # Accept either code or name
    sel_names = set(countries)
    df_p = _df_gdp.copy()
    geo_in = [k for k, v in GDP_PEERS.items() if v in sel_names]
    df_p = df_p[df_p[_GEO_G].isin(geo_in)].copy()
    df_p['Country'] = df_p[_GEO_G].map(GDP_PEERS)
    fig, ax = plt.subplots(figsize=(14, 6))
    for country, grp in df_p.groupby('Country'):
        grp_s = grp.sort_values(_TIM_G)
        style = dict(lw=3.5, color='crimson') if country == 'Italy' else dict(lw=1.5, alpha=0.85)
        ax.plot(grp_s[_TIM_G].astype(str), grp_s[_OBS_G], label=country, **style)
    ax.axhline(100, color='grey', lw=1, ls=':', label='EU27 = 100')
    ax.set_ylabel('Volume index (EU27 = 100)')
    ax.set_title('GDP per capita volume index — Italy vs selected peers', fontweight='bold')
    ax.legend(loc='lower left', fontsize=9)
    plt.xticks(rotation=45)
    savefig('s4_gdp_per_capita.png')

if _WIDGETS and _df_gdp is not None:
    avail = [v for k, v in GDP_PEERS.items() if k in _df_gdp[_GEO_G].values]
    default = [c for c in ['Italy','Germany','France','Spain','EU27 avg','Greece'] if c in avail]
    interact(plot_gdp,
             countries=widgets.SelectMultiple(options=avail, value=default[:6],
                                              description='Countries:',
                                              style={'description_width': 'initial'},
                                              layout=widgets.Layout(height='150px')))
else:
    plot_gdp()
"""))

cells.append(code("""\
# ── S4b — Gini coefficient (interactive country selection) ────────────────────
GINI_PEERS = {
    'ITA': 'Italy', 'DEU': 'Germany', 'FRA': 'France', 'ESP': 'Spain',
    'GBR': 'United Kingdom', 'GRC': 'Greece', 'POL': 'Poland', 'PRT': 'Portugal',
}

def plot_gini(countries=None):
    if _df_gini is None:
        print('S4b: Gini dataset not available.'); return
    if countries is None:
        countries = list(GINI_PEERS.values())[:5]
    geo_in = [k for k, v in GINI_PEERS.items() if v in set(countries)]
    df_p   = _df_gini[_df_gini[_REF_Gi].isin(geo_in)].copy()
    df_p['Country'] = df_p[_REF_Gi].map(GINI_PEERS)
    fig, ax = plt.subplots(figsize=(14, 6))
    for country, grp in df_p.groupby('Country'):
        grp_s = grp.sort_values(_TIM_Gi).dropna(subset=[_OBS_Gi])
        style = dict(lw=3.5, color='crimson') if country == 'Italy' else dict(lw=1.5, alpha=0.85)
        ax.plot(grp_s[_TIM_Gi].astype(str), grp_s[_OBS_Gi], label=country, marker='o', ms=3, **style)
    ax.set_ylabel('Gini coefficient (0 = perfect equality)')
    ax.set_title('Income inequality (Gini) — Italy vs peers', fontweight='bold')
    ax.legend()
    plt.xticks(rotation=45)
    savefig('s4_gini.png')

if _WIDGETS and _df_gini is not None:
    avail_g = [v for k, v in GINI_PEERS.items() if k in _df_gini[_REF_Gi].values]
    default_g = [c for c in ['Italy','Germany','France','Spain','United Kingdom'] if c in avail_g]
    interact(plot_gini,
             countries=widgets.SelectMultiple(options=avail_g, value=default_g,
                                              description='Countries:',
                                              style={'description_width': 'initial'},
                                              layout=widgets.Layout(height='140px')))
else:
    plot_gini()
"""))

cells.append(code("""\
# ── S4c — Productivity vs educational attainment (scatter) ────────────────────
def plot_productivity(highlight=None):
    if _df_prod is None:
        print('S4c: productivity dataset not available.'); return
    ENT_P  = find_col(_df_prod, 'Entity')
    YR_P   = find_col(_df_prod, 'Year')
    EDU_P  = find_col(_df_prod, 'average years', 'educ')
    PROD_P = find_col(_df_prod, 'output per hour', 'productivity')
    if not all([ENT_P, YR_P, EDU_P, PROD_P]):
        print(f'S4c: required columns not found. Columns: {list(_df_prod.columns[:8])}'); return
    _df_prod[EDU_P]  = _df_prod[EDU_P].apply(parse_num)
    _df_prod[PROD_P] = _df_prod[PROD_P].apply(parse_num)
    df_valid = _df_prod.dropna(subset=[EDU_P, PROD_P])
    latest_per = df_valid.groupby(ENT_P)[YR_P].max().reset_index()
    latest_per.columns = [ENT_P, '_yr']
    df_lat = df_valid.merge(latest_per, on=ENT_P)
    df_latest = df_lat[df_lat[YR_P] == df_lat['_yr']].drop(columns=['_yr'])

    if highlight is None:
        highlight = ['Italy', 'United Kingdom', 'Germany', 'France', 'Spain', 'Greece']
    df_focus = df_latest[df_latest[ENT_P].isin(highlight)]

    fig, ax = plt.subplots(figsize=(13, 7))
    ax.scatter(df_latest[EDU_P], df_latest[PROD_P], alpha=0.18, color='lightgray', s=28)
    for _, row in df_focus.iterrows():
        clr = '#d62728' if row[ENT_P] == 'Italy' else '#1f77b4'
        ax.scatter(row[EDU_P], row[PROD_P], s=130, color=clr, zorder=5)
        ax.annotate(row[ENT_P], (row[EDU_P], row[PROD_P]),
                    textcoords='offset points', xytext=(5, 3),
                    fontsize=9, fontweight='bold' if row[ENT_P] == 'Italy' else 'normal')
    ax.set_xlabel('Average years of education (15–64)')
    ax.set_ylabel('Output per hour worked (USD)')
    ax.set_title('Productivity vs educational attainment (latest data per country)', fontweight='bold')
    savefig('s4_productivity_vs_education.png')

if _WIDGETS and _df_prod is not None:
    ENT_P2 = find_col(_df_prod, 'Entity')
    all_countries = sorted(_df_prod[ENT_P2].dropna().unique().tolist()) if ENT_P2 else []
    default_h = [c for c in ['Italy','United Kingdom','Germany','France','Spain','Greece']
                 if c in all_countries]
    interact(plot_productivity,
             highlight=widgets.SelectMultiple(options=all_countries, value=default_h,
                                              description='Highlight:',
                                              style={'description_width': 'initial'},
                                              layout=widgets.Layout(height='160px')))
else:
    plot_productivity()
"""))

cells.append(code("""\
# ── S4d — Brain drain: emigration trend ───────────────────────────────────────
def plot_emigration(country='Italy'):
    if _df_emig is None:
        print('S4d: emigration dataset not available.'); return
    ENT3 = find_col(_df_emig, 'Entity')
    YR3  = find_col(_df_emig, 'Year')
    EMI  = find_col(_df_emig, 'emigrants', 'Total')
    if not all([ENT3, YR3, EMI]):
        print(f'S4d: columns not found. Cols: {list(_df_emig.columns[:6])}'); return
    _df_emig[EMI] = _df_emig[EMI].apply(parse_num)
    df_c = _df_emig[_df_emig[ENT3] == country].sort_values(YR3).dropna(subset=[EMI])
    if df_c.empty:
        print(f'S4d: no emigration data for {country}'); return
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(df_c[YR3], df_c[EMI], marker='o', ms=4, color='darkorange', lw=2)
    ax.fill_between(df_c[YR3], df_c[EMI], alpha=0.15, color='darkorange')
    ax.set_ylabel('Total emigrants')
    ax.set_title(f'Total number of emigrants — {country}', fontweight='bold')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1e6:.1f}M'))
    savefig('s4_emigration.png')

if _WIDGETS and _df_emig is not None:
    ENT_e = find_col(_df_emig, 'Entity')
    ctrs_e = sorted(_df_emig[ENT_e].dropna().unique().tolist()) if ENT_e else ['Italy']
    default_e = 'Italy' if 'Italy' in ctrs_e else ctrs_e[0]
    interact(plot_emigration,
             country=widgets.Dropdown(options=ctrs_e, value=default_e,
                                      description='Country:',
                                      style={'description_width': 'initial'}))
else:
    plot_emigration()
"""))

# ── Section 5: Textbook Market ───────────────────────────────────────────────
cells.append(md("""\
---
## Section 5 — Textbook Market & Cost Burden

Italy's mandatory textbook system creates a significant financial burden on families —  
especially for lower-income households.

- **S5a** Mean textbook expenses by school level  
- **S5b** Top publishers by book count (market concentration)  
- **S5c** Mandatory vs optional split  
- **S5d** Regional distribution by curriculum type  

Use the **region dropdown** to compare local patterns.
"""))

cells.append(code("""\
# ── Load textbook data ────────────────────────────────────────────────────────
_df_libri = None
_df_prim_exp = _df_sec_exp = None

try:
    libri_dir = ROOT / 'MinIstruzione/LibriDiTesto'
    parts = []
    for csv_f in sorted(libri_dir.glob('*.csv')):
        try:
            df_part = smart_read_csv(csv_f)
            parts.append(df_part)
        except Exception:
            pass
    if parts:
        _df_libri = pd.concat(parts, ignore_index=True)
        _df_libri.columns = [str(c).strip() for c in _df_libri.columns]
        print(f'Textbook dataset: {_df_libri.shape}')
except Exception as e:
    print(f'Textbook load failed: {e}')

try:
    _df_prim_exp = smart_read_csv(ROOT / 'ItalyPrimarySchoolBookExpenses.csv')
    _df_prim_exp.columns = [str(c).strip() for c in _df_prim_exp.columns]
    print(f'Primary expenses: {_df_prim_exp.shape}')
except Exception as e:
    print(f'Primary expenses load failed: {e}')

try:
    _df_sec_exp = smart_read_csv(ROOT / 'ItalianMeanSecondarySchoolExpenses.csv')
    _df_sec_exp.columns = [str(c).strip() for c in _df_sec_exp.columns]
    print(f'Secondary expenses: {_df_sec_exp.shape}')
except Exception as e:
    print(f'Secondary expenses load failed: {e}')
"""))

cells.append(code("""\
# ── S5a — Average expenses by school level ────────────────────────────────────
try:
    if _df_prim_exp is not None or _df_sec_exp is not None:
        exp_data = {}
        if _df_prim_exp is not None:
            val_col = next((c for c in _df_prim_exp.columns
                            if any(k in c.upper() for k in ['SPESA','COST','EUR','TOTAL','MEAN','AVG'])), None)
            if val_col:
                _df_prim_exp[val_col] = _df_prim_exp[val_col].apply(parse_num)
                exp_data['Primary'] = _df_prim_exp[val_col].mean()
        if _df_sec_exp is not None:
            val_col2 = next((c for c in _df_sec_exp.columns
                             if any(k in c.upper() for k in ['SPESA','COST','EUR','TOTAL','MEAN','AVG'])), None)
            if val_col2:
                _df_sec_exp[val_col2] = _df_sec_exp[val_col2].apply(parse_num)
                exp_data['Secondary'] = _df_sec_exp[val_col2].mean()
        if exp_data:
            fig, ax = plt.subplots(figsize=(7, 5))
            bars = ax.bar(list(exp_data.keys()), list(exp_data.values()),
                          color=['#1f77b4', '#ff7f0e'])
            ax.bar_label(bars, fmt='€%.0f', padding=3)
            ax.set_ylabel('Mean expenditure (€)')
            ax.set_title('Average textbook expenditure by school level', fontweight='bold')
            savefig('s5_expenses_by_level.png')
        else:
            print('S5a: expense value column not found')
    else:
        print('S5a: expense datasets not available')
except Exception as e:
    print(f'S5a skipped: {e}')
"""))

cells.append(code("""\
# ── S5b — Publisher market concentration (interactive region) ─────────────────
def plot_publishers(region='All', top_n=15):
    if _df_libri is None:
        print('S5b: textbook dataset not available.'); return
    PUB  = find_col(_df_libri, 'EDITORE', 'PUBLISHER', 'CASA')
    REG_L = find_col(_df_libri, 'REGIONE', 'REGION')
    if not PUB:
        print(f'S5b: publisher column not found. Cols: {list(_df_libri.columns[:8])}'); return
    df = _df_libri.copy()
    if region != 'All' and REG_L and region in df[REG_L].values:
        df = df[df[REG_L] == region]
    by_pub = df[PUB].value_counts().head(top_n)
    if by_pub.empty:
        print(f'S5b: no publisher data for region={region}'); return
    fig, ax = plt.subplots(figsize=(12, max(4, top_n * 0.45)))
    ax.barh(by_pub.index[::-1], by_pub.values[::-1], color='steelblue')
    ax.set_xlabel('Number of adopted titles')
    title_sfx = f' — {region}' if region != 'All' else ''
    ax.set_title(f'Top {top_n} publishers by adopted book count{title_sfx}', fontweight='bold')
    savefig('s5_publisher_concentration.png')

if _WIDGETS and _df_libri is not None:
    REG_L2 = find_col(_df_libri, 'REGIONE', 'REGION')
    regs_l = ['All'] + (sorted(_df_libri[REG_L2].dropna().unique().tolist()) if REG_L2 else [])
    interact(plot_publishers,
             region=widgets.Dropdown(options=regs_l, value='All',
                                     description='Region:',
                                     style={'description_width': 'initial'}),
             top_n=widgets.IntSlider(min=5, max=30, step=1, value=15,
                                     description='Top N publishers:',
                                     style={'description_width': 'initial'}))
else:
    plot_publishers()
"""))

cells.append(code("""\
# ── S5c — Mandatory vs optional split ────────────────────────────────────────
def plot_mandatory_split(region='All'):
    if _df_libri is None:
        print('S5c: textbook dataset not available.'); return
    OBBLIG = find_col(_df_libri, 'OBBLIGATORIO', 'MANDATORY', 'OBB')
    REG_L3 = find_col(_df_libri, 'REGIONE', 'REGION')
    if not OBBLIG:
        print(f'S5c: mandatory column not found.'); return
    df = _df_libri.copy()
    if region != 'All' and REG_L3 and region in df[REG_L3].values:
        df = df[df[REG_L3] == region]
    counts = df[OBBLIG].value_counts()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(counts.values, labels=counts.index, autopct='%1.1f%%',
           colors=['#d62728', '#2ca02c', '#1f77b4'], startangle=90)
    title_sfx = f' — {region}' if region != 'All' else ''
    ax.set_title(f'Mandatory vs optional textbooks{title_sfx}', fontweight='bold')
    savefig('s5_mandatory_split.png')

if _WIDGETS and _df_libri is not None:
    OBBLIG2 = find_col(_df_libri, 'OBBLIGATORIO', 'MANDATORY', 'OBB')
    if OBBLIG2:
        REG_L4 = find_col(_df_libri, 'REGIONE', 'REGION')
        regs_m = ['All'] + (sorted(_df_libri[REG_L4].dropna().unique().tolist()) if REG_L4 else [])
        interact(plot_mandatory_split,
                 region=widgets.Dropdown(options=regs_m, value='All',
                                         description='Region:',
                                         style={'description_width': 'initial'}))
    else:
        plot_mandatory_split()
else:
    plot_mandatory_split()
"""))

# ── Section 6: Cross-Dimensional Synthesis ───────────────────────────────────
cells.append(md("""\
---
## Section 6 — Cross-Dimensional Synthesis

This section links all the data sources together:  
- NEET rates × GDP per capita (regional)  
- NEET rates × Liceo density (school track)  
- Education spending × NEET outcome  

> These correlations help identify which structural factors most strongly predict NEET risk.
"""))

cells.append(code("""\
# ── S6a — NEET vs GDP per capita scatter (by EU country) ─────────────────────
try:
    # NEET rate: Eurostat NEET data (if available)
    neet_eu_path = next(
        (p for p in sorted(ROOT.rglob('*.csv'))
         if 'edat_lfse' in p.name.lower() or 'neet' in str(p).lower()
         and 'eurostat' in str(p).lower()), None)
    gdp_eu_path  = ROOT / 'oecd/eurostat_gdp_per_capita.csv'

    if neet_eu_path and _df_gdp is not None:
        df_neet_eu = smart_read_csv(neet_eu_path)
        df_neet_eu.columns = [str(c).strip() for c in df_neet_eu.columns]
        _OBS_N  = find_col(df_neet_eu, 'OBS_VALUE')
        _GEO_N  = find_col(df_neet_eu, 'geo', 'GEO')
        _TIM_N  = find_col(df_neet_eu, 'TIME_PERIOD', 'TIME')
        if _OBS_N and _GEO_N and _TIM_N:
            df_neet_eu[_OBS_N] = df_neet_eu[_OBS_N].apply(parse_num)
            lat_n = df_neet_eu[_TIM_N].astype(str).max()
            neet_lat = (df_neet_eu[df_neet_eu[_TIM_N].astype(str) == lat_n]
                        .groupby(_GEO_N)[_OBS_N].mean().dropna())

            lat_g = _df_gdp[_TIM_G].astype(str).max()
            gdp_lat = (_df_gdp[_df_gdp[_TIM_G].astype(str) == lat_g]
                       .groupby(_GEO_G)[_OBS_G].mean().dropna())

            combined = pd.DataFrame({'NEET': neet_lat, 'GDP_idx': gdp_lat}).dropna()
            fig, ax = plt.subplots(figsize=(12, 7))
            ax.scatter(combined['GDP_idx'], combined['NEET'], alpha=0.6, s=60, color='steelblue')
            for geo, row in combined.iterrows():
                clr = 'crimson' if geo == 'IT' else 'black'
                fw  = 'bold' if geo == 'IT' else 'normal'
                ax.annotate(geo, (row['GDP_idx'], row['NEET']),
                            textcoords='offset points', xytext=(4, 3),
                            fontsize=8, color=clr, fontweight=fw)
            ax.set_xlabel('GDP per capita volume index (EU27 = 100)')
            ax.set_ylabel('NEET rate (%)')
            ax.set_title(f'NEET rate vs GDP per capita — EU countries ({lat_n})',
                         fontweight='bold')
            # Regression line
            from numpy.polynomial.polynomial import polyfit
            x, y = combined['GDP_idx'].values, combined['NEET'].values
            mask = np.isfinite(x) & np.isfinite(y)
            if mask.sum() > 2:
                b, m = polyfit(x[mask], y[mask], 1)
                xs = np.linspace(x[mask].min(), x[mask].max(), 100)
                ax.plot(xs, b + m * xs, 'r--', lw=1.5, alpha=0.7, label='Trend')
                ax.legend()
            savefig('s6_neet_vs_gdp_scatter.png')
            print(f'S6a: {len(combined)} EU countries | year={lat_n}')
        else:
            print(f'S6a: column detection failed in NEET Eurostat file')
    else:
        print('S6a: Eurostat NEET EU file or GDP file not found — skipped')
except Exception as e:
    print(f'S6a skipped: {e}')
"""))

cells.append(code("""\
# ── S6b — NEET vs Liceo density (regional correlation) ───────────────────────
try:
    if _neet_reg is not None and _df_scuole is not None:
        # Regional NEET (latest annual)
        df_ann_r = (_neet_reg[_neet_reg[_FREQ_R] == 'A'].copy()
                    if _FREQ_R else _neet_reg.copy())
        if _AGE_R and 'Y15-29' in df_ann_r[_AGE_R].values:
            df_ann_r = df_ann_r[df_ann_r[_AGE_R] == 'Y15-29']
        lat_rn = df_ann_r[_TIME_R].astype(str).max()
        neet_by_reg = (df_ann_r[df_ann_r[_TIME_R].astype(str) == lat_rn]
                       .groupby(_GEO_R)[_OBS_R].mean().dropna())
        neet_by_reg = neet_by_reg[
            ~neet_by_reg.index.str.upper().str.contains(EXCL, regex=True)]

        # Liceo ratio by region
        df_sec2 = _df_scuole[_df_scuole['TRACK'].isin(SECONDARY)].copy()
        sbr2    = df_sec2.groupby([REG_S, 'TRACK'])[COD_S].count().unstack('TRACK').fillna(0)
        sbr2['ratio'] = (
            sbr2.get('Liceo (Academic)', pd.Series(0, index=sbr2.index)) /
            sbr2.get('Istituto Professionale', pd.Series(1, index=sbr2.index)).replace(0, 1))
        liceo_ratio = sbr2['ratio']

        # Align by region name (fuzzy: strip & upper)
        neet_idx = neet_by_reg.index.str.strip().str.upper()
        lic_idx  = liceo_ratio.index.str.strip().str.upper()
        common   = set(neet_idx) & set(lic_idx)
        if len(common) >= 5:
            neet_vals  = [neet_by_reg[neet_by_reg.index.str.strip().str.upper() == r].iloc[0]
                          for r in sorted(common)]
            lic_vals   = [liceo_ratio[liceo_ratio.index.str.strip().str.upper() == r].iloc[0]
                          for r in sorted(common)]
            labels_reg = sorted(common)
            fig, ax = plt.subplots(figsize=(11, 7))
            ax.scatter(lic_vals, neet_vals, s=90, color='steelblue', zorder=5)
            for lab, lv, nv in zip(labels_reg, lic_vals, neet_vals):
                ax.annotate(lab.title(), (lv, nv), textcoords='offset points',
                            xytext=(4, 3), fontsize=8)
            ax.set_xlabel('Liceo-to-Professionale ratio (higher = more academic schools)')
            ax.set_ylabel('NEET count (thousands)')
            ax.set_title('Regional NEET count vs Liceo density', fontweight='bold')
            from numpy.polynomial.polynomial import polyfit as pfn
            xv, yv = np.array(lic_vals), np.array(neet_vals)
            m_ok = np.isfinite(xv) & np.isfinite(yv)
            if m_ok.sum() > 2:
                b2, m2 = pfn(xv[m_ok], yv[m_ok], 1)
                xs2 = np.linspace(xv[m_ok].min(), xv[m_ok].max(), 80)
                ax.plot(xs2, b2 + m2 * xs2, 'r--', lw=1.5, alpha=0.7, label='Trend')
                ax.legend()
            savefig('s6_neet_vs_liceo_density.png')
            print(f'S6b: {len(common)} matched regions')
        else:
            print(f'S6b: only {len(common)} regions matched — scatter skipped')
    else:
        print('S6b: NEET regional or school dataset not available')
except Exception as e:
    print(f'S6b skipped: {e}')
"""))

# ── Section 7: OECD Comparative ─────────────────────────────────────────────
cells.append(md("""\
---
## Section 7 — OECD Comparative: Education Spending & Outcomes

Italy spends less on education (as % of GDP) than most OECD peers.  
This section uses OECD Education at a Glance data to show:
- Per-student spending vs outcomes
- Funding sources (public vs private)
- Education attainment by migrant background

Use the **level selector** (primary / secondary / tertiary) to drill in.
"""))

cells.append(code("""\
# ── Load OECD education finance data ─────────────────────────────────────────
_df_oecd_gdp  = None
_df_oecd_pstu = None
_df_oecd_fund = None
_df_oecd_att  = None

def _try_oecd(path, label):
    try:
        df = smart_read_csv(ROOT / path)
        df.columns = [str(c).strip() for c in df.columns]
        print(f'{label}: {df.shape}')
        return df
    except Exception as e:
        print(f'{label} failed: {e}')
        return None

_df_oecd_gdp  = _try_oecd('oecd/oecd_education_fin_gdp.csv', 'OECD edu % GDP')
_df_oecd_pstu = _try_oecd('oecd/oecd_education_fin_perstud.csv', 'OECD per-student')
_df_oecd_fund = _try_oecd('oecd/oecd_education_funding_sources.csv', 'OECD funding sources')
_df_oecd_att  = _try_oecd('oecd/oecd_education_attainment_migration.csv', 'OECD attainment migration')
"""))

cells.append(code("""\
# ── S7a — Education spending as % of GDP (interactive level & year) ───────────
def plot_oecd_gdp_spend(level='All', year=None, top_n=25):
    if _df_oecd_gdp is None:
        print('S7a: OECD GDP spending dataset not available.'); return
    GEO_OE  = find_col(_df_oecd_gdp, 'REF_AREA', 'geo', 'LOCATION')
    OBS_OE  = find_col(_df_oecd_gdp, 'OBS_VALUE')
    TIM_OE  = find_col(_df_oecd_gdp, 'TIME_PERIOD', 'TIME', 'obsTime')
    LEV_OE  = find_col(_df_oecd_gdp, 'EDUCATION_LEV', 'ISCED_LEVEL', 'LEVEL')
    if not all([GEO_OE, OBS_OE, TIM_OE]):
        print(f'S7a: column detection failed. Cols: {list(_df_oecd_gdp.columns[:8])}'); return
    _df_oecd_gdp[OBS_OE] = _df_oecd_gdp[OBS_OE].apply(parse_num)
    df = _df_oecd_gdp.copy()
    if LEV_OE and level != 'All' and level in df[LEV_OE].values:
        df = df[df[LEV_OE] == level]
    years_oe = sorted(df[TIM_OE].astype(str).unique())
    if year is None or year not in years_oe:
        year = years_oe[-1]
    df_yr = df[df[TIM_OE].astype(str) == year]
    by_geo = df_yr.groupby(GEO_OE)[OBS_OE].mean().dropna().sort_values(ascending=True).tail(top_n)
    clrs   = ['crimson' if g == 'ITA' else 'steelblue' for g in by_geo.index]
    fig, ax = plt.subplots(figsize=(12, max(5, len(by_geo) * 0.45)))
    ax.barh(by_geo.index, by_geo.values, color=clrs)
    ax.set_xlabel('Education expenditure (% of GDP)')
    ax.set_title(f'Education spending as % of GDP — {year} (level: {level})', fontweight='bold')
    savefig('s7_oecd_edu_gdp.png')

if _WIDGETS and _df_oecd_gdp is not None:
    TIM_OE2 = find_col(_df_oecd_gdp, 'TIME_PERIOD', 'TIME', 'obsTime')
    LEV_OE2 = find_col(_df_oecd_gdp, 'EDUCATION_LEV', 'ISCED_LEVEL', 'LEVEL')
    yrs_oe  = sorted(_df_oecd_gdp[TIM_OE2].astype(str).unique()) if TIM_OE2 else ['latest']
    levs_oe = ['All'] + (sorted(_df_oecd_gdp[LEV_OE2].dropna().unique().tolist())
                         if LEV_OE2 else [])
    interact(plot_oecd_gdp_spend,
             level=widgets.Dropdown(options=levs_oe, value='All',
                                    description='Education level:',
                                    style={'description_width': 'initial'}),
             year=widgets.Dropdown(options=yrs_oe, value=yrs_oe[-1],
                                   description='Year:',
                                   style={'description_width': 'initial'}),
             top_n=widgets.IntSlider(min=5, max=40, step=1, value=25,
                                     description='Top N countries:',
                                     style={'description_width': 'initial'}))
else:
    plot_oecd_gdp_spend()
"""))

cells.append(code("""\
# ── S7b — Per-student expenditure comparison ──────────────────────────────────
def plot_per_student(year=None, top_n=25):
    if _df_oecd_pstu is None:
        print('S7b: per-student dataset not available.'); return
    GEO_PS  = find_col(_df_oecd_pstu, 'REF_AREA', 'geo', 'LOCATION')
    OBS_PS  = find_col(_df_oecd_pstu, 'OBS_VALUE')
    TIM_PS  = find_col(_df_oecd_pstu, 'TIME_PERIOD', 'TIME', 'obsTime')
    if not all([GEO_PS, OBS_PS, TIM_PS]):
        print(f'S7b: column detection failed.'); return
    _df_oecd_pstu[OBS_PS] = _df_oecd_pstu[OBS_PS].apply(parse_num)
    years_ps = sorted(_df_oecd_pstu[TIM_PS].astype(str).unique())
    if year is None or year not in years_ps:
        year = years_ps[-1]
    by_geo_ps = (_df_oecd_pstu[_df_oecd_pstu[TIM_PS].astype(str) == year]
                 .groupby(GEO_PS)[OBS_PS].mean().dropna()
                 .sort_values(ascending=True).tail(top_n))
    clrs_ps = ['crimson' if g == 'ITA' else 'steelblue' for g in by_geo_ps.index]
    fig, ax = plt.subplots(figsize=(12, max(5, len(by_geo_ps) * 0.45)))
    ax.barh(by_geo_ps.index, by_geo_ps.values, color=clrs_ps)
    ax.set_xlabel('Annual expenditure per student (USD PPP)')
    ax.set_title(f'Education expenditure per student — {year}', fontweight='bold')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
    savefig('s7_oecd_per_student.png')

if _WIDGETS and _df_oecd_pstu is not None:
    TIM_PS2 = find_col(_df_oecd_pstu, 'TIME_PERIOD', 'TIME', 'obsTime')
    yrs_ps  = sorted(_df_oecd_pstu[TIM_PS2].astype(str).unique()) if TIM_PS2 else ['latest']
    interact(plot_per_student,
             year=widgets.Dropdown(options=yrs_ps, value=yrs_ps[-1],
                                   description='Year:',
                                   style={'description_width': 'initial'}),
             top_n=widgets.IntSlider(min=5, max=40, step=1, value=25,
                                     description='Top N:',
                                     style={'description_width': 'initial'}))
else:
    plot_per_student()
"""))

# ── Section 8: Policy Synthesis ──────────────────────────────────────────────
cells.append(md("""\
---
## Section 8 — Policy Synthesis & Recommendations

### Key findings

| Finding | Evidence |
|---------|----------|
| Italy's NEET rate is the highest in the EU for the 15–29 age group | ISTAT NEET data |
| NEETs are overwhelmingly concentrated among early school-leavers | S1a — incidence by education |
| Southern regions have both fewer Liceo schools *and* more NEETs | S2b, S6b correlation |
| Italy spends below the EU average on education (% of GDP) | S7a — OECD EAG |
| University dropout remains high (~15–20%) | S3f — MUR dropout data |
| Brain drain (emigration) accelerated post-2008 | S4d — OurWorldData |

### Policy recommendations

| # | Recommendation | Rationale |
|---|---------------|-----------|
| 1 | Expand Istituto Professionale density in Southern provinces | Reduce geographic barriers |
| 2 | Create an adult HE access pathway (no diploma required, merit-based) | Constitutional compliance + NEET re-integration |
| 3 | Raise education spending to ≥ 5% GDP | Close gap with EU peers |
| 4 | Means-test and expand DSU grants (diritto allo studio) | Target support to at-risk groups |
| 5 | Pilot comprehensive lower-secondary reforms | Delay tracking from 14 to 16 |
| 6 | Cap mandatory textbook costs per school level | Reduce family financial burden |

### Constitutional grounding

Italian Constitutional Art. 33–34 establishes *merito* (merit) as the principle governing  
university access. Allowing merit-based entry without a diploma gate is not a radical reform —  
it is a return to constitutional intent.

---
*Notebook generated automatically from local datasets.  
All charts are saved to `neet_outputs/`. Data sources: ISTAT, MUR, MinIstruzione, Eurostat,  
World Bank, OECD, OurWorldData.*
"""))

cells.append(code("""\
# ── Final manifest ────────────────────────────────────────────────────────────
import json as _json
from datetime import datetime

figures = sorted([f.name for f in OUT.glob('s*.png')])
manifest_out = {
    'generated': datetime.now().isoformat(),
    'notebook':  'italy_universal_interactive.ipynb',
    'figures':   figures,
    'sections': [
        'S1: NEET Landscape (education level, region, trend, citizenship)',
        'S2: Tripartite school system (track density by area and region)',
        'S3: Higher-education pipeline (matric, dropout, graduation)',
        'S4: Economic context (GDP, Gini, productivity, brain drain)',
        'S5: Textbook market (cost burden, publishers, mandatory split)',
        'S6: Cross-dimensional synthesis (NEET vs GDP, NEET vs Liceo density)',
        'S7: OECD comparative (education spending, per-student, attainment)',
        'S8: Policy synthesis and recommendations',
    ],
}
(OUT / 'universal_manifest.json').write_text(
    _json.dumps(manifest_out, indent=2, ensure_ascii=False))
print(f"Universal notebook complete — {len(figures)} figures saved to {OUT.resolve()}")
print(_json.dumps(manifest_out, indent=2, ensure_ascii=False))
"""))

# ── Write notebook ────────────────────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0",
        },
    },
    "cells": cells,
}

out_path = Path(__file__).parent.parent / "Notebooks" / "italy_universal_interactive.ipynb"
out_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"Created: {out_path}  ({out_path.stat().st_size:,} bytes, {len(cells)} cells)")
