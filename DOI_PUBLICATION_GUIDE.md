# 🚀 OSF / Zenodo DOI Publication Protocol

To formalize Phase 1 and mint your rigorous academic DOI, follow these exact steps to publish the "Italienation: Educational Black Box" compendium.

## Step 1: Prepare the Archive
Because the repository contains 877 data files, it is best practice to bundle the data directory before uploading it to Zenodo, while keeping the documentation loose for readers to view in the browser.

1. Open your terminal in the repository root (`C:\Users\Dell\Documents\Antigravity\Italienation`).
2. Compress the data directory:
   - On Windows (PowerShell): `Compress-Archive -Path local_data -DestinationPath Italienation_Data_Archive.zip`
   - Alternatively, you can zip it manually via the Windows File Explorer.

## Step 2: Upload to Zenodo (or OSF)
1. Navigate to **Zenodo.org** (or osf.io) and log in with your ORCID or GitHub account.
2. Click **"New Upload"**.
3. **Drag and Drop** the following files into the upload queue:
   - `Italienation_Data_Archive.zip`
   - `datapackage.json` (The Frictionless registry)
   - `README.md` (The Master Abstract)
   - `DATA_TRACEABILITY_MATRIX.md` (Crucial for reproducibility proof)

## Step 3: Fill the Metadata Fields
Copy and paste the exact metadata to ensure academic rigor:

*   **Upload Type**: Dataset (or Publication -> Report, depending on your preference)
*   **Title**: Italienation: The Cybernetic Machinery of the Italian Educational System
*   **Creators**: [Your Name / ORCID]
*   **Description**: *Open the `README.md` in your text editor and copy the entire text starting from the "Abstract" section.*
*   **Access Right**: Open Access
*   **License**: Creative Commons Attribution 4.0 International (CC-BY 4.0). *(This is standard for Open Science and ensures you are cited).*
*   **Keywords**: `Education`, `Italy`, `POSIWID`, `Socio-Economic Reproduction`, `NEET`, `Brain Drain`, `Cybernetics`, `Open Data`

## Step 4: Mint the DOI
1. Review the files and metadata.
2. Click **Publish**.
3. Zenodo will instantly generate a permanent **DOI** (Digital Object Identifier) for your dataset. 

Once this DOI is minted, Phase 1 is officially immortalized in the scientific record. We can then begin Phase 2 (The Scrollytelling UI) and reference this exact DOI in the web application.
