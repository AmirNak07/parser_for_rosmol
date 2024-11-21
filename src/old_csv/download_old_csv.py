from gspread.client import Client

from utils import delete_old_projects


def download_csv_from_table(client: Client, key: str, work_sheet: str) -> list:
    print("Установка старой таблицы")
    sheet = client.open_by_key(key)
    worksheet = sheet.worksheet(work_sheet)
    data = worksheet.get_all_records()

    cards = []
    for project in data:
        fields = []
        for field in list(project.values()):
            fields.append(field)
        cards.append(fields.copy())

    result = delete_old_projects(cards)
    return result
