import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

BASE_URL = "https://redforce.live/"
PAGE_URL = BASE_URL

OUTPUT_FILE = "sources.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
}

def fetch_links():
    session = requests.Session()

    # Allow scraping sites that block bots
    session.headers.update(HEADERS)

    # Stronger retry system
    adapter = requests.adapters.HTTPAdapter(max_retries=5)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    r = session.get(PAGE_URL, timeout=25)   # extended timeout
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    links = []

    pattern = re.compile(r"(https?://[^\"'>]+\.m3u8[^\"'>]*)")
    matches = pattern.findall(r.text)

    for i, url in enumerate(matches):
        links.append({
            "name": f"Channel {i+1}",
            "group": "LiveTV",
            "url": url
        })

    return links


def save_list(links):
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(links, f, indent=2, ensure_ascii=False)


def main():
    try:
        links = fetch_links()
        print(f"Found {len(links)} links")
        save_list(links)
        print("sources.json updated:", datetime.utcnow().isoformat())
    except Exception as e:
        print("Scraper Error:", e)


if __name__ == "__main__":
    main()
