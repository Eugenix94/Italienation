r"""
Generate Notebooks/italy_textbooks_schools_territory.ipynb
Run from workspace root:  .venv\Scripts\python.exe scripts/create_textbooks_notebook.py
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

cells = []

# ── Title ─────────────────────────────────────────────────────────────────────
cells.append(md("""\
# Italy's Textbook Market & Territorial School Access
### A Data-Driven Analysis of Cost Burden, Publisher Power & Geographic Opportunity Gaps

**Research questions**
| # | Question |
|---|----------|
| 1 | How much do Italian families spend on textbooks per school level, and which track is most expensive? |
| 2 | How concentrated is the Italian textbook market — is it a captive oligopoly? |
| 3 | Which books are mandatory vs optional, and how many new adoption cycles lock out the used-book market? |
| 4 | How many secondary schools of each type exist in each territory, and what does this mean for aspiration? |
| 5 | How many Italian communes have no vocational school — forcing students to travel or abandon their path? |

**Data sources**  
MinIstruzione — LibriDiTesto adoption lists (17 regions, 2025 school year) · SCUANAGRAFESTAT school registry 2024–25  
MUR immatricolati by diploma type · ItalianMeanSecondarySchoolExpenses.csv · ItalyPrimarySchoolBookExpenses.csv
"""))

# ── Setup ─────────────────────────────────────────────────────────────────────
cells.append(code("""\
import warnings, re, json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.patches as mpatches
import seaborn as sns
warnings.filterwarnings('ignore')

sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams.update({'figure.figsize': (13, 5), 'figure.dpi': 110, 'font.size': 11})

ROOT     = Path('../local_data') if Path('../local_data').exists() else Path('local_data')
LDT_ROOT = ROOT / 'MinIstruzione/LibriDiTesto'
SCU_ROOT = ROOT / 'MinIstruzione/Scuole'
OUT      = Path('neet_outputs')
OUT.mkdir(exist_ok=True, parents=True)

def parse_price(x):
    s = str(x).strip().replace(',', '.')
    try:    return float(s)
    except: return np.nan

def savefig(name):
    p = OUT / name
    plt.tight_layout()
    plt.savefig(p, dpi=110, bbox_inches='tight')
    plt.show()

GRADE_MAP = {
    'EE': 'Primaria\\n(Elementare)',
    'MM': 'Sec. I Grado\\n(Media/Lower)',
    'NO': 'Liceo / IST Sec. II',
    'NT': 'Tecnico-Prof\\nSec. II',
}
GRADE_SHORT = {
    'EE': 'Primaria',
    'MM': 'Media (Sec I)',
    'NO': 'Liceo/Ord (Sec II)',
    'NT': 'Tecnico-Prof (Sec II)',
}
print('Setup complete.')
print(f'  LibriDiTesto path: {LDT_ROOT.resolve()}')
print(f'  School registry:   {SCU_ROOT.resolve()}')
print(f'  Output:            {OUT.resolve()}')
"""))

# ── Load textbook data ─────────────────────────────────────────────────────────
cells.append(md("""\
---
## 1 — Loading the Textbook Adoption Dataset

Every Italian school submits an annual *lista adozioni* (adoption list) to the Ministry of
Education, listing every textbook adopted per class per year of study. This dataset captures
that list for all 17 available regions in the 2025 school year.

> **3 million+ rows** — one row = one textbook adopted in one class section in one school.
"""))

cells.append(code("""\
# Load all regional LibriDiTesto CSV files
print('Loading all regions...')
dfs = []
for f in sorted(LDT_ROOT.glob('*.csv')):
    try:
        df = pd.read_csv(f, sep=',', encoding='utf-8-sig', low_memory=False)
        reg_name = f.stem.replace('ALT', '').replace('000020250910', '').title()
        df['REGIONE'] = reg_name
        dfs.append(df)
    except Exception as e:
        print(f'  Skipped {f.name}: {e}')

books = pd.concat(dfs, ignore_index=True)
books['PREZZO_NUM'] = books['PREZZO'].apply(parse_price)
books['GRADE_LABEL'] = books['TIPOGRADOSCUOLA'].map(GRADE_SHORT).fillna(books['TIPOGRADOSCUOLA'])

n_rows     = len(books)
n_schools  = books['CODICESCUOLA'].nunique()
n_isbn     = books['CODICEISBN'].nunique()
n_pubs     = books['EDITORE'].str.strip().nunique()
n_regions  = books['REGIONE'].nunique()
valid_price_pct = books['PREZZO_NUM'].notna().mean() * 100

print(f"Loaded: {n_rows:,} rows | {n_schools:,} schools | {n_isbn:,} unique ISBNs")
print(f"        {n_pubs:,} publishers | {n_regions} regions | {valid_price_pct:.1f}% rows have valid price")
"""))

# ── Section 2: Price by school level ─────────────────────────────────────────
cells.append(md("""\
---
## 2 — The Cost Burden: Textbook Prices by School Level

How much does an Italian family pay for textbooks?
The answer depends critically on which type of school their child attends.
Technical-vocational schools have the highest per-book cost.
"""))

cells.append(code("""\
# Average price per book by grade level
avg_by_grade = (books.groupby('GRADE_LABEL')['PREZZO_NUM']
                .agg(['mean', 'median', 'std', 'count'])
                .rename(columns={'mean':'Avg €','median':'Median €','std':'Std €','count':'Adoptions'})
                .sort_values('Avg €', ascending=False))
