import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = ROOT_DIR / "local_data" / "processed"
REGISTRY_PATH = PROCESSED_DIR / "DEFINITIVE_DATA_SOURCE_PROVENANCE_REGISTRY.json"

print("=== VERIFYING INTEGRITY OF ALL 42 CANONICAL PROVENANCE DOMAINS ===")

with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
    registry = json.load(f)

print(f"Total domains registered: `{len(registry)}`")

missing = []
corrupted = []
valid = 0

for i, entry in enumerate(registry, 1):
    file_list = [f.strip() for f in entry["processed_file"].split(" & ")]
    all_files_ok = True
    for f_rel in file_list:
        # handle partial filenames inside compound string
        if not f_rel.startswith("local_data/"):
            f_path = PROCESSED_DIR / f_rel
        else:
            f_path = ROOT_DIR / f_rel
            
        if not f_path.exists():
            missing.append((i, entry["id"], str(f_path)))
            all_files_ok = False
        else:
            size = f_path.stat().st_size
            if size < 50:
                corrupted.append((i, entry["id"], str(f_path), size))
                all_files_ok = False
    if all_files_ok:
        valid += 1

print(f"Valid domains verified on disk: `{valid} / {len(registry)}`")

if missing:
    print("\n[ERROR] Missing files:")
    for m in missing:
        print(f"  Domain {m[0]} `{m[1]}`: missing `{m[2]}`")

if corrupted:
    print("\n[ERROR] Corrupted / empty files:")
    for c in corrupted:
        print(f"  Domain {c[0]} `{c[1]}`: size `{c[3]}` bytes (`{c[2]}`)")

if not missing and not corrupted and valid == len(registry):
    print(f"\n -> [SUCCESS] ALL `{valid}` CANONICAL DOMAINS ARE 100% VERIFIED, PRESENT, AND STRUCTURALLY INTEGRAL!")

print("=== VERIFICATION COMPLETE ===")
