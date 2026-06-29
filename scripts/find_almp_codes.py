import requests
import xml.etree.ElementTree as ET

ESTAT_DF = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow"
print("Fetching Eurostat Dataflows...")
r = requests.get(ESTAT_DF, timeout=30)
if r.status_code == 200:
    root = ET.fromstring(r.text)
    ids = []
    for elem in root.iter():
        eid = elem.attrib.get("id")
        if eid and 'lmp' in eid.lower():
            ids.append(eid)
    print("Found LMP related dataflows:", set(ids))
else:
    print("Failed to fetch dataflows:", r.status_code)