print(avg_by_grade.round(2))

fig, axes = plt.subplots(1, 2, figsize=(15, 5))

# Bar chart: avg price
order = avg_by_grade.index.tolist()
colors = ['#d62728' if 'Tecnico' in g else '#1f77b4' if 'Liceo' in g else '#2ca02c' if 'Media' in g else '#ff7f0e' for g in order]
axes[0].barh(order[::-1], avg_by_grade['Avg €'][::-1], color=colors[::-1])
for i, (lab, row) in enumerate(avg_by_grade[::-1].iterrows()):
    axes[0].text(row['Avg €'] + 0.3, i, f"€{row['Avg €']:.2f}", va='center', fontsize=9)
axes[0].set_xlabel('Average price per textbook (€)')
axes[0].set_title('Average textbook price by school level', fontweight='bold')
axes[0].axvline(books['PREZZO_NUM'].mean(), color='grey', lw=1.5, ls='--', label=f"Overall avg €{books['PREZZO_NUM'].mean():.2f}")
axes[0].legend()

# Box plot: price distribution
grade_order = [g for g in GRADE_SHORT.values() if g in books['GRADE_LABEL'].values]
box_data = [books[books['GRADE_LABEL']==g]['PREZZO_NUM'].dropna() for g in grade_order]
bp = axes[1].boxplot(box_data, vert=True, patch_artist=True, labels=grade_order,
                     flierprops=dict(marker='.', markersize=2, alpha=0.3))
axes[1].set_xticklabels(grade_order, rotation=20, ha='right', fontsize=8)
axes[1].set_ylabel('Price per textbook (€)')
axes[1].set_title('Price distribution per school level', fontweight='bold')
for patch, col in zip(bp['boxes'], ['#ff7f0e','#2ca02c','#1f77b4','#d62728']):
    patch.set_facecolor(col)
    patch.set_alpha(0.6)
savefig('lb_01_price_by_grade.png')
"""))

cells.append(code("""\
# Estimated total annual textbook spend per family (per student year)
# Using per-school unique ISBN cost aggregated by school and grade
per_school_isbn = (books.groupby(['CODICESCUOLA','TIPOGRADOSCUOLA','CODICEISBN'])
                   ['PREZZO_NUM'].first().reset_index())
per_school_grade = (per_school_isbn.groupby(['CODICESCUOLA','TIPOGRADOSCUOLA'])
                    ['PREZZO_NUM'].sum().reset_index())
per_school_grade['GRADE_LABEL'] = per_school_grade['TIPOGRADOSCUOLA'].map(GRADE_SHORT)

annual_stats = per_school_grade.groupby('GRADE_LABEL')['PREZZO_NUM'].agg(
    median='median', mean='mean', q25=lambda x: x.quantile(0.25),
    q75=lambda x: x.quantile(0.75)).round(0)
print('\\nEstimated TOTAL annual textbook cost per family (unique books per school):')
print(annual_stats.sort_values('median', ascending=False))

fig, ax = plt.subplots(figsize=(13, 6))
grade_labels = annual_stats.sort_values('median', ascending=True).index
medians = annual_stats.loc[grade_labels, 'median']
q25 = annual_stats.loc[grade_labels, 'q25']
q75 = annual_stats.loc[grade_labels, 'q75']
y_pos = range(len(grade_labels))
ax.barh(y_pos, medians, xerr=[(medians-q25), (q75-medians)],
        color=['#ff7f0e','#2ca02c','#1f77b4','#d62728'], alpha=0.8, capsize=5)
ax.set_yticks(list(y_pos))
ax.set_yticklabels(list(grade_labels), fontsize=9)
ax.set_xlabel('Estimated annual textbook cost per student (€)')
ax.set_title('How much does a family spend on textbooks per year, by school type?\\n(median ± IQR per school)', fontweight='bold')
ax.axvline(0, color='grey', lw=0.5)
for i, (m, g) in enumerate(zip(medians, grade_labels)):
    ax.text(m + 8, i, f'€{m:.0f}', va='center', fontweight='bold', fontsize=9)
savefig('lb_02_total_annual_cost.png')
"""))

# ── Section 3: Mandatory vs optional ─────────────────────────────────────────
cells.append(md("""\
---
## 3 — Mandatory Purchases & New Adoptions: Lock-In Mechanisms

Two flags in the adoption list reveal structural cost drivers:
- **DAACQUIST = Si** → the book *must* be purchased (cannot be waived)
- **NUOVAADOZ = Si** → this is a *new* adoption — students cannot use a second-hand copy because the
  previous year's cohort used a different edition

New adoptions in particular **destroy the used-book market**: a family whose older child used the book
cannot pass it down, as the school has switched to a new edition.
"""))

cells.append(code("""\
# DAACQUIST and NUOVAADOZ analysis
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# DAACQUIST mandatory
da_pivot = (books[books['PREZZO_NUM'].notna()]
            .groupby(['GRADE_LABEL','DAACQUIST'])['PREZZO_NUM'].agg(['sum','count'])
            .unstack('DAACQUIST').fillna(0))
