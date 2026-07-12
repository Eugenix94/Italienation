"""
Run NEET & MUR analysis and save outputs (CSV + plots).
Produces files under Notebooks/neet_outputs/
"""
from pathlib import Path
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
import runpy

sns.set(style="whitegrid")

ROOT = Path('local_data')
OUT = Path('Notebooks') / 'neet_outputs'
OUT.mkdir(parents=True, exist_ok=True)

# Helper readers
import csv

def smart_read_csv(path):
    path = str(path)
    # Try common separators with the fast C engine first (handles quoted commas reliably)
    encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1']
    seps = [';', ',', '\t']
    for enc in encodings:
        for sep in seps:
            try:
                df = pd.read_csv(path, sep=sep, engine='c', encoding=enc, low_memory=False)
                if df.shape[1] > 1:
                    return df
            except Exception:
                continue
    # If that fails, try the python engine with automatic sep sniffing
    for enc in encodings:
        try:
            df = pd.read_csv(path, engine='python', encoding=enc, sep=None, low_memory=False)
            if df.shape[1] > 1:
                return df
        except Exception:
            continue
    # Last-resort: decode bytes with replacement and parse
    try:
        with open(path, 'rb') as fh:
            raw = fh.read()
        text = raw.decode('utf-8', errors='replace')
        import io
        return pd.read_csv(io.StringIO(text), sep=None, engine='python')
    except Exception:
        return pd.read_csv(path, engine='python', sep=None, encoding='latin-1', low_memory=False)

import numpy as _np

def parse_numeric(x):
    if x is None:
        return _np.nan
    s = str(x).strip()
    if s in ['', 'N', 'n', '-', 'nan', 'NaN', 'None']:
        return _np.nan
    if re.match(r'^\d{1,3}(?:\.\d{3})+$', s):
        return float(s.replace('.', ''))
    if ',' in s and '.' not in s:
        try:
            return float(s.replace(',', '.'))
        except:
            return _np.nan
    if '.' in s and ',' in s:
        try:
            return float(s.replace('.', '').replace(',', '.'))
        except:
            return _np.nan
    try:
        return float(s)
    except:
        return _np.nan


def parse_neet_incidence_manual(path):
    """Tolerant line-based parser for problematic NEET incidence CSVs.
    Returns a DataFrame with columns matching the expected file.
    """
    import re
    from pathlib import Path
    p = Path(path)
    rows = []
    with p.open('r', encoding='utf-8', errors='replace') as fh:
        header = fh.readline()
        for line in fh:
            line = line.rstrip('\n')
            matches = list(re.finditer(r'(\d{4}(?:-Q\d)?),(-?\d+[\.,]?\d*)', line))
            if not matches:
                continue
            m = matches[-1]
            time = m.group(1)
            obs = m.group(2).replace(',', '.')
            leading = line[:m.start()]
            tokens = leading.split(',')
            while len(tokens) < 11:
                tokens.append('')
            titolo = ','.join(tokens[11:]).strip()
            try:
                obs_v = float(obs)
            except:
                try:
                    obs_v = float(obs.replace('.', '').replace(',', '.'))
                except:
                    obs_v = _np.nan
            rows.append({
                'FREQ': tokens[0],
                'Frequenza': tokens[1],
                'REF_AREA': tokens[2],
                'Territorio': tokens[3],
                'DATA_TYPE': tokens[4],
                'Indicatore': tokens[5],
                'SEX': tokens[6],
                'Sesso': tokens[7],
                'AGE': tokens[8],
                'Età': tokens[9],
                'EDU_LEV_HIGHEST': tokens[10],
                'Titolo di studio': titolo,
                'TIME_PERIOD': time,
                'Osservazione': obs_v
            })
    return pd.DataFrame(rows)

# Find candidate files
print('Searching for input files...')
neet_incidence = None
neet_counts = None
for p in ROOT.rglob('*.csv'):
    n = p.name.lower()
    if 'incidenza' in n and 'neet' in n:
        neet_incidence = p
    if 'dati regionali' in n or ('neet' in n and 'dati' in n and 'reg' in n):
        # pick regional counts file (if exists)
        neet_counts = p

# fallback picks
if neet_incidence is None:
    for p in ROOT.rglob('*.csv'):
        if 'titolo' in p.name.lower() and 'neet' in p.name.lower():
            neet_incidence = p
if neet_counts is None:
    for p in ROOT.rglob('*.csv'):
        if 'wstatus' in p.name.lower() or 'dati regionali' in p.name.lower():
            neet_counts = p

