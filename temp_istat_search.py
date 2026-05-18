import requests
from bs4 import BeautifulSoup

def scan(url):
    print('URL=', url)
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
    print('STATUS', r.status_code, 'LEN', len(r.text))
    soup = BeautifulSoup(r.text, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        txt = ' '.join(a.get_text(' ', strip=True).split())
        if any(k in href.lower() for k in ['csv','xlsx','xls','zip','json','sdmx','open-data','download']) or any(k in txt.lower() for k in ['csv','xlsx','xls','zip','json','sdmx','open data','download']):
            print('   ', txt[:120], '=>', href)
    print('\n---\n')

for q in ['lavoro+sommerso','mobilita+sociale','lavoro sommerso','mobilita sociale']:
    scan(f'https://www.istat.it/it/ricerca?q={q}')
    scan(f'https://www.istat.it/it/archivio?search={q}')
