import os

from dotenv import load_dotenv

load_dotenv()

BROWSER_TYPE = os.environ.get("BROWSER")
