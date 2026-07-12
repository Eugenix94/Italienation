import os
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

print("=== STARTING COMPLETE OSF/ZENODO & FAIR STANDARD DIRECTORY REORGANIZATION ===")

# 1. Create top-level directories
dirs_to_create = [
    "processed_data",
    "notebooks",
    "docs",
    "scripts",
    "archive/scripts_legacy",
    "archive/notebooks_legacy",
    "web"
]

for d in dirs_to_create:
    (ROOT_DIR / d).mkdir(parents=True, exist_ok=True)
    print(f"  -> Created/verified directory: `{d}`")

# 2. Move local_data/processed -> processed_data/
local_processed = ROOT_DIR / "local_data" / "processed"
processed_data = ROOT_DIR / "processed_data"

if local_processed.exists():
    print("  -> Moving contents of `local_data/processed/` to root `processed_data/`...")
    for item in local_processed.iterdir():
        dest = processed_data / item.name
        if not dest.exists():
            shutil.move(str(item), str(dest))
            print(f"     [MOVED] {item.name} -> processed_data/{item.name}")
        else:
            # If already exists or updating, overwrite/move
            if item.is_file():
                shutil.copy2(str(item), str(dest))
                item.unlink()

# Also check data_processed and api_data if they contain CSVs/JSONs to merge into processed_data or local_data
for old_data_dir in ["data_processed", "api_data"]:
    old_p = ROOT_DIR / old_data_dir
    if old_p.exists() and old_p.is_dir():
        print(f"  -> Merging legacy `{old_data_dir}/` files...")
        for item in old_p.iterdir():
            if item.is_file() and item.suffix in [".csv", ".json"]:
                dest = processed_data / item.name
                if not dest.exists():
                    shutil.copy2(str(item), str(dest))
        # Move directory itself to archive
        shutil.move(str(old_p), str(ROOT_DIR / "archive" / old_data_dir))

# 3. Move major documentation monographs to docs/
docs_dir = ROOT_DIR / "docs"
monographs_to_docs = [
    "LA_SINTESI_SCIENTIFICA_E_CAUSAL_STRUTTURALE_DEFINITIVA_66_DOMINI.md",
    "CATALOGO_COMPLETO_LINK_DIRETTI_66_DOMINI_PROOF_OF_DATA.md",
    "CERTIFICAZIONE_SCIENTIFICA_DI_GIUSTIFICABILITA_E_SATURAZIONE_66_DOMINI.md",
    "SCIENTIFIC_OPEN_DATA_PORTAL_HANDBOOK.md",
    "EXHAUSTIVE_EMPIRICAL_SYNTHESIS_MATRIX_AND_PROOF_OF_AXIOMS.md"
]

for mono in monographs_to_docs:
    src = processed_data / mono
    if src.exists():
        dest = docs_dir / mono
        shutil.copy2(str(src), str(dest))
        print(f"     [DOC MOVED] processed_data/{mono} -> docs/{mono}")

# Also check if HOLISTIC_CRITICAL_DATA_AUDIT.md and other root docs should be copied/linked to docs/
for root_doc in ["HOLISTIC_CRITICAL_DATA_AUDIT.md", "MISSING_DATA_AUDIT_AND_RESEARCH_ROADMAP.md"]:
    src = ROOT_DIR / root_doc
    if src.exists():
        shutil.copy2(str(src), str(docs_dir / root_doc))

