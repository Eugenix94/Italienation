import urllib.request
import re
import sys

url = 'https://www.youtube.com/watch?v=Zfq6VzcH42Y'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
        title_match = re.search(r'<title>(.*?)</title>', html)
        if title_match:
            print('TITLE:', title_match.group(1))
        
        desc_match = re.search(r'"shortDescription":"(.*?)"', html)
        if desc_match:
            print('DESC:', desc_match.group(1).encode('utf-8').decode('unicode_escape'))
        else:
            print("Description not found easily in JSON.")
except Exception as e:
    print('Error:', e)
