import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import ID_TABLE, NAME_SPREADSHEET
from src.parse_html import parse_html
from src.handle_html import create_projects
from src.google_api import write_to_table

def main() -> None:
    id_table = ID_TABLE
    name_worksheet = NAME_SPREADSHEET

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope)
    client = gspread.authorize(creds)
    
    html = parse_html()
    handled_html = create_projects(html)
    write_to_table(client, id_table, name_worksheet, handled_html)
    print("Готово")


if __name__ == "__main__":
    main()