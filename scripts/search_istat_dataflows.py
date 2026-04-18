"""
Search ISTAT SDMX catalogue for dataflows matching keywords.
Used to find updated dataflow IDs for datasets that have gaps.
"""
import requests

BASE_URL = "https://sdmx.istat.it/SDMXWS/rest"

SEARCH_TERMS = [
    "povert",    # poverty new series
    "spese",     # household spending
    "consumi",   # consumption/spending
    "istruzione", # education
    "abbandono",  # early school leavers
    "asilo",     # childcare/nursery
    "nido",      # nursery
    "scuola",    # schools
]

def get_all_dataflows():
    url = f"{BASE_URL}/dataflow/IT1/all/latest"
    headers = {"Accept": "application/vnd.sdmx.structure+xml;version=2.1"}
    r = requests.get(url, timeout=60, headers=headers)
    r.raise_for_status()
    return r.text

def search_dataflows(xml_text: str, terms: list[str]) -> list[dict]:
    import xml.etree.ElementTree as ET
    root = ET.fromstring(xml_text)

    ns = {
        "str": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure",
        "com": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common",
        "mes": "http://www.sdmx.org/resources/sdmxml/schemas/v2_1/message",
    }

    results = []
    for df in root.iter("{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}Dataflow"):
        flow_id = df.get("id", "")
        version = df.get("version", "")
        # Get name text
        names = df.findall(".//{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}Name")
        name_it = ""
        name_en = ""
        for n in names:
            lang = n.get("{http://www.w3.org/XML/1998/namespace}lang", "")
            val = (n.text or "").strip()
            if lang == "it":
                name_it = val
            elif lang == "en":
                name_en = val

        combined = (name_it + " " + name_en + " " + flow_id).lower()
        for term in terms:
            if term.lower() in combined:
                results.append({
                    "id": flow_id,
                    "version": version,
                    "name_it": name_it,
                    "name_en": name_en,
                    "matched_term": term,
                })
                break  # avoid duplicates per dataflow

    return sorted(results, key=lambda x: x["matched_term"] + x["id"])


if __name__ == "__main__":
    print("Fetching ISTAT dataflow catalogue...")
    xml_text = get_all_dataflows()
    print(f"Catalogue fetched ({len(xml_text):,} bytes). Searching...")

    matches = search_dataflows(xml_text, SEARCH_TERMS)
    print(f"\nFound {len(matches)} matching dataflows:\n")
    print(f"{'ID':<12} {'Ver':<6} {'Term':<14} {'Name (IT)'}")
    print("-" * 90)
    for m in matches:
        print(f"{m['id']:<12} {m['version']:<6} {m['matched_term']:<14} {m['name_it'][:60]}")
