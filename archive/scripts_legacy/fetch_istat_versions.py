"""Quick script to discover versions for target ISTAT dataflow IDs."""
import requests
import xml.etree.ElementTree as ET

ids = [
    "612_939","612_937","613_935","613_934","613_936",
    "34_201","34_202","34_727","34_219","498_1104",
    "52_607","52_912","183_464","28_185",
    "31_124","31_214","392_636","392_585",
    "150_908","151_914","56_259","56_189","56_190",
    "172_931","52_1044","47_850",
]

print(f"{'ID':<15} {'VER':<8} NAME")
print("-" * 80)
for did in ids:
    r = requests.get(
        f"https://sdmx.istat.it/SDMXWS/rest/dataflow/IT1/{did}",
        timeout=15, headers={"Accept": "application/xml"},
    )
    root = ET.fromstring(r.text)
    ver = "?"
    name_en = ""
    name_it = ""
    for el in root.iter():
        if "Dataflow" in el.tag and el.get("id") == did:
            ver = el.get("version", "?")
        if "Name" in el.tag and el.text:
            lang = el.get("{http://www.w3.org/XML/1998/namespace}lang", "")
            if lang == "en" and not name_en:
                name_en = el.text.strip()[:70]
            if lang == "it" and not name_it:
                name_it = el.text.strip()[:70]
    name = name_en or name_it
    print(f"{did:<15} {ver:<8} {name}")
