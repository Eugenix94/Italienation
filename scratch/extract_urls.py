import os, re
import json

d = r'C:\Users\Dell\Documents\Antigravity\Italienation\scripts'
urls = {}
for f in os.listdir(d):
    if f.endswith('.py'):
        try:
            with open(os.path.join(d, f), encoding='utf-8') as file:
                content = file.read()
                found_urls = set(re.findall(r'https?://[^\s\"\'\\]+', content))
                if found_urls:
                    urls[f] = list(found_urls)
        except Exception as e:
            print(f"Error reading {f}: {e}")

with open(r'C:\Users\Dell\Documents\Antigravity\Italienation\scratch\extract_urls.json', 'w') as out:
    json.dump(urls, out, indent=4)
print("Extracted URLs.")
