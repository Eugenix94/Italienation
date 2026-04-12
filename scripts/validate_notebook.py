"""Validation script: runs all notebook code cells to verify correctness."""
import warnings, re, json
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for testing
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
warnings.filterwarnings('ignore')

sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams.update({'figure.figsize': (12, 5), 'figure.dpi': 110})

ROOT = Path('local_data')
OUT  = Path('Notebooks/neet_outputs')
OUT.mkdir(exist_ok=True, parents=True)

def smart_read_csv(path, **kw):
    path = str(path)
    for enc in ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1']:
        for sep in [';', ',', '\t']:
            try:
                df = pd.read_csv(path, sep=sep, encoding=enc, low_memory=False, **kw)
                if df.shape[1] > 1:
                    return df
            except Exception:
                pass
    try:
        raw = Path(path).read_bytes()
        import io
        return pd.read_csv(io.StringIO(raw.decode('utf-8', errors='replace')), sep=None, engine='python')
    except Exception:
        return pd.read_csv(path, engine='python', sep=None, encoding='latin-1', low_memory=False)

def find_col(df, *kw):
    for k in kw:
        for c in df.columns:
            if k.upper() in str(c).upper():
                return c
    return None

def parse_num(x):
    if x is None: return np.nan
    s = str(x).strip()
    if s in ('', 'N', 'n', '-', 'nan', 'NaN', 'None', ':', '..', 'n/a'): return np.nan
    if re.match(r'^\d{1,3}(?:\.\d{3})+$', s): return float(s.replace('.', ''))
    if ',' in s and '.' not in s:
        try: return float(s.replace(',', '.'))
        except: return np.nan
    if '.' in s and ',' in s:
        try: return float(s.replace('.', '').replace(',', '.'))
        except: return np.nan
    try: return float(s)
    except: return np.nan

def savefig(name, tight=True):
    p = OUT / name
    if tight: plt.tight_layout()
    plt.savefig(p, dpi=110, bbox_inches='tight')
    plt.close()
    print(f'  [OK] saved {p}')

errors = []

# ── S1a: NEET incidence by education ──────────────────────────────────────────
try:
    inc_path = next(
        (p for p in ROOT.glob('*.csv') if 'incidenza' in p.name.lower() or 'titolo' in p.name.lower()),
        None
    )
    df_inc = smart_read_csv(inc_path)
    df_inc.columns = [str(c).strip() for c in df_inc.columns]
    TIME = find_col(df_inc, 'TIME_PERIOD', 'TIME')
    OBS  = find_col(df_inc, 'Osservazione', 'OBS_VALUE', 'OBS')
    EDU  = find_col(df_inc, 'Titolo', 'EDU_LEV', 'EDU')
    AGE  = find_col(df_inc, 'AGE')
    df_inc[OBS] = df_inc[OBS].apply(parse_num)
    latest = df_inc[TIME].astype(str).dropna().max()
    df_l   = df_inc[df_inc[TIME].astype(str) == latest].copy()
    pref_age = ''
    if AGE:
        for a in ['Y18-29', 'Y15-29', 'Y15-24']:
            if a in df_l[AGE].values:
                df_l = df_l[df_l[AGE] == a]; pref_age = a; break
    by_edu = df_l.groupby(EDU)[OBS].mean().dropna().sort_values(ascending=True)
    colours = sns.color_palette('RdYlGn', len(by_edu))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.barh(by_edu.index, by_edu.values, color=colours)
    ax.set_xlabel('NEET incidence (%)')
    ax.set_title(f'NEET incidence by education level — Italy {latest} ({pref_age})', fontweight='bold')
    savefig('s1_neet_by_education.png')
    print(f'S1a OK: {len(by_edu)} education groups, highest={by_edu.max():.1f}%')
except Exception as e:
    errors.append(f'S1a NEET by education: {e}')
    print(f'S1a ERROR: {e}')

