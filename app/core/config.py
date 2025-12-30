import logging
import os

import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = os.getenv("TMDB_BASE_URL")

if not API_KEY or not BASE_URL:
    logging.error("TMDB_API_KEY or TMDB_BASE_URL not set in environment variables.")
    raise ValueError("Configuration missing.")

# Initialize client for asynchronous connections
tmdb_client = httpx.AsyncClient(
    base_url=BASE_URL,
    params={"api_key": API_KEY}
)
