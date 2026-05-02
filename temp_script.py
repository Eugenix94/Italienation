import requests, sys, zipfile, io

sys.stdout.reconfigure(encoding="utf-8")

s = requests.Session()
h = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# Get school codes from anagrafica
url_anag = "https://www.siope.it/Siope/documenti/siope2/open/last/SIOPE_ANAGRAFICHE.zip"
r_anag = s.get(url_anag, headers=h, timeout=30)
zf_anag = zipfile.ZipFile(io.BytesIO(r_anag.content))

school_codes = set()
school_info = {}
for name in zf_anag.namelist():
    if "ENTI_SIOPE" in name:
        content = zf_anag.open(name).read().decode("utf-8", errors="replace")
        for line in content.strip().split("\n"):
            parts = [p.strip('"') for p in line.split(",")]
            if len(parts) >= 9 and parts[8] == "ENTI_VOL_FIN_IS":
                school_codes.add(parts[0])
                school_info[parts[0]] = parts[4]  # name
        break

print(f"School codes loaded: {len(school_codes)}")

# Download 2026 USCITE and count matching rows
url = "https://www.siope.it/Siope/documenti/siope2/open/last/SIOPE_USCITE.2026.zip"
print("Streaming USCITE 2026...")
r = s.get(url, headers=h, timeout=120, stream=True)
data = b"".join(r.iter_content(65536))
zf = zipfile.ZipFile(io.BytesIO(data))

csv_name = zf.namelist()[0]
content = zf.open(csv_name).read().decode("utf-8", errors="replace")
lines = content.strip().split("\n")
print(f"Total rows in 2026 USCITE: {len(lines):,}")

# Filter for schools - check both 9-digit codes and 15-digit codes (first 9 chars)
school_rows = []
for line in lines:
    parts = [p.strip('"') for p in line.strip().split(",")]
    if len(parts) < 5:
        continue
    ente = parts[0].strip('"')
    # Entity code can be 9 chars or 15 chars (entity+sub)
    code9 = ente[:9] if len(ente) >= 9 else ente
    if code9 in school_codes or ente in school_codes:
        school_rows.append(parts)

print(f"School rows in 2026 USCITE: {len(school_rows):,}")
if school_rows:
    print(f"\nFirst 5 school rows:")
    for row in school_rows[:5]:
        ente = row[0][:9]
        name = school_info.get(ente, school_info.get(row[0], "?"))
        print(f"  {row[0]}, {row[1]}, mese={row[2]}, cod={row[3]}, amount={int(row[4])/100:.2f}€  [{name[:50]}]")