print('NEET incidence file:', neet_incidence)
print('NEET counts file:', neet_counts)

# MUR iscritti files (expected under MUR/MUR_iscritti)
mur_iscr_root = ROOT / 'MUR' / 'MUR_iscritti'
iscr_anno_nasc = mur_iscr_root / 'iscritti_per_anno_nascita.csv'
iscr_anno = mur_iscr_root / 'iscritti_per_anno.csv'
iscr_ateneo = mur_iscr_root / 'iscritti_per_ateneo.csv'
iscr_corso = mur_iscr_root / 'iscritti_per_corso_2019_25.csv'

files = {
    'iscr_anno_nasc': iscr_anno_nasc if iscr_anno_nasc.exists() else None,
    'iscr_anno': iscr_anno if iscr_anno.exists() else None,
    'iscr_ateneo': iscr_ateneo if iscr_ateneo.exists() else None,
    'iscr_corso': iscr_corso if iscr_corso.exists() else None,
}
print('MUR files found:', files)

# laureati (degree completions)
laureati_root = ROOT / 'MUR' / 'laureati'
laureati_by_year = laureati_root / '01_laureatixanno.csv'
laureati_by_ateneo = laureati_root / '02_laureatixateneo.csv'
files['laureati_by_year'] = laureati_by_year if laureati_by_year.exists() else None
files['laureati_by_ateneo'] = laureati_by_ateneo if laureati_by_ateneo.exists() else None
print('Laureati files:', files['laureati_by_year'], files['laureati_by_ateneo'])

# contrib/exemptions (MUR contributions)
contrib_path = None
for p in (ROOT / 'MUR').rglob('*.csv'):
    if 'esonero' in p.name.lower() or 'contrib' in p.name.lower() or 'contribuzione' in p.name.lower():
        contrib_path = p
        break
files['contrib'] = contrib_path
print('Contrib/exemptions:', contrib_path)

# Load and analyse NEET incidence
if neet_incidence is not None:
    df_inc = smart_read_csv(neet_incidence)
    df_inc.columns = [c.strip() for c in df_inc.columns]
    # detect columns
    def find_col(df, keywords):
        cols = df.columns.astype(str)
        for k in keywords:
            for c in cols:
                if k.upper() in c.upper():
                    return c
        return None
    TIME_COL = find_col(df_inc, ['TIME_PERIOD', 'TIME', 'TIME_PERIOD'])
    EDU_COL = find_col(df_inc, ['TITOL', 'EDU', 'EDU_LEV', 'Titolo'])
    OBS_COL = find_col(df_inc, ['Osservazione', 'OBS', 'OBSERVATION'])
    AGE_COL = find_col(df_inc, ['AGE', 'Età', 'Eta'])
    # parse obs
    if OBS_COL:
        df_inc[OBS_COL] = df_inc[OBS_COL].apply(parse_numeric)
    latest = None
    if TIME_COL:
        latest = df_inc[TIME_COL].astype(str).max()
    # prefer common age groups
    pref_age = None
    if AGE_COL is not None and latest is not None:
        df_latest = df_inc[df_inc[TIME_COL].astype(str) == latest].copy()
        for a in ['Y18-29', 'Y15-29', 'Y15-24', 'Y15-34']:
            if a in df_latest[AGE_COL].astype(str).values:
                pref_age = a
                break
        if pref_age is not None:
            df_latest = df_latest[df_latest[AGE_COL].astype(str) == pref_age]
    else:
        df_latest = df_inc.copy()
    if EDU_COL and OBS_COL:
        byedu = df_latest.groupby(EDU_COL)[OBS_COL].mean().sort_values(ascending=False)
        # ensure no NaNs and write as a two-column CSV with an explicit header
        byedu = byedu.dropna()
        byedu_df = byedu.rename('Incidence').to_frame()
        out_csv = OUT / 'neet_incidence_by_education.csv'
        byedu_df.to_csv(out_csv, index_label=EDU_COL)
        print('Saved', out_csv)
        # plot
        plt.figure(figsize=(10,8))
        sns.barplot(x=byedu_df['Incidence'].values, y=byedu_df.index, palette='viridis')
        plt.xlabel('Incidence (%)')
        title_age = pref_age if pref_age else ''
        plt.title(f'NEET incidence by education level — {latest} {title_age}')
        plt.tight_layout()
        figpath = OUT / 'neet_incidence_by_education.png'
        plt.savefig(figpath)
        plt.close()
        print('Saved', figpath)
        # if result empty (parsing issues), try manual tolerant parser
        if byedu_df.shape[0] == 0:
            try:
                df_manual = parse_neet_incidence_manual(neet_incidence)
                df_manual_cols = df_manual.columns
                if 'Titolo di studio' in df_manual_cols and 'Osservazione' in df_manual_cols:
                    latest_manual = df_manual['TIME_PERIOD'].astype(str).max()
                    # prefer pref_age when available
                    if AGE_COL is not None:
                        pref_age_manual = None
                        for a in ['Y18-29', 'Y15-29', 'Y15-24', 'Y15-34']:
                            if a in df_manual['AGE'].astype(str).unique():
                                pref_age_manual = a
                                break
                        if pref_age_manual is not None:
                            df_m_latest = df_manual[df_manual['TIME_PERIOD'].astype(str) == latest_manual]
                            df_m_latest = df_m_latest[df_m_latest['AGE'].astype(str).str.contains(pref_age_manual)]
                        else:
                            df_m_latest = df_manual[df_manual['TIME_PERIOD'].astype(str) == latest_manual]
                    else:
                        df_m_latest = df_manual[df_manual['TIME_PERIOD'].astype(str) == latest_manual]
                    byedu2 = df_m_latest.groupby('Titolo di studio')['Osservazione'].mean().sort_values(ascending=False)
                    byedu2 = byedu2.dropna()
                    byedu2.rename('Incidence').to_frame().to_csv(out_csv, index_label='Titolo di studio')
                    print('Saved (manual) ', out_csv)
            except Exception:
                pass

