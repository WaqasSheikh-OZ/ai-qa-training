import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "https://practicesoftwaretesting.com")
BROWSER = os.getenv("BROWSER", "chromium").lower()
HEADLESS = os.getenv("HEADLESS", "true").lower() in {"1", "true", "yes"}
