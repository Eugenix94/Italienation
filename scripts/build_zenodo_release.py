import os
import zipfile
import shutil
from pathlib import Path

def create_release():
    print("Starting Zenodo Release Packaging...")
    
    # Define paths
    base_dir = Path(r"C:\Users\Dell\Documents\Antigravity\Italienation")
    release_zip = base_dir / "Italienation_Data_Release_v1.zip"
    
    # Directories to include
    dirs_to_include = [
        "local_data/processed",
        "notebooks/regional_profiles",
        "notebooks/archive",
        "scripts"
    ]
    
    # Specific files to include
    files_to_include = [
        ".zenodo.json",
        "OSF_README.md"
    ]
    
    # Remove existing zip if present
    if release_zip.exists():
        os.remove(release_zip)
        
    total_files = 0
    with zipfile.ZipFile(release_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add directories
        for d in dirs_to_include:
            dir_path = base_dir / d
            if dir_path.exists():
                for root, _, files in os.walk(dir_path):
                    for file in files:
                        if not file.endswith('.pyc') and "__pycache__" not in root and ".ipynb_checkpoints" not in root:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(base_dir)
                            zipf.write(file_path, arcname)
                            total_files += 1
            else:
                print(f"Warning: Directory {d} not found.")
                
        # Add specific files
        for f in files_to_include:
            file_path = base_dir / f
            if file_path.exists():
                zipf.write(file_path, f)
                total_files += 1
            else:
                print(f"Warning: File {f} not found.")
                
    print(f"\nSuccessfully packaged {total_files} files into {release_zip.name}")
    print(f"Archive size: {os.path.getsize(release_zip) / (1024*1024):.2f} MB")
    print("Ready for Zenodo upload!")

if __name__ == "__main__":
    create_release()
