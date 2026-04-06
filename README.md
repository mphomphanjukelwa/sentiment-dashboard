# Sentiment Dashboard

A real-time news sentiment analysis pipeline built with Python and DistilBERT. Fetches live headlines from 150,000+ news sources via NewsAPI, classifies each one as positive or negative using a pre-trained transformer model, and outputs a formatted sentiment report.

Built as Phase 1 of a 6-month AI/ML portfolio project targeting roles at FAANG-tier companies.

---

## What it does

- Fetches live news headlines on any topic (e.g. `"nvidia"`, `"bitcoin"`, `"climate change"`)
- Runs each headline through DistilBERT, a transformer-based NLP model fine-tuned for sentiment classification
- Outputs a sentiment report showing positive/negative split, confidence scores, and most extreme headlines
- Fully modular — the fetcher, analyzer, and runner are separate files that can be extended independently

---

## Demo output

```
Fetching 20 headlines about: 'nvidia'
--------------------------------------------------
Fetched 20 articles. Running sentiment analysis...

=======================================================
  SENTIMENT REPORT — NVIDIA
=======================================================
  Total articles : 20
  Positive       : 13  (65%)
  Negative       : 7   (35%)

  [█████████████░░░░░░░] 65% positive

  Most positive headline:
  [+] 0.999 | NVIDIA smashes earnings expectations again
      Source: Reuters

  Most negative headline:
  [-] 0.998 | AI chip shortage causes production delays
      Source: BBC News
=======================================================
```

---

## Tech stack

| Layer | Tool | Purpose |
|---|---|---|
| Language | Python 3.11 | Core language |
| NLP Model | DistilBERT (HuggingFace) | Sentiment classification |
| ML Framework | PyTorch | Model inference backend |
| Data Source | NewsAPI | Live headlines from 150k+ sources |
| Config | python-dotenv | Secure API key management |
| Planned | Streamlit + Plotly | Interactive web dashboard (Week 2) |
| Planned | SQLite | Persistent sentiment history (Week 2) |

---

## Project structure

```
sentiment-dashboard/
├── news_fetcher.py        # Connects to NewsAPI, fetches headlines by topic
├── sentiment_analyzer.py  # Loads DistilBERT, classifies text sentiment
├── main.py                # Entry point — runs the full pipeline
├── .env                   # API keys (not committed — see setup below)
├── .gitignore             # Excludes venv, .env, __pycache__
└── requirements.txt       # All dependencies with pinned versions
```

---

## Setup

### Prerequisites

- Python 3.11 (not 3.12+ — some ML libraries lag behind)
- A free NewsAPI key from [newsapi.org](https://newsapi.org)
- Git

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/sentiment-dashboard.git
cd sentiment-dashboard
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

You should see `(.venv)` at the start of your terminal prompt.

### 3. Install dependencies

Always use `python -m pip` to ensure packages install into the active venv:

```bash
python -m pip install -r requirements.txt
```

> First run downloads the DistilBERT model (~250MB). This is cached after the first run.

### 4. Configure your API key

Create a `.env` file in the project root:

```
NEWS_API_KEY=your_newsapi_key_here
```

Never commit this file. It is already listed in `.gitignore`.

---

## Usage

### Run the pipeline

```bash
python main.py
```

By default this searches for `"nvidia"` headlines. To change the topic, open `main.py` and edit the last line:

```python
run_pipeline(topic="tesla", limit=20)
```

### Change the topic without editing the file

You can also call the function directly from a Python shell:

```python
from main import run_pipeline
run_pipeline(topic="openai", limit=50)
```

### Topic ideas to try

```
"artificial intelligence"   "bitcoin"        "climate change"
"tesla"                     "openai"         "apple"
"amazon"                    "cybersecurity"  "federal reserve"
```

---

## How it works

### Architecture

```
NewsAPI ──► news_fetcher.py ──► list of article dicts
                                        │
                                        ▼
                          sentiment_analyzer.py
                          (DistilBERT via HuggingFace)
                                        │
                                        ▼
                                    main.py
                               (report + output)
```

### Sentiment model

The project uses `distilbert-base-uncased-finetuned-sst-2-english` — a lightweight version of BERT fine-tuned on the Stanford Sentiment Treebank (SST-2) dataset. It classifies text as `POSITIVE` or `NEGATIVE` with a confidence score between 0.0 and 1.0.

DistilBERT was chosen over full BERT because:
- 40% smaller and 60% faster with only 3% accuracy loss
- Runs on CPU without a GPU
- Widely used in production NLP systems

### Data pipeline

1. `fetch_headlines(topic, page_size)` calls the NewsAPI `/everything` endpoint, filtering for English-language articles sorted by recency
2. Each article is represented as a dict: `{title, text, url, source}`
3. `analyze_articles(articles)` iterates over the list, concatenates title + description, and passes each to `analyze_sentiment()`
4. `analyze_sentiment(text)` truncates to 500 characters (DistilBERT's 512-token limit), runs inference, and returns `{label, score}`
5. `run_pipeline()` aggregates results and renders the report

---

## Skills demonstrated

- **NLP / Transformers** — loading and running a pre-trained HuggingFace model for inference
- **REST API integration** — authenticated requests to NewsAPI with environment-variable key management
- **Modular Python design** — separation of concerns across fetcher, analyzer, and runner modules
- **Virtual environment management** — isolated dependencies with pinned versions
- **Data pipeline design** — structured flow from raw API response to enriched output

---

## Roadmap

This project is being built in weekly increments:

- [x] Week 1 — NewsAPI fetcher + DistilBERT sentiment pipeline
- [ ] Week 2 — SQLite database layer for persistent sentiment history
- [ ] Week 3 — Streamlit dashboard with Plotly trend charts and live refresh
- [ ] Week 4 — BERTopic clustering to group headlines by theme
- [ ] Week 5–6 — Deploy to Streamlit Cloud with public demo link

---

## Notes on the free NewsAPI tier

The free plan allows 100 requests/day and returns articles from the past 30 days. During development this project uses approximately 5–10 requests per session. If you hit the daily limit, wait until midnight UTC for it to reset.

---

## License

MIT