# NEET absolute counts (national) from counts file
if neet_counts is not None:
    df_counts = smart_read_csv(neet_counts)
    df_counts.columns = [c.strip() for c in df_counts.columns]
    # try to find REF_AREA and OBS columns
    ref = None
    obs = None
    timec = None
    for c in df_counts.columns:
        if 'REF' in c.upper() or 'REF_AREA' in c.upper():
            ref = c
        if 'Osservazione' in c or 'OBS' in c.upper():
            obs = c
        if 'TIME' in c.upper():
            timec = c
    if ref and obs and timec:
        df_counts[obs] = df_counts[obs].apply(parse_numeric)
        df_it = df_counts[df_counts[ref].astype(str).str.upper().str.contains('IT')]
        # take latest year
        if timec:
            latest_time = df_it[timec].astype(str).max()
            df_it_latest = df_it[df_it[timec].astype(str) == latest_time]
        else:
            df_it_latest = df_it
        # Save sample
        out = OUT / 'neet_counts_national_sample.csv'
        df_it_latest.to_csv(out, index=False)
        print('Saved', out)

# Load enrolment files and compute top atenei
if files.get('iscr_ateneo') is not None:
    df_at = smart_read_csv(files['iscr_ateneo'])
    df_at.columns = [c.strip() for c in df_at.columns]
    # find columns
    col_anno = None
    col_aten = None
    col_isc = None
    for c in df_at.columns:
        if 'Anno' in c or 'AnnoA' in c:
            col_anno = c
        if 'Ateneo' in c or 'ATEN' in c.upper() or 'AteneoNOME' in c:
            col_aten = c
        if any(x in c.upper() for x in ['ISC', 'Isc']):
            col_isc = c
    if col_aten and col_isc:
        # coerce numeric
        df_at[col_isc] = df_at[col_isc].apply(parse_numeric)
        summary_at = df_at.groupby(col_aten)[col_isc].sum().sort_values(ascending=False)
        summary_out = OUT / 'iscritti_by_ateneo_top20.csv'
        summary_at.head(50).to_csv(summary_out)
        print('Saved', summary_out)
        plt.figure(figsize=(10,10))
        sns.barplot(x=summary_at.head(20).values, y=summary_at.head(20).index, palette='crest')
        plt.xlabel('Enrolled students')
        plt.title('Top 20 universities by enrolment (sum over sexes)')
        plt.tight_layout()
        fig_at = OUT / 'top20_atenei_enrolment.png'
        plt.savefig(fig_at)
        plt.close()
        print('Saved', fig_at)

