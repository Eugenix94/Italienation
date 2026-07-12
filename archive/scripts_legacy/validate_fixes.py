"""Quick validation of the four fixed sections."""
import warnings, re, json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
warnings.filterwarnings('ignore')
sns.set_theme(style='whitegrid', palette='muted')

ROOT = Path('local_data')
OUT  = Path('Notebooks/neet_outputs')
OUT.mkdir(exist_ok=True, parents=True)

def smart_read_csv(path, **kw):
    path = str(path)
    for enc in ['utf-8-sig', 'utf-8', 'cp1252', 'latin-1']:
        for sep in [';', ',', '\t']:
            try:
                df = pd.read_csv(path, sep=sep, encoding=enc, low_memory=False, **kw)
                if df.shape[1] > 1: return df
            except: pass

def find_col(df, *kw):
    for k in kw:
        for c in df.columns:
            if k.upper() in str(c).upper(): return c
    return None

def parse_num(x):
    if x is None: return np.nan
    s = str(x).strip()
    if s in ('','N','n','-','nan','NaN','None',':','..','n/a'): return np.nan
    if re.match(r'^\d{1,3}(?:\.\d{3})+$',s): return float(s.replace('.',''))
    if ',' in s and '.' not in s:
        try: return float(s.replace(',','.'))
        except: return np.nan
    try: return float(s)
    except: return np.nan

errors = []

# === FIX 1: S1a with quotechar="'" ===
print('=== S1a ===')
try:
    inc_path = next((p for p in ROOT.glob('*.csv') if 'incidenza' in p.name.lower() and 'titolo' in p.name.lower()), None)
    df_inc = pd.read_csv(str(inc_path), sep=',', encoding='utf-8-sig', quotechar="'", low_memory=False)
    df_inc.columns = [str(c).strip() for c in df_inc.columns]
    TIME = find_col(df_inc, 'TIME_PERIOD', 'TIME')
    OBS  = find_col(df_inc, 'Osservazione', 'OBS_VALUE', 'OBS')
    EDU  = find_col(df_inc, 'Titolo')
    AGE  = find_col(df_inc, 'AGE')
    df_inc[OBS] = df_inc[OBS].apply(parse_num)
    mask = (df_inc['FREQ'] == 'A') & (df_inc['REF_AREA'] == 'IT') & (df_inc['SEX'] == 9)
    df_it = df_inc[mask].copy()
    latest = df_it[TIME].astype(str).max()
    df_l = df_it[df_it[TIME].astype(str) == latest].copy()
    pref_age = 'all'
    if AGE:
        for a in ['Y15-29', 'Y18-29', 'Y15-34', 'Y15-24']:
            if a in df_l[AGE].values:
                df_l = df_l[df_l[AGE] == a]; pref_age = a; break
    by_edu = df_l[df_l[EDU] != 'Totale'].groupby(EDU)[OBS].mean().dropna()
    print(f'  OK: {len(by_edu)} education groups | {pref_age} | values: {by_edu.round(1).to_dict()}')
except Exception as e:
    errors.append(f'S1a: {e}'); print(f'  ERROR: {e}')

# === FIX 2: S1b regional with annual fallback ===
print('=== S1b ===')
try:
    reg_path = next((p for p in ROOT.glob('*.csv') if 'regionali' in p.name.lower() and 'neet' in p.name.lower()), None)
    df_reg = smart_read_csv(reg_path)
    df_reg.columns = [str(c).strip() for c in df_reg.columns]
    T2 = find_col(df_reg, 'TIME_PERIOD'); OBS2 = find_col(df_reg, 'Osservazione')
    GEO = find_col(df_reg, 'Territorio'); AGE2 = find_col(df_reg, 'AGE'); FREQ2 = find_col(df_reg, 'FREQ')
    df_reg[OBS2] = df_reg[OBS2].apply(parse_num)
    df_annual = df_reg[df_reg[FREQ2] == 'A'].copy()
    if AGE2 and 'Y15-29' in df_annual[AGE2].values:
        df_annual = df_annual[df_annual[AGE2] == 'Y15-29']
    EXCL = r'ITALIA|TOTALE|NORD|SUD|CENTRO|ISOLE|MEZZOGIORNO'
    by_reg, lat2 = pd.Series(dtype=float), ''
    for yr in sorted(df_annual[T2].astype(str).unique(), reverse=True):
        df_yr = df_annual[df_annual[T2].astype(str) == yr]
        br = df_yr.groupby(GEO)[OBS2].mean().dropna()
        br_filt = br[~br.index.str.upper().str.contains(EXCL, na=False, regex=True)]
        if len(br_filt) >= 5:
            by_reg = br_filt.sort_values(ascending=False)
            lat2 = yr; break
    print(f'  OK: {len(by_reg)} regions | year={lat2} | top={by_reg.index[0] if len(by_reg)>0 else "N/A"}')
