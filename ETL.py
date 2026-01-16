# Gestion des fichiers et dossiers 
import os

# Lecture de fichiers CSV (les .txt sont lus comme des CSV à une colonne)
import csv

# Manipulation et export de données tabulaires
import pandas as pd

# Expressions régulières pour le nettoyage des textes
import re


# =====================================================
# --- CONFIGURATION ET FILTRES ---
# =====================================================

# Lignes à ignorer si elles commencent par ces préfixes
LIGNES_A_SUPPRIMER = ("Japanese:", "German:", "Spanish:")

# Clés (champs) à supprimer complètement du dataset final
CLES_A_SUPPRIMER = {
    "Genre", "Theme", "Rating", "Source", "Licensors", "Producers",
    "Broadcast", "Status", "French", "Aired", "Synonyms", "Total",
    "On-Hold", "Watching", "Plan to Watch", "Dropped", "Popularity", "Ranked"
}


# =====================================================
# --- FONCTIONS DE NETTOYAGE INDIVIDUELLES ---
# =====================================================

def nettoyer_premiered(texte):
    """
    Sépare la saison et l'année à partir du champ 'Premiered'
    Exemple : "Spring 2021" → ("Spring", 2021)
    """
    if not texte:
        return None, None

    match = re.match(r"(Spring|Summer|Fall|Winter)\s+(\d{4})", texte.strip())
    if match:
        season, year = match.groups()
        return season, int(year)

    return None, None


def score_nettoyage(texte):
    """
    Nettoie et convertit le score en float.
    Ignore les valeurs invalides.
    """
    if not texte:
        return None

    # Vérifie si les 4 premiers caractères correspondent à un nombre
    val = texte[:4].replace(".", "")
    return float(texte[:4]) if val.isdigit() else None


def duree_nettoyage(texte):
    """
    Convertit une durée textuelle en minutes.
    Exemple : "1 hr. 30 min." → 90
    """
    if not texte:
        return None

    texte = texte.lower().strip()

    # Cas non exploitables
    if texte in {"unknown", "?"}:
        return None

    minutes = 0

    # Extraction des heures
    h = re.search(r"(\d+)\s*hr\.?", texte)
    if h:
        minutes += int(h.group(1)) * 60

    # Extraction des minutes
    m = re.search(r"(\d+)\s*min", texte)
    if m:
        minutes += int(m.group(1))

    return minutes if minutes > 0 else None


def extraire_rang(texte):
    """
    Extrait uniquement le rang numérique
    Exemple : "#123 based on..." → "#123"
    """
    return texte.split("based", 1)[0].strip() if texte else None


def garder_premier_studio(texte):
    """
    Conserve uniquement le premier studio listé
    """
    return texte.split(",", 1)[0].strip() if texte else None


def nettoyer_genres_themes(texte):
    """
    Nettoie les genres / thèmes :
    - Supprime les doublons
    - Corrige les répétitions exactes (ex: ActionAction → Action)
    """
    if not texte:
        return texte

    elements = [e.strip() for e in texte.split(",")]
    nettoyes = []

    for elem in elements:
        longueur = len(elem)

        # Détection des répétitions exactes
        if longueur % 2 == 0:
            moitie = longueur // 2
            if elem[:moitie] == elem[moitie:]:
                elem = elem[:moitie]

        nettoyes.append(elem)

    # Suppression des doublons tout en conservant l'ordre
    return ",".join(dict.fromkeys(nettoyes))


def anime_to_dict(anime_lines):
    """
    Convertit une liste de lignes [Clé:Valeur] en dictionnaire Python
    """
    data = {}

    for champ in anime_lines:
        texte = champ[0]

        if ":" in texte:
            key, value = texte.split(":", 1)
            data[key.strip()] = value.strip()

    return data


# =====================================================
# --- FONCTION PRINCIPALE DE TRAITEMENT ---
# =====================================================

def process_mal_data(dossier_source=r"donnees_MAL", chemin_export_excel=r"MAL_dataset.xlsx"):
    """
    - Lit les fichiers .txt extraits de MyAnimeList
    - Nettoie et normalise les données
    - Exporte le tout dans un fichier Excel
    """
    mal_extraction = []

    # -------------------------------------------------
    # 1. Lecture et filtrage des fichiers
    # -------------------------------------------------

    if not os.path.exists(dossier_source):
        print(f"Erreur : Le dossier {dossier_source} n'existe pas.")
        return

    for filename in sorted(os.listdir(dossier_source)):
        if filename.endswith(".txt"):
            filepath = os.path.join(dossier_source, filename)

            # Ajout du nom de l'anime comme première ligne
            fichier_data = [["Name:" + filename.replace(".txt", "")]]

            with open(filepath, newline="", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=";")

                for ligne in reader:
                    if not ligne:
                        continue

                    valeur = ligne[0]
                    key = valeur.split(":", 1)[0]

                    # Application des filtres
                    if not valeur.startswith(LIGNES_A_SUPPRIMER) and key not in CLES_A_SUPPRIMER:
                        fichier_data.append(ligne)

            mal_extraction.append(fichier_data)

    # -------------------------------------------------
    # 2. Conversion en dictionnaires + nettoyage
    # -------------------------------------------------

    anime_dicts = []

    for anime_lines in mal_extraction:
        anime = anime_to_dict(anime_lines)

        # Nettoyage champ par champ
        if "Score" in anime:
            anime["Score"] = score_nettoyage(anime["Score"])

        if "Duration" in anime:
            anime["Duration"] = duree_nettoyage(anime["Duration"])

        if "Ranked" in anime:
            anime["Ranked"] = extraire_rang(anime["Ranked"])

        if "Studios" in anime:
            anime["Studios"] = garder_premier_studio(anime["Studios"])

        for field in ["Genres", "Themes", "Demographic"]:
            if field in anime:
                anime[field] = nettoyer_genres_themes(anime[field])

        # Séparation saison / année
        if "Premiered" in anime:
            season, year = nettoyer_premiered(anime["Premiered"])
            anime["Season"], anime["Year"] = season, year
            del anime["Premiered"]

        anime_dicts.append(anime)

    # -------------------------------------------------
    # 3. Création du DataFrame et nettoyage final
    # -------------------------------------------------

    df = pd.DataFrame(anime_dicts)

    # Conversion des colonnes numériques avec suppression des virgules
    cols_to_fix = ["Members", "Favorites", "Completed"]

    for col in cols_to_fix:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').replace('nan', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    # Gestion du nombre d'épisodes
    if "Episodes" in df.columns:
        df["Episodes"] = pd.to_numeric(
            df["Episodes"].replace("Unknown", None),
            errors="coerce"
        ).astype("Int64")

    # -------------------------------------------------
    # 4. Export Excel
    # -------------------------------------------------

    df.to_excel(chemin_export_excel, index=False)
    print(f"✔ Export terminé : {chemin_export_excel} ({len(df)} entrées)")

    return df


# Lancement du traitement
process_mal_data()