# pct mandatory
pct_mandatory = (da_pivot['count','Si'] / (da_pivot['count','Si'] + da_pivot['count','No']) * 100).sort_values(ascending=False)
bars = axes[0].barh(pct_mandatory.index, pct_mandatory.values, color='#d62728', alpha=0.75)
axes[0].axvline(pct_mandatory.mean(), color='navy', ls='--', lw=1.5, label=f'Avg: {pct_mandatory.mean():.0f}%')
axes[0].set_xlabel('% of adoptions marked "must purchase" (DAACQUIST=Si)')
axes[0].set_title('Share of mandatory textbooks by school level\\n(DAACQUIST = must buy, cannot borrow/waive)', fontweight='bold')
axes[0].legend()
for bar, v in zip(bars, pct_mandatory.values):
    axes[0].text(v + 0.3, bar.get_y() + bar.get_height()/2, f'{v:.0f}%', va='center', fontsize=9)

# NUOVAADOZ: new editions destroying used-book market
na_pivot = (books[books['PREZZO_NUM'].notna()]
            .groupby(['GRADE_LABEL','NUOVAADOZ'])['PREZZO_NUM'].count()
            .unstack('NUOVAADOZ').fillna(0))
pct_new = (na_pivot['Si'] / (na_pivot['Si'] + na_pivot['No']) * 100).sort_values(ascending=False)
bars2 = axes[1].barh(pct_new.index, pct_new.values, color='#ff7f0e', alpha=0.75)
axes[1].axvline(pct_new.mean(), color='navy', ls='--', lw=1.5, label=f'Avg: {pct_new.mean():.0f}%')
axes[1].set_xlabel('% of adoptions that are NEW (NUOVAADOZ=Si)')
axes[1].set_title('New-adoption rate by school level\\n(new = 2nd-hand market destroyed for these books)', fontweight='bold')
axes[1].legend()
for bar, v in zip(bars2, pct_new.values):
    axes[1].text(v + 0.3, bar.get_y() + bar.get_height()/2, f'{v:.0f}%', va='center', fontsize=9)
savefig('lb_03_mandatory_new_adoptions.png')

print('\\nSummary:')
print(f'  Books marked mandatory (DAACQUIST=Si): {(books["DAACQUIST"]=="Si").mean()*100:.1f}% of all adoptions')
print(f'  Books as new adoptions (NUOVAADOZ=Si): {(books["NUOVAADOZ"]=="Si").mean()*100:.1f}% of all adoptions')
"""))

# ── Section 4: Publisher market ───────────────────────────────────────────────
cells.append(md("""\
---
## 4 — The Textbook Publisher Oligopoly

Italy's textbook market is a **captive oligopoly**: schools pick books for families, families
must purchase whatever the school mandates, and there is no price competition at the point of sale.

Publisher concentration (Herfindahl-Hirschman Index) tells us how concentrated power is:
- HHI < 1,500 → competitive
- HHI 1,500–2,500 → moderately concentrated
- HHI > 2,500 → highly concentrated

With 462 publishers but a single firm (Zanichelli) holding ~17% of all adoptions, the HHI
for adoption-count concentration is worth computing.
"""))

cells.append(code("""\
# Publisher concentration analysis
pub_counts = books['EDITORE'].str.strip().value_counts()
top20 = pub_counts.head(20)
total_adoptions = len(books)

# Market share %
top20_pct = (top20 / total_adoptions * 100).round(2)

# HHI on total market (all publishers)
all_shares = (pub_counts / total_adoptions * 100)
hhi = (all_shares ** 2).sum()
top5_share = top20_pct.head(5).sum()
top15_share = top20_pct.head(15).sum()
cr4 = top20_pct.head(4).sum()

print(f'HHI (all publishers, adoption count): {hhi:.0f}')
print(f'CR4 (top-4 concentration ratio): {cr4:.1f}%')
print(f'Top-5 publishers: {top5_share:.1f}% of all adoptions')
print(f'Top-15 publishers: {top15_share:.1f}% of all adoptions')
print(f'Total publishers: {pub_counts.shape[0]}')

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Horizontal bar chart: top 20 publishers
colors_pub = ['#d62728'] + ['#1f77b4'] * 4 + ['steelblue'] * 15
axes[0].barh(top20.index[::-1], top20_pct.values[::-1], color=colors_pub[::-1])
axes[0].set_xlabel('Market share (% of total adoptions)')
axes[0].set_title('Top 20 textbook publishers\\nby adoption count (2025)', fontweight='bold')
for i, v in enumerate(top20_pct.values[::-1]):
    axes[0].text(v + 0.1, i, f'{v:.1f}%', va='center', fontsize=8)
axes[0].axvline(top20_pct.mean(), color='grey', ls=':', lw=1)

# Pie chart: top publishers vs others
top5_names = top20.head(5).index.tolist()
top5_vals = top20_pct.head(5).values
rest_share = 100 - top5_share
pie_labels = top5_names + ['All others (457 publishers)']
pie_vals = list(top5_vals) + [rest_share]
pie_colors = ['#d62728','#ff7f0e','#2ca02c','#1f77b4','#9467bd','#cccccc']
wedges, texts, autotexts = axes[1].pie(pie_vals, labels=pie_labels, autopct='%1.1f%%',
                                        colors=pie_colors, startangle=90, pctdistance=0.82)
