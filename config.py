import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="config/.env", override=True)

ROSMOL_FORUMS_URL = os.environ.get("ROSMOL_FORUMS_URL")
ROSMOL_FORUMS_PATH = os.environ.get("ROSMOL_FORUMS_PATH")
