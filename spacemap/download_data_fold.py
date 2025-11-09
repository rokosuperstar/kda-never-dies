import os
import requests

BASE_URL = "https://ariaom.com/spacemap/data"
DATA_DIR = "data"

FILES = [
    "calendar.json",
    "dronePos.json",
    "enginePos.json",
    "equipment.json",
    "gameData.json",
    "laserPos.json",
    "mapObjects.json",
    "mapObjects.new.json",
    "Models.json",
    "Models.new.json",
    "shopItems.json",
    "Sounds.json",
    "spacemap.json",
    "SubmenuItems.json",
    "texts_cz.json",
    "texts_de.json",
    "texts_en.json",
    "texts_es.json",
    "texts_fr.json",
    "texts_ru.json",
    "texts_tr.json",
    "uiElements.json"
]

def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    for filename in FILES:
        url = f"{BASE_URL}/{filename}"
        out_path = os.path.join(DATA_DIR, filename)

        print("GET:", url)
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            with open(out_path, "wb") as f:
                f.write(r.content)
            print("OK:", filename)
        else:
            print("FAIL:", filename, r.status_code)

if __name__ == "__main__":
    main()
