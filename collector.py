
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

TOPICS = {
    "AI Safety & Agents":
        '"AI safety" OR "AI agents" OR "alignment" when:1d',
    "AI Chips & Supply Chain":
        '"NVIDIA" OR "TSMC" OR "HBM" OR "AI chips" when:1d',
    "Technology Investing":
        '"hyperscaler" OR "enterprise AI" OR "tech earnings" when:1d',
    "Public X Discussions":
        'site:x.com "AI agents" OR "AI chips" when:1d'
}

def search_news(query):
    encoded = urllib.parse.quote(query)
    url = (
        "https://news.google.com/rss/search?q="
        + encoded
        + "&hl=en-US&gl=US&ceid=US:en"
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        xml_data = response.read()

    root = ET.fromstring(xml_data)
    articles = []

    for item in root.findall("./channel/item")[:10]:
        articles.append({
            "title": item.findtext("title", ""),
            "url": item.findtext("link", ""),
            "published": item.findtext("pubDate", "")
        })

    return articles

def main():
    results = {
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "topics": {}
    }

    for topic, query in TOPICS.items():
        try:
            results["topics"][topic] = search_news(query)
            print(f"Collected: {topic}")
        except Exception as error:
            results["topics"][topic] = []
            print(f"Error collecting {topic}: {error}")

    with open("news.json", "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    print("Collection complete.")

if __name__ == "__main__":
    main()
