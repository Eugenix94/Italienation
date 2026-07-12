import os
import requests
import csv
import re
from urllib.parse import urlparse

BASE_OUTPUT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'local_data', 'MUR'))
os.makedirs(BASE_OUTPUT, exist_ok=True)

DATASET_SLUGS = [
    'laureati',
    '2024-contribuzione-e-interventi-atenei',
    '2025-collegi-universitari',
    '2025-contribuzione-e-interventi-afam',
    'serie-storica-sul-personale-universitario',
    'dati-per-bilancio-di-genere',
    'diplomati-afam-serie-storica',
    'iscritti-afam-serie-storica',
    '2025-diritto-allo-studio-universitario-dsu-regionale',
    'immatricolati'
]

CKAN_BASE = 'https://dati-ustat.mur.gov.it'
HEADERS = {
    'User-Agent': 'python-requests/MUR-API-downloader (contact: you@example.com)'
}


def sanitize_name(name: str) -> str:
    name = re.sub(r"[^\w\s-]", "", name)
    name = re.sub(r"\s+", "_", name).strip("_")
    return name[:120] or 'dataset'


def get_dataset_info(slug: str):
    url = f'{CKAN_BASE}/api/3/action/package_show'
    r = requests.get(url, params={'id': slug}, headers=HEADERS, timeout=60)
    r.raise_for_status()
    payload = r.json()
    if not payload.get('success'):
        raise RuntimeError(f'Package show failed {slug}')
    return payload['result']


def download_resource(resource, out_folder):
    if resource.get('format', '').lower() != 'csv':
        return None

    csv_url = resource.get('url') or resource.get('package_url')
    if not csv_url:
        return None

    parsed = urlparse(csv_url)
    file_name = os.path.basename(parsed.path) or sanitize_name(resource.get('name', 'resource'))
    if not file_name.lower().endswith('.csv'):
        file_name = f'{file_name}.csv'

    dest_path = os.path.join(out_folder, file_name)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with requests.get(csv_url, headers=HEADERS, stream=True, timeout=120) as resp:
        resp.raise_for_status()
        with open(dest_path, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

    return dest_path


def main():
    manifest = []

    for slug in DATASET_SLUGS:
        print('Processing dataset', slug)
        try:
            info = get_dataset_info(slug)
        except Exception as e:
            print('  ERROR fetching dataset info', e)
            manifest.append([slug, '', '', '', 'ERROR', str(e)])
            continue

        dataset_title = info.get('title', slug)
        folder = os.path.join(BASE_OUTPUT, sanitize_name(slug))
        os.makedirs(folder, exist_ok=True)

        resources = info.get('resources', []) or []
        if not resources:
            print('  No resources found for', slug)
            manifest.append([slug, dataset_title, '', '', 'NO_RESOURCES', ''])
            continue

        for res in resources:
            if not res.get('format') or res.get('format').lower() != 'csv':
                continue
            try:
                local_path = download_resource(res, folder)
                status = 'OK' if local_path else 'SKIPPED'
                print('  downloaded', res.get('name'), '->', local_path)
                manifest.append([slug, dataset_title, res.get('name', ''), res.get('url',''), status, ''])
            except Exception as e:
                print('  ERROR', res.get('name', ''), e)
                manifest.append([slug, dataset_title, res.get('name', ''), res.get('url',''), 'ERROR', str(e)])

    manifest_path = os.path.join(BASE_OUTPUT, 'mur_dataset_manifest.csv')
    with open(manifest_path, 'w', newline='', encoding='utf-8') as mf:
        w = csv.writer(mf)
        w.writerow(['slug', 'title', 'resource_name', 'resource_url', 'status', 'error'])
        w.writerows(manifest)

    print('Done. Manifest at', manifest_path)


if __name__ == '__main__':
    main()
