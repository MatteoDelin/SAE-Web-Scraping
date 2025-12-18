import requests
import urllib.robotparser as robotparser
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0; +https://example.com/bot-info)"
}

def check_scraping_access(url):
    result = {
        "url": url,
        "robots_allowed": None,
        "http_status": None,
        "blocked_reason": None,
        "anti_bot_suspected": False
    }

    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    # 1️⃣ Vérification robots.txt
    rp = robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        result["robots_allowed"] = rp.can_fetch(HEADERS["User-Agent"], url)
    except Exception:
        result["robots_allowed"] = "unknown"

    # 2️⃣ Test réel de requête
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        result["http_status"] = response.status_code

        if response.status_code in [401, 403]:
            result["blocked_reason"] = "Accès refusé (403/401)"
        elif response.status_code == 429:
            result["blocked_reason"] = "Rate limit (429)"
        elif response.status_code >= 500:
            result["blocked_reason"] = "Erreur serveur"

        # 3️⃣ Détection basique anti-bot
        anti_bot_keywords = [
            "captcha", "cloudflare", "access denied",
            "verify you are human", "blocked"
        ]
        body_lower = response.text.lower()
        if any(k in body_lower for k in anti_bot_keywords):
            result["anti_bot_suspected"] = True

    except requests.exceptions.RequestException as e:
        result["blocked_reason"] = str(e)

    return result

url = "https://myanimelist.net"
info = check_scraping_access(url)

for k, v in info.items():
    print(f"{k}: {v}")
