import anthropic
import os
from datetime import datetime
from combined_fetcher import fetch_all_articles as fetch_articles


def generate_briefing(articles):
    article_block = ""
    for i, a in enumerate(articles, 1):
        article_block += f"Article {i}:\nSource: {a['source']}\nTitle: {a['title']}\nSummary: {a['summary'][:300]}\n---\n"

    today = datetime.now().strftime('%d %B %Y')

    prompt = f"""You are a senior GCC energy analyst. Write a weekly briefing for a GCC energy CEO reading on their phone between meetings.

HARD RULES:
- TOTAL OUTPUT: 300 words maximum.
- Each development: 2 sentences of analysis only.
- Signal to Watch: 2 sentences only.
- Market Pulse: 1 sentence only.
- No padding. No filler. No over-explanation.

USE THIS EXACT FORMAT — copy it exactly including the blank lines:

---
**GRIDSCOPE | GCC ENERGY INTELLIGENCE | {today}**

---

**30-SECOND READ**

[2 sentences. Most important GCC energy story and its implication.]

---

**TOP 3 DEVELOPMENTS**

**1. [Headline, max 15 words]**

[2 sentences. End with GCC implication.]

**2. [Headline, max 15 words]**

[2 sentences. End with GCC implication.]

**3. [Headline, max 15 words]**

[2 sentences. End with GCC implication.]

---

**SIGNAL TO WATCH**

[2 sentences. Name specific companies or countries.]

---

**MARKET PULSE**

[1 sentence only.]

---
*GridScope | Powered by Claude AI*

Here are this week's articles:

{article_block}

Write the briefing now. Maximum 300 words. Keep blank lines between every section label and its content."""

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=600,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return message.content[0].text


if __name__ == "__main__":
    print("Fetching articles...\n")
    articles = fetch_articles()
    print(f"\nGenerating briefing from {len(articles)} articles...\n")
    print("=" * 60)
    briefing = generate_briefing(articles)
    print(briefing)
    print("=" * 60)