from re import fullmatch


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
