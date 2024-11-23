from gspread.client import Client
from loguru import logger


@logger.catch
def write_to_table(client: Client, table_id: str, worklist: str, data: str) -> None:
    sheet = client.open_by_key(table_id)
    worksheet = sheet.worksheet(worklist)
    worksheet.clear()
    worksheet.append_rows(values=data)
    logger.info("Отправка данных в гугл таблицу")
