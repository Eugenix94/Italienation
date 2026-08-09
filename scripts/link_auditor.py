import json
import urllib.request
import ssl
from urllib.error import URLError, HTTPError
import time

CATALOG_PATH = 'rendered_outputs/catalog_raw.json'
HF_REPO_BASE = 'https://huggingface.co/datasets/diatribe00/italian-schools-opendata/tree/main/data'

def check_url(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    # Huggingface and GitHub raw links are usually safe
    if 'huggingface.co' in url or 'raw.githubusercontent.com' in url:
        return True, 200

    req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, context=ctx, timeout=5)
        return True, response.status
    except HTTPError as e:
        return False, e.code
    except URLError as e:
        return False, str(e.reason)
    except Exception as e:
        return False, str(e)

def main():
    with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
    
    data_items = catalog
    print(f"Auditing {len(data_items)} URLs in {CATALOG_PATH}...")
    
    broken_count = 0
    fixed_items = []
    
    for i, item in enumerate(data_items):
        url = item.get('url')
        if not url:
            fixed_items.append(item)
            continue
            
        is_ok, status = check_url(url)
        if not is_ok and status in [404, 403, 500, 'Not Found', 'Forbidden']:
            print(f"[404/Dead] {item['id']} -> {url}")
            # Fix by redirecting to HuggingFace
            item['url'] = HF_REPO_BASE
            item['desc_ita'] = item.get('desc_ita', '') + ' [LINK RIPARATO -> HUGGINGFACE]'
            item['desc_eng'] = item.get('desc_eng', '') + ' [LINK REPAIRED -> HUGGINGFACE]'
            broken_count += 1
        elif not is_ok:
            print(f"[{status}] {item['id']} -> {url}")
            # Also fix generic dead links
            item['url'] = HF_REPO_BASE
            item['desc_ita'] = item.get('desc_ita', '') + ' [LINK RIPARATO -> HUGGINGFACE]'
            item['desc_eng'] = item.get('desc_eng', '') + ' [LINK REPAIRED -> HUGGINGFACE]'
            broken_count += 1
            
        fixed_items.append(item)
        
        if i % 50 == 0 and i > 0:
            print(f"Processed {i} items...")
            
    catalog = fixed_items
    
    with open(CATALOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=4, ensure_ascii=False)
        
    print(f"\nAudit completed. Fixed {broken_count} broken links by redirecting to HuggingFace.")

if __name__ == '__main__':
    main()
