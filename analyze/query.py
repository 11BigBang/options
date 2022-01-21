import sqlite3, time, os
from datetime import datetime as dt
from datetime import timedelta

class Query:
    def __init__(self):
        self.conn = sqlite3.connect('C:/Users/wbmar/OneDrive/Documents/python_projects/options/options.db')
        self.c = self.conn.cursor()

    def get_data(self, metric, start, end):
        start_unix = time.mktime(dt.strptime(start, "%Y-%m-%d").timetuple())
        end_unix = time.mktime(dt.strptime(end, "%Y-%m-%d").timetuple())

        self.c.execute("SELECT date, ? FROM gme WHERE date BETWEEN ? AND ?", (metric, start_unix, end_unix))
        data = self.c.fetchall()
        self.conn.close()

        unix_list = [item[0] for item in data]
        date_list = [dt.fromtimestamp(int(ts)) for ts in unix_list] # Converts Unix timestamp to local datetime
        last_list = [item[1] for item in data]

        return(date_list, last_list)

    def suggest_dates(self):
        self.c.execute("SELECT MAX(date) FROM gme")
        ts = self.c.fetchone()[0] + 86400 # Adds 1 day to unix time
        self.conn.close()

        start = dt.utcfromtimestamp(ts).strftime('%Y-%m-%d')
        end = (dt.today()-timedelta(days=1)).strftime('%Y-%m-%d')

        return start, end


