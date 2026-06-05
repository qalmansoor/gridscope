from fetcher import fetch_articles as fetch_rss_articles
from news_fetcher import fetch_news_api_articles

def fetch_all_articles(max_rss=15, max_newsapi=15):
    """
    Combines RSS and NewsAPI sources into a single deduplicated article list.
    """
    print("=" * 50)
    print("FETCHING RSS SOURCES")
    print("=" * 50)
    rss_articles = fetch_rss_articles(max_per_feed=3)

    print("\n" + "=" * 50)
    print("FETCHING NEWSAPI SOURCES")
    print("=" * 50)
    newsapi_articles = fetch_news_api_articles(max_articles=max_newsapi)

    # Combine and deduplicate by title
    seen_titles = set()
    combined = []

    for article in rss_articles + newsapi_articles:
        title = article.get("title", "").strip().lower()
        if title not in seen_titles:
            seen_titles.add(title)
            combined.append(article)

    print(f"\n{'=' * 50}")
    print(f"COMBINED TOTAL: {len(combined)} unique articles")
    print(f"  RSS: {len(rss_articles)} | NewsAPI: {len(newsapi_articles)}")
    print(f"{'=' * 50}\n")

    return combined


if __name__ == "__main__":
    articles = fetch_all_articles()
    for a in articles:
        print(f"[{a['source']}] {a['title']}")