# cohort mapping: use iscritti_per_anno_nascita
if files.get('iscr_anno_nasc') is not None:
    df_nasc = smart_read_csv(files['iscr_anno_nasc'])
    df_nasc.columns = [c.strip() for c in df_nasc.columns]
    # sum sexes for 2024/2025
    cols = df_nasc.columns
    anncol = None
    nasccol = None
    isccol = None
    for c in cols:
        if 'AnnoA' in c or 'Anno' == c:
            anncol = c
        if 'AnnoNascita' in c or 'AnnoN' in c:
            nasccol = c
        if any(x in c.upper() for x in ['ISC', 'Isc']):
            isccol = c
    if anncol and nasccol and isccol:
        df_nasc[isccol] = df_nasc[isccol].apply(parse_numeric)
        cohort_2425 = df_nasc[df_nasc[anncol].astype(str).str.contains('2024')]
        cohort_sum = cohort_2425.groupby(nasccol)[isccol].sum().sort_index()
        cohort_out = OUT / 'cohort_iscritti_2024_2025_by_birthyear.csv'
        cohort_sum.to_csv(cohort_out)
        print('Saved', cohort_out)

# dropout trend
mur_root = ROOT / 'MUR'
if (mur_root / 'tassoabbandono_180226.csv').exists():
    df_t = smart_read_csv(mur_root / 'tassoabbandono_180226.csv')
    df_t.columns = [c.strip() for c in df_t.columns]
    # assume first col is year label
    yearcol = df_t.columns[0]
    valcol = None
    for c in df_t.columns[1:]:
        if 'TOT' in c.upper() or 'TA_' in c.upper() or 'TA' == c:
            valcol = c
            break
    if valcol is None:
        valcol = df_t.columns[1]
    df_t[valcol] = df_t[valcol].astype(str).str.replace(',', '.').str.replace(' ', '')
    df_t[valcol] = pd.to_numeric(df_t[valcol], errors='coerce')
    out = OUT / 'dropout_rate_time_series.csv'
    df_t[[yearcol, valcol]].to_csv(out, index=False)
    print('Saved', out)
    plt.figure(figsize=(8,4))
    plt.plot(df_t[yearcol], df_t[valcol], marker='o')
    plt.xticks(rotation=45)
    plt.title('University dropout rate')
    plt.tight_layout()
    figd = OUT / 'dropout_rate_trend.png'
    plt.savefig(figd)
    plt.close()
    print('Saved', figd)

# exemptions / contributions summary
if contrib_path is not None and contrib_path.exists():
    d = smart_read_csv(contrib_path)
    d.columns = [c.strip() for c in d.columns]
    es_cols = [c for c in d.columns if 'ESONERO' in c.upper() or 'ESONER' in c.upper() or 'ESON' in c.upper()]
    if len(es_cols) == 0:
        # fallback numeric columns
        numeric_cols = []
        for c in d.columns:
            try:
                sample = d[c].dropna().iloc[0]
                _ = parse_numeric(sample)
                numeric_cols.append(c)
            except Exception:
                pass
        es_cols = numeric_cols
    for c in es_cols:
        d[c] = d[c].astype(str).apply(parse_numeric)
    if 'DESCRIZIONE_ESONERO_TOTALE' in d.columns:
        tot_by_desc = d.groupby('DESCRIZIONE_ESONERO_TOTALE')[es_cols].sum().sum(axis=1).sort_values(ascending=False)
        tot_by_desc.to_csv(OUT / 'exemptions_by_description.csv')
        print('Saved', OUT / 'exemptions_by_description.csv')

# laureati summary (completion)
if files.get('laureati_by_year') is not None:
    df_l = smart_read_csv(files['laureati_by_year'])
    df_l.columns = [c.strip() for c in df_l.columns]
    # try to find year and count
    ycol = None
    ccol = None
    for c in df_l.columns:
        if 'Anno' in c or 'ANNO' in c.upper() or 'anno' in c.lower():
            ycol = c
        if any(x in c.upper() for x in ['LAU', 'LAURE', 'ISCR', 'NUM']):
            ccol = c
    if ycol and ccol:
        df_l[ccol] = df_l[ccol].apply(parse_numeric)
        df_l.groupby(ycol)[ccol].sum().to_csv(OUT / 'laureati_by_year_summary.csv')
        print('Saved', OUT / 'laureati_by_year_summary.csv')

print('\nDone. Outputs saved to', OUT.resolve())
print('Files:')
for f in sorted(OUT.glob('*')):
    print('-', f.name)

# Short textual summary file
summary = OUT / 'summary.txt'
with summary.open('w', encoding='utf8') as fh:
    fh.write('Generated NEET & MUR analysis outputs.\n')
    fh.write('See CSVs and PNGs in this folder for details.\n')
print('Wrote', summary)
print('Analysis complete.')

