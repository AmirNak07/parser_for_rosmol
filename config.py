import os

from dotenv import load_dotenv

load_dotenv(override=True)

BROWSER_TYPE = os.environ.get("BROWSER")
ID_TABLE = os.getenv("ID_TABLE")
NAME_SPREADSHEET = os.getenv("SPREADSHEET")
