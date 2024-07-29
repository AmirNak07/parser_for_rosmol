from datetime import datetime
import json


from bs4 import BeautifulSoup
import httpx
from browser import html

soup = BeautifulSoup(html, "html.parser")


def create_project_link(a):
    a = str(a).split()[1].replace('href="', "").replace('">', "")
    return "https://events.myrosmol.ru" + a


def create_request(link):
    response = httpx.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        all_info_title = [i.text.strip().replace(u'\xa0', u' ') for i in soup.find_all(
            "div", class_="properties-preview-item-name")]
        all_info_value = [i.text.strip().replace(u'\xa0', u' ') for i in soup.find_all(
            "div", class_="properties-preview-item-value")]
        all_info = list(zip(all_info_title, all_info_value))
        return all_info


def put_application(response):
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


def put_categories(response):
    for i in response:
        if i[0] == "Категории участников:":
            return i[1]
    return "-"


print("Процесс записи данных в JSON...")
cards = {}

for i in range(len(soup.find_all("div", class_="catalog-section-item-base"))):
    cards[i] = {
        # Название
        "title": " ".join(soup.find_all("div", class_="catalog-section-item-name")[i].text.split()),

        # Место
        "place": " ".join(soup.find_all("div", class_="catalog-section-forum-region")[i].text.split()),

        # Даты
        "date": soup.find_all("div", class_="period-event-tile-date")[i].text,

        # Заявка до
        "application_before": put_application(create_request(create_project_link(soup.find_all("div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)))),

        # Категория участников
        "category_of_participants": put_categories(create_request(create_project_link(soup.find_all("div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)))),

        # Ссылка не проект
        "project_link": create_project_link(soup.find_all("div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)),

        # Проекты по месяцам(исходя из даты, надо обговорить с Викой) - гемор

        # Конец заявки для календаря(снова к Вике) = заявка до
        "end_of_application": put_application(create_request(create_project_link(soup.find_all("div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True))))
    }
print("Готово")

with open("rosmol_parsed.json", "w", encoding="utf-8") as file:
    json.dump(cards, file, ensure_ascii=False, indent=4)

print("Результат записан в файл rosmol_parsed.json <3")
