import urllib.request
import json
import urllib.parse

url = 'https://dati.gov.it/api/3/action/package_search?q=' + urllib.parse.quote('scuole statali province autonome')
req = urllib.request.urlopen(url)
data = json.loads(req.read())

results = []
for r in data['result']['results']:
    csv_urls = [r2['url'] for r2 in r['resources'] if r2['format'].lower() == 'csv']
    if csv_urls:
        results.append({
            'title': r['title'],
            'url': csv_urls[0]
        })

print(json.dumps(results, indent=2))
