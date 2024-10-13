from datetime import datetime


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