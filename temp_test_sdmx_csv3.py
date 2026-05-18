import requests
bases = ['https://esploradati.istat.it/SDMXWS/rest', 'https://sdmx.istat.it/SDMXWS/rest']
flows = [('172_931','1.0'), ('52_1203','1.0'), ('151_914','1.2')]
for base in bases:
    print('BASE', base)
    for fid, ver in flows:
        url = f'{base}/data/IT1,{fid},{ver}/all?format=SDMX-CSV'
        try:
            r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=60)
            print(' ', fid, r.status_code, len(r.text))
            if r.status_code != 200:
                print('   ', r.text[:200])
        except Exception as e:
            print('   ERR', fid, e)
    print('---')
