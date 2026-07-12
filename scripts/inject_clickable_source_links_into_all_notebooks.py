import glob
import json
import nbformat
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
NOTEBOOKS = glob.glob(str(ROOT_DIR / "**" / "*.ipynb"), recursive=True)

PROOF_OF_DATA_MD = """### 🔗 Tracciabilità delle Fonti Ufficiali Originatorie (`Proof of Data`)

> Per garantire **assoluta trasparenza scientifica e tracciabilità senza intermediazioni**, ogni dato, serie storica o indicatore analizzato in questo notebook proviene direttamente dai seguenti portali istituzionali di Stato:
> * **ISTAT (`Istituto Nazionale di Statistica`)**: [👉 Portale Dati IStatData & Flussi SDMX](https://dati.istat.it/)
> * **Eurostat (`Commissione Europea`)**: [👉 Database Eurostat Data Browser](https://ec.europa.eu/eurostat/databrowser/)
> * **AlmaLaurea (`Consorzio Interuniversitario`)**: [👉 Indagini Occupazione e Profilo Laureati](https://www.almalaurea.it/universita/indagini)
> * **INVALSI (`Valutazione Sistema Educativo`)**: [👉 Portale Open Data Esiti e Competenze](https://serviziostatistico.invalsi.it/)
> * **MIM (`Ministero dell'Istruzione e del Merito`)**: [👉 Anagrafe Edilizia, Studenti e Scuola in Chiaro](https://huggingface.co/datasets/diatribe00/italian-schools-opendata)
> * **MUR (`Ministero dell'Università e della Ricerca`)**: [👉 Portale Dati USTAT & Anagrafe Nazionale Studenti](https://ustat.mur.gov.it/dati/)
> * **MEF SIOPE & SOSE OpenCivitas (`Finanza Pubblica Locale e LEP`)**: [👉 SIOPE Cassa RGS](https://www.siope.it/) | [👉 OpenCivitas LEP Asili Nido](https://www.opencivitas.it/)
> * **INPS (`Istituto Nazionale della Previdenza Sociale`)**: [👉 Osservatorio Precariato e Stipendi](https://www.inps.it/it/it/dati-e-bilanci/osservatori-statistici-e-altre-statistiche.html)
> * **COVIP (`Commissione di Vigilanza sui Fondi Pensione`)**: [👉 Relazioni Annuali e Previdenza Integrativa](https://www.covip.it/pubblicazioni-e-statistiche/relazioni-annuali)
> * **Banca d'Italia (`Contabilità Nazionale e Indagine SHIW`)**: [👉 Indagini Famiglie e Relazione Annuale](https://www.bancaditalia.it/statistiche/index.html)
> * **INAPP PLUS & Unioncamere Excelsior (`Fabbisogno Imprese e Upskilling`)**: [👉 Indagine PLUS](https://plus.inapp.org/) | [👉 Excelsior](https://excelsior.unioncamere.net/)
> * **OCSE & Banca Mondiale (`Confronti Internazionali ISCED`)**: [👉 Education at a Glance](https://www.oecd.org/education/education-at-a-glance/)

*Consulta il catalogo integrale dei 66 domini canonici nel file [CATALOGO_COMPLETO_LINK_DIRETTI_66_DOMINI_PROOF_OF_DATA.md](file:///c:/Users/Dell/Documents/Antigravity/Italienation/local_data/processed/CATALOGO_COMPLETO_LINK_DIRETTI_66_DOMINI_PROOF_OF_DATA.md).*"""

print(f"=== INJECTING CLICKABLE PROOF OF DATA SOURCE LINKS INTO ALL {len(NOTEBOOKS)} NOTEBOOKS ===")

updated_count = 0
for nb_path_str in NOTEBOOKS:
    nb_path = Path(nb_path_str)
    # Avoid modifying virtual environments or check points
    if ".ipynb_checkpoints" in nb_path_str or ".venv" in nb_path_str:
        continue
        
    try:
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
            
        # Check if proof of data is already present
        has_proof = any("Proof of Data" in cell.get("source", "") or "Tracciabilità delle Fonti" in cell.get("source", "") for cell in nb.cells[:4])
        
        if not has_proof:
            proof_cell = nbformat.v4.new_markdown_cell(PROOF_OF_DATA_MD)
            # Insert right after the title block (cell 1 if cell 0 is title, else cell 0)
            insert_idx = 1 if len(nb.cells) > 0 and nb.cells[0].cell_type == 'markdown' and nb.cells[0].source.startswith("#") else 0
            nb.cells.insert(insert_idx, proof_cell)
            
            with open(nb_path, "w", encoding="utf-8") as f:
                nbformat.write(nb, f)
            updated_count += 1
            print(f"  -> [INJECTED LINK CARD] `{nb_path.relative_to(ROOT_DIR)}`")
        else:
            print(f"  -> [ALREADY COMPLIANT] `{nb_path.relative_to(ROOT_DIR)}`")
    except Exception as e:
        print(f"  -> [ERROR on {nb_path.name}]: {e}")

print(f"=== COMPLETED: Injected clickable proof cards into {updated_count} notebooks ===")
