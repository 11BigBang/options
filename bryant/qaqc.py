"""Module that ensures scrapes are working properly.

check_dates function ensure displays weekdays that don't have any data in database.
It is important to note that the trading holidays will be printed.
"""
import sqlite3, time
from datetime import datetime as dt
from datetime import date

from utils import get_weekdays

def check_dates(start, end):
    start = date.fromisoformat(start)
    end = date.fromisoformat(end)
    conn = sqlite3.connect('../options.db')
    c = conn.cursor()
    dates = c.execute("""SELECT DISTINCT 
                            date 
                         FROM 
                            gme
                         WHERE
                            date BETWEEN ? AND ?""", (time.mktime(start.timetuple()), time.mktime(end.timetuple())))
    unix_list = [item[0] for item in dates]
    dates_scraped = [(dt.fromtimestamp(int(ts))).date() for ts in unix_list]  # Converts Unix timestamp to local datetime
    conn.commit()
    conn.close()

    weekdays = get_weekdays(start=start, end=end)
    for weekday in weekdays:
        if weekday not in dates_scraped:
            print(weekday)

check_dates(start='2020-12-01', end='2021-01-15')