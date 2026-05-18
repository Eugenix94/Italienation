import requests, xml.etree.ElementTree as ET
BASE_URL = 'https://sdmx.istat.it/SDMXWS/rest'
for endpoint in ['/dataflow/IT1/all','/dataflow/IT1']: 
    url = BASE_URL + endpoint
    print('URL', url)
    try:
        r = requests.get(url, timeout=120, headers={'Accept':'application/vnd.sdmx.structure+xml;version=2.1'})
        print(' status', r.status_code, 'len', len(r.text))
        if r.status_code == 200:
            root = ET.fromstring(r.text)
            print(' dataflows', len(list(root.iter('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Dataflow'))))
            break
    except Exception as e:
        print(' error', e)