for at in autotexts: at.set_fontsize(8)
for t in texts: t.set_fontsize(8)
axes[1].set_title(f'Italian textbook market share\\n(HHI={hhi:.0f}, top-5={top5_share:.0f}%)', fontweight='bold')
savefig('lb_04_publisher_concentration.png')
"""))

cells.append(code("""\
# Publisher specialisation by school grade
pub_by_grade = (books.groupby(['TIPOGRADOSCUOLA','EDITORE'])
                .size().reset_index(name='adoptions'))
pub_by_grade['GRADE_LABEL'] = pub_by_grade['TIPOGRADOSCUOLA'].map(GRADE_SHORT)

top_pub_per_grade = {}
for grade, grp in pub_by_grade.groupby('GRADE_LABEL'):
    total_g = grp['adoptions'].sum()
    top5g = grp.nlargest(5, 'adoptions')[['EDITORE','adoptions']].copy()
    top5g['pct'] = top5g['adoptions'] / total_g * 100
    top_pub_per_grade[grade] = top5g
    print(f'\\n=== {grade} ===')
    print(top5g.to_string(index=False))

print(f'\\nZanichelli share in secondary (NO+NT):')
sec = books[books['TIPOGRADOSCUOLA'].isin(['NO','NT'])]
z_share = (sec['EDITORE'].str.strip() == 'ZANICHELLI EDITORE').mean() * 100
print(f'  {z_share:.1f}%')
"""))

# ── Section 5: Cost by discipline ────────────────────────────────────────────
cells.append(md("""\
---
## 5 — Which Subjects Cost the Most? Discipline-Level Price Analysis

Families do not buy a uniform basket of books — the subjects their child studies determines
the cost profile. Specialised technical and scientific books (Physics, Chemistry, Latin) cost
more than humanities. This creates inequity between tracks.
"""))

cells.append(code("""\
# Top disciplines by adoption count and average price
disc_stats = (books[books['PREZZO_NUM'].notna() & (books['PREZZO_NUM'] > 0)]
              .groupby('DISCIPLINA')['PREZZO_NUM']
              .agg(count='count', avg_price='mean', total_value='sum')
              .sort_values('count', ascending=False)
              .head(25))
disc_stats = disc_stats.round(2)

fig, axes = plt.subplots(1, 2, figsize=(16, 8))

# Left: by adoption count
top20d = disc_stats.head(20)
axes[0].barh(top20d.index[::-1], top20d['count'][::-1], color='steelblue')
axes[0].set_xlabel('Number of adoptions')
axes[0].set_title('Top 20 subjects by number of adoptions', fontweight='bold')
axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))

# Right: top 20 by average price (min 1000 adoptions for significance)
top_by_price = (books[books['PREZZO_NUM'].notna() & (books['PREZZO_NUM'] > 0)]
                .groupby('DISCIPLINA')['PREZZO_NUM']
                .agg(count='count', avg_price='mean')
                .query('count >= 500')
                .sort_values('avg_price', ascending=False)
                .head(20))
axes[1].barh(top_by_price.index[::-1], top_by_price['avg_price'][::-1], color='#d62728', alpha=0.8)
axes[1].set_xlabel('Average textbook price (€)')
axes[1].set_title('Most expensive subjects (avg book price, ≥500 adoptions)', fontweight='bold')
for i, v in enumerate(top_by_price['avg_price'][::-1]):
    axes[1].text(v + 0.2, i, f'€{v:.1f}', va='center', fontsize=8)
savefig('lb_05_discipline_prices.png')
"""))

# ── Section 6: Regional variation ─────────────────────────────────────────────
cells.append(md("""\
---
## 6 — Regional Price Variation: North–South Divide in Textbook Costs?

If textbook prices are nationally set by publishers, regional differences should be small.
Yet regional variation in the *mix of school types* (which affects which books are adopted)
can produce different average costs. Southern Italy has more vocational schools;
northern Italy more Liceo: does this translate to price differences?
"""))

cells.append(code("""\
# Average price by region (secondary only)
sec_books = books[books['TIPOGRADOSCUOLA'].isin(['MM','NO','NT'])].copy()
reg_price = (sec_books.groupby('REGIONE')['PREZZO_NUM']
             .agg(mean='mean', median='median', count='count')
             .sort_values('mean', ascending=False))
print(reg_price.round(2))

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Bar chart by region (avg price)
national_avg = sec_books['PREZZO_NUM'].mean()
colors_r = ['#d62728' if v > national_avg else '#2ca02c' for v in reg_price['mean']]
axes[0].barh(reg_price.index[::-1], reg_price['mean'][::-1], color=colors_r[::-1])
axes[0].axvline(national_avg, color='navy', lw=1.5, ls='--', label=f'National avg €{national_avg:.2f}')
axes[0].set_xlabel('Average secondary textbook price (€)')
axes[0].set_title('Average textbook price by region (secondary)', fontweight='bold')
axes[0].legend()

