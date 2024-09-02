from datetime import datetime
from re import fullmatch
import time

from bs4 import BeautifulSoup
import httpx
from browser import html
import gspread
from gspread.client import Client
from oauth2client.service_account import ServiceAccountCredentials
import schedule

from config import ID_TABLE, NAME_SPREADSHEET


def create_project_link(link: str) -> str:
    link = str(link).split()[1].replace('href="', "").replace('">', "")
    return "https://events.myrosmol.ru" + link


def create_request(link: str) -> str:
    response = httpx.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        all_info_title = [i.text.strip().replace(u'\xa0', u' ') for i in soup.find_all(
            "div", class_="properties-preview-item-name")]
        all_info_value = [i.text.strip().replace(u'\xa0', u' ') for i in soup.find_all(
            "div", class_="properties-preview-item-value")]
        all_info = list(zip(all_info_title, all_info_value))
        return all_info


def put_application(response: str) -> str:
    date_to_num = {
        "января": 1,
        "февраля": 2,
        "марта": 3,
        "апреля": 4,
        "мая": 5,
        "июня": 6,
        "июля": 7,
        "августа": 8,
        "сентября": 9,
        "ноября": 10,
        "октября": 11,
        "декабря": 12
    }

    for i in response:
        if i[0] == "Дата окончания регистрации:":
            day, month, year = i[1].split()
            month = date_to_num[month]
            true_date = datetime(int(year), month, int(day))
            return true_date.strftime("%d.%m.%Y %X")
    return "-"


def put_categories(response: str) -> str:
    for i in response:
        if i[0] == "Категории участников:":
            return i[1]
    return "-"


def create_month(my_date: str) -> str:
    date_to_num = {
        "января": 1,
        "февраля": 2,
        "марта": 3,
        "апреля": 4,
        "мая": 5,
        "июня": 6,
        "июля": 7,
        "августа": 8,
        "сентября": 9,
        "октября": 10,
        "ноября": 11,
        "декабря": 12
    }

    correct_date_to_num = {
        "январь": 1,
        "февраль": 2,
        "март": 3,
        "апрель": 4,
        "май": 5,
        "июнь": 6,
        "июль": 7,
        "август": 8,
        "сентябрь": 9,
        "октябрь": 10,
        "ноябрь": 11,
        "декабрь": 12
    }

    num_to_month = {
        1: "январь",
        2: "февраль",
        3: "март",
        4: "апрель",
        5: "май",
        6: "июнь",
        7: "июль",
        8: "август",
        9: "сентябрь",
        10: "октябрь",
        11: "ноябрь",
        12: "декабрь"
    }

    my_date = my_date.replace("–", "-")

    format1 = fullmatch(r"\d{1,2} \D+ - \d{1,2} \D+",
                        my_date)  # 4 октября - 1 ноября
    format2 = fullmatch(r"\D+ - \D+", my_date)  # июнь - октябрь
    format3 = fullmatch(r"\d{1,2} - \d{1,2} \D+", my_date)  # 20 - 23 ноября

    month = []
    result = []

    # Для дат других форматов
    if format1 is None and format2 is None and format3 is None:
        return "-"

    # Для даты формата "4 сентября - 1 ноября"
    if format1 is not None:
        for i in my_date.split(" - "):
            day, months = i.split()
            months = date_to_num[months]
            if month != [] and day == "1":
                months -= 1
            if months == 0:
                months = 12
            month.append(months)

        if month[0] > month[1]:
            month[1] += 12

        for i in range(month[0], month[1] + 1):
            if i <= 12:
                result.append(num_to_month[i])
            else:
                result.append(num_to_month[i % 12])

    # Для даты формата "июнь - сентябрь"
    if format2 is not None:
        month = my_date.split(" - ")
        month[0] = correct_date_to_num[month[0]]
        month[1] = correct_date_to_num[month[1]]

        if month[0] > month[1]:
            month[1] += 12

        for i in range(month[0], month[1] + 1):
            if i <= 12:
                result.append(num_to_month[i])
            else:
                result.append(num_to_month[i % 12])

    # Для даты формата "20 - 23 ноября"
    if format3 is not None:
        result.append(num_to_month[date_to_num[my_date.split()[-1]]])

    if len(result) == 1:
        return result[0]
    else:
        return ", ".join(result)


