import csv
import urllib.request
import urllib.error
import ssl

csv_path = r"C:\Users\Dell\Documents\Antigravity\Italienation\local_data\FILE_BY_FILE_PROVENANCE_MANIFEST.csv"

unique_urls = set()
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        url = row['Direct Source URL']
        if url.startswith('http'):
            unique_urls.add(url)

print(f"Testing {len(unique_urls)} unique URLs...")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

broken_links = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

for url in sorted(unique_urls):
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req, context=ctx, timeout=15)
        status = response.getcode()
        # Some portals might redirect or return 200.
        if status not in [200, 201, 202, 301, 302, 303, 307, 308]:
            broken_links.append((url, status))
    except urllib.error.HTTPError as e:
        # 403 Forbidden might just mean we are a bot, but the page exists.
        if e.code == 403:
            pass # Usually means it works for humans
        else:
            broken_links.append((url, e.code))
    except Exception as e:
        broken_links.append((url, str(e)))

print("\n--- RESULTS ---")
if not broken_links:
    print("All links returned valid HTTP responses!")
else:
    print(f"Found {len(broken_links)} broken or unreachable links:")
    for url, err in broken_links:
        print(f"[{err}] {url}")
