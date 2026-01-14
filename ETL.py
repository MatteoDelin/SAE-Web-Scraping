import os
import csv
import pandas as pd
import re

# --- CONFIGURATION ET FILTRES ---
LIGNES_A_SUPPRIMER = ("Japanese:", "German:", "Spanish:")
CLES_A_SUPPRIMER = {
    "Genre", "Theme", "Rating", "Source", "Licensors", "Producers",
    "Broadcast", "Status", "French", "Aired", "Synonyms", "Total",
    "On-Hold", "Watching", "Plan to Watch", "Dropped","Popularity","Ranked"
}

# --- FONCTIONS DE NETTOYAGE INDIVIDUELLES ---
def nettoyer_premiered(texte):
    if not texte: return None, None
    match = re.match(r"(Spring|Summer|Fall|Winter)\s+(\d{4})", texte.strip())
    if match:
        season, year = match.groups()
        return season, int(year)
    return None, None

def score_nettoyage(texte):
    if not texte: return None
    val = texte[:4].replace(".", "")
    return float(texte[:4]) if val.isdigit() else None

def duree_nettoyage(texte):
    if not texte: return None
    texte = texte.lower().strip()
    if texte in {"unknown", "?"}: return None
    minutes = 0
    h = re.search(r"(\d+)\s*hr\.?", texte)
    if h: minutes += int(h.group(1)) * 60
    m = re.search(r"(\d+)\s*min", texte)
    if m: minutes += int(m.group(1))
    return minutes if minutes > 0 else None

def extraire_rang(texte):
    return texte.split("based", 1)[0].strip() if texte else None

def garder_premier_studio(texte):
    return texte.split(",", 1)[0].strip() if texte else None

def nettoyer_genres_themes(texte):
    if not texte: return texte
    elements = [e.strip() for e in texte.split(",")]
    nettoyes = []
    for elem in elements:
        longueur = len(elem)
        if longueur % 2 == 0:
            moitie = longueur // 2
            if elem[:moitie] == elem[moitie:]:
                elem = elem[:moitie]
        nettoyes.append(elem)
    return ",".join(dict.fromkeys(nettoyes))

def anime_to_dict(anime_lines):
    """Convertit une liste de lignes [Clé:Valeur] en dictionnaire Python."""
    data = {}
    for champ in anime_lines:
        texte = champ[0]
        if ":" in texte:
            key, value = texte.split(":", 1)
            data[key.strip()] = value.strip()
    return data

# --- FONCTION PRINCIPALE DE TRAITEMENT ---

def process_mal_data(dossier_source=r"donneMAL", chemin_export_excel=r"MAL_dataset.xlsx"):
    """
    Lit les fichiers .txt d'un dossier, les nettoie et les exporte en Excel.
    """
    mal_extraction = []

    # 1. Lecture et filtrage des fichiers
    if not os.path.exists(dossier_source):
        print(f"Erreur : Le dossier {dossier_source} n'existe pas.")
        return

    for filename in sorted(os.listdir(dossier_source)):
        if filename.endswith(".txt"):
            filepath = os.path.join(dossier_source, filename)
            fichier_data = [["Name:" + filename.replace(".txt", "")]]

            with open(filepath, newline="", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=";")
                for ligne in reader:
                    if not ligne: continue
                    valeur = ligne[0]
                    key = valeur.split(":", 1)[0]
                    if not valeur.startswith(LIGNES_A_SUPPRIMER) and key not in CLES_A_SUPPRIMER:
                        fichier_data.append(ligne)
            
            mal_extraction.append(fichier_data)

    # 2. Conversion en dictionnaires et nettoyage
    anime_dicts = []
    for anime_lines in mal_extraction:
        anime = anime_to_dict(anime_lines)
        
        # Application des filtres de nettoyage
        if "Score" in anime: anime["Score"] = score_nettoyage(anime["Score"])
        if "Duration" in anime: anime["Duration"] = duree_nettoyage(anime["Duration"])
        if "Ranked" in anime: anime["Ranked"] = extraire_rang(anime["Ranked"])
        if "Studios" in anime: anime["Studios"] = garder_premier_studio(anime["Studios"])
        
        for field in ["Genres", "Themes", "Demographic"]:
            if field in anime: anime[field] = nettoyer_genres_themes(anime[field])

        if "Premiered" in anime:
            season, year = nettoyer_premiered(anime["Premiered"])
            anime["Season"], anime["Year"] = season, year
            del anime["Premiered"]
        
        anime_dicts.append(anime)

    # 3. Création du DataFrame et formatage final
    df = pd.DataFrame(anime_dicts)
    
    # Nettoyage des colonnes numériques (gestion des virgules et types)
    cols_to_fix = ["Members", "Favorites", "Completed"]
    for col in cols_to_fix:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').replace('nan', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

    if "Episodes" in df.columns:
        df['Episodes'] = pd.to_numeric(df['Episodes'].replace('Unknown', None), errors='coerce').astype('Int64')

    # 4. Export
    df.to_excel(chemin_export_excel, index=False)
    print(f"✔ Export terminé : {chemin_export_excel} ({len(df)} entrées)")
    return df