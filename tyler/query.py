import sqlite3, time
from datetime import datetime as dt


def get_data(metric, start, end):
    start_unix = time.mktime(dt.strptime(start, "%Y-%m-%d").timetuple())
    end_unix = time.mktime(dt.strptime(end, "%Y-%m-%d").timetuple())

    conn = sqlite3.connect('../options.db')
    c = conn.cursor()

    c.execute("SELECT date, ? FROM gme WHERE date BETWEEN ? AND ?", (metric, start_unix, end_unix))
    data = c.fetchall()
    conn.close()

    unix_list = [item[0] for item in data]
    date_list = [dt.fromtimestamp(int(ts)) for ts in unix_list] # Converts Unix timestamp to local datetime
    last_list = [item[1] for item in data]

    return(date_list, last_list)


