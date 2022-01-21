"""Module that ensures scrapes are working properly.

check_dates function ensure displays weekdays that don't have any data in database.
It is important to note that the trading holidays will be printed.
"""
import sqlite3, time
from datetime import datetime as dt
from datetime import date

from .utils import get_weekdays

def check_dates(start, end):
    start = date.fromisoformat(start)
    unix_start = time.mktime(start.timetuple())
    end = date.fromisoformat(end)
    unix_end = time.mktime(end.timetuple())

    conn = sqlite3.connect('C:/Users/wbmar/OneDrive/Documents/python_projects/options/options.db')
    c = conn.cursor()
    dates = c.execute("""SELECT DISTINCT 
                            date 
                         FROM 
                            gme
                         WHERE
                            date BETWEEN ? AND ?""", (unix_start, unix_end))

    unix_list = [item[0] for item in dates]
    dates_scraped = [(dt.fromtimestamp(int(ts))).date() for ts in unix_list]  # Converts Unix timestamp to local datetime

    conn.commit()
    conn.close()

    weekdays = get_weekdays(start=start, end=end)
    print("The following days don't have a single entry in the database:\nNote:  They may only be listed due to market closures.")
    for weekday in weekdays:
        if weekday not in dates_scraped:
            print(weekday)