def delete_old_projects(cards):
    titles = ["title", "place", "date", "application_before", "category_of_participants",
              "project_link", "month_of_project", "platform", "end_of_application"]
    result = [titles]

    for i in cards:
        try:
            if datetime.now() > datetime.strptime(i[3], "%d.%m.%Y %X"):
                pass
            else:
                result.append(i)
        except ValueError:
            result.append(i)

    return result


def create_projects(soup) -> list:
    print("Процесс парсинга...")
    cards = []
    card = []

    for i in range(len(soup.find_all("div", class_="catalog-section-item-base"))):
        # Название
        card.append(" ".join(soup.find_all(
            "div", class_="catalog-section-item-name")[i].text.split()))

        # Место
        card.append(" ".join(soup.find_all(
            "div", class_="catalog-section-forum-region")[i].text.split()))

        # Даты
        card.append(soup.find_all(
            "div", class_="period-event-tile-date")[i].text)

        # Заявка до
        card.append(put_application(create_request(create_project_link(soup.find_all(
            "div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)))))

        # Категория участников
        card.append(put_categories(create_request(create_project_link(soup.find_all("div", class_="catalog-section-item-name")
                    [i].findChildren("a", recursive=False, href=True)))).replace("\r", "").replace("\n", ""))

        # Ссылка не проект
        card.append(create_project_link(soup.find_all(
            "div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)))

        # Проекты по месяцам
        card.append(create_month(
            str(soup.find_all("div", class_="period-event-tile-date")[i].text)))

        # Платформа
        card.append("Росмолодежь")

        # Конец заявки для календаря = заявка до
        card.append(put_application(create_request(create_project_link(soup.find_all(
            "div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)))))

        cards.append(card.copy())
        card.clear()

    result = delete_old_projects(cards)

    print("Мероприятия готовы")
    return result


# def download_csv_from_table(client: Client, key: str, work_sheet: str) -> list:
#     print("Установка старой таблицы")
#     sheet = client.open_by_key(key)
#     worksheet = sheet.worksheet(work_sheet)
#     data = worksheet.get_all_records()

#     cards = []
#     for project in data:
#         fields = []
#         for field in list(project.values()):
#             fields.append(field)
#         cards.append(fields.copy())

#     result = delete_old_projects(cards)
#     return result


# def update_table(old_csv, new_csv):
#     print("Сортировка данных в таблице")
#     titles = old_csv.pop(0)
#     link = titles.index("project_link")
#     application_before = titles.index("application_before")
#     new_csv.pop(0)
#     result = []
#     if len(old_csv) == 0:
#         result.extend(new_csv)
#         return result

#     result = [tuple(titles)]

#     for new in range(len(new_csv)):
#         for old in range(len(old_csv)):
#             if new_csv[new][link] == old_csv[old][link]:
#                 if new_csv[new][application_before] != old_csv[old][application_before]:
#                     old_csv[old][application_before] = new_csv[new][application_before]
#                     result.append(tuple(old))
#                     break

#     for old in old_csv:
#         result.append(tuple(old))

#     for new in new_csv:
#         result.append(tuple(new))

#     result = list(set(tuple(result)))
#     print(result)
#     return result


def write_to_table(client: Client, table_id: str, worklist: str, data: str) -> None:
    sheet = client.open_by_key(table_id)
    worksheet = sheet.worksheet(worklist)
    worksheet.clear()
    worksheet.append_rows(values=data)


def main() -> None:
    id_table = ID_TABLE
    name_worksheet = NAME_SPREADSHEET

    soup = BeautifulSoup(html, "html.parser")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", scope)
    client = gspread.authorize(creds)

    new_csv = create_projects(soup)
    write_to_table(client, id_table, name_worksheet, new_csv)


if __name__ == "__main__":
    # schedule.every().day.at("00:01", "Europe/Moscow").do(timer)
    schedule.every(3).hours.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
