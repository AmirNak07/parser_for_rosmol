import os
import json

from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env", override=True)

SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
SHEET_NAME = os.environ.get("SHEET_NAME")
ROSMOL_FORUMS_URL = os.environ.get("ROSMOL_FORUMS_URL")
ROSMOL_FORUMS_PATH = os.environ.get("ROSMOL_FORUMS_PATH")
ROSMOL_FORUMS_PARAM = os.environ.get("ROSMOL_FORUMS_PARAM")
ROSMOL_FORUMS_PARAM = json.loads(ROSMOL_FORUMS_PARAM)
