#!/usr/bin/env python
import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path('local_data')
LDT_ROOT = ROOT / 'MinIstruzione' / 'LibriDiTesto'
cols = ['CODICESCUOLA','CODICEISBN','DISCIPLINA','TITOLO','EDITORE','PREZZO']

def parse_price(s):
    try:
        return float(str(s).strip().replace(',','.'))
    except:
        return np.nan

# Load only needed columns
frames = []
for f in sorted(LDT_ROOT.glob('*.csv')):
    try:
        df = pd.read_csv(f, sep=',', encoding='utf-8-sig', usecols=cols, low_memory=False)
        frames.append(df)
    except Exception as e:
        print(f'skipped {f.name}: {e}')

books = pd.concat(frames, ignore_index=True)
books['PREZZO_NUM'] = books['PREZZO'].apply(parse_price)

# 1) Unique ISBNs per discipline
books_per_subject = books.groupby('DISCIPLINA')['CODICEISBN'].nunique().sort_values(ascending=False)
print('\nTop 20 disciplines by unique ISBN count:')
print(books_per_subject.head(20).to_string())

# 2) Schools adopting each ISBN
schools_per_isbn = books.groupby('CODICEISBN')['CODICESCUOLA'].nunique().sort_values(ascending=False)

# Gather meta for top ISBNs
top_isbns = schools_per_isbn.head(20)
meta = books.groupby('CODICEISBN').agg(
    TITOLO=('TITOLO', lambda s: s.dropna().iloc[0] if len(s.dropna())>0 else ''),
    EDITORE=('EDITORE', lambda s: s.dropna().iloc[0] if len(s.dropna())>0 else ''),
    PREZZO_AVG=('PREZZO_NUM','mean')
)

print('\nTop 20 ISBNs by number of unique schools adopting:')
for isbn, n in top_isbns.items():
    if isbn in meta.index:
        row = meta.loc[isbn]
        price = row['PREZZO_AVG']
        price_str = f"€{price:.2f}" if not pd.isna(price) else 'NA'
        title = (row['TITOLO'] or '').replace('\n',' ')[:120]
        editor = (row['EDITORE'] or '')
    else:
        price_str = 'NA'
        title = ''
        editor = ''
    print(f"{isbn} | {int(n):,} schools | {price_str} | {editor} | {title}")

print('\nSchools-per-ISBN distribution (describe):')
print(schools_per_isbn.describe().round(1).to_string())
