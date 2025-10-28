import os
import json
import requests

# Cesty
JSON_FILE = "spacemap\data\Models.new.json"    
BASE_URL = "https://atomic.ariaom.com/"
DOWNLOAD_DIR = "ships_downloads"

# Načítanie JSON
with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Vytvor adresár pre sťahovanie
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

ships = data.get("ships", {})

for ship_id, info in ships.items():
    path = info["path"]
    start = info["start"]
    end = info["end"]
    is_webp = info["isWebp"]
    custom_ext = info.get("customExtension")
    ext = custom_ext if custom_ext else ("webp" if is_webp else "png")

    # Výstupný adresár
    ship_dir = os.path.join(DOWNLOAD_DIR, path.replace("/", "_"))
    os.makedirs(ship_dir, exist_ok=True)

    # Ak start == 0 a end == 0 → jedno 0.png
    if start == 0 and end == 0:
        filename = f"0.{ext}"
        local_path = os.path.join(ship_dir, filename)
        url = f"{BASE_URL}{path}/0.{ext}"

        if os.path.exists(local_path):
            print(f"[SKIP] {local_path} uz existuje")
            continue

        print(f"[DOWNLOAD] {url}")
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(resp.content)
        except Exception as e:
            print(f"[ERROR] {url} - {e}")

    # Inak stiahni všetky od start po end
    else:
        for i in range(start, end + 1):
            filename = f"{i}.{ext}"
            local_path = os.path.join(ship_dir, filename)
            url = f"{BASE_URL}{path}/{i}.{ext}"

            if os.path.exists(local_path):
                print(f"[SKIP] {local_path} uz existuje")
                continue

            print(f"[DOWNLOAD] {url}")
            try:
                resp = requests.get(url)
                resp.raise_for_status()
                with open(local_path, "wb") as f:
                    f.write(resp.content)
            except Exception as e:
                print(f"[ERROR] {url} - {e}")

print("\nHotovo...vsetky chybajuce ship subory boli spracovane!")