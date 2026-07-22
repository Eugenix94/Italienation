with open('scripts/extract_command_center.py', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('"HuggingFace School Register", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata"', '"Ministero dell\'Istruzione (MIM)", "https://dati.istruzione.it/opendata/opendata/catalogo/"')
code = code.replace('"HuggingFace", "https://huggingface.co/datasets/diatribe00/italian-schools-opendata"', '"Ministero dell\'Istruzione (MIM)", "https://dati.istruzione.it/opendata/opendata/catalogo/"')

with open('scripts/extract_command_center.py', 'w', encoding='utf-8') as f:
    f.write(code)

print('Updated links in extract_command_center.py')
