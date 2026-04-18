import pandas as pd
path = 'local_data/MUR/MUR_iscritti/iscritti_per_anno.csv'
print('path', path)
df = None
for enc in ['utf-8','utf-8-sig','cp1252','iso-8859-1']:
    try:
        df = pd.read_csv(path, sep=';', encoding=enc, low_memory=False)
        print('OK enc', enc)
        break
    except Exception as e:
        print('fail', enc, type(e).__name__, e)

if df is None:
    raise SystemExit('no df')

print('columns', df.columns.tolist())
print(df.head())
for c in df.columns:
    if 'anno' in c.lower():
        print('year col', c, df[c].dropna().astype(str).unique()[:20])
