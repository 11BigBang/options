from datetime import date, timedelta
from datetime import datetime as dt

def get_fridays(start=date(date.today().year, 1, 1), end=date.today()):
    """Creates a list of dates for every Friday within timeframe.

    Arguments:
        start - format: '%Y/%m/%d'
        end
            format:  '%Y/%m/%d'
            default: current date
    """
    if not isinstance(start, date):
        start = date.fromisoformat(start)
    if not isinstance(end, date):
        end = date.fromisoformat(end)

    fri_list = []
    temp = start + timedelta(days = (4 - start.weekday() + 7) % 7)

    while temp < end:
        fri_list.append(temp)
        temp += timedelta(days=7)

    return fri_list

def get_weekdays(start=date(date.today().year, 1, 1), end=date.today()):
    if not isinstance(start, date):
        start = date.fromisoformat(start)
    if not isinstance(end, date):
        end = date.fromisoformat(end)

    weekday_list = []
    temp = start
    while temp <= end:
        if temp.weekday() < 5:
            weekday_list.append(temp)
        temp += timedelta(days=1)

    return weekday_list

# w = get_weekdays(start='2021-08-01', end='2021-08-12')
# for i in w:
#     print(i)

# get_fridays(start='2021-02-13', end='2021-08-12')
# get_fridays()