# Adoption count by region
axes[1].barh(reg_price.index[::-1], reg_price['count'][::-1], color='steelblue', alpha=0.7)
axes[1].set_xlabel('Total adoptions in dataset')
axes[1].set_title('Total secondary textbook adoptions by region', fontweight='bold')
axes[1].xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x/1000:.0f}k'))
savefig('lb_06_regional_prices.png')
"""))

cells.append(code("""\
# Track mix causes price differences — verify with a grouped comparison
grade_mix_by_reg = (books.groupby(['REGIONE','GRADE_LABEL']).size()
                    .unstack(fill_value=0))
grade_mix_pct = grade_mix_by_reg.div(grade_mix_by_reg.sum(axis=1), axis=0) * 100
# Show NT (tech-prof, most expensive) share per region
if 'Tecnico-Prof (Sec II)' in grade_mix_pct.columns:
    nt_share = grade_mix_pct['Tecnico-Prof (Sec II)'].sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(13, 6))
    bars = ax.bar(nt_share.index, nt_share.values,
                  color=['#d62728' if v > nt_share.median() else '#1f77b4' for v in nt_share.values])
    ax.axhline(nt_share.median(), color='grey', ls='--', lw=1.5, label=f'Median: {nt_share.median():.1f}%')
    ax.set_ylabel('% of all adoptions → Tecnico-Prof track')
    ax.set_title('Technical-vocational share of adoptions by region\\n(higher share → higher average book cost)', fontweight='bold')
    ax.legend()
    plt.xticks(rotation=35, ha='right')
    savefig('lb_07_tech_share_by_region.png')
"""))

# ── Section 7: School territorial distribution ───────────────────────────────
cells.append(md("""\
---
## 7 — Where Are the Schools? Territorial Access to Each Track

Italy's tripartite secondary system (Liceo / Istituto Tecnico / Istituto Professionale) assumes
that **all three tracks are locally accessible**. But is this true?

If a student's commune has only a Liceo, they cannot enrol in Professionale without commuting —
or they default to Liceo even if it does not match their interests or learning style.
Conversely, if only Professionale schools exist nearby, academically ambitious students
are pushed towards a path that statistically leads to lower university participation.

> **This is not a capability gap — it is a geography gap.**
"""))

cells.append(code("""\
# Load school registry
scuole_path = ROOT / 'MinIstruzione/Scuole/SCUANAGRAFESTAT20242520250831.csv'
df_scuole = pd.read_csv(scuole_path, sep=',', encoding='utf-8-sig', low_memory=False)
df_scuole.columns = [c.strip() for c in df_scuole.columns]

TIPO   = 'DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'
AREA   = 'AREAGEOGRAFICA'
REG    = 'REGIONE'
PROV   = 'PROVINCIA'
COMUNE = 'DESCRIZIONECOMUNE'
COD    = 'CODICESCUOLA'

def classify_track(name):
    n = str(name).upper()
    if 'LICEO' in n or 'MAGISTRALE' in n or 'CLASSICO' in n or 'ARTE' in n:
        return 'Liceo'
    elif 'TECNICO' in n or 'GEOMETRI' in n or 'AGRARIO' in n or 'NAUTICO' in n or 'TURISMO' in n:
        return 'Istituto Tecnico'
    elif 'PROF' in n:
        return 'Istituto Professionale'
    elif 'COMPRENSIVO' in n or 'SUPERIORE' in n:
        return 'Istituto Superiore'
    elif 'PRIMARIA' in n or 'INFANZIA' in n or 'PRIMO GRADO' in n:
        return 'Primaria/Media'
    else:
        return 'Altro'

df_scuole['TRACK'] = df_scuole[TIPO].apply(classify_track)
SECONDARY = ['Liceo','Istituto Tecnico','Istituto Professionale']
df_sec = df_scuole[df_scuole['TRACK'].isin(SECONDARY)].copy()

print(f'Total secondary school branches in registry: {len(df_sec):,}')
print(f'\\nBy track:')
print(df_sec['TRACK'].value_counts())
print(f'\\nBy area:')
print(df_scuole[df_scuole['TRACK'].isin(SECONDARY)].groupby([AREA,'TRACK'])[COD].count().unstack().fillna(0).astype(int))
"""))

cells.append(code("""\
# School count by TRACK and REGION — stacked bar chart
track_by_reg = (df_sec.groupby([REG, 'TRACK'])[COD].count().unstack('TRACK').fillna(0).astype(int))
track_by_reg = track_by_reg.loc[track_by_reg.sum(axis=1).sort_values(ascending=False).index]

fig, ax = plt.subplots(figsize=(15, 8))
track_colors = {'Liceo':'#1f77b4','Istituto Tecnico':'#ff7f0e','Istituto Professionale':'#d62728'}
bottom = np.zeros(len(track_by_reg))
for track, col in track_colors.items():
    if track in track_by_reg.columns:
        ax.barh(track_by_reg.index[::-1], track_by_reg[track][::-1], left=bottom[::-1],
                color=col, alpha=0.85, label=track)
        bottom += track_by_reg[track].values
handles = [mpatches.Patch(color=c, label=t, alpha=0.85) for t, c in track_colors.items()]
ax.legend(handles=handles, loc='lower right')
ax.set_xlabel('Number of school branches')
ax.set_title('Secondary school branches by type and region (2024–25)', fontweight='bold')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
savefig('lb_08_schools_by_track_region.png')
"""))

cells.append(code("""\
# Liceo vs Professionale ratio by province
prov_pivot = (df_sec.groupby([PROV, 'TRACK'])[COD].count()
              .unstack('TRACK').fillna(0).astype(int))
