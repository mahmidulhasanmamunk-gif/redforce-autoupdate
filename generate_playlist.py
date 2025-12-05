import json
import requests
from datetime import datetime

INPUT_FILE = "sources.json"
OUTPUT_FILE = "playlist.m3u"

def is_alive(url):
    try:
        r = requests.get(url, timeout=8)
        return r.status_code == 200
    except:
        return False


def load_sources():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def build_m3u(sources):
    lines = ["#EXTM3U\n"]

    for s in sources:
        name = s["name"]
        group = s["group"]
        url = s["url"]

        if not is_alive(url):
            continue

        lines.append(f'#EXTINF:-1 group-title="{group}",{name}\n')
        lines.append(url + "\n")

    lines.append(f"# Updated: {datetime.utcnow().isoformat()}Z\n")
    return "".join(lines)


def main():
    sources = load_sources()
    playlist = build_m3u(sources)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(playlist)

    print("playlist.m3u generated")


if __name__ == "__main__":
    main()
