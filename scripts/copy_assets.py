import os
import glob
import shutil
from pathlib import Path

def copy_assets():
    dest_dir = Path('rendered_outputs/assets/charts')
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Collect all charts
    chart_files = []
    chart_files.extend(glob.glob('archive/data_processed/charts/**/*.png', recursive=True))
    chart_files.extend(glob.glob('archive/notebooks_legacy/Notebooks/neet_outputs/**/*.png', recursive=True))
    
    # Copy them over
    copied = 0
    for f in chart_files:
        src = Path(f)
        dst = dest_dir / src.name
        if not dst.exists():
            shutil.copy2(src, dst)
            copied += 1
            
    print(f"Copied {copied} charts to {dest_dir}. Total charts available: {len(list(dest_dir.glob('*.png')))}")

if __name__ == '__main__':
    copy_assets()
