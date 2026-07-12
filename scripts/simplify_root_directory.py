import os
import shutil
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

print("=== STARTING ULTRA-CLEAN ROOT DIRECTORY SIMPLIFICATION ===")

# 1. Ensure core directories exist
core_dirs = ["local_data", "processed_data", "notebooks", "docs", "scripts", "web", "archive"]
for d in core_dirs:
    (ROOT_DIR / d).mkdir(parents=True, exist_ok=True)

# 2. Move extra markdown files from root to docs/
md_to_docs = [
    "ACADEMIC_AND_GRANT_STRATEGY.md",
    "ANPAL_REPLACEMENT_STRATEGY.md",
    "DATASET_STATISTICAL_CONNECTIONS.md",
    "HOLISTIC_CRITICAL_DATA_AUDIT.md",
    "MISSING_DATA_AUDIT_AND_RESEARCH_ROADMAP.md"
]
for md in md_to_docs:
    src = ROOT_DIR / md
    if src.exists():
        dest = ROOT_DIR / "docs" / md
        shutil.move(str(src), str(dest))
        print(f"  [MOVED TO DOCS] {md} -> docs/{md}")

# 3. Move web files (`index.html`, `netlify.toml`) to web/ if they are sitting in root
for wf in ["index.html", "netlify.toml"]:
    src = ROOT_DIR / wf
    if src.exists():
        dest = ROOT_DIR / "web" / wf
        if not dest.exists():
            shutil.move(str(src), str(dest))
            print(f"  [MOVED TO WEB] {wf} -> web/{wf}")
        else:
            shutil.copy2(str(src), str(dest))
            src.unlink()

# 4. Move root capstone notebook to notebooks/00_master_capstone_oted_66_domains.ipynb if still sitting in root
root_nb = ROOT_DIR / "capstone_oted_epistemological_reconstruction_66_domains.ipynb"
if root_nb.exists():
    dest_nb = ROOT_DIR / "notebooks" / "00_master_capstone_oted_66_domains.ipynb"
    shutil.move(str(root_nb), str(dest_nb))
    print(f"  [MOVED ROOT NOTEBOOK] capstone_oted...ipynb -> notebooks/00_master_capstone_oted_66_domains.ipynb")

# Move fetch_api.py to archive/scripts_legacy/
fetch_py = ROOT_DIR / "fetch_api.py"
if fetch_py.exists():
    shutil.move(str(fetch_py), str(ROOT_DIR / "archive" / "scripts_legacy" / "fetch_api.py"))

# 5. Move legacy root directories to archive/
legacy_root_dirs = [
    "01_Documentation_and_Monographs",
    "03_Verified_Statistical_Repository_66_Domains",
    "04_Automation_and_ETL_Pipelines",
    "05_Policy_Simulator_and_Web_App",
    "archive_and_debug_history",
    "exports_stash",
    "hf_space_publish",
    "holistic_analysis",
    "neet_outputs",
    "paper",
    "rendered_notebooks"
]

for ldir in legacy_root_dirs:
    src_dir = ROOT_DIR / ldir
    if src_dir.exists() and src_dir.is_dir():
        dest_dir = ROOT_DIR / "archive" / ldir
        if not dest_dir.exists():
            shutil.move(str(src_dir), str(dest_dir))
            print(f"  [ARCHIVED FOLDER] {ldir}/ -> archive/{ldir}/")
        else:
            # If target already exists in archive, merge/remove
            for item in src_dir.iterdir():
                d_item = dest_dir / item.name
                if not d_item.exists():
                    shutil.move(str(item), str(d_item))
            shutil.rmtree(str(src_dir), ignore_errors=True)
            print(f"  [MERGED TO ARCHIVE] {ldir}/ -> archive/{ldir}/")

# Also let's simplify scripts/ folder: keep only core 6 scripts, move the rest to archive/scripts_legacy/
core_scripts = [
    "build_and_integrate_6_final_uncovered_sources.py",
    "build_exhaustive_empirical_synthesis_matrix.py",
    "build_master_capstone_monograph.py",
    "certify_60_domains_justifiable_completeness.py",
    "verify_and_export_66_direct_links_catalog.py",
    "inject_clickable_source_links_into_all_notebooks.py",
    "reorganize_repo_to_osf_zenodo_standards.py",
    "simplify_root_directory.py"
]

scripts_dir = ROOT_DIR / "scripts"
if scripts_dir.exists():
    for sc in scripts_dir.iterdir():
        if sc.is_file() and sc.name.endswith(".py") and sc.name not in core_scripts:
            dest = ROOT_DIR / "archive" / "scripts_legacy" / sc.name
            if not dest.exists():
                shutil.move(str(sc), str(dest))

# Print final root directory structure
print("\n=== FINAL ROOT DIRECTORY STRUCTURE ===")
for item in sorted(ROOT_DIR.iterdir()):
    if item.name.startswith("."):
        continue
    if item.is_dir():
        print(f"  📁 {item.name}/")
    else:
        print(f"  📄 {item.name}")

print("\n✅ ROOT DIRECTORY IS NOW SPOTLESS AND ULTRA-SIMPLIFIED!")
