"""
Fetch useful INVALSI open datasets from the official archive and save a manifest.

Source archive:
https://serviziostatistico.invalsi.it/archivio-dati/?_sft_invalsi_ss_data_collective=open-data

What this script does:
1. Crawls archive pages (pagination)
2. Collects dataset post URLs
3. Extracts direct downloadable files (csv/xlsx/zip) from each post
4. Filters to high-value datasets for this project (NEET/education outcomes)
5. Downloads files and writes a JSON manifest

Run:
    .venv\\Scripts\\python.exe api_data/fetch_scripts/fetch_invalsi_open_data.py
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = ROOT / "local_data" / "INVALSI"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MANIFEST = OUT_DIR / "invalsi_manifest.json"

ARCHIVE_BASE = "https://serviziostatistico.invalsi.it/archivio-dati/?_sft_invalsi_ss_data_collective=open-data"
POST_RE = re.compile(r'https://serviziostatistico\.invalsi\.it/invalsi_ss_data/[^"\'\s<>]+/?', re.I)
FILE_RE = re.compile(r'https?://[^"\'\s<>]+\.(?:csv|xlsx|zip)(?:\?[^"\'\s<>]*)?', re.I)

# Focus on files that are analytically useful for your NEET/education pipeline.
PRIORITY_KEYWORDS = [
    "punteggi",
    "livelli",
    "traguardi",
    "dispersione",
    "eccellenza",
    "wle",
    "dashboard",
    "report_generale",
    "info_territoriali",
    "sll",
]

RECENT_YEAR_TOKENS = [
    "2024-2025",
    "2024-25",
    "2023-2024",
    "2023-24",
    "2025",
    "2024",
]

DEPRIORITY_KEYWORDS = [
    "microdati-campione",
]

FILE_PRIORITY_KEYWORDS = [
    "livelli",
    "wle",
    "traguardi",
    "variabilita",
    "qescs",
    "digicomp",
    "trend",
    "dispersione",
    "eccellenti",
    "report_generale",
    "sll",
]

FILE_DEPRIORITY_KEYWORDS = [
    "tracciato",
    "note",
]

MAX_DOWNLOADS = 12
DOWNLOAD_OFFSET = int(os.getenv("INVALSI_DOWNLOAD_OFFSET", "0"))


@dataclass
class FileEntry:
    post_url: str
    file_url: str
    file_name: str
    downloaded: bool
    bytes: int
    note: str = ""


def get(url: str, timeout: int = 25) -> requests.Response | None:
    try:
        return requests.get(url, timeout=timeout)
    except Exception as exc:
        print(f"  [ERROR] {url} -> {exc}")
        return None


def discover_post_urls(max_pages: int = 2) -> list[str]:
    print("\n[1/4] Discovering INVALSI dataset posts...")
    found: set[str] = set()

    for page in range(1, max_pages + 1):
        url = ARCHIVE_BASE if page == 1 else f"{ARCHIVE_BASE}&sf_paged={page}"
        r = get(url)
        if r is None or r.status_code != 200:
            print(f"  [WARN] archive page {page} unavailable")
            continue

        matches = set(POST_RE.findall(r.text))
        if not matches:
            print(f"  page {page}: 0 posts")
        else:
            print(f"  page {page}: {len(matches)} posts")
        found |= matches
        time.sleep(0.2)

    urls = sorted(found)
    print(f"  total posts discovered: {len(urls)}")
    return urls


def score_post(url: str) -> int:
    u = url.lower()
    score = sum(3 for k in PRIORITY_KEYWORDS if k in u)
    score += sum(4 for token in RECENT_YEAR_TOKENS if token in u)

    if "2024-2025" in u or "2024-25" in u:
        score += 8
    elif "2023-2024" in u or "2023-24" in u:
        score += 5

    if "rapporto" in u:
        score += 4
    if "popolazione" in u or "territorial" in u:
        score += 2

    score -= sum(6 for k in DEPRIORITY_KEYWORDS if k in u)
    return score


def extract_file_links(post_url: str) -> set[str]:
    r = get(post_url)
    if r is None or r.status_code != 200:
        return set()

    links = set(FILE_RE.findall(r.text))

    # Sometimes links are relative; try a basic href fallback.
    hrefs = re.findall(r'href=["\']([^"\']+)["\']', r.text, flags=re.I)
    for h in hrefs:
        h_low = h.lower()
        if any(h_low.endswith(ext) for ext in (".csv", ".xlsx", ".zip")):
            links.add(urljoin(post_url, h))

    return links


def safe_name(file_url: str, post_url: str) -> str:
    path_name = Path(urlparse(file_url).path).name or "download.bin"
    slug = Path(urlparse(post_url).path.rstrip("/")).name
    return f"{slug}__{path_name}"


def score_file_url(file_url: str) -> int:
    u = file_url.lower()
    score = sum(3 for k in FILE_PRIORITY_KEYWORDS if k in u)
    score += sum(4 for token in RECENT_YEAR_TOKENS if token in u)

    if u.endswith(".csv"):
        score += 3
    elif u.endswith(".xlsx"):
        score += 2
    elif u.endswith(".zip"):
        score += 1

    score -= sum(6 for k in FILE_DEPRIORITY_KEYWORDS if k in u)
    return score


def download_file(file_url: str, post_url: str) -> tuple[bool, int, str, str]:
    name = safe_name(file_url, post_url)
    out = OUT_DIR / name

    if out.exists() and out.stat().st_size > 256:
        return True, out.stat().st_size, name, "skip-existing"

    r = get(file_url)
    if r is None:
        return False, 0, name, "request-failed"

    if r.status_code != 200:
        return False, 0, name, f"http-{r.status_code}"

    content = r.content
    if len(content) < 64:
        return False, len(content), name, "tiny-file"

    out.write_bytes(content)
    return True, len(content), name, "downloaded"


def main():
    post_urls = discover_post_urls(max_pages=2)
    if not post_urls:
        print("\nNo dataset posts discovered.")
        return

    # Keep posts that are likely useful for analysis first.
    ranked_posts = sorted(post_urls, key=score_post, reverse=True)
    useful_posts = [p for p in ranked_posts if score_post(p) > 0]

    # Fallback: if keyword matching is too strict, still process first N posts.
    if len(useful_posts) < 8:
        useful_posts = ranked_posts[:5]
    else:
        useful_posts = useful_posts[:5]

    print(f"\n[2/4] Extracting file links from {len(useful_posts)} candidate posts...")
    post_to_files: dict[str, set[str]] = {}

    for i, p in enumerate(useful_posts, start=1):
        files = extract_file_links(p)
        post_to_files[p] = files
        print(f"  {i:02d}. {Path(urlparse(p).path).name}: {len(files)} files")
        time.sleep(0.1)

    all_pairs: list[tuple[str, str]] = []
    for p, files in post_to_files.items():
        for f in sorted(files):
            all_pairs.append((p, f))

    all_pairs.sort(key=lambda pair: (score_post(pair[0]) + score_file_url(pair[1])), reverse=True)

    target_pairs = all_pairs[DOWNLOAD_OFFSET : DOWNLOAD_OFFSET + MAX_DOWNLOADS]
    print(
        f"\n[3/4] Downloading {len(target_pairs)} of {len(all_pairs)} discovered files "
        f"(offset={DOWNLOAD_OFFSET}, limit={MAX_DOWNLOADS})..."
    )
    entries: list[FileEntry] = []

    for p, f in target_pairs:
        ok, size, name, note = download_file(f, p)
        entries.append(
            FileEntry(
                post_url=p,
                file_url=f,
                file_name=name,
                downloaded=ok,
                bytes=size,
                note=note,
            )
        )
        tag = "OK" if ok else "MISS"
        print(f"  [{tag}] {name} ({size} bytes) {note}")
        time.sleep(0.05)

    manifest = {
        "source": ARCHIVE_BASE,
        "posts_discovered": len(post_urls),
        "posts_processed": len(useful_posts),
        "files_discovered": len(all_pairs),
        "files_offset": DOWNLOAD_OFFSET,
        "files_attempted": len(target_pairs),
        "files_downloaded": sum(1 for e in entries if e.downloaded),
        "entries": [asdict(e) for e in entries],
    }

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")

    print("\n[4/4] Done")
    print(f"  manifest: {MANIFEST.relative_to(ROOT)}")
    print(f"  downloaded files: {manifest['files_downloaded']}")


if __name__ == "__main__":
    main()
