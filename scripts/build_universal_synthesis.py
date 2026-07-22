import pandas as pd
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent.parent
LOCAL_DATA = ROOT / "local_data" / "huggingface"
PROCESSED_DATA = ROOT / "processed_data"

provincia_to_regione = {
    'TO':'Piemonte', 'VC':'Piemonte', 'NO':'Piemonte', 'CN':'Piemonte', 'AT':'Piemonte', 'AL':'Piemonte', 'BI':'Piemonte', 'VB':'Piemonte',
    'AO':'Valle d\'Aosta',
    'GE':'Liguria', 'SV':'Liguria', 'IM':'Liguria', 'SP':'Liguria',
    'MI':'Lombardia', 'BG':'Lombardia', 'BS':'Lombardia', 'CO':'Lombardia', 'CR':'Lombardia', 'MN':'Lombardia', 'PV':'Lombardia', 'SO':'Lombardia', 'VA':'Lombardia', 'LC':'Lombardia', 'LO':'Lombardia', 'MB':'Lombardia',
    'VR':'Veneto', 'VI':'Veneto', 'BL':'Veneto', 'TV':'Veneto', 'VE':'Veneto', 'PD':'Veneto', 'RO':'Veneto',
    'UD':'Friuli-Venezia Giulia', 'GO':'Friuli-Venezia Giulia', 'PN':'Friuli-Venezia Giulia', 'TS':'Friuli-Venezia Giulia',
    'TN':'Trentino-Alto Adige', 'BZ':'Trentino-Alto Adige',
    'BO':'Emilia-Romagna', 'FE':'Emilia-Romagna', 'FO':'Emilia-Romagna', 'FC':'Emilia-Romagna', 'MO':'Emilia-Romagna', 'PR':'Emilia-Romagna', 'PC':'Emilia-Romagna', 'RA':'Emilia-Romagna', 'RE':'Emilia-Romagna', 'RN':'Emilia-Romagna',
    'FI':'Toscana', 'AR':'Toscana', 'GR':'Toscana', 'LI':'Toscana', 'LU':'Toscana', 'MS':'Toscana', 'PI':'Toscana', 'PT':'Toscana', 'SI':'Toscana', 'PO':'Toscana',
    'PG':'Umbria', 'TR':'Umbria',
    'AN':'Marche', 'AP':'Marche', 'MC':'Marche', 'PS':'Marche', 'PU':'Marche', 'FM':'Marche',
    'RM':'Lazio', 'VT':'Lazio', 'RI':'Lazio', 'LT':'Lazio', 'FR':'Lazio',
    'AQ':'Abruzzo', 'CH':'Abruzzo', 'PE':'Abruzzo', 'TE':'Abruzzo',
    'CB':'Molise', 'IS':'Molise',
    'NA':'Campania', 'AV':'Campania', 'CE':'Campania', 'BN':'Campania', 'SA':'Campania',
    'BA':'Puglia', 'FG':'Puglia', 'LE':'Puglia', 'TA':'Puglia', 'BR':'Puglia', 'BT':'Puglia',
    'PZ':'Basilicata', 'MT':'Basilicata',
    'CS':'Calabria', 'CZ':'Calabria', 'RC':'Calabria', 'KR':'Calabria', 'VV':'Calabria',
    'PA':'Sicilia', 'CT':'Sicilia', 'ME':'Sicilia', 'AG':'Sicilia', 'CL':'Sicilia', 'EN':'Sicilia', 'SR':'Sicilia', 'TP':'Sicilia', 'RG':'Sicilia',
    'CA':'Sardegna', 'SS':'Sardegna', 'NU':'Sardegna', 'OR':'Sardegna', 'SU':'Sardegna'
}

