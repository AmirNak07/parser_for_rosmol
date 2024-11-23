import json
import os
import sys

from dotenv import load_dotenv

load_dotenv(dotenv_path="./config/.env", override=True)

ID_TABLE = os.getenv("ID_TABLE")
NAME_SPREADSHEET = os.getenv("SPREADSHEET")
with open("config/logs.json", "r", encoding="utf-8") as file:
    LOGS_CONFIG = json.load(file)

for handler in LOGS_CONFIG["handlers"]:
    if handler["sink"] == "sys.stdout":
        handler["sink"] = sys.stdout
