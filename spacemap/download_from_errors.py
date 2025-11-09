import os
import re
import requests
from urllib.parse import urlsplit
from concurrent.futures import ThreadPoolExecutor, as_completed

NEW_DOMAIN = "ariaom.com"

def extract_links(text):
    pattern = r'https?://[^\s)]+'
    return re.findall(pattern, text)

def convert_url(u):
    u = u.split("?")[0]
    parsed = urlsplit(u)
    forced = f"https://{NEW_DOMAIN}{parsed.path}"
    forced = forced.replace("//spacemap", "/spacemap")
    return forced

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

    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(out_path, "wb") as f:
                f.write(r.content)
            print("OK:", out_path)
        else:
            print("FAIL:", url, r.status_code)
    except Exception as e:
        print("ERR:", url, str(e))

def process_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    links = extract_links(content)
    urls = []

    for link in links:
        new_url = convert_url(link)
        if "/spacemap/" in new_url:
            urls.append(new_url)

    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = [pool.submit(download_file, u) for u in urls]
        for _ in as_completed(futures):
            pass

if __name__ == "__main__":
    process_txt("C:/Users/rocka/Desktop/dogs/kda-never-dies/spacemap/a.txt")