except Exception as e:
    errors.append(f'S1b: {e}'); print(f'  ERROR: {e}')

# === FIX 3: S5c productivity per-entity latest year ===
print('=== S5c ===')
try:
    df_prod = smart_read_csv(ROOT / 'ourWorldData/productivity-vs-educational-attainment/productivity-vs-educational-attainment.csv')
    df_prod.columns = [str(c).strip() for c in df_prod.columns]
    EDU_P = find_col(df_prod, 'average years', 'educ')
    PROD_P = find_col(df_prod, 'output per hour', 'productivity')
    ENT = find_col(df_prod, 'Entity'); YR_P = find_col(df_prod, 'Year')
    df_prod[EDU_P] = df_prod[EDU_P].apply(parse_num)
    df_prod[PROD_P] = df_prod[PROD_P].apply(parse_num)
    df_valid = df_prod.dropna(subset=[EDU_P, PROD_P])
    latest_per = df_valid.groupby(ENT)[YR_P].max().reset_index()
    latest_per.columns = [ENT, '_yr']
    df_lat = df_valid.merge(latest_per, on=ENT)
    df_latest_p = df_lat[df_lat[YR_P] == df_lat['_yr']].drop(columns=['_yr'])
    focus = ['Italy', 'United Kingdom', 'Germany', 'France', 'Spain', 'Greece']
    df_focus = df_latest_p[df_latest_p[ENT].isin(focus)]
    print(f'  OK: {len(df_focus)} focus countries | {len(df_latest_p)} total | Italy year={df_focus[df_focus[ENT]=="Italy"][YR_P].values}')
except Exception as e:
    errors.append(f'S5c: {e}'); print(f'  ERROR: {e}')

# === FIX 4: S5f education spending without EDU_LEV filter ===
print('=== S5f ===')
try:
    df_fin = smart_read_csv(ROOT / 'oecd/oecd_education_fin_gdp.csv')
    df_fin.columns = [str(c).strip() for c in df_fin.columns]
    REF_F = find_col(df_fin, 'REF_AREA'); OBS_F = find_col(df_fin, 'OBS_VALUE')
    TIM_F = find_col(df_fin, 'TIME_PERIOD', 'TIME'); SRC_F = find_col(df_fin, 'EXP_SOURCE')
    df_fin[OBS_F] = df_fin[OBS_F].apply(parse_num)
    df_fin_t = df_fin[df_fin[SRC_F] == '_T'].copy()
    fin_peers = {'ITA':'Italy','GBR':'United Kingdom','DEU':'Germany','FRA':'France','ESP':'Spain'}
    df_fin_p = df_fin_t[df_fin_t[REF_F].isin(fin_peers)].copy()
    df_fin_p['Country'] = df_fin_p[REF_F].map(fin_peers)
    lat_f2 = df_fin_p[TIM_F].max()
    df_fin_lat = df_fin_p[df_fin_p[TIM_F] == lat_f2]
    by_ctry_f = df_fin_lat.groupby('Country')[OBS_F].mean().dropna().sort_values(ascending=False)
    print(f'  OK: {by_ctry_f.round(2).to_dict()} | year={lat_f2}')
except Exception as e:
    errors.append(f'S5f: {e}'); print(f'  ERROR: {e}')

print()
if errors:
    print(f'ERRORS ({len(errors)}):')
    for e in errors: print(f'  {e}')
else:
    print('All 4 fixes validated OK.')
