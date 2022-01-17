from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, sqlite3
from datetime import timedelta, date, datetime

from utils import get_weekdays

class ScrapeChain:
    """Scrapes options chains.

    Arguments
    - start: The start date for the interval to scrape.
    - end: The end date for the interval to scrape.

    The scrape includes both start and end date.
    """
    def __init__(self, start, end):
        self.begin = datetime.now()
        print(self.begin)
        self.conn = sqlite3.connect('../options.db')
        self.c = self.conn.cursor()

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        service = Service('C:\Program Files (x86)\chromedriver.exe')
        self.driver = webdriver.Chrome(service=service, options=options)
        time.sleep(5)

        self.start = start
        self.end = end

        # example URL 'https://omnieq.com/underlyings/NYSE/GME/chain/2019/03/22/historical/2019/03/22'
        self.URL_1 = 'https://omnieq.com/underlyings/NYSE/GME/chain/'
        self.URL_3 = '/historical/'

        self.weekdays = get_weekdays(start=self.start, end=self.end)
        self.expiries = self.get_expiries()

        for weekday in self.weekdays:
            print(f"Scraping data for {weekday}...")
            empties, count = 0, 0
            for expiry in self.expiries:
                if weekday > expiry:
                    continue
                self.driver.get(f"{self.URL_1}{expiry.strftime('%Y/%m/%d')}{self.URL_3}{weekday.strftime('%Y/%m/%d')}")
                count += 1
                if self.driver.title == 'Page Not Found':
                    empties += 1
                    if empties > 2 and count == empties :
                        # Ensures we don't keep scraping on a holiday
                        break
                else:
                    data = self.driver.find_elements(By.TAG_NAME, 'td')
                    self.clean_append(data, weekday, expiry)
            print("Done.")

        print(f'Finished {datetime.now()}, Run time was {datetime.now() - self.begin}')

    def get_expiries(self):
        print("Getting expiries...")
        dt_start = date.fromisoformat(self.start)
        fri = dt_start + timedelta(days=(4 - dt_start.weekday() + 7) % 7) # Find first Friday
        expiries, td_list = [], [-1, -1, 5, 1] # td_list is for timedelta to Thu to Wed to Mon to Tue
        step = timedelta(weeks=1)

        while fri < (date.today() + timedelta(weeks=170)):
            # Expiries only go out to a maximum of 39 months, so this ensures all expiries are covered
            expiry = fri
            self.driver.get(f"{self.URL_1}{fri.strftime('%Y/%m/%d')}")

            if fri - date.today() > timedelta(weeks=52):
                # Allow for checking following week on yearlies
                td_list += [1, 1, 1, 3]

            search_ct = 0
            while self.driver.title == 'Page Not Found' and search_ct < len(td_list):
                # Searches days around the expected Friday for the actual expiry
                expiry += timedelta(days=td_list[search_ct])
                self.driver.get(f"{self.URL_1}{expiry.strftime('%Y/%m/%d')}")
                search_ct += 1

            if self.driver.title != 'Page Not Found':
                expiries.append(expiry)

            if step == timedelta(weeks=1) and (fri - date.today()) > timedelta(weeks=52) and self.driver.title != 'Page Not Found':
                # If an expiry has been found that is 1 year past today's date, it is guaranteed to be a yearly
                # so we must start jumping ahead a year at a time.
                step = timedelta(weeks=52)

            fri += step

        print("Done.")
        return expiries


    def clean_append(self, data, weekday, expiry):
        """ Changes data to proper data types and forms into row to add to database.

        Takes each piece of data and changes it into proper SQLite3 datatype after taking out characters
        such as '%' and '$'. It also splits 'bid/size' and 'ask/size' columns into 2 pieces of data each.
        """
        ct = 0
        row = []
        for datum in data:
            if datum.text == '':
                row.append(None)
                if ct in [4, 6]:
                    row.append(None)
                    ct += 1 # Data for 'bid/size' and 'ask/size' are split into 2 data points each so 'ct' must be iterated twice
                ct += 1
                continue
            mod_1 = datum.text.replace(',', '')
            if ct in [0, 1]: # Symbol, Type
                row.append(mod_1)
            elif ct in [2, 11, 12, 13, 14, 15]: # Strike, Delta, Theta, Gamma, Rho
                row.append(float(mod_1))
            elif ct == 3: # Last
                last = float(mod_1.replace('$', ''))
                row.append(last)
            elif ct in [4, 6]: # Bid/Size, Ask/Size
                basize1 = mod_1.replace('$', '')
                basize2 = basize1.replace(' ', '')
                b_a = float(basize2.split('/')[0])
                size = float(basize2.split('/')[1])
                row.append(b_a)
                row.append(size)
                ct += 1  # Additional count since it's split into 2 data points
            elif ct in [8, 9]: # Volume, OI (Open Interest)
                vol_IO = int(mod_1)
                row.append(vol_IO)
            elif ct == 10: # IV (Implied Volatility)
                iv = float(mod_1.replace('%', ''))
                row.append(iv)
            ct += 1

            if len(row) == 16:
                # It is important to remember this is 16 because we are splitting
                # bid / size and ask / size into 2 columns each.
                self.insert_data(row, weekday, expiry)
                ct = 0
                row = []

    def insert_data(self, row, weekday, expiry):
        """Inserts row into the database.

        WARNING:  This method must only be called within the initialization of ScrapeChain
        object.  Calling it out side of this will result in error or improper data entry.

        The following 2 lines of code convert the weekday and expiry to Unix so it can be
        stored in the SQLite database as an integer.
        """
        row.insert(0, time.mktime(weekday.timetuple()))
        row.insert(0, time.mktime(expiry.timetuple()))
        self.c.execute(
            """INSERT INTO gme
            (expiry, date, symbol, type, strike, last, bid, b_size,
            ask, a_size, volume, OI, IV, delta, theta, gamma, vega, rho)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            row)
        self.conn.commit()

