import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

BASE_URL = "https://redforce.live/"
PAGE_URL = BASE_URL

OUTPUT_FILE = "sources.json"

def fetch_links():
    r = requests.get(PAGE_URL, timeout=10)
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
    links = fetch_links()
    print(f"Found {len(links)} links")
    save_list(links)
    print("sources.json updated:", datetime.utcnow().isoformat())


if __name__ == "__main__":
    main()
