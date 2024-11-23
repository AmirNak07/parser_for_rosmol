import time

import gspread
import schedule
from loguru import logger
from oauth2client.service_account import ServiceAccountCredentials

from config import ID_TABLE, LOGS_CONFIG, NAME_SPREADSHEET
from src.google_api import write_to_table
from src.handle_html import create_projects
from src.parse_html import parse_html


@logger.catch(level="ERROR")
def main() -> None:
    logger.remove()
    logger.configure(**LOGS_CONFIG)

    id_table = ID_TABLE
    name_worksheet = NAME_SPREADSHEET

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "config/credentials.json", scope)
    client = gspread.authorize(creds)

    logger.info("Начало парсинга")
    html = parse_html()
    handled_html = create_projects(html)
    write_to_table(client, id_table, name_worksheet, handled_html)
    logger.info("Парсинг прошёл успешно")


if __name__ == "__main__":
    # schedule.every().day.at("00:01", "Europe/Moscow").do(main)
    schedule.every(3).hours.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
