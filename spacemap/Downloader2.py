import os
import re
import requests
from urllib.parse import urlsplit

ORIG_DOMAIN = "kristof-danko-alfons.shop"
NEW_DOMAIN  = "ariaom.com"

def extract_links(text):
    pattern = r'https?://[^\s)]+'
    return re.findall(pattern, text)

def convert_url(u):
    u = u.replace(ORIG_DOMAIN, NEW_DOMAIN)
    u = u.split("?")[0]
    u = u.replace("//spacemap", "/spacemap")  # fix double slash
    return u

def download_file(url):
    parts = urlsplit(url).path.split('/')
    if "spacemap" not in parts:
        return

    idx = parts.index("spacemap") + 1
    sub_path_parts = [p for p in parts[idx:-1] if p.strip() != ""]
    filename = parts[-1]

    out_dir = os.path.join("downloads", *sub_path_parts)
    os.makedirs(out_dir, exist_ok=True)

    out_path = os.path.join(out_dir, filename)

    if os.path.exists(out_path):
        print("SKIP:", out_path)
        return

    r = requests.get(url, timeout=10)
    if r.status_code == 200:
        with open(out_path, "wb") as f:
            f.write(r.content)
        print("OK:", out_path)
    else:
        print("FAIL:", url, r.status_code)


def process_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    links = extract_links(content)

    for link in links:
        new_url = convert_url(link)
        if "/spacemap/" not in new_url:
            continue
        download_file(new_url)

if __name__ == "__main__":
    process_txt("C:/Users/rocka/Desktop/dogs/kda-never-dies/spacemap/a.txt")
