import os

from dotenv import load_dotenv

load_dotenv(override=True)

ID_TABLE = os.getenv("ID_TABLE")
NAME_SPREADSHEET = os.getenv("SPREADSHEET")
