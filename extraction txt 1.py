import os
import csv
import pandas as pd

# =========================
# 📁 CHEMINS
# =========================
DOSSIER = r"C:/Users/timeo/Documents/cours/année 2/SAE/scraping/MAL extractions"
CHEMIN_EXCEL = r"C:/Users/timeo/Documents/cours/année 2/SAE/MAL_dataset.xlsx"

# =========================
# 🚫 FILTRES
# =========================

# lignes à supprimer par préfixe (langues)
LIGNES_A_SUPPRIMER = (
    "Japanese:",
    "German:",
    "Spanish:"
)

# clés à supprimer STRICTEMENT
CLES_A_SUPPRIMER = {
    "Genre",      # on garde "Genres"
    "Theme",      # on garde "Themes"
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
    "Watching"
}

# =========================
# 1️⃣ LECTURE + NETTOYAGE
# =========================
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

                # filtres combinés
                if not valeur.startswith(LIGNES_A_SUPPRIMER) and key not in CLES_A_SUPPRIMER:
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

anime_dicts = [anime_to_dict(anime) for anime in MAL_extraction]

# =========================
# 3️⃣ NETTOYAGES SPÉCIFIQUES
# =========================

def score_nettoyage(texte):
    return texte[:5]

def duree_nettoyage(texte):
    return texte[:6]

def extraire_rang(texte):
    if "based" in texte:
        return texte.split("based", 1)[0]
    return texte

def garder_premier_studio(texte):
    if "," in texte:
        return texte.split(",", 1)[0].strip()
    return texte

for anime in anime_dicts:
    if "Score" in anime:
        anime["Score"] = score_nettoyage(anime["Score"])

    if "Duration" in anime:
        anime["Duration"] = duree_nettoyage(anime["Duration"])

    if "Ranked" in anime:
        anime["Ranked"] = extraire_rang(anime["Ranked"])

    if "Studios" in anime:
        anime["Studios"] = garder_premier_studio(anime["Studios"])


def nettoyer_doublon_et_virgule(texte):
    # 1️⃣ garder avant la virgule
    texte = texte.split(",", 1)[0].strip()

    # 2️⃣ supprimer doublon exact (ChildcareChildcare, SeinenSeinen, etc.)
    longueur = len(texte)
    if longueur % 2 == 0:
        moitie = longueur // 2
        if texte[:moitie] == texte[moitie:]:
            texte = texte[:moitie]

    return texte


for anime in anime_dicts:
    if "Themes" in anime:
        anime["Themes"] = nettoyer_doublon_et_virgule(anime["Themes"])

    if "Demographic" in anime:
        anime["Demographic"] = nettoyer_doublon_et_virgule(anime["Demographic"])

    if "Genres" in anime:
        anime["Genres"] = nettoyer_doublon_et_virgule(anime["Genres"])


# =========================
# 4️⃣ EXPORT EXCEL
# =========================
df = pd.DataFrame(anime_dicts)
df.to_excel(CHEMIN_EXCEL, index=False)

print("\n✅ Export Excel terminé")
print(f"📄 Fichier créé : {CHEMIN_EXCEL}")
