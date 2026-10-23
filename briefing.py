
import json
from datetime import datetime, timezone

PRIORITY_WORDS = {
    "AI Safety & Agents": [
        "safety", "alignment", "benchmark", "frontier",
        "agent", "research", "model"
    ],
    "AI Chips & Supply Chain": [
        "nvidia", "tsmc", "hbm", "gpu", "chip",
        "packaging", "memory", "supply"
    ],
    "Technology Investing": [
        "earnings", "revenue", "capex", "hyperscaler",
        "enterprise", "cloud", "investment"
    ],
    "Public X Discussions": [
        "agent", "research", "security",
        "benchmark", "ai", "chip"
    ]
}

def score(article, category):
    title = article.get("title", "").lower()
    return sum(
        1 for word in PRIORITY_WORDS[category]
        if word in title
    )

def main():
    with open("news.json", encoding="utf-8") as f:
        news = json.load(f)

    date = datetime.now(timezone.utc).strftime("%B %d, %Y")

    lines = [
        f"AI INTELLIGENCE BRIEF — {date}",
        "",
        "AI Safety | Semiconductors | Tech Investing",
        ""
    ]

    for category, articles in news["topics"].items():
        lines.append(f"=== {category.upper()} ===")

        ranked = sorted(
            articles,
            key=lambda a: score(a, category),
            reverse=True
        )

        for article in ranked[:3]:
            lines.append(f"• {article['title']}")
            lines.append(article["url"])
            lines.append("")

    lines.append(
        "Note: Headlines are automatically selected. "
        "Claims and investment implications have not "
        "been independently verified."
    )

    with open("briefing.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("Briefing generated successfully.")

if __name__ == "__main__":
    main()