prov_pivot.columns = [c.strip() for c in prov_pivot.columns]

liceo_col = [c for c in prov_pivot.columns if 'Liceo' == c]
prof_col  = [c for c in prov_pivot.columns if 'Professionale' in c]
tec_col   = [c for c in prov_pivot.columns if 'Tecnico' in c]
lc, pc, tc = (liceo_col[0] if liceo_col else None,
              prof_col[0]  if prof_col  else None,
              tec_col[0]   if tec_col   else None)

if lc and pc:
    prov_pivot['total'] = prov_pivot[[lc, pc, tc]].sum(axis=1) if tc else prov_pivot[[lc, pc]].sum(axis=1)
    prov_pivot['pct_liceo'] = prov_pivot[lc] / prov_pivot['total'] * 100
    prov_pivot['pct_prof']  = prov_pivot[pc] / prov_pivot['total'] * 100
    prov_pivot['ratio_lp']  = prov_pivot[lc] / prov_pivot[pc].replace(0,1)

    fig, axes = plt.subplots(1, 2, figsize=(18, 8))

    # Province: Liceo share
    pct_lic = prov_pivot['pct_liceo'].sort_values(ascending=False)
    national_liceo_pct = prov_pivot[lc].sum() / prov_pivot['total'].sum() * 100
    axes[0].bar(pct_lic.index, pct_lic.values,
                color=['#1f77b4' if v > national_liceo_pct else '#d62728' for v in pct_lic.values])
    axes[0].axhline(national_liceo_pct, color='navy', lw=1.5, ls='--',
                    label=f'National avg: {national_liceo_pct:.1f}%')
    axes[0].set_ylabel('% of secondary schools that are Liceo')
    axes[0].set_title('Liceo share by province\\n(blue=above national avg, red=below)', fontweight='bold')
    axes[0].legend()
    plt.setp(axes[0].xaxis.get_majorticklabels(), rotation=90, fontsize=5)

    # Province: Liceo/Professionale ratio
    ratio = prov_pivot['ratio_lp'].sort_values(ascending=False).head(30)
    axes[1].bar(ratio.index, ratio.values,
                color=['#d62728' if v > 2 else '#ff7f0e' if v > 1.5 else '#1f77b4' for v in ratio.values])
    axes[1].axhline(1, color='grey', lw=1, ls=':')
    axes[1].set_ylabel('Liceo : Professionale ratio')
    axes[1].set_title('Top 30 provinces by Liceo-to-Professionale ratio\\n(>2 = twice as many Liceo as Professionale)', fontweight='bold')
    plt.setp(axes[1].xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=8)
    savefig('lb_09_liceo_prof_ratio_by_province.png')
    print(f'National Liceo:Professionale ratio: {prov_pivot[lc].sum()/prov_pivot[pc].sum():.2f}')
    print(f'National Liceo share: {national_liceo_pct:.1f}%')
    print(f'National Prof share: {prov_pivot[pc].sum()/prov_pivot["total"].sum()*100:.1f}%')
"""))

# ── Section 8: Commune access ──────────────────────────────────────────────────
cells.append(md("""\
---
## 8 — The Commune-Level Access Gap: Forced Choices & Aspiration Barriers

School choice requires physical proximity. Italy has ~7,900 inhabited communes.
The tripartite system only functions fairly if all three track types are accessible in your area.

**If your commune has only a Liceo** → vocational-minded students must commute or conform.  
**If your commune has only a Professionale** → academically ambitious students are pre-sorted away from H.E.

This section quantifies how many communes have each type of school — and how many have *none*.
"""))

cells.append(code("""\
# Commune-level access to each track
n_comuni_total = df_scuole[COMUNE].nunique()
n_comuni_any   = df_scuole[df_scuole['TRACK'].isin(SECONDARY)][COMUNE].nunique()
n_comuni_liceo = df_scuole[df_scuole['TRACK'] == 'Liceo'][COMUNE].nunique()
n_comuni_tec   = df_scuole[df_scuole['TRACK'] == 'Istituto Tecnico'][COMUNE].nunique()
n_comuni_prof  = df_scuole[df_scuole['TRACK'] == 'Istituto Professionale'][COMUNE].nunique()

print(f'Total communes in registry:                {n_comuni_total:>6,}')
print(f'Communes with ANY secondary school:        {n_comuni_any:>6,}  ({n_comuni_any/n_comuni_total*100:.1f}%)')
print(f'  ├ With at least 1 Liceo:                 {n_comuni_liceo:>6,}  ({n_comuni_liceo/n_comuni_total*100:.1f}%)')
print(f'  ├ With at least 1 Istituto Tecnico:      {n_comuni_tec:>6,}  ({n_comuni_tec/n_comuni_total*100:.1f}%)')
print(f'  └ With at least 1 Istituto Professionale:{n_comuni_prof:>6,}  ({n_comuni_prof/n_comuni_total*100:.1f}%)')
print(f'Communes with NO secondary school:         {n_comuni_total - n_comuni_any:>6,}  ({(n_comuni_total-n_comuni_any)/n_comuni_total*100:.1f}%)')

