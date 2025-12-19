import requests
import urllib.robotparser as robotparser
from urllib.parse import urlparse
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0; +https://example.com/bot-info)"
}

def can_scrape(url):
    """
    Vérifie si le scraping est autorisé via robots.txt
    """
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(HEADERS["User-Agent"], url)
    except Exception:
        return False


def scrape_by_class(url, class_name):
    """
    Récupère le contenu de toutes les balises ayant la classe donnée
    """
    if not can_scrape(url):
        raise PermissionError("Le scraping est interdit par robots.txt")

    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        raise Exception(f"Erreur HTTP : {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")

    elements = soup.find_all(class_=class_name)

    results = []
    for el in elements:
        # texte nettoyé
        text = el.get_text(strip=True)
        if text:
            results.append(text)

    return results


# 🧪 Exemple d'utilisation
if __name__ == "__main__":
    url = "https://anilist.co/anime/21/ONE-PIECE"
    class_to_scrape = "data"

    try:
        data = scrape_by_class(url, class_to_scrape)
        for i, item in enumerate(data, 1):
            print(f"{i}. {item}")
    except Exception as e:
        print("Erreur :", e)
