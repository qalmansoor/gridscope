from newsapi import NewsApiClient
import os

# Only pull from these trusted energy and business sources
TRUSTED_SOURCES = (
    "bbc.co.uk,reuters.com,ft.com,bloomberg.com,"
    "spglobal.com,oilprice.com,energymonitor.ai,"
    "pv-tech.org,rechargenews.com,offshore-energy.biz,"
    "al-monitor.com,arabnews.com,gulfbusiness.com,"
    "thenationalnews.com,zawya.com,meed.com,"
    "hydrogeninsight.com,carbonbrief.org,energycentral.com,"
    "argusmedia.com,platts.com,naturalgasintel.com"
)

def fetch_news_api_articles(max_articles=15):
    """
    Fetches GCC and Middle East energy articles via NewsAPI.
    Uses source whitelist to ensure quality.
    """
    import streamlit as st
    api_key = os.environ.get("NEWS_API_KEY") or st.secrets.get("NEWS_API_KEY")
    if not api_key:
        print("✗ NewsAPI: No API key found in environment variables")
        return []

    newsapi = NewsApiClient(api_key=api_key)

    queries = [
        "Saudi Arabia energy OR electricity OR solar OR oil",
        "UAE energy OR ADNOC OR EWEC OR Masdar",
        "GCC energy transition OR renewable",
        "OPEC oil production Gulf",
        "Middle East power generation OR utilities",
    ]

    all_articles = []
    seen_titles = set()

    for query in queries:
        try:
            response = newsapi.get_everything(
                q=query,
                language="en",
                sort_by="publishedAt",
                page_size=10,
                domains=TRUSTED_SOURCES
            )

            articles = response.get("articles", [])
            added = 0

            for article in articles:
                title = article.get("title", "No title")

                if title in seen_titles:
                    continue
                seen_titles.add(title)

                formatted = {
                    "source": f"NewsAPI — {article.get('source', {}).get('name', 'Unknown')}",
                    "title": title,
                    "summary": article.get("description") or article.get("content") or "No summary available",
                    "link": article.get("url", ""),
                    "published": article.get("publishedAt", "Unknown date")
                }

                all_articles.append(formatted)
                added += 1

            print(f"✓ NewsAPI '{query[:45]}': {added} articles from trusted sources")

        except Exception as e:
            print(f"✗ NewsAPI query failed — {e}")

    result = all_articles[:max_articles]
    print(f"\nNewsAPI total articles: {len(result)}")
    return result


if __name__ == "__main__":
    articles = fetch_news_api_articles()
    for a in articles:
        print(f"\n[{a['source']}] {a['title']}")
        print(f"  {a['summary'][:150]}...")