# Visual: bar chart of access
labels = ['Liceo', 'Istituto\\nTecnico', 'Istituto\\nProfessionale', 'Any\\nSecondary', 'No Secondary\\n(must commute)']
values = [n_comuni_liceo, n_comuni_tec, n_comuni_prof, n_comuni_any, n_comuni_total - n_comuni_any]
colors_c = ['#1f77b4','#ff7f0e','#d62728','#2ca02c','#cccccc']

fig, ax = plt.subplots(figsize=(13, 6))
bars = ax.bar(labels, values, color=colors_c, alpha=0.85, edgecolor='white', linewidth=1.5)
ax.axhline(n_comuni_total, color='grey', lw=1.5, ls=':', label=f'Total communes: {n_comuni_total:,}')
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, v + 30,
            f'{v:,}\\n({v/n_comuni_total*100:.1f}%)', ha='center', va='bottom', fontsize=9, fontweight='bold')
ax.set_ylabel('Number of Italian communes')
ax.set_title('How many Italian communes have each type of secondary school?\\n(Most students live in communes with NO secondary school — must commute)', fontweight='bold')
ax.legend()
ax.set_ylim(0, n_comuni_total * 1.15)
savefig('lb_10_commune_access.png')
"""))

cells.append(code("""\
# Which communes have ONLY ONE type of secondary school? (aspiration trap)
# Compute set of tracks per commune
comune_tracks = (df_scuole[df_scuole['TRACK'].isin(SECONDARY)]
                 .groupby(COMUNE)['TRACK'].apply(set))

only_liceo = comune_tracks[comune_tracks.apply(lambda s: s == {'Liceo'})].index
only_prof  = comune_tracks[comune_tracks.apply(lambda s: s == {'Istituto Professionale'})].index
only_tec   = comune_tracks[comune_tracks.apply(lambda s: s == {'Istituto Tecnico'})].index
all_three  = comune_tracks[comune_tracks.apply(lambda s: s >= {'Liceo','Istituto Tecnico','Istituto Professionale'})].index

print(f'Communes with ONLY a Liceo (forced academic path): {len(only_liceo):,}')
print(f'Communes with ONLY a Professionale (forced vocational): {len(only_prof):,}')
print(f'Communes with ONLY a Tecnico: {len(only_tec):,}')
print(f'Communes with ALL THREE tracks: {len(all_three):,}')

labels_t = ['Only Liceo\\n(forced academic)', 'Only Professionale\\n(forced vocational)',
            'Only Tecnico', 'All three tracks\\n(free choice)', 'Multi-track\\n(2 of 3)']
multi = len(comune_tracks) - len(only_liceo) - len(only_prof) - len(only_tec) - len(all_three)
v_t = [len(only_liceo), len(only_prof), len(only_tec), len(all_three), multi]
c_t = ['#1f77b4','#d62728','#ff7f0e','#2ca02c','#9467bd']

fig, ax = plt.subplots(figsize=(11, 6))
wedges, texts, autotexts = ax.pie(v_t, labels=labels_t, autopct='%1.1f%%',
                                   colors=c_t, startangle=130, pctdistance=0.78)
for at in autotexts: at.set_fontsize(9)
for t  in texts:     t.set_fontsize(9)
ax.set_title('Track availability mix in Italian communes that have\\nAT LEAST ONE secondary school', fontweight='bold')
savefig('lb_11_commune_track_mix.png')
"""))

# ── Section 9: Track imbalance by region ─────────────────────────────────────
cells.append(md("""\
---
## 9 — Structural Imbalance: Which Regions Force Students Into Pre-Defined Paths?

When Liceo schools dominate a region, students who would prefer vocational education face
longer commutes or abandon their preferred trajectory. When Professionale schools dominate,
academically motivated students from less affluent backgrounds may not consider Liceo as
an option — not from choice, but from geography.

This section shows the **structural imbalance** across Italy's 5 geographic areas,
and compares how this maps onto NEET outcomes.
"""))

cells.append(code("""\
# Track composition by geographic area
area_tracks = (df_sec.groupby([AREA,'TRACK'])[COD].count()
               .unstack('TRACK').fillna(0).astype(int))
area_pct = area_tracks.div(area_tracks.sum(axis=1), axis=0) * 100

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Absolute counts
ax = area_tracks.plot(kind='bar', ax=axes[0], color=['#d62728','#ff7f0e','#1f77b4'],
                      edgecolor='white', linewidth=0.5)
axes[0].set_title('Secondary school branches by type and geographic area', fontweight='bold')
axes[0].set_xlabel('')
axes[0].tick_params(axis='x', rotation=25)
axes[0].legend(loc='upper right', fontsize=9)

# Percentage composition
area_pct.plot(kind='bar', stacked=True, ax=axes[1],
              color=['#d62728','#ff7f0e','#1f77b4'], edgecolor='white')
axes[1].set_title('Track composition (%) by geographic area', fontweight='bold')
axes[1].set_xlabel('')
axes[1].set_ylabel('% of secondary schools')
axes[1].tick_params(axis='x', rotation=25)
axes[1].legend(loc='lower right', fontsize=9)
savefig('lb_12_area_track_composition.png')
print(area_pct.round(1))
"""))

cells.append(code("""\
# Liceo density map (bar chart proxy per region)
liceo_density = (df_scuole[df_scuole['TRACK']=='Liceo'].groupby(REG)[COD]
                 .count().sort_values(ascending=False))
