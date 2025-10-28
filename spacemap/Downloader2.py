import os
import json
import requests

# Cesty
JSON_FILE = "a.txt"   # súbor so zoznamom
BASE_URL = "https://ariaom.com/spacemap/"
DOWNLOAD_DIR = "downloads"

# Načítaj dáta
with open(JSON_FILE, "r", encoding="utf-8") as f:
    text = f.read()
    # Ak nie je validný JSON, oprav ho načítaním ako dictionary zo stringu
    if not text.strip().startswith("{"):
        text = "{" + text.strip().rstrip(",") + "}"
    data = json.loads(text)

os.makedirs(DOWNLOAD_DIR, exist_ok=True)

for key, info in data.items():
    path = info.get("path")
    use_atlas = info.get("useAtlas", False)
    is_single = info.get("isSingleFile", False)

    if not path or not use_atlas:
        continue

    # len pre atlasové veci
    subdir = path.replace("/", "_")
    target_dir = os.path.join(DOWNLOAD_DIR, subdir)
    os.makedirs(target_dir, exist_ok=True)

    png_url = f"{BASE_URL}{path}.png"
    json_url = f"{BASE_URL}{path}.json"

    for url in [png_url, json_url]:
        filename = os.path.basename(url)
        local_path = os.path.join(target_dir, filename)

        if os.path.exists(local_path):
            print(f"[SKIP] {local_path} uz existuje")
            continue

        print(f"[DOWNLOAD] {url}")
        try:
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(f"[ERROR] {url} - {e}")

print("\nHotovo, všetky atlasové .png a .json súbory boli spracované.")
