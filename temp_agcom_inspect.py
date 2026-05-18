import requests
r = requests.get('https://geo.agcom.it/opendata', headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
print(r.status_code)
text = r.text
for token in ['zip','csv','xls','xlsx','json','reportistica','open maps','tabulati','download','opendata']:
    if token in text.lower():
        print('FOUND', token)
print('--- raw snippet ---')
for word in ['download','tabulati','csv','zip','reportistica','open maps']:
    i = text.lower().find(word)
    if i != -1:
        print(word, repr(text[max(0,i-100):i+200]))
