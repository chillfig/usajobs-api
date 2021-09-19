from dotenv import load_dotenv
import os

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASS = os.getenv("SENDER_PASS")

RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

DB_NAME = 'usajobs.db'
OUTPUT_PATH = 'report.csv'

FILTER_ENABLED = False

DATA_POSITIONS = ["Data Scientist", "Data Analyst", "Data Engineer"] # Or None
# DATA_POSITIONS = None

KEYWORDS = ["data", "analytics", "ML", "AI"]
# KEYWORDS = None

RESULTS_PER_PAGE_LIMIT = 500
