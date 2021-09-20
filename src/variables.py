from dotenv import load_dotenv
import os

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASS = os.getenv("SENDER_PASS")

DB_NAME = "usajobs.db"

RESULTS_PER_PAGE_LIMIT = 500
