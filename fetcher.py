import feedparser

FEEDS = {
    # Global energy with GCC relevance
    "Financial Times Energy": "https://www.ft.com/energy?format=rss",
    "Energy Monitor": "https://www.energymonitor.ai/feed/",
    "Carbon Brief": "https://www.carbonbrief.org/feed",
    "Oil Price News": "https://oilprice.com/rss/main",
    "BBC Business": "http://feeds.bbci.co.uk/news/business/rss.xml",

    # Middle East focused
    "Al Monitor": "https://www.al-monitor.com/rss",
    "Offshore Energy": "https://www.offshore-energy.biz/feed/",
    "Energy Central": "https://energycentral.com/rss.cfm",

    # Renewables and technology
    "PV Tech": "https://www.pv-tech.org/feed",
    "Energy Storage News": "https://www.energystoragenews.com/feed/",
    "Hydrogen Insight": "https://www.hydrogeninsight.com/rss",
    "S&P Commodity Natural Gas": "https://www.spglobal.com/commodityinsights/en/rss-feed/natural-gas",
}

def fetch_articles(max_per_feed=3):
    all_articles = []

    for source, url in FEEDS.items():
        try:
            feed = feedparser.parse(url)
            entries = feed.entries[:max_per_feed]

            for entry in entries:
                article = {
                    "source": source,
                    "title": entry.get("title", "No title"),
                    "summary": entry.get("summary", "No summary available"),
                    "link": entry.get("link", ""),
                    "published": entry.get("published", "Unknown date")
                }
                all_articles.append(article)

            if len(entries) > 0:
                print(f"[OK] {source}: fetched {len(entries)} articles")
            else:
                print(f"[FAIL] {source}: connected but returned 0 articles")

        except Exception as e:
            print(f"[FAIL] {source}: failed - {e}")

    return all_articles


if __name__ == "__main__":
    articles = fetch_articles()
    print(f"\nTotal articles fetched: {len(articles)}")