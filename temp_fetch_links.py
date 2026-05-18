import requests
import re
from bs4 import BeautifulSoup
urls = [
    'https://www.istat.it/it/archivio/lavoro+sommerso',
    'https://www.istat.it/it/archivio/mobilita+sociale',
    'https://geo.agcom.it/opendata',
    'https://opencoesione.gov.it/it/opendata/',
    'https://www.interno.gov.it/it/stampa-e-comunicazione/dati-e-statistiche/crimine-italia-analisi-e-dati-pubblica-sicurezza'
]
for url in urls:
    print('URL=', url)
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
        print('STATUS', r.status_code, 'LEN', len(r.text))
        soup = BeautifulSoup(r.text, 'html.parser')
        links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            txt = ' '.join(a.get_text(' ', strip=True).split())
            if re.search(r'csv|xls|xlsx|zip|data|download|open data|opendata|SDMX|sdmx', href, re.I) or re.search(r'csv|xls|xlsx|zip|download|open data|opendata|SDMX|sdmx', txt, re.I):
                links.append((txt, href))
        for t, h in links[:20]:
            print('   ', t[:120], '=>', h)
    except Exception as e:
        print('ERR', e)
    print()
