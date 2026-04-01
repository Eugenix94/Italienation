import os
import requests
import pandas as pd

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "local_data", "MUR_iscritti"))
os.makedirs(OUT, exist_ok=True)

# Academic years to keep
YEARS = ["2023/24", "2024/25"]

# Resources from dati-ustat.mur.gov.it (Iscritti dataset)
RESOURCES = {
    "iscritti_per_anno": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/e76fcb62-22c5-4ff9-a425-e06f3d6f8330/download/01_iscrittixanno.csv",
    "iscritti_per_dimensione_ateneo": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/68bc6df4-d607-436c-ae73-484a7d99694f/download/01bis_iscrittixdimensioneateneo.csv",
    "iscritti_per_ateneo": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/32d26e28-a0b5-45f3-9152-6072164f3e63/download/02_iscrittixateneo.csv",
    "iscritti_per_gruppo": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/4534ed12-dd41-4eb3-9201-ce783fb51e7f/download/03_iscrittixgruppo.csv",
    "iscritti_per_tipologia_corso": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/f62e0f3b-5ee1-489a-a1d1-6794943a6408/download/04_iscrittixtipocorso.csv",
    "iscritti_per_classe": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/373294ff-b051-4ec1-996f-e52078640279/download/05_iscrittixclasse.csv",
    "iscritti_per_anno_nascita": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/07cce4d9-42a1-41e0-ba5d-0f9b0a21195d/download/06_iscrittixannonascita.csv",
    "iscritti_per_comune_residenza": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/eae4ee94-0797-41d2-b007-bc6dad3ef3e2/download/07_iscrittixresidenza.csv",
    "internazionali_per_anno": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/f0fb0a0a-02a6-44bb-a2b9-feadc9d05f16/download/08_iscrittiinternazionalixanno.csv",
    "internazionali_per_paese": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/d59f3379-7536-43c2-b6f8-deb808970503/download/09_iscrittiinternazionalixpaese.csv",
    "internazionali_per_ateneo": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/27ba8d3b-9a54-4a75-8798-2010bc7c205a/download/10_iscrittiinternazionalixateneo.csv",
    "internazionali_per_classe": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/69caceed-cab6-400e-a5c1-439323c9d5c4/download/11_iscrittiinternazionalixclasse.csv",
    "iscritti_per_anno_corso": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/b62d9430-ad67-4ea2-bf85-129f44b56530/download/12_iscrittixannocorso.csv",
    "iscritti_per_corso_2019_25": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/ad5a1516-ccd3-4eb8-a889-f584f04de578/download/13_iscrittixcorso.csv",
    "iscritti_in_sede_fuori_sede": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/349e58d7-6ea6-4b99-99cb-b8748fccbaf6/download/14c_iscrittixsedescuolasecondariasedecorso.csv",
    "iscritti_per_regione": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/42446e78-9baa-4c82-9c56-251ce43654f4/download/14b_iscrittixresidenzasedecorsoclasse.csv",
    "iscritti_per_provincia": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/b270ef1a-c219-48b1-8399-b1458e225d39/download/14a_iscrittixresidenzasedecorsogruppo.csv",
    "iscritti_fuori_corso": "https://dati-ustat.mur.gov.it/dataset/3dd9ca7f-9cc9-4a1a-915c-e569b181dbd5/resource/876d093a-f939-4193-bf21-5eaa7b340db5/download/19_iscrittixfuoricorso.csv",
}


def download_file(name, url):
    response = requests.get(url, stream=True, timeout=120)
    response.raise_for_status()
    local_path = os.path.join(OUT, f"{name}.csv")

    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return local_path


def filter_by_years(path):
    encodings = ["utf-8", "utf-8-sig", "cp1252", "iso-8859-1"]
    separators = [";", ","]
    df = None

    for enc in encodings:
        for sep in separators:
            try:
                df = pd.read_csv(path, sep=sep, encoding=enc, low_memory=False)
                if df is not None and not df.empty:
                    break
            except Exception:
                df = None
        if df is not None:
            break

    if df is None:
        raise ValueError(f"Could not read CSV file: {path}")

    year_cols = [c for c in df.columns if c.lower() in ["annoa", "anno_accademico", "anno", "anno_accademico_descrizione"]]
    if year_cols:
        col = year_cols[0]
        df = df[df[col].astype(str).isin(YEARS)]

    df.to_csv(path, index=False, encoding="utf-8")


def main():
    print(f"Downloading {len(RESOURCES)} MUR 'Iscritti' datasets to {OUT}")
    for name, url in RESOURCES.items():
        print(f"- {name}")
        try:
            local_path = download_file(name, url)
            filter_by_years(local_path)
            print(f"  saved and filtered: {local_path}")
        except requests.exceptions.HTTPError as e:
            print(f"  SKIPPED {name}: HTTP error {e}")
        except Exception as e:
            print(f"  ERROR {name}: {e}")

    print("Done: datasets downloaded/filtered (some resources may be skipped on error)")


if __name__ == "__main__":
    main()
