import re
import os
import pathlib
import urllib.request
import urllib.error
from urllib.parse import urlsplit, urlunsplit

SOURCE_HOST = "ciganini.misolini.kda-perfect.space"
TARGET_HOST = "no1.ariaom.com"

# zoberie ľubovoľnú príponu (.xyz), query/fragment už ďalej neriešime (odstrihneme nižšie)
URL_RE = re.compile(
    r"https?://[^\s'\"<>]+?\.[A-Za-z0-9]{1,10}(?=(?:[?#]|[\s'\"<>]|$))",
    re.IGNORECASE
)
UA = "Mozilla/5.0 (URL-grabber/1.1)"

def extract_urls(text: str):
    # nájdi a odstrihni query/fragment
    raw = URL_RE.findall(text)
    clean = []
    seen = set()
    for u in raw:
        u2 = u.split('#', 1)[0].split('?', 1)[0]
        if u2 not in seen:
            seen.add(u2)
            clean.append(u2)
    return clean

def rewrite_host(url: str) -> str:
    parts = urlsplit(url)
    host = parts.netloc.lower()
    if host in (SOURCE_HOST.lower(), "localhost:3000"):
        parts = parts._replace(netloc=TARGET_HOST)
    return urlunsplit(parts)

def url_to_local_path(url: str) -> pathlib.Path:
    parts = urlsplit(url)
    clean_path = parts.path.lstrip("/")  # nech nie je absolútna
    # normalizácia // -> /
    clean_path = os.path.normpath(clean_path)
    if clean_path in (".", ""):
        clean_path = "index"
    return pathlib.Path(clean_path)

def ensure_parent_dir(p: pathlib.Path):
    p.parent.mkdir(parents=True, exist_ok=True)

def download(url: str, dest: pathlib.Path):
    if dest.exists():
        print(f"[SKIP] existuje -> {dest}")
        return
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            if resp.status != 200:
                raise urllib.error.HTTPError(url, resp.status, f"HTTP {resp.status}", resp.headers, None)
            ensure_parent_dir(dest)
            with open(dest, "wb") as f:
                f.write(resp.read())
        print(f"[OK] {url} -> {dest}")
    except Exception as e:
        print(f"[FAIL] {url} ({e})")

def main():
    base_dir = pathlib.Path(__file__).parent
    txt_file = base_dir / "lol.txt"

    with open(txt_file, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    urls = extract_urls(content)
    print(f"Nájdených URL: {len(urls)}")

    for orig in urls:
        final_url = rewrite_host(orig)
        dest = base_dir / url_to_local_path(final_url)
        download(final_url, dest)

if __name__ == "__main__":
    main()
