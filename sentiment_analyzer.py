# sentiment_analyzer.py
# Loads DistilBERT and classifies text as
# POSITIVE or NEGATIVE with a confidence score

from transformers import pipeline

# This line downloads the DistilBERT model the FIRST time only.
# Download size: ~250MB. Expected time: 2–4 minutes.
# After that it's cached — every future run is instant.
# Do not close the terminal while it downloads.
print("Loading DistilBERT model...")
print("(First run downloads ~250MB — please wait)")

classifier = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

print("Model loaded and ready.\n")


def analyze_sentiment(text):
    """
    Runs sentiment analysis on a string of text.

    Parameters:
        text : any string — a headline, sentence, paragraph

    Returns a dict:
        {
          "label": "POSITIVE" or "NEGATIVE",
          "score": confidence from 0.0 to 1.0
        }
    """
    # Return neutral for empty or very short text
    if not text or len(text.strip()) < 3:
        return {"label": "NEUTRAL", "score": 0.5}

    # DistilBERT's maximum input is 512 tokens.
    # We slice to 500 characters as a safe approximation.
    result = classifier(text[:500])[0]

    return {
        "label" : result["label"],
        "score" : round(result["score"], 3)
    }


def analyze_articles(articles):
    """
    Accepts a list of article dicts (from news_fetcher.py)
    and adds 'sentiment' and 'confidence' keys to each one.
    Modifies and returns the same list.
    """
    for article in articles:
        # Combine title + description for richer analysis
        content = article["title"] + " " + article.get("text", "")
        result = analyze_sentiment(content)

        article["sentiment"]   = result["label"]
        article["confidence"]  = result["score"]

    return articles

# ── Test block ──────────────────────────────────────────
if __name__ == "__main__":
    test_cases = [
        "NVIDIA stock surges to record high on AI chip demand",
        "Tech layoffs hit 50,000 workers as recession fears grow",
        "Apple releases software update for iPhone",
    ]
    print("Running test cases:\n")
    for text in test_cases:
        r = analyze_sentiment(text)
        bar = "█" * int(r["score"] * 20)
        print(f"  {r['label']:9} {r['score']} {bar}")
        print(f"  {text[:65]}\n")

