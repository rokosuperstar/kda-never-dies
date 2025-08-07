import os
import requests

# Ak chceš načítať zo súboru, odkomentuj a uprav tento riadok:
# with open('lol.txt', encoding='utf-8') as f:
#     ship_names = [line.strip() for line in f if line.strip()]

# Alebo použijeme priamo tvoj list:
ship_names = [
    "infernoSentinel",
    "infernoVenom",
    "infernoSolace",
    "infernoDimi",
    "infernoSpectrum",
    "ginferno"
]

BASE_URL = "https://eu.ariaom.com/spacemap/ships/"
DEST_PATH = r"C:\Users\rocka\Desktop\kda-mod\kda-mod\spacemap\spacemap\ships"

START_INDEX = 0
END_INDEX = 64

for name in ship_names:
    folder = os.path.join(DEST_PATH, name)
    os.makedirs(folder, exist_ok=True)
    print(f"\n--- {name} ---")
    for i in range(START_INDEX, END_INDEX + 1):
        url = f"{BASE_URL}{name}/{i}.webp"
        dest_file = os.path.join(folder, f"{i}.webp")
        if os.path.exists(dest_file):
            print(f"Existuje: {i}.webp, preskakujem.")
            continue
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200 and r.content:
                with open(dest_file, "wb") as f:
                    f.write(r.content)
                print(f"Stiahnuté: {i}.webp")
            else:
                print(f"Chyba alebo neexistuje: {i}.webp (status {r.status_code})")
        except Exception as e:
            print(f"Chyba {i}.webp: {e}")