prov_name_to_regione = {
    'AGRIGENTO': 'SICILIA', 'ALESSANDRIA': 'PIEMONTE', 'ANCONA': 'MARCHE', 'AREZZO': 'TOSCANA', 'ASCOLI PICENO': 'MARCHE',
    'ASTI': 'PIEMONTE', 'AVELLINO': 'CAMPANIA', 'BARI': 'PUGLIA', 'BARLETTA-ANDRIA-TRANI': 'PUGLIA', 'BELLUNO': 'VENETO',
    'BENEVENTO': 'CAMPANIA', 'BERGAMO': 'LOMBARDIA', 'BIELLA': 'PIEMONTE', 'BOLOGNA': 'EMILIA-ROMAGNA', 'BRESCIA': 'LOMBARDIA',
    'BRINDISI': 'PUGLIA', 'CAGLIARI': 'SARDEGNA', 'CALTANISSETTA': 'SICILIA', 'CAMPOBASSO': 'MOLISE', 'CASERTA': 'CAMPANIA',
    'CATANIA': 'SICILIA', 'CATANZARO': 'CALABRIA', 'CHIETI': 'ABRUZZO', 'COMO': 'LOMBARDIA', 'COSENZA': 'CALABRIA',
    'CREMONA': 'LOMBARDIA', 'CROTONE': 'CALABRIA', 'CUNEO': 'PIEMONTE', 'ENNA': 'SICILIA', 'FERMO': 'MARCHE',
    'FERRARA': 'EMILIA-ROMAGNA', 'FIRENZE': 'TOSCANA', 'FOGGIA': 'PUGLIA', "FORLI'-CESENA": 'EMILIA-ROMAGNA', 'FROSINONE': 'LAZIO',
    'GENOVA': 'LIGURIA', 'GORIZIA': 'FRIULI-VENEZIA GIULIA', 'GROSSETO': 'TOSCANA', 'IMPERIA': 'LIGURIA', 'ISERNIA': 'MOLISE',
    "L'AQUILA": 'ABRUZZO', 'LA SPEZIA': 'LIGURIA', 'LATINA': 'LAZIO', 'LECCE': 'PUGLIA', 'LECCO': 'LOMBARDIA',
    'LIVORNO': 'TOSCANA', 'LODI': 'LOMBARDIA', 'LUCCA': 'TOSCANA', 'MACERATA': 'MARCHE', 'MANTOVA': 'LOMBARDIA',
    'MASSA-CARRARA': 'TOSCANA', 'MATERA': 'BASILICATA', 'MESSINA': 'SICILIA', 'MILANO': 'LOMBARDIA', 'MODENA': 'EMILIA-ROMAGNA',
    'MONZA E DELLA BRIANZA': 'LOMBARDIA', 'NAPOLI': 'CAMPANIA', 'NOVARA': 'PIEMONTE', 'NUORO': 'SARDEGNA', 'ORISTANO': 'SARDEGNA',
    'PADOVA': 'VENETO', 'PALERMO': 'SICILIA', 'PARMA': 'EMILIA-ROMAGNA', 'PAVIA': 'LOMBARDIA', 'PERUGIA': 'UMBRIA',
    'PESARO E URBINO': 'MARCHE', 'PESCARA': 'ABRUZZO', 'PIACENZA': 'EMILIA-ROMAGNA', 'PISA': 'TOSCANA', 'PISTOIA': 'TOSCANA',
    'PORDENONE': 'FRIULI-VENEZIA GIULIA', 'POTENZA': 'BASILICATA', 'PRATO': 'TOSCANA', 'RAGUSA': 'SICILIA', 'RAVENNA': 'EMILIA-ROMAGNA',
    'REGGIO CALABRIA': 'CALABRIA', 'REGGIO EMILIA': 'EMILIA-ROMAGNA', 'RIETI': 'LAZIO', 'RIMINI': 'EMILIA-ROMAGNA', 'ROMA': 'LAZIO',
    'ROVIGO': 'VENETO', 'SALERNO': 'CAMPANIA', 'SASSARI': 'SARDEGNA', 'SAVONA': 'LIGURIA', 'SIENA': 'TOSCANA',
    'SIRACUSA': 'SICILIA', 'SONDRIO': 'LOMBARDIA', 'SUD SARDEGNA': 'SARDEGNA', 'TARANTO': 'PUGLIA', 'TERAMO': 'ABRUZZO',
    'TERNI': 'UMBRIA', 'TORINO': 'PIEMONTE', 'TRAPANI': 'SICILIA', 'TREVISO': 'VENETO', 'TRIESTE': 'FRIULI-VENEZIA GIULIA',
    'UDINE': 'FRIULI-VENEZIA GIULIA', 'VARESE': 'LOMBARDIA', 'VENEZIA': 'VENETO', 'VERBANO-CUSIO-OSSOLA': 'PIEMONTE', 'VERCELLI': 'PIEMONTE',
    'VERONA': 'VENETO', 'VIBO VALENTIA': 'CALABRIA', 'VICENZA': 'VENETO', 'VITERBO': 'LAZIO'
}

def clean_regione(r):
    r = r.lower().replace("valle d'aosta/vallée d'aoste", "valle d'aosta")
    r = r.replace("trentino-alto adige/südtirol", "trentino-alto adige")
    r = r.replace("trentino alto adige", "trentino-alto adige")
    r = r.replace("friuli venezia giulia", "friuli-venezia giulia")
    r = r.replace("emilia romagna", "emilia-romagna")
    return r.strip().upper()

print("--- 1. Processing Teachers Precariousness ---")
df_sup = pd.read_parquet(LOCAL_DATA / 'personale' / 'DOCSUPXXV.parquet')
df_tit = pd.read_parquet(LOCAL_DATA / 'personale' / 'DOCTIT.parquet')

# Sum substitutes
df_sup['tot_sup'] = pd.to_numeric(df_sup['DOCENTISUPPLENTIMASCHI'], errors='coerce').fillna(0) + pd.to_numeric(df_sup['DOCENTISUPPLENTIFEMMINE'], errors='coerce').fillna(0)
sup_prov = df_sup.groupby('PROVINCIA')['tot_sup'].sum().reset_index()

