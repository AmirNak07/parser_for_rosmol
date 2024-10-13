def update_table(old_csv, new_csv):
    print("Сортировка данных в таблице")
    titles = old_csv.pop(0)
    link = titles.index("project_link")
    application_before = titles.index("application_before")
    new_csv.pop(0)
    result = []
    if len(old_csv) == 0:
        result.extend(new_csv)
        return result

    result = [tuple(titles)]

    for new in range(len(new_csv)):
        for old in range(len(old_csv)):
            if new_csv[new][link] == old_csv[old][link]:
                if new_csv[new][application_before] != old_csv[old][application_before]:
                    old_csv[old][application_before] = new_csv[new][application_before]
                    result.append(tuple(old))
                    break

    for old in old_csv:
        result.append(tuple(old))

    for new in new_csv:
        result.append(tuple(new))

    result = list(set(tuple(result)))
    print(result)
    return result