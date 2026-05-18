import requests
import xml.etree.ElementTree as ET
BASE_URL = 'https://sdmx.istat.it/SDMXWS/rest'
url = f'{BASE_URL}/dataflow/IT1/all/latest'
headers = {'Accept': 'application/vnd.sdmx.structure+xml;version=2.1'}
r = requests.get(url, timeout=120, headers=headers)
r.raise_for_status()
root = ET.fromstring(r.text)
terms = ['sommerso', 'informale', 'informal', 'sociale', 'mobilita', 'mobilità', 'povertà', 'pobrezza', 'occupazione', 'lavoro', 'emigrazione']
print('total dataflows', len(list(root.iter('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Dataflow'))))
for df in root.iter('{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Dataflow'):
    flow_id = df.get('id', '')
    version = df.get('version', '')
    names = []
    for n in df.findall('.//{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Name'):
        lang = n.get('{http://www.w3.org/XML/1998/namespace}lang', '')
        names.append((lang, (n.text or '').strip()))
    combined = ' '.join([t for _, t in names]).lower() + ' ' + flow_id.lower()
    for term in terms:
        if term in combined:
            print(term, flow_id, version, names)
            break
