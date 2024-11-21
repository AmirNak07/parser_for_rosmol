from datetime import datetime


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
        "октября": 10,
        "ноября": 11,
        "декабря": 12
    }

    for i in response:
        if i[0] == "Дата окончания регистрации:":
            day, month, year = i[1].split()
            month = date_to_num[month]
            true_date = datetime(int(year), month, int(day))
            return true_date.strftime("%d.%m.%Y %X")
    return "-"
