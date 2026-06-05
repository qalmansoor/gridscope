import feedparser

FEEDS = {
    # Global energy with GCC relevance
    "Financial Times Energy": "https://www.ft.com/energy?format=rss",
    "Energy Monitor": "https://www.energymonitor.ai/feed/",
    "Carbon Brief": "https://www.carbonbrief.org/feed",
    "Oil Price News": "https://oilprice.com/rss/main",
    "BBC Business": "http://feeds.bbci.co.uk/news/business/rss.xml",

    # Middle East focused
    "Arab News Business": "https://www.arabnews.com/cat/3/rss.xml",
    "Arab News Energy": "https://www.arabnews.com/tags/energy/rss.xml",
    "Gulf Times Business": "https://www.gulf-times.com/rss/feed/3",
    "Al Monitor Energy": "https://www.al-monitor.com/rss",
    "MENA FN Energy": "https://menafn.com/rss/menafn_energy.xml",
    "zawya Business": "https://www.zawya.com/rss/economy",

    # Renewables and transition
    "Renewables Now": "https://renewablesnow.com/feed/",
    "PV Tech": "https://www.pv-tech.org/feed",
    "Recharge News": "https://www.rechargenews.com/rss",
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
                print(f"✓ {source}: fetched {len(entries)} articles")
            else:
                print(f"✗ {source}: connected but returned 0 articles")

        except Exception as e:
            print(f"✗ {source}: failed — {e}")

    return all_articles


if __name__ == "__main__":
    articles = fetch_articles()
    print(f"\nTotal articles fetched: {len(articles)}")
    for a in articles:
        print(f"\n[{a['source']}] {a['title']}")
        print(f"  {a['summary'][:150]}...")