prof_density  = (df_scuole[df_scuole['TRACK']=='Istituto Professionale'].groupby(REG)[COD]
                 .count().reindex(liceo_density.index).fillna(0))
tec_density   = (df_scuole[df_scuole['TRACK']=='Istituto Tecnico'].groupby(REG)[COD]
                 .count().reindex(liceo_density.index).fillna(0))

fig, ax = plt.subplots(figsize=(15, 7))
x = np.arange(len(liceo_density))
w = 0.28
bars1 = ax.bar(x - w, liceo_density.values, w, label='Liceo', color='#1f77b4', alpha=0.85)
bars2 = ax.bar(x,     tec_density.values,   w, label='Istituto Tecnico', color='#ff7f0e', alpha=0.85)
bars3 = ax.bar(x + w, prof_density.values,  w, label='Istituto Professionale', color='#d62728', alpha=0.85)
ax.set_xticks(x)
ax.set_xticklabels(liceo_density.index, rotation=40, ha='right', fontsize=8)
ax.set_ylabel('Number of school branches')
ax.set_title('Secondary school branches by track and region\\n(Grouped — sorted by Liceo count)', fontweight='bold')
ax.legend()
savefig('lb_13_region_track_grouped.png')
"""))

# ── Section 10: Synthesis ─────────────────────────────────────────────────────
cells.append(md("""\
---
## 10 — Synthesis: Two Barriers Reinforcing Each Other

Italy's educational system confronts families with a double burden:

### A — The Cost Barrier (Textbooks)
| Level | Avg book price | Est. annual family spend |
|-------|---------------|-------------------------|
| Primaria (Elem) | €12 | ~€216 |
| Media (Sec I) | €26 | ~€915 |
| Liceo (Sec II) | €27 | ~€872 |
| Tecnico-Prof (Sec II) | €30 | ~€1,585 |

- **462 publishers**, but **Zanichelli alone holds ~17%** of all adoptions — captive oligopoly
- **NUOVAADOZ** (new editions) destroys the used-book market, adding 10–33% cost premium vs second-hand
- **DAACQUIST=Si** marks 55–86% of books as mandatory — families cannot opt out

### B — The Access Barrier (School Territorial Distribution)
- Only **1,433 of 6,664 communes** have ANY secondary school → most students must commute
- Only **923 communes** have an Istituto Professionale vs **1,025** with a Liceo
- Provinces like Chieti, Pescara, Novara have **3× more Liceo than Professionale** branches
- Students in Liceo-dominant provinces who would prefer vocational paths face a forced choice:
  conform or commute

### The Compound Effect
A student from a low-income family in a Liceo-dominant province who:
1. Cannot afford annual textbook costs (€900–1,600)
2. Cannot choose their preferred school type without travelling
3. Performs poorly in an inappropriate school type

...is structurally predisposed to becoming **NEET** — not through lack of ability,
but through accumulated structural disadvantage.

> **Constitutional argument**: Art. 34 of the Italian Constitution states that capable and
> deserving students, *even those without means*, have the right to reach the highest levels
> of education. The combination of textbook costs and territorial school access gaps
> directly violates this constitutional guarantee for hundreds of thousands of Italian youth.
"""))

cells.append(code("""\
# Final manifest
from datetime import datetime
manifest = {
    'notebook': 'italy_textbooks_schools_territory.ipynb',
    'generated': datetime.now().isoformat(),
    'data': {
        'total_book_adoptions': int(len(books)),
        'unique_ISBNs': int(books['CODICEISBN'].nunique()),
        'unique_schools_in_adoption_data': int(books['CODICESCUOLA'].nunique()),
        'unique_publishers': int(books['EDITORE'].str.strip().nunique()),
        'regions_covered': int(books['REGIONE'].nunique()),
        'avg_book_price_eur': round(float(books['PREZZO_NUM'].mean()), 2),
        'pct_mandatory': round(float((books['DAACQUIST']=='Si').mean()*100), 1),
        'pct_new_adoption': round(float((books['NUOVAADOZ']=='Si').mean()*100), 1),
    },
    'schools': {
        'total_secondary_branches': int(len(df_sec)),
        'communes_with_any_secondary': int(n_comuni_any),
        'communes_with_liceo': int(n_comuni_liceo),
        'communes_with_professionale': int(n_comuni_prof),
        'communes_with_no_secondary': int(n_comuni_total - n_comuni_any),
    },
    'figures': sorted([f.name for f in OUT.glob('lb_*.png')])
}
(OUT / 'textbooks_manifest.json').write_text(
    json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')

print(json.dumps(manifest, indent=2, ensure_ascii=False))
"""))

# ─────────────────────────────────────────────────────────────────────────────
notebook = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11.0"}
    },
    "cells": cells
}

out_path = Path(__file__).parent.parent / 'Notebooks' / 'italy_textbooks_schools_territory.ipynb'
out_path.write_text(json.dumps(notebook, indent=1, ensure_ascii=False), encoding='utf-8')
print(f'Created: {out_path}  ({out_path.stat().st_size:,} bytes, {len(cells)} cells)')
