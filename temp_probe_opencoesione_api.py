import requests
for url in ['https://opencoesione.gov.it/api','https://opencoesione.gov.it/api/','https://opencoesione.gov.it/it/api','https://opencoesione.gov.it/it/opendata/api','https://opencoesione.gov.it/it/opendata.json']:
    try:
        r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=30)
        print(url, r.status_code, r.headers.get('content-type','')[:60])
        print(r.text[:400])
    except Exception as e:
        print(url, 'ERR', e)
    print('---')
