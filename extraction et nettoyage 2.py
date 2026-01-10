import os
import csv
import pandas as pd
import re

# DEFINITION DES CHEMINS
DOSSIER = r"donneMAL"
CHEMIN_EXCEL = r"MAL_dataset.xlsx"

# FILTRES

LIGNES_A_SUPPRIMER = (
    "Japanese:",
    "German:",
    "Spanish:"
)

CLES_A_SUPPRIMER = {
    "Genre",
    "Theme",
    "Rating",
    "Source",
    "Licensors",
    "Producers",
    "Broadcast",
    "Status",
    "French",
    "Aired",
    "Synonyms",
    "Total",
    "On-Hold",
    "Watching",
    "Plan to Watch",
    "Dropped"
}


#LECTURE + NETTOYAGE
MAL_extraction = []

for filename in sorted(os.listdir(DOSSIER)):
    if filename.endswith(".txt"):
        filepath = os.path.join(DOSSIER, filename)
        fichier_data = []

        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=";")
            for ligne in reader:
                valeur = ligne[0]
                key = valeur.split(":", 1)[0]

                if not valeur.startswith(LIGNES_A_SUPPRIMER) and key not in CLES_A_SUPPRIMER:
                    fichier_data.append(ligne)

        MAL_extraction.append(fichier_data)
        print(f"✔ {filename} chargé ({len(fichier_data)} lignes)")

print(f"\nTotal fichiers chargés : {len(MAL_extraction)}")


#CONVERSION EN DICTS

def anime_to_dict(anime):
    data = {}
    for champ in anime:
        texte = champ[0]
        if ":" in texte:
            key, value = texte.split(":", 1)
            data[key.strip()] = value.strip()
    return data

anime_dicts = [anime_to_dict(anime) for anime in MAL_extraction]

#NETTOYAGES SPÉCIFIQUES

def nettoyer_premiered(texte):
    if not texte:
        return None, None

    texte = texte.strip()

    # format attendu : "Fall 2017"
    match = re.match(r"(Spring|Summer|Fall|Winter)\s+(\d{4})", texte)
    if match:
        season, year = match.groups()
        return season, int(year)

    return None, None

def score_nettoyage(texte):
    return float(texte[:4]) if texte[:4].replace(".", "").isdigit() else None

def duree_nettoyage(texte):
    if not texte:
        return None

    texte = texte.lower().strip()
    if texte in {"unknown", "?"}:
        return None

    minutes = 0

    # heures (hr ou hr.)
    h = re.search(r"(\d+)\s*hr\.?", texte)
    if h:
        minutes += int(h.group(1)) * 60

    # minutes
    m = re.search(r"(\d+)\s*min", texte)
    if m:
        minutes += int(m.group(1))

    return minutes if minutes > 0 else None


def extraire_rang(texte):
    return texte.split("based", 1)[0].strip()

def garder_premier_studio(texte):
    return texte.split(",", 1)[0].strip()

def nettoyer_genres_themes(texte):
    if not texte:
        return texte

    elements = texte.split(",")
    nettoyes = []

    for elem in elements:
        elem = elem.strip()
        longueur = len(elem)

        if longueur % 2 == 0:
            moitie = longueur // 2
            if elem[:moitie] == elem[moitie:]:
                elem = elem[:moitie]

        nettoyes.append(elem)

    return ",".join(dict.fromkeys(nettoyes))


#APPLICATION DES NETTOYAGES

for anime in anime_dicts:
    if "Score" in anime:
        anime["Score"] = score_nettoyage(anime["Score"])

    if "Duration" in anime:
        anime["Duration"] = duree_nettoyage(anime["Duration"])

    if "Ranked" in anime:
        anime["Ranked"] = extraire_rang(anime["Ranked"])

    if "Studios" in anime:
        anime["Studios"] = garder_premier_studio(anime["Studios"])

    if "Genres" in anime:
        anime["Genres"] = nettoyer_genres_themes(anime["Genres"])

    if "Themes" in anime:
        anime["Themes"] = nettoyer_genres_themes(anime["Themes"])

    if "Demographic" in anime:
        anime["Demographic"] = nettoyer_genres_themes(anime["Demographic"])


    if "Premiered" in anime:
        season, year = nettoyer_premiered(anime["Premiered"])
        anime["Season"] = season
        anime["Year"] = year
        del anime["Premiered"]


#EXPORT EXCEL

df = pd.DataFrame(anime_dicts)

# Traites les colones au format de nombre Americain
df["Members"] = df['Members'].str.replace(',', '')
df['Members'] = df['Members'].astype(int)
df["Favorites"] = df['Favorites'].str.replace(',', '')
df['Favorites'] = df['Favorites'].astype(int)
df["Completed"] = df['Completed'].str.replace(',', '')
df['Completed'] = df['Completed'].astype(int)
df['Episodes'] = pd.to_numeric(df['Episodes'].replace('Unknown', None), errors='coerce').astype('Int64')

df.to_excel(CHEMIN_EXCEL, index=False)

print("Export Excel terminé")