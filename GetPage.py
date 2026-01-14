import requests
import urllib.robotparser as robotparser
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"
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

def scrape_by_class(url, class_name, lien = False):
    """
    Récupère le contenu de toutes les balises ayant la classe donnée
    """
    if not can_scrape(url):
        raise PermissionError("Le scraping est interdit par robots.txt")

    response = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    elements = soup.find_all(class_=class_name)
    results = []
    for el in elements:
        if lien :
            text = el.get("href") 
        else :
            text = el.get_text(strip=True)
        if text:
            results.append(text)
    return results

def get_data_page_mal(url):
    class_to_scrape = "spaceit_pad"
    data = scrape_by_class(url+"/stats", class_to_scrape)
    return data

def get_url_mal(s,n):
    url = "https://myanimelist.net/topanime.php?limit="
    class_to_scrape = "hoverinfo_trigger fl-l ml12 mr8"
    ls_url = []
    for i in range(s,n,50):
        print(i)
        ls_url += scrape_by_class(url+str(i), class_to_scrape, True)
    return ls_url

def export_txt(texte, nom):
    nom_nettoye = re.sub(r'[^\w\s.-]', '_', nom)
    nom_nettoye = nom_nettoye[:150]
    with open("donneMAL/" + nom_nettoye + ".txt", "w", encoding="utf-8") as f:
        f.write("\n".join(texte))

def GetPage():
    lien_mal=get_url_mal(0,1500)
    print("Scrape lien fini")
    for i in range(len(lien_mal)):
        data=get_data_page_mal(lien_mal[i])
        export_txt(data,lien_mal[i].strip('/').split('/')[-1])
        print(i,") scrape fini pour :"+lien_mal[i].strip('/').split('/')[-1])