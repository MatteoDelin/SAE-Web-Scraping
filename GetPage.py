# Bibliothèque pour effectuer des requêtes HTTP
import requests
# Module pour lire et interpréter le fichier robots.txt
import urllib.robotparser as robotparser
# Permet de découper et analyser une URL
from urllib.parse import urlparse
# Librairie pour parser le HTML
from bs4 import BeautifulSoup
# Module pour les expressions régulières (nettoyage des noms de fichiers)
import re


# En-têtes HTTP envoyés avec chaque requête
# Le User-Agent est important pour ne pas être bloqué par certains sites
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"
}


def can_scrape(url):
    """
    Vérifie si le scraping de l'URL est autorisé
    en lisant le fichier robots.txt du site.
    Retourne True si autorisé, False sinon.
    """
    # Analyse de l'URL (schéma, domaine, etc.)
    parsed = urlparse(url)

    # Construction de l'URL du fichier robots.txt
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    # Création du parser robots.txt
    rp = robotparser.RobotFileParser()
    try:
        # Chargement et lecture du fichier robots.txt
        rp.set_url(robots_url)
        rp.read()

        # Vérifie si le User-Agent a le droit d'accéder à l'URL
        return rp.can_fetch(HEADERS["User-Agent"], url)
    except Exception:
        # En cas d'erreur, on considère que le scraping est interdit
        return False


def scrape_by_class(url, class_name, lien=False):
    """
    Scrape une page web et récupère le contenu de toutes les balises
    ayant la classe CSS donnée.

    - url : page à scraper
    - class_name : classe CSS à rechercher
    - lien : si True, récupère l'attribut 'href', sinon le texte
    """
    # Vérification des règles robots.txt
    if not can_scrape(url):
        raise PermissionError("Le scraping est interdit par robots.txt")

    # Requête HTTP GET
    response = requests.get(url, headers=HEADERS, timeout=10)

    # Parsing du HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Recherche de toutes les balises ayant la classe donnée
    elements = soup.find_all(class_=class_name)

    results = []

    # Parcours des éléments trouvés
    for el in elements:
        if lien:
            # Si lien=True, on récupère l'attribut href
            text = el.get("href")
        else:
            # Sinon, on récupère le texte visible
            text = el.get_text(strip=True)

        # On ajoute uniquement les valeurs non vides
        if text:
            results.append(text)

    return results


def get_data_page_mal(url):
    """
    Récupère les statistiques d'une page MyAnimeList
    """
    class_to_scrape = "spaceit_pad"

    # Ajout de /stats à l'URL
    data = scrape_by_class(url + "/stats", class_to_scrape)

    return data


def get_url_mal(s, n):
    """
    Récupère les URLs des pages d'anime depuis le classement MyAnimeList

    - s : index de départ
    - n : index de fin
    """
    url = "https://myanimelist.net/topanime.php?limit="
    class_to_scrape = "hoverinfo_trigger fl-l ml12 mr8"

    ls_url = []

    # MyAnimeList affiche 50 résultats par page
    for i in range(s, n, 50):
        print(i)

        # Récupération des liens (href)
        ls_url += scrape_by_class(url + str(i), class_to_scrape, True)

    return ls_url


def export_txt(texte, nom):
    """
    Exporte les données dans un fichier texte
    en nettoyant le nom du fichier.
    """
    # Suppression des caractères interdits dans les noms de fichiers
    nom_nettoye = re.sub(r'[^\w\s.-]', '_', nom)

    # Limite de longueur du nom de fichier
    nom_nettoye = nom_nettoye[:150]

    # Écriture dans un fichier texte
    with open("donneMAL/" + nom_nettoye + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(texte))


def GetPage():
    """
    Fonction principale :
    - récupère tous les liens d'anime
    - scrape leurs statistiques
    - exporte les données dans des fichiers texte
    """
    # Récupération des URLs des animes
    lien_mal = get_url_mal(0, 1500)
    print("Scrape lien fini")

    # Parcours de chaque anime
    for i in range(len(lien_mal)):
        data = get_data_page_mal(lien_mal[i])

        # Nom du fichier basé sur l'URL
        nom = lien_mal[i].strip('/').split('/')[-1]

        export_txt(data, nom)
        print(i, ") scrape fini pour :", nom)

    print("Scrapping de tous les liens finis, données exportées dans : donneMal")


# Lancement du script
GetPage()
