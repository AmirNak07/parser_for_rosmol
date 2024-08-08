from datetime import datetime
from re import fullmatch
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


def create_month(date):
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
    
    date = date.replace("–", "-")
    
    format1 = fullmatch(r"\d{1,2} \D+ - \d{1,2} \D+", date) # 4 октября - 1 ноября
    format2 = fullmatch(r"\D+ - \D+", date) # июнь - октябрь
    format3 = fullmatch(r"\d{1,2} - \d{1,2} \D+", date) # 20 - 23 ноября

    month = []
    result = []

    # Для дат других форматов
    if format1 is None and format2 is None and format3 is None:
        return "-"

    # Для даты формата "4 сентября - 1 ноября"
    if format1 is not None:
        for i in date.split(" - "):
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
        month = date.split(" - ")
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
        result.append(num_to_month[date_to_num[date.split()[-1]]])

    if len(result) == 1:
        return result[0]
    else:
        return ", ".join(result)


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
        "category_of_participants": put_categories(create_request(create_project_link(soup.find_all("div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)))).replace("\r", "").replace("\n", ""),

        # Ссылка не проект
        "project_link": create_project_link(soup.find_all("div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True)),

        # Проекты по месяцам(исходя из даты, надо обговорить с Викой) - гемор
        "month_of_project": create_month(str(soup.find_all("div", class_="period-event-tile-date")[i].text)),

        # Платформа
        "platform": "Росмолодежь",

        # Конец заявки для календаря(снова к Вике) = заявка до
        "end_of_application": put_application(create_request(create_project_link(soup.find_all("div", class_="catalog-section-item-name")[i].findChildren("a", recursive=False, href=True))))
    }
print("Готово")

with open("rosmol_parsed.json", "w", encoding="utf-8") as file:
    json.dump(cards, file, ensure_ascii=False, indent=4)

print("Результат записан в файл rosmol_parsed.json <3")