# ── S1b: NEET by region ────────────────────────────────────────────────────────
try:
    reg_path = next(
        (p for p in ROOT.glob('*.csv') if 'regionali' in p.name.lower() and 'neet' in p.name.lower()),
        None
    )
    df_reg = smart_read_csv(reg_path)
    df_reg.columns = [str(c).strip() for c in df_reg.columns]
    T2   = find_col(df_reg, 'TIME_PERIOD', 'TIME')
    OBS2 = find_col(df_reg, 'Osservazione', 'OBS')
    GEO  = find_col(df_reg, 'Territorio')
    AGE2 = find_col(df_reg, 'AGE')
    df_reg[OBS2] = df_reg[OBS2].apply(parse_num)
    lat2 = df_reg[T2].astype(str).max()
    df_r = df_reg[df_reg[T2].astype(str) == lat2].copy()
    if AGE2 and 'Y15-29' in df_r[AGE2].values:
        df_r = df_r[df_r[AGE2] == 'Y15-29']
    by_reg = (df_r.groupby(GEO)[OBS2].mean().dropna().sort_values(ascending=False).head(25))
    by_reg = by_reg[~by_reg.index.str.upper().str.contains('ITALIA|TOTALE|NORD|SUD|CENTRO|ISOLE')]
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.bar(by_reg.index, by_reg.values, color='steelblue')
    ax.set_ylabel('NEET rate (%)')
    ax.set_title(f'NEET rate by region — {lat2}', fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    savefig('s1_neet_by_region.png')
    print(f'S1b OK: {len(by_reg)} regions')

    # trend
    nat_mask = df_reg[GEO].astype(str).str.upper().str.contains('ITALIA')
    df_nat = df_reg[nat_mask]
    if AGE2 and 'Y15-29' in df_nat[AGE2].values:
        df_nat = df_nat[df_nat[AGE2] == 'Y15-29']
    trend = df_nat.groupby(T2)[OBS2].mean().sort_index().dropna()
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(trend.index.astype(str), trend.values, marker='o', color='crimson')
    ax.set_title('Italy NEET rate trend', fontweight='bold')
    plt.xticks(rotation=45)
    savefig('s1_neet_trend.png')
    print(f'S1b trend OK: {len(trend)} years, latest={trend.iloc[-1]:.1f}%')
except Exception as e:
    errors.append(f'S1b regional: {e}')
    print(f'S1b ERROR: {e}')

# ── S2: Schools ────────────────────────────────────────────────────────────────
try:
    scuole_path = ROOT / 'MinIstruzione/Scuole/SCUANAGRAFESTAT20242520250831.csv'
    df_scuole   = smart_read_csv(scuole_path)
    df_scuole.columns = [str(c).strip() for c in df_scuole.columns]
    TIPO = 'DESCRIZIONETIPOLOGIAGRADOISTRUZIONESCUOLA'
    AREA = 'AREAGEOGRAFICA'
    REG  = 'REGIONE'
    def classify_track(name):
        n = str(name).upper()
        if 'LICEO' in n or 'MAGISTRALE' in n or 'ARTE' in n: return 'Liceo (Academic)'
        elif 'TECNICO' in n or 'GEOMETRI' in n or 'AGRARIO' in n: return 'Istituto Tecnico'
        elif 'PROF' in n: return 'Istituto Professionale'
        elif any(x in n for x in ['PRIMARIA', 'INFANZIA', 'PRIMO GRADO', 'COMPRENSIVO']): return 'Primary/Lower Secondary'
        else: return 'Other / Mixed'
    df_scuole['TRACK'] = df_scuole[TIPO].apply(classify_track)
    df_sec = df_scuole[df_scuole['TRACK'].isin(['Liceo (Academic)', 'Istituto Tecnico', 'Istituto Professionale'])].copy()
    pivot = df_sec.groupby([AREA, 'TRACK'])['CODICESCUOLA'].count().unstack('TRACK').fillna(0).astype(int)
    ax = pivot.plot(kind='bar', figsize=(12, 6))
    ax.set_title('Schools by track and area', fontweight='bold')
    plt.xticks(rotation=25, ha='right')
    savefig('s2_schools_by_track_area.png')
    school_by_reg = df_sec.groupby([REG, 'TRACK'])['CODICESCUOLA'].count().unstack('TRACK').fillna(0).astype(int)
    school_by_reg['Liceo_Prof_ratio'] = school_by_reg.get('Liceo (Academic)', 0) / school_by_reg.get('Istituto Professionale', 1)
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    school_by_reg.drop(columns=['Liceo_Prof_ratio'], errors='ignore').sort_values('Istituto Professionale').plot(kind='barh', ax=axes[0])
    axes[0].set_title('Schools by track per region', fontweight='bold')
    ratio_sorted = school_by_reg['Liceo_Prof_ratio'].sort_values(ascending=False)
    axes[1].barh(ratio_sorted.index, ratio_sorted.values)
    axes[1].set_title('Liceo/Professionale ratio', fontweight='bold')
    savefig('s2_school_track_ratio_by_region.png')
    print(f'S2-schools OK: {len(df_sec)} secondary branches, {len(pivot)} areas')
except Exception as e:
    errors.append(f'S2 schools: {e}')
    print(f'S2 schools ERROR: {e}')

# ── S2 students ────────────────────────────────────────────────────────────────
try:
    df_alu = smart_read_csv(ROOT / 'MinIstruzione/Alunni/ALUSECGRADOINDPAR20242520250831.csv')
    df_alu.columns = [str(c).strip() for c in df_alu.columns]
    M_COL = find_col(df_alu, 'ALUNNIMASCHI')
    F_COL = find_col(df_alu, 'ALUNNIFEMMINE')
    TRK   = find_col(df_alu, 'TIPOPERCORSO')
    IND   = find_col(df_alu, 'INDIRIZZO')
    df_alu[M_COL] = df_alu[M_COL].apply(parse_num)
    df_alu[F_COL] = df_alu[F_COL].apply(parse_num)
    df_alu['TOTALE'] = df_alu[[M_COL, F_COL]].sum(axis=1)
    by_track = df_alu.groupby(TRK)['TOTALE'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(by_track.values, labels=by_track.index, autopct='%1.1f%%')
    ax.set_title('Students by secondary track', fontweight='bold')
    savefig('s2_students_by_track.png')
    if IND:
        by_ind = df_alu.groupby(IND)['TOTALE'].sum().sort_values(ascending=False).head(20)
        fig, ax = plt.subplots(figsize=(12, 7))
        ax.barh(by_ind.index[::-1], by_ind.values[::-1])
        ax.set_title('Top 20 secondary curricula', fontweight='bold')
        savefig('s2_top_indirizzo.png')
    print(f'S2-students OK: track breakdown: {by_track.to_dict()}')
except Exception as e:
    errors.append(f'S2 students: {e}')
    print(f'S2 students ERROR: {e}')

# ── S3a: Diploma → university ─────────────────────────────────────────────────
try:
    df_dip = smart_read_csv(ROOT / 'MUR/immatricolati/10_immatricolatixdiplomascuolasecondariaxclasse.csv')
    df_dip.columns = [str(c).strip() for c in df_dip.columns]
    DIP_COL  = find_col(df_dip, 'Diploma_tipo', 'Diploma')
    IMM_COL  = find_col(df_dip, 'Imm')
    ANNO_COL = find_col(df_dip, 'AnnoA', 'Anno')
    df_dip[IMM_COL] = df_dip[IMM_COL].apply(parse_num)
    latest_anno = df_dip[ANNO_COL].astype(str).max()
    df_d_lat = df_dip[df_dip[ANNO_COL].astype(str) == latest_anno]
    by_dip = df_d_lat.groupby(DIP_COL)[IMM_COL].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.barh(by_dip.index, by_dip.values)
    ax.set_title(f'Matriculations by diploma type — {latest_anno}', fontweight='bold')
    savefig('s3_matriculations_by_diploma.png')
    pct = by_dip / by_dip.sum() * 100
    print(f'S3a OK: {len(by_dip)} diploma types. Pct: {pct.sort_values(ascending=False).head(3).round(1).to_dict()}')
except Exception as e:
    errors.append(f'S3a diploma: {e}')
    print(f'S3a ERROR: {e}')

# ── S3b: Diploma by province ──────────────────────────────────────────────────
try:
    df_res = smart_read_csv(ROOT / 'MUR/immatricolati/11_immatricolatixdiplomascuolaxresidenza.csv')
    df_res.columns = [str(c).strip() for c in df_res.columns]
    DIP2 = find_col(df_res, 'Diploma_tipo')
    PROV = find_col(df_res, 'ProvinciaRES', 'Provincia')
    IMM2 = find_col(df_res, 'Imm')
    AN2  = find_col(df_res, 'AnnoA')
    df_res[IMM2] = df_res[IMM2].apply(parse_num)
    lat_r = df_res[AN2].astype(str).max()
    df_r2 = df_res[df_res[AN2].astype(str) == lat_r]
    pivot_res = df_r2.groupby([PROV, DIP2])[IMM2].sum().unstack(DIP2).fillna(0)
    liceo_cols = [c for c in pivot_res.columns if 'LICEO' in str(c).upper()]
    if liceo_cols:
        pivot_res['pct_liceo'] = pivot_res[liceo_cols].sum(axis=1) / pivot_res.sum(axis=1) * 100
        pct_liceo_prov = pivot_res['pct_liceo'].sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(13, 8))
        ax.bar(pct_liceo_prov.index, pct_liceo_prov.values)
        ax.set_title('Liceo share of uni entrants by province', fontweight='bold')
        plt.xticks(rotation=90, fontsize=5)
        savefig('s3_liceo_share_by_province.png')
    print(f'S3b OK: {len(pivot_res)} provinces')
except Exception as e:
    errors.append(f'S3b province: {e}')
    print(f'S3b ERROR: {e}')

# ── S3c: Grade distribution ───────────────────────────────────────────────────
try:
    df_vote = smart_read_csv(ROOT / 'MUR/immatricolati/16_immatricolatixvotodiplomascuolasec.csv')
    df_vote.columns = [str(c).strip() for c in df_vote.columns]
    VOTO = find_col(df_vote, 'Diploma_Voto', 'Voto')
    IMM3 = find_col(df_vote, 'Imm')
    AN3  = find_col(df_vote, 'AnnoA')
    df_vote[IMM3] = df_vote[IMM3].apply(parse_num)
    lat_v = df_vote[AN3].astype(str).max()
    by_voto = df_vote[df_vote[AN3].astype(str) == lat_v].groupby(VOTO)[IMM3].sum().sort_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(by_voto.index.astype(str), by_voto.values, color='steelblue')
    ax.set_title(f'Diploma grade distribution of uni entrants — {lat_v}', fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    savefig('s3_diploma_grade_distribution.png')
    print(f'S3c OK: {len(by_voto)} grade bands')
except Exception as e:
    errors.append(f'S3c grades: {e}')
    print(f'S3c ERROR: {e}')

# ── S3d: Geographic mobility ──────────────────────────────────────────────────
try:
    df_fuori = smart_read_csv(ROOT / 'MUR/MUR_iscritti/iscritti_in_sede_fuori_sede.csv')
    df_fuori.columns = [str(c).strip() for c in df_fuori.columns]
    ISC  = find_col(df_fuori, 'Isc')
    PROVD = find_col(df_fuori, 'ProvinciaSede', 'Dip')
    PROVC = find_col(df_fuori, 'provcorso', 'Corso')
    AN4   = find_col(df_fuori, 'AnnoA')
    df_fuori[ISC] = df_fuori[ISC].apply(parse_num)
    lat_f = df_fuori[AN4].astype(str).max()
    df_f  = df_fuori[df_fuori[AN4].astype(str) == lat_f].copy()
    if PROVD and PROVC:
        df_f['fuori'] = df_f[PROVD].astype(str) != df_f[PROVC].astype(str)
        in_vs_out = df_f.groupby('fuori')[ISC].sum()
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.pie(in_vs_out.values, labels=['In-province', 'Out-of-province'], autopct='%1.1f%%')
        ax.set_title('Geographic mobility of university students', fontweight='bold')
        savefig('s3_geographic_mobility.png')
        print(f'S3d OK: in_vs_out={in_vs_out.to_dict()}')
    else:
        print(f'S3d: PROVD={PROVD} PROVC={PROVC}')
except Exception as e:
    errors.append(f'S3d mobility: {e}')
    print(f'S3d ERROR: {e}')

# ── S4: University flows ───────────────────────────────────────────────────────
try:
    df_imm = smart_read_csv(ROOT / 'MUR/immatricolati/01_immatricolatixanno.csv')
    df_imm.columns = [str(c).strip() for c in df_imm.columns]
    AN5 = find_col(df_imm, 'AnnoA')
    if 'Imm' in df_imm.columns:
        df_imm['Imm'] = df_imm['Imm'].apply(parse_num)
        tot_col = 'Imm'
    else:
        df_imm['Imm_M'] = df_imm.get('Imm_M', pd.Series(0, index=df_imm.index)).apply(parse_num)
        df_imm['Imm_F'] = df_imm.get('Imm_F', pd.Series(0, index=df_imm.index)).apply(parse_num)
        df_imm['Imm'] = df_imm[['Imm_M', 'Imm_F']].sum(axis=1)
        tot_col = 'Imm'
    trend_imm = df_imm.groupby(AN5)[tot_col].sum().sort_index()
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(trend_imm.index.astype(str), trend_imm.values, marker='o')
    ax.set_title('Immatricolati trend', fontweight='bold')
    plt.xticks(rotation=45)
    savefig('s4_immatricolati_trend.png')
    print(f'S4a OK: {len(trend_imm)} years')
except Exception as e:
    errors.append(f'S4a imm: {e}')
    print(f'S4a ERROR: {e}')

try:
    df_drop = smart_read_csv(ROOT / 'MUR/tassoabbandono_180226.csv')
    df_drop.columns = [str(c).strip() for c in df_drop.columns]
    yr_col  = df_drop.columns[0]
    val_col = df_drop.columns[1]
    df_drop[val_col] = df_drop[val_col].apply(parse_num)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(df_drop[yr_col].astype(str), df_drop[val_col], marker='s', color='crimson')
    ax.set_title('Dropout rate trend', fontweight='bold')
    plt.xticks(rotation=45)
    savefig('s4_dropout_trend.png')
    print(f'S4b dropout OK: {len(df_drop)} years')
except Exception as e:
    errors.append(f'S4b dropout: {e}')
    print(f'S4b ERROR: {e}')

try:
    df_lau = smart_read_csv(ROOT / 'MUR/laureati/01_laureatixanno.csv')
    df_lau.columns = [str(c).strip() for c in df_lau.columns]
    AN6 = find_col(df_lau, 'AnnoA', 'Anno')
    LAU = find_col(df_lau, 'Lau')
    if LAU:
        df_lau[LAU] = df_lau[LAU].apply(parse_num)
        trend_lau = df_lau.groupby(AN6)[LAU].sum().sort_index()
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(trend_lau.index.astype(str), trend_lau.values, marker='^', color='green')
        ax.set_title('Laureati trend', fontweight='bold')
        plt.xticks(rotation=45)
        savefig('s4_laureati_trend.png')
        print(f'S4c laureati OK: {len(trend_lau)} years')
    else:
        print(f'S4c: LAU col not found. Cols={list(df_lau.columns[:6])}')
except Exception as e:
    errors.append(f'S4c laureati: {e}')
    print(f'S4c ERROR: {e}')

# ── S5: Economic context ───────────────────────────────────────────────────────
try:
    df_gdp = smart_read_csv(ROOT / 'oecd/eurostat_gdp_per_capita.csv')
    df_gdp.columns = [str(c).strip() for c in df_gdp.columns]
    OBS_G = find_col(df_gdp, 'OBS_VALUE')
    GEO_G = find_col(df_gdp, 'geo')
    TIM_G = find_col(df_gdp, 'TIME_PERIOD', 'TIME')
    df_gdp[OBS_G] = df_gdp[OBS_G].apply(parse_num)
    peers = {'IT': 'Italy', 'DE': 'Germany', 'FR': 'France', 'ES': 'Spain',
             'EU27_2020': 'EU27 avg', 'UK': 'United Kingdom', 'EL': 'Greece'}
    df_gdp_p = df_gdp[df_gdp[GEO_G].isin(peers.keys())].copy()
    df_gdp_p['Country'] = df_gdp_p[GEO_G].map(peers)
    fig, ax = plt.subplots(figsize=(13, 6))
    for country, grp in df_gdp_p.groupby('Country'):
        grp_s = grp.sort_values(TIM_G)
        ax.plot(grp_s[TIM_G].astype(str), grp_s[OBS_G], label=country, lw=2.5 if country == 'Italy' else 1.5)
    ax.axhline(100, color='grey', lw=1, ls=':')
    ax.set_title('GDP per capita volume index', fontweight='bold')
    ax.legend()
    plt.xticks(rotation=45)
    savefig('s5_gdp_per_capita.png')
    it_vals = df_gdp_p[df_gdp_p['Country'] == 'Italy'].sort_values(TIM_G)
    it_gdp_latest = it_vals[OBS_G].iloc[-1] if len(it_vals) > 0 else np.nan
    print(f'S5a GDP OK: Italy latest={it_gdp_latest}')
except Exception as e:
    errors.append(f'S5a GDP: {e}')
    print(f'S5a ERROR: {e}')

try:
    df_gini = smart_read_csv(ROOT / 'WB_WDI_SI_POV_GINI.csv')
    df_gini.columns = [str(c).strip() for c in df_gini.columns]
    REF_G  = find_col(df_gini, 'REF_AREA')
    OBS_Gi = find_col(df_gini, 'OBS_VALUE')
    TIM_Gi = find_col(df_gini, 'TIME_PERIOD', 'TIME')
    df_gini[OBS_Gi] = df_gini[OBS_Gi].apply(parse_num)
    gini_peers = {'ITA': 'Italy', 'DEU': 'Germany', 'FRA': 'France', 'ESP': 'Spain', 'GBR': 'United Kingdom'}
    df_gi_p = df_gini[df_gini[REF_G].isin(gini_peers.keys())].copy()
    df_gi_p['Country'] = df_gi_p[REF_G].map(gini_peers)
    fig, ax = plt.subplots(figsize=(13, 6))
    for country, grp in df_gi_p.groupby('Country'):
        grp_s = grp.sort_values(TIM_Gi)
        ax.plot(grp_s[TIM_Gi].astype(str), grp_s[OBS_Gi], label=country)
    ax.set_title('Gini coefficient', fontweight='bold')
    ax.legend()
    plt.xticks(rotation=45)
    savefig('s5_gini.png')
    print(f'S5b Gini OK')
except Exception as e:
    errors.append(f'S5b Gini: {e}')
    print(f'S5b ERROR: {e}')

try:
    df_prod = smart_read_csv(ROOT / 'ourWorldData/productivity-vs-educational-attainment/productivity-vs-educational-attainment.csv')
    df_prod.columns = [str(c).strip() for c in df_prod.columns]
    EDU_P = find_col(df_prod, 'average years', 'educ', 'years of')
    PROD_P = find_col(df_prod, 'output per hour', 'productivity')
    ENT   = find_col(df_prod, 'Entity')
    YR_P  = find_col(df_prod, 'Year')
    df_prod[EDU_P] = df_prod[EDU_P].apply(parse_num)
    df_prod[PROD_P] = df_prod[PROD_P].apply(parse_num)
    latest_yr_p = df_prod[YR_P].max()
    df_latest_p = df_prod[df_prod[YR_P] == latest_yr_p].dropna(subset=[EDU_P, PROD_P])
    focus = ['Italy', 'United Kingdom', 'Germany', 'France', 'Spain', 'Greece']
    df_focus = df_latest_p[df_latest_p[ENT].isin(focus)]
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.scatter(df_latest_p[EDU_P], df_latest_p[PROD_P], alpha=0.3, color='lightgray', s=30)
    for _, row in df_focus.iterrows():
        ax.scatter(row[EDU_P], row[PROD_P], s=100, color='red' if row[ENT] == 'Italy' else 'steelblue')
        ax.annotate(row[ENT], (row[EDU_P], row[PROD_P]), textcoords='offset points', xytext=(4, 3), fontsize=8)
    ax.set_title('Productivity vs education attainment', fontweight='bold')
    savefig('s5_productivity_vs_education.png')
    print(f'S5c productivity OK: {len(df_focus)} focus countries')
except Exception as e:
    errors.append(f'S5c prod: {e}')
    print(f'S5c ERROR: {e}')

try:
    df_comp = smart_read_csv(ROOT / 'ourWorldData/completion-rate-of-upper-secondary-education-sdg/completion-rate-of-upper-secondary-education-sdg.csv')
    df_comp.columns = [str(c).strip() for c in df_comp.columns]
    RATE = find_col(df_comp, 'Completion rate', 'rate')
    ENT2 = find_col(df_comp, 'Entity')
    YR2  = find_col(df_comp, 'Year')
    comp_countries = ['Italy', 'United Kingdom', 'Germany', 'France', 'Spain']
    df_comp_f = df_comp[df_comp[ENT2].isin(comp_countries)].copy()
    df_comp_f[RATE] = df_comp_f[RATE].apply(parse_num)
    fig, ax = plt.subplots(figsize=(12, 5))
    for country, grp in df_comp_f.groupby(ENT2):
        ax.plot(grp[YR2], grp[RATE], label=country, lw=2)
    ax.set_title('Upper-secondary completion rate', fontweight='bold')
    ax.legend()
    savefig('s5_secondary_completion.png')
    print(f'S5d completion OK')

    # Brain drain
    df_emig = smart_read_csv(ROOT / 'ourWorldData/total-number-of-emigrants.csv')
    df_emig.columns = [str(c).strip() for c in df_emig.columns]
    ENT3 = find_col(df_emig, 'Entity')
    YR3  = find_col(df_emig, 'Year')
    EMI  = find_col(df_emig, 'emigrants', 'Total')
    df_emig[EMI] = df_emig[EMI].apply(parse_num)
    it_emig = df_emig[df_emig[ENT3] == 'Italy'].sort_values(YR3)
    if len(it_emig) > 0:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(it_emig[YR3].astype(str), it_emig[EMI], color='#d62728')
        ax.set_title('Italian emigrants (brain drain)', fontweight='bold')
        plt.xticks(rotation=45)
        savefig('s5_brain_drain.png')
        print(f'S5e brain drain OK: {len(it_emig)} rows')
except Exception as e:
    errors.append(f'S5de comp/emig: {e}')
    print(f'S5de ERROR: {e}')

try:
    df_fin = smart_read_csv(ROOT / 'oecd/oecd_education_fin_gdp.csv')
    df_fin.columns = [str(c).strip() for c in df_fin.columns]
    REF_F  = find_col(df_fin, 'REF_AREA')
    OBS_F  = find_col(df_fin, 'OBS_VALUE')
    TIM_F  = find_col(df_fin, 'TIME_PERIOD', 'TIME')
    SRC_F  = find_col(df_fin, 'EXP_SOURCE')
    EDU_F  = find_col(df_fin, 'EDUCATION_LEV')
    df_fin[OBS_F] = df_fin[OBS_F].apply(parse_num)
    df_fin_t = df_fin[(df_fin[SRC_F] == '_T') & (df_fin[EDU_F] == '_T')].copy()
    fin_peers = {'ITA': 'Italy', 'GBR': 'United Kingdom', 'DEU': 'Germany', 'FRA': 'France', 'ESP': 'Spain'}
    df_fin_p = df_fin_t[df_fin_t[REF_F].isin(fin_peers.keys())].copy()
    df_fin_p['Country'] = df_fin_p[REF_F].map(fin_peers)
    lat_f2 = df_fin_p[TIM_F].max()
    df_fin_lat = df_fin_p[df_fin_p[TIM_F] == lat_f2]
    by_ctry_f = df_fin_lat.groupby('Country')[OBS_F].mean().sort_values(ascending=False)
    if len(by_ctry_f) > 0:
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(by_ctry_f.index, by_ctry_f.values, color=['#d62728' if c == 'Italy' else '#1f77b4' for c in by_ctry_f.index])
        ax.set_title(f'Education spending % GDP — {lat_f2}', fontweight='bold')
        plt.xticks(rotation=30, ha='right')
        savefig('s5_education_spending_gdp.png')
    print(f'S5f edu spending OK: {by_ctry_f.round(2).to_dict()}')
except Exception as e:
    errors.append(f'S5f spending: {e}')
    print(f'S5f ERROR: {e}')

# ── S6: Exemptions ────────────────────────────────────────────────────────────
try:
    contrib_root = ROOT / 'MUR/2024-contribuzione-e-interventi-atenei'
    contrib_file = None
    for p in contrib_root.rglob('*.csv'):
        contrib_file = p; break
    if contrib_file is None:
        for p in (ROOT / 'MUR').rglob('*.csv'):
            if any(k in p.name.lower() for k in ['esonero', 'contrib', 'contribuzione']):
                contrib_file = p; break
    print(f'S6 contrib file: {contrib_file}')
    if contrib_file:
        df_ex = smart_read_csv(contrib_file)
        df_ex.columns = [str(c).strip() for c in df_ex.columns]
        ATEN_E = find_col(df_ex, 'Ateneo', 'ATEN')
        DESC_E = find_col(df_ex, 'DESCRIZIONE', 'DESC')
        num_cols_e = []
        for c in df_ex.columns:
            try:
                v = parse_num(df_ex[c].dropna().astype(str).iloc[0])
                if not np.isnan(v): num_cols_e.append(c)
            except: pass
        for c in num_cols_e:
            df_ex[c] = df_ex[c].apply(parse_num)
        df_ex['total_exempt'] = df_ex[num_cols_e].sum(axis=1)
        if DESC_E:
            by_desc = df_ex.groupby(DESC_E)['total_exempt'].sum().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(12, 8))
            by_desc.head(15).sort_values().plot(kind='barh', ax=ax)
            ax.set_title('Exemption categories', fontweight='bold')
            savefig('s6_exemptions_by_category.png')
        print(f'S6 exemptions OK: {len(df_ex)} rows, {len(num_cols_e)} numeric cols')
except Exception as e:
    errors.append(f'S6 exemptions: {e}')
    print(f'S6 ERROR: {e}')

# ── S7: UK ────────────────────────────────────────────────────────────────────
try:
    df_uk431 = smart_read_csv(ROOT / 'UKSDGstats/4-3-1.csv')
    df_uk431.columns = [str(c).strip() for c in df_uk431.columns]
    SER_U = find_col(df_uk431, 'Series')
    VAL_U = find_col(df_uk431, 'Value')
    YR_U  = find_col(df_uk431, 'Year')
    REG_U = find_col(df_uk431, 'Region')
    df_uk431[VAL_U] = df_uk431[VAL_U].apply(parse_num)
    uk_trend = df_uk431.groupby([YR_U, SER_U])[VAL_U].mean().unstack(SER_U).sort_index()
    if len(uk_trend) > 0:
        fig, ax = plt.subplots(figsize=(12, 5))
        for col in uk_trend.columns:
            ax.plot(uk_trend.index.astype(str), uk_trend[col], marker='o', ms=4, label=col[:60])
        ax.set_title('UK adult learning participation (SDG 4.3.1)', fontweight='bold')
        ax.legend(fontsize=7)
        plt.xticks(rotation=45)
        savefig('s7_uk_adult_learning.png')
    print(f'S7 UK OK: {len(uk_trend)} years')
except Exception as e:
    errors.append(f'S7 UK: {e}')
    print(f'S7 ERROR: {e}')

# ── Summary ───────────────────────────────────────────────────────────────────
generated = sorted(OUT.glob('s*.png'))
print(f'\n{"="*60}')
print(f'DONE — Generated {len(generated)} figures')
if errors:
    print(f'ERRORS ({len(errors)}):')
    for e in errors:
        print(f'  ✗ {e}')
else:
    print('All sections ran without errors.')
