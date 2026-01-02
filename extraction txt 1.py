import os
import csv

DOSSIER = r"C:/Users/timeo/Documents/cours/année 2/SAE/scraping/MAL extractions"

LIGNES_A_SUPPRIMER = ("Japanese:", "English:", "German:", "Spanish:")

MAL_extraction = []

# =========================
# 1️⃣ LECTURE + NETTOYAGE
# =========================
for filename in sorted(os.listdir(DOSSIER)):
    if filename.endswith(".txt"):
        filepath = os.path.join(DOSSIER, filename)

        fichier_data = []

        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for ligne in reader:
                valeur = ligne[0]

                if not valeur.startswith(LIGNES_A_SUPPRIMER):
                    fichier_data.append(ligne)

        MAL_extraction.append(fichier_data)
        print(f"✔ {filename} chargé ({len(fichier_data)} lignes)")

print(f"\nTotal fichiers chargés : {len(MAL_extraction)}")

# =========================
# 2️⃣ CONVERSION EN DICTS
# =========================
def anime_to_dict(anime):
    data = {}

    for champ in anime:
        texte = champ[0]

        if ":" in texte:
            key, value = texte.split(":", 1)
            data[key.strip()] = value.strip()

    return data


anime_dicts = []

for anime in MAL_extraction:
    anime_dicts.append(anime_to_dict(anime))

# =========================
# 3️⃣ TEST
# =========================
print("\nExemple anime sous forme dictionnaire :\n")
print(anime_dicts)


import pandas as pd

# =========================
# 4️⃣ EXPORT EXCEL
# =========================

# création du DataFrame à partir des dictionnaires
df = pd.DataFrame(anime_dicts)

# export Excel
df.to_excel("C:/Users/timeo/Documents/cours/année 2/SAE/MAL_dataset.xlsx", index=False)
print("Fichier créé :", os.path.abspath(fichier_excel))