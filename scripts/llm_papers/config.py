"""Configuration for LLM papers pipeline."""

from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONTENT_DIR = PROJECT_ROOT / "content" / "blog"
SCRIPTS_DIR = Path(__file__).resolve().parent
STATE_FILE = SCRIPTS_DIR / "processed_papers.json"
LOG_FILE = SCRIPTS_DIR / "pipeline.log"

# arXiv settings
ARXIV_CATEGORIES = ["cs.CL", "cs.AI"]
ARXIV_KEYWORDS = [
    "large language model",
    "LLM",
    "transformer",
    "GPT",
    "BERT",
    "instruction tuning",
    "RLHF",
    "prompt engineering",
    "chain of thought",
    "retrieval augmented generation",
    "RAG",
    "fine-tuning",
    "alignment",
    "reasoning",
]
ARXIV_MAX_RESULTS = 50

# Semantic Scholar settings
SEMANTIC_SCHOLAR_KEYWORDS = [
    "large language model",
    "LLM reasoning",
    "transformer architecture",
]
SEMANTIC_SCHOLAR_LIMIT = 20

# Hugging Face Daily Papers
HF_DAILY_PAPERS_URL = "https://huggingface.co/papers"

# LLM keyword filter (applied to HF papers title/abstract)
LLM_FILTER_KEYWORDS = [
    "language model", "LLM", "transformer", "GPT", "BERT",
    "instruction tuning", "RLHF", "prompt", "chain of thought",
    "retrieval augmented", "RAG", "fine-tuning", "alignment",
    "reasoning", "tokeniz", "attention mechanism", "in-context learning",
    "few-shot", "zero-shot", "text generation", "natural language",
    "chatbot", "dialogue", "summarization", "translation",
    "question answering", "NLP", "embedding",
]

# Fetch window (days to look back for papers)
FETCH_WINDOW_DAYS = 3

# Pipeline settings
TOP_N_PAPERS = 5  # Number of papers to feature with screenshots
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
REQUEST_DELAY = 3.0  # seconds between API calls

# Popularity scoring
POPULARITY_THRESHOLD = 3.0  # Minimum composite score to be considered "popular"
MULTI_SOURCE_BONUS = 5.0  # Bonus for appearing in multiple sources
HF_UPVOTE_WEIGHT = 1.0  # Weight for HuggingFace upvotes
CITATION_WEIGHT = 2.0  # Weight for citation count
MIN_PAPERS_TO_POST = 1  # Minimum popular papers required to publish a blog post

# Hugo settings
HUGO_TAGS = ["LLM", "AI", "論文"]
HUGO_CATEGORIES = ["LLM", "AI", "論文"]