# --- Additional analysis: costs & student privileges (exemptions) ---
print('\nRunning costs & privileges analysis...')
# cost files (local summaries)
primary_cost_file = ROOT / 'ItalyPrimarySchoolBookExpenses.csv'
secondary_cost_file = ROOT / 'ItalianMeanSecondarySchoolExpenses.csv'
costs_summary = {}
def first_numeric_col(df):
    for c in df.columns:
        try:
            sample = df[c].dropna().astype(str).iloc[0]
        except Exception:
            continue
        v = parse_numeric(sample)
        if not _np.isnan(v):
            return c
    return None

if primary_cost_file.exists():
    try:
        dfp = smart_read_csv(primary_cost_file)
        dfp.columns = [c.strip() for c in dfp.columns]
        ccol = first_numeric_col(dfp)
        if ccol:
            dfp[ccol] = dfp[ccol].apply(parse_numeric)
            costs_summary['primary_mean'] = float(dfp[ccol].mean())
    except Exception:
        pass

if secondary_cost_file.exists():
    try:
        dfs = smart_read_csv(secondary_cost_file)
        dfs.columns = [c.strip() for c in dfs.columns]
        ccol = first_numeric_col(dfs)
        if ccol:
            dfs[ccol] = dfs[ccol].apply(parse_numeric)
            costs_summary['secondary_mean'] = float(dfs[ccol].mean())
    except Exception:
        pass

if costs_summary:
    import json
    (OUT / 'student_costs_summary.json').write_text(json.dumps(costs_summary, indent=2), encoding='utf8')
    print('Saved', OUT / 'student_costs_summary.json')

# Exemptions / contributions by ateneo
if contrib_path is not None and contrib_path.exists():
    try:
        d = smart_read_csv(contrib_path)
        d.columns = [c.strip() for c in d.columns]
        # Try to detect an ateneo identifier column
        at_col = None
        for c in d.columns:
            if 'ATEN' in c.upper() and ('COD' in c.upper() or 'ID' in c.upper() or 'CODE' in c.upper()):
                at_col = c
                break
        if at_col is None:
            for c in d.columns:
                if 'ATENEO' in c.upper():
                    at_col = c
                    break
        # numeric columns
        num_cols = []
        for c in d.columns:
            try:
                sample = d[c].dropna().astype(str).iloc[0]
                if not _np.isnan(parse_numeric(sample)):
                    num_cols.append(c)
            except Exception:
                continue
        if len(num_cols) > 0:
            for c in num_cols:
                d[c] = d[c].astype(str).apply(parse_numeric).fillna(0)
            d['exemptions_total'] = d[num_cols].sum(axis=1)
            if at_col is not None:
                ex_by_at = d.groupby(at_col)['exemptions_total'].sum().sort_values(ascending=False)
                ex_by_at.to_csv(OUT / 'exemptions_by_ateneo.csv', header=['exemptions'])
                print('Saved', OUT / 'exemptions_by_ateneo.csv')
                # try to compute ratio to enrolment if enrolment file available
                if files.get('iscr_ateneo') is not None and files['iscr_ateneo'].exists():
                    try:
                        df_enr = smart_read_csv(files['iscr_ateneo'])
                        df_enr.columns = [c.strip() for c in df_enr.columns]
                        # find code and enrolment cols
                        code_col = None
                        enr_col = None
                        for c in df_enr.columns:
                            if 'ATEN' in c.upper() and ('COD' in c.upper() or 'ID' in c.upper()):
                                code_col = c
                            if any(x in c.upper() for x in ['ISC', 'Isc', 'ENR']):
                                enr_col = c
                        if code_col and enr_col:
                            df_enr[enr_col] = df_enr[enr_col].apply(parse_numeric).fillna(0)
                            enr_sum = df_enr.groupby(code_col)[enr_col].sum()
                            merged = pd.DataFrame({'exemptions': ex_by_at}).join(enr_sum.rename('enrolments'), how='left')
                            merged['exemptions_per_1000'] = (merged['exemptions'] / merged['enrolments']).replace(_np.inf, _np.nan) * 1000
                            merged.to_csv(OUT / 'exemptions_enrolment_ratio.csv')
                            print('Saved', OUT / 'exemptions_enrolment_ratio.csv')
                    except Exception:
                        pass
            else:
                d[['exemptions_total']].sum().to_csv(OUT / 'exemptions_total_summary.csv')
                print('Saved', OUT / 'exemptions_total_summary.csv')
    except Exception:
        print('Exemptions analysis failed')
