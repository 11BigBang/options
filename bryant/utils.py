from datetime import date, timedelta
from datetime import datetime as dt


def get_weekdays(start=date(date.today().year, 1, 1), end=date.today()):
    if not isinstance(start, date):
        start = date.fromisoformat(start)
    if not isinstance(end, date):
        end = date.fromisoformat(end)
    if start > end:
        raise ValueError('Your end date must be later that start date.')

    weekday_list = []
    temp = start
    while temp <= end:
        if temp.weekday() < 5:
            weekday_list.append(temp)
        temp += timedelta(days=1)

    return weekday_list
