import requests
flows = [
    ('47_850_DF_DCIS_SERVSOCEDU1_1','1.0'),
    ('47_850_DF_DCIS_SERVSOCEDU1_2','1.0'),
    ('47_850_DF_DCIS_SERVSOCEDU1_3','1.0'),
    ('47_850_DF_DCIS_SERVSOCEDU1_5','1.0'),
    ('47_850_DF_DCIS_SERVSOCEDU1_6','1.0'),
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