# 4. Rename & Consolidate Notebooks cleanly into notebooks/
notebooks_dir = ROOT_DIR / "notebooks"
notebook_mapping = {
    "capstone_oted_epistemological_reconstruction_66_domains.ipynb": "00_master_capstone_oted_66_domains.ipynb",
    "Final_Analysis/italienation_holistic_master_analysis.ipynb": "01_holistic_master_statistical_analysis.ipynb",
    "Notebooks/italy_openpolis_neet_poverty.ipynb": "02_origin_early_childhood_and_educational_poverty.ipynb",
    "Notebooks/italy_textbooks_schools_territory.ipynb": "03_origin_textbook_burden_and_household_spending.ipynb",
    "Notebooks/italy_tripartite_school_system.ipynb": "04_tracking_tripartite_system_provenance.ipynb",
    "Notebooks/italy_middle_to_upper_transition_analysis.ipynb": "05_tracking_middle_to_upper_transition_and_barriers.ipynb",
    "Notebooks/italy_bocciatura_repeaters_full_analysis_v2.ipynb": "06_tracking_repeaters_and_implicit_dropout.ipynb",
    "Notebooks/neet_italy_analysis.ipynb": "07_transition_neet_youth_unemployment_panel.ipynb",
    "Notebooks/italy_oecd_triangle_mobility_analysis.ipynb": "08_transition_social_mobility_and_intermittency.ipynb",
    "Notebooks/education_spending_outcomes.ipynb": "09_destination_fiscal_landscape_and_siope_delays.ipynb",
    "Notebooks/territorial_expenditure_analysis.ipynb": "10_destination_territorial_expenditure_and_deficits.ipynb",
    "Notebooks/italy_capital_formation_h_c_i.ipynb": "11_destination_tfp_stagnation_and_human_capital.ipynb",
    "Notebooks/07_geospatial_tripartite_distribution.ipynb": "12_geospatial_territorial_maps_nuts2_nuts3.ipynb",
    "Notebooks/openEURYDICE_Italy_Summary.ipynb": "13_international_benchmarks_eurydice_oecd_wb.ipynb",
    "Notebooks/data_inventory_comprehensive.ipynb": "14_data_inventory_and_schematic_explorer.ipynb"
}

print("  -> Renaming and consolidating active notebooks into `notebooks/`...")
for src_rel, dest_name in notebook_mapping.items():
    src_p = ROOT_DIR / src_rel
    dest_p = notebooks_dir / dest_name
    if src_p.exists():
        shutil.copy2(str(src_p), str(dest_p))
        print(f"     [NOTEBOOK RENAMED] {src_rel} -> notebooks/{dest_name}")

# Move remaining notebooks / legacy folders into archive/notebooks_legacy/
for leg_nb_dir in ["Notebooks", "02_Interactive_Notebooks_and_Visuals", "Final_Analysis"]:
    old_nb_p = ROOT_DIR / leg_nb_dir
    if old_nb_p.exists() and old_nb_p.is_dir():
        shutil.move(str(old_nb_p), str(ROOT_DIR / "archive" / "notebooks_legacy" / leg_nb_dir))
        print(f"     [ARCHIVED LEGACY FOLDER] {leg_nb_dir} -> archive/notebooks_legacy/{leg_nb_dir}")

# 5. Clean up root temporary scripts (temp_*.py, temp_*.xml, temp_*.txt)
print("  -> Cleaning root directory temporary probe files into `archive/scripts_legacy/`...")
for root_item in ROOT_DIR.iterdir():
    if root_item.is_file() and (root_item.name.startswith("temp_") or root_item.name.startswith("fast_scan_")):
        shutil.move(str(root_item), str(ROOT_DIR / "archive" / "scripts_legacy" / root_item.name))

# Move non-core scripts in scripts/ to archive/scripts_legacy/ if they are temporary/legacy
scripts_dir = ROOT_DIR / "scripts"
core_scripts = [
    "build_and_integrate_6_final_uncovered_sources.py",
    "build_exhaustive_empirical_synthesis_matrix.py",
    "build_master_capstone_monograph.py",
    "certify_60_domains_justifiable_completeness.py",
    "verify_and_export_66_direct_links_catalog.py",
    "inject_clickable_source_links_into_all_notebooks.py",
    "reorganize_repo_to_osf_zenodo_standards.py"
]

for sc in scripts_dir.iterdir():
    if sc.is_file() and sc.name.endswith(".py") and sc.name not in core_scripts:
        # Move to archive/scripts_legacy/
        dest = ROOT_DIR / "archive" / "scripts_legacy" / sc.name
        if not dest.exists():
            shutil.move(str(sc), str(dest))

print("=== REORGANIZATION COMPLETE: Spotless OSF/Zenodo & FAIR Standard Directory Structure Achieved! ===")