# Sum tenured
df_tit['tot_tit'] = pd.to_numeric(df_tit['DOCENTITITOLARIMASCHI'], errors='coerce').fillna(0) + pd.to_numeric(df_tit['DOCENTITITOLARIFEMMINE'], errors='coerce').fillna(0)
tit_prov = df_tit.groupby('PROVINCIA')['tot_tit'].sum().reset_index()

teach = pd.merge(sup_prov, tit_prov, on='PROVINCIA', how='inner')
teach['Regione'] = teach['PROVINCIA'].map(prov_name_to_regione)

teach_reg = teach.groupby('Regione').sum(numeric_only=True).reset_index()
teach_reg['Precariousness_Rate'] = teach_reg['tot_sup'] / (teach_reg['tot_sup'] + teach_reg['tot_tit']) * 100
teach_reg['Regione'] = teach_reg['Regione'].apply(clean_regione)

print("--- 2. Processing School Infrastructure Decay ---")
df_anag = pd.read_parquet(LOCAL_DATA / 'edilizia_scolastica' / 'EDIANAGRAFESTA202120242520250806.parquet')
df_sic = pd.read_parquet(LOCAL_DATA / 'edilizia_scolastica' / 'EDICONSICUREZZASTA202120242520250806.parquet')
df_amb = pd.read_parquet(LOCAL_DATA / 'edilizia_scolastica' / 'EDIAMBIENTESTA202120242520250806.parquet')

# Anagrafica map
anag_map = df_anag[['CODICEEDIFICIO', 'SIGLAPROVINCIA']].drop_duplicates()
anag_map['Regione'] = anag_map['SIGLAPROVINCIA'].map(provincia_to_regione)

# Sicurezza
sic = pd.merge(df_sic, anag_map, on='CODICEEDIFICIO', how='left')
sic['Regione'] = sic['Regione'].fillna('Sconosciuto').apply(clean_regione)

# Count total buildings per region
tot_bld = sic.groupby('Regione')['CODICEEDIFICIO'].nunique().reset_index().rename(columns={'CODICEEDIFICIO': 'Tot_Edifici'})

# Agibilita = SI
agib = sic[sic['CERTIFICATOSEGNALAZIONEAGIBILITA'] == 'SI']
agib_cnt = agib.groupby('Regione')['CODICEEDIFICIO'].nunique().reset_index().rename(columns={'CODICEEDIFICIO': 'Edifici_Agibili'})

bld_reg = pd.merge(tot_bld, agib_cnt, on='Regione', how='left').fillna(0)
bld_reg['No_Agibilita_Rate'] = ((bld_reg['Tot_Edifici'] - bld_reg['Edifici_Agibili']) / bld_reg['Tot_Edifici']) * 100

# Degrado urbano
amb = pd.merge(df_amb, anag_map, on='CODICEEDIFICIO', how='left')
amb['Regione'] = amb['Regione'].fillna('Sconosciuto').apply(clean_regione)
degrado = amb[amb['ZONAURBANADEGRADATA'] == 'SÌ']
deg_cnt = degrado.groupby('Regione')['CODICEEDIFICIO'].nunique().reset_index().rename(columns={'CODICEEDIFICIO': 'Edifici_Degrado'})
bld_reg = pd.merge(bld_reg, deg_cnt, on='Regione', how='left').fillna(0)
bld_reg['Degrado_Urbano_Rate'] = (bld_reg['Edifici_Degrado'] / bld_reg['Tot_Edifici']) * 100


print("--- 3. Merging with NEET Data ---")
df_neet = pd.read_csv(PROCESSED_DATA / 'istat_neet_regional_time_series.csv')
df_neet['Regione'] = df_neet['Regione'].apply(clean_regione)
neet_reg = df_neet[['Regione', 'istat_neet_15_29_serie_storica_tasso_pct']].rename(columns={'istat_neet_15_29_serie_storica_tasso_pct': 'NEET_Rate'})

# Final Merge
final = pd.merge(teach_reg[['Regione', 'Precariousness_Rate']], bld_reg[['Regione', 'No_Agibilita_Rate', 'Degrado_Urbano_Rate']], on='Regione', how='inner')
final = pd.merge(final, neet_reg, on='Regione', how='inner')

# Calculate an overall "Structural Decay Index" (Simple average of percentages)
final['Structural_Decay_Index'] = (final['Precariousness_Rate'] + final['No_Agibilita_Rate'] + final['Degrado_Urbano_Rate']) / 3

final = final.sort_values('NEET_Rate', ascending=False).round(2)
out_path = PROCESSED_DATA / 'holistic_educational_decay_index.csv'
final.to_csv(out_path, index=False)
print(f"Saved Universal Synthesis to {out_path}")
print("Teach Regions:", teach_reg['Regione'].unique())
print("Bld Regions:", bld_reg['Regione'].unique())
print("NEET Regions:", neet_reg['Regione'].unique())
print(final.head())
