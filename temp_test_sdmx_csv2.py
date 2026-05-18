import requests
flows = [
    ('172_931','1.0'),
    ('52_1203','1.0'),
    ('151_914','1.2'),
    ('150_915','1.2'),
    ('34_201','1.0'),
    ('34_202','1.0')
]
for fid, ver in flows:
    url = f'https://sdmx.istat.it/SDMXWS/rest/data/IT1,{fid},{ver}/all?format=SDMX-CSV'
    print(url)
    try:
        r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=60)
        print(' status', r.status_code, 'len', len(r.text))
        print(r.text[:400])
    except Exception as e:
        print(' ERR', e)
    print('---')
