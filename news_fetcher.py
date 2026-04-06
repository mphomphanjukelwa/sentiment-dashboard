# news_fetcher.py
# Connects to NewsAPI and pulls real headlines
# from 150,000+ news sources worldwide

from newsapi import NewsApiClient
import os
from dotenv import load_dotenv

# Reads your .env file and loads NEWS_API_KEY
# into the environment so os.getenv() can find it
load_dotenv()

def get_news_client():
    """Creates and returns a NewsAPI connection."""
    api_key = os.getenv("NEWS_API_KEY")

    # Safety check — tells you clearly if .env is misconfigured
    if not api_key:
        raise ValueError(
            "NEWS_API_KEY not found. Check your .env file."
        )

    return NewsApiClient(api_key=api_key)

def fetch_headlines(topic, page_size=50):
    """
    Fetches recent news headlines about a topic.

    Parameters:
        topic     : keyword to search e.g. 'nvidia', 'AI', 'bitcoin'
        page_size : how many articles to fetch (max 100 on free plan)

    Returns:
        A list of dicts. Each dict = one article with keys:
        title, text, url, source
    """
    client = get_news_client()
    # get_everything() searches all sources for a keyword
    # sort by publishedAt = most recent articles first
    response = client.get_everything(
        q=topic,
        language='en',
        sort_by='publishedAt',
        page_size=page_size
    )

    articles = []
    for article in response['articles']:

        # Some articles have None for title or description
        # We use 'or ""' to replace None with an empty string
        title = article['title'] or ""
        description = article['description'] or ""

        # Skip articles with no title — nothing to analyze
        if not title:
            continue
        
        articles.append({
            "title"  : title,
            "text"   : description,
            "url"    : article['url'] or "",
            "source" : article['source']['name'] or "Unknown"
        })

    return articles


# ── Test block ──────────────────────────────────────────
# This only runs when you execute THIS file directly:
#   python news_fetcher.py
# It will NOT run when main.py imports from this file.
if __name__ == "__main__":
    print("Testing NewsAPI connection...")
    articles = fetch_headlines("artificial intelligence", page_size=5)

    if not articles:
        print("No articles returned. Check your API key.")
    else:
        print(f"Successfully fetched {len(articles)} articles:\n")
        for a in articles:
            print(f"  [{a['source']}]")
            print(f"   {a['title'][:70]}")
            print()