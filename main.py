# main.py
# The entry point of the project.
# Imports from our two modules and runs the full pipeline:
#   1. Fetch headlines from NewsAPI
#   2. Run DistilBERT sentiment on each headline
#   3. Print a formatted report

from news_fetcher import fetch_headlines
from sentiment_analyzer import analyze_articles


def run_pipeline(topic="artificial intelligence", limit=20):
    """
    Full pipeline: fetch → analyze → report.

    Parameters:
        topic : keyword to search e.g. 'nvidia', 'tesla', 'bitcoin'
        limit : number of articles to fetch and analyze
    """
    print(f"\nFetching {limit} headlines about: '{topic}'")
    print("-" * 50)

    # Step 1: Fetch articles from NewsAPI
    articles = fetch_headlines(topic, page_size=limit)

    if not articles:
        print("No articles found. Try a different topic.")
        return

    print(f"Fetched {len(articles)} articles. Running sentiment analysis...")

    # Step 2: Add sentiment labels to every article
    articles = analyze_articles(articles)

    # Step 3: Split into positive and negative lists
    positive = [a for a in articles if a["sentiment"] == "POSITIVE"]
    negative = [a for a in articles if a["sentiment"] == "NEGATIVE"]
    pct_pos  = len(positive) / len(articles) * 100

    # Step 4: Print the report
    print(f"\n{'='*55}")
    print(f"  SENTIMENT REPORT — {topic.upper()}")
    print(f"{'='*55}")
    print(f"  Total articles : {len(articles)}")
    print(f"  Positive        : {len(positive)}  ({pct_pos:.0f}%)")
    print(f"  Negative        : {len(negative)}  ({100-pct_pos:.0f}%)")

    # Visual sentiment bar e.g.  [████████░░░░░░░░]  55% positive
    filled = int(pct_pos / 5)
    bar = "█" * filled + "░" * (20 - filled)
    print(f"\n  [{bar}] {pct_pos:.0f}% positive\n")

    # Most confident POSITIVE headline
    if positive:
        top_pos = max(positive, key=lambda a: a["confidence"])
        print(f"  Most positive headline:")
        print(f"  [+] {top_pos['confidence']} | {top_pos['title'][:60]}")
        print(f"      Source: {top_pos['source']}")

# Most confident NEGATIVE headline
    if negative:
        top_neg = max(negative, key=lambda a: a["confidence"])
        print(f"\n  Most negative headline:")
        print(f"  [-] {top_neg['confidence']} | {top_neg['title'][:60]}")
        print(f"      Source: {top_neg['source']}")

    print(f"\n{'='*55}")
    print(f"\nAll {len(articles)} headlines:\n")

    for a in articles:
        icon = "[+]" if a["sentiment"] == "POSITIVE" else "[-]"
        print(f"  {icon} {a['confidence']} | {a['title'][:55]}")
        print(f"       {a['source']}")


if __name__ == "__main__":
    # Change the topic to anything you're interested in:
    # "nvidia", "bitcoin", "climate change", "apple", "tesla"
    run_pipeline(topic="nvidia", limit=20)