import re
import os
import pathlib
import urllib.request
import urllib.error
from urllib.parse import urlsplit, urlunsplit

SOURCE_HOST = "ciganini.misolini.kda-perfect.space"
TARGET_HOST = "eu.ariaom.com"

URL_RE = re.compile(r"https?://[^\s'\"<>]+?\.(?:png|jpe?g|webp)", re.IGNORECASE)
UA = "Mozilla/5.0 (URL-grabber/1.0)"

# nájde všetky url
def extract_urls(text: str):
    raw = URL_RE.findall(text)
    return list(dict.fromkeys(raw))  # dedupe

# prepíše host
def rewrite_host(url: str) -> str:
    parts = urlsplit(url)
    if parts.netloc.lower() == SOURCE_HOST.lower():
        parts = parts._replace(netloc=TARGET_HOST)
    return urlunsplit(parts)

# pre URL vráti lokálnu cestu podľa path
def url_to_local_path(url: str) -> pathlib.Path:
    parts = urlsplit(url)
    clean_path = parts.path.lstrip("/")  # odseknúť leading "/"
    return pathlib.Path(clean_path)

def ensure_parent_dir(p: pathlib.Path):
    p.parent.mkdir(parents=True, exist_ok=True)

def download(url: str, dest: pathlib.Path):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            if resp.status != 200:
                raise urllib.error.HTTPError(url, resp.status, f"HTTP {resp.status}", resp.headers, None)
            ensure_parent_dir(dest)
            with open(dest, "wb") as f:
                f.write(resp.read())
        print(f"[OK] {url} -> {dest}")
    except Exception as e:
        print(f"[FAIL] {url} ({e})")

def main():
    # cesta k lol.txt v tom istom priečinku
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
