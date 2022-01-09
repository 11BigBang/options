from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, sqlite3
from datetime import timedelta

from utils import get_fridays, get_weekdays

class ScrapeChain:
    """Scrapes options chains.

    Arguments
    - ex_start: The start date for the expiry dates to scrape.
    - ex_end: The end date for the expiry dates to scrape.
    - day_start: The start date for the "data from" to scrape.
    - day_end: The end date for the "data from" to scrape.
    """
    def __init__(self, ex_start, ex_end, day_start, day_end):
        conn = sqlite3.connect('options.db')
        c = conn.cursor()

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        service = Service('C:\Program Files (x86)\chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        time.sleep(5)

        self.ex_start = ex_start
        self.ex_end = ex_end
        self.day_start = day_start
        self.day_end = day_end

        # example URL 'https://omnieq.com/underlyings/NYSE/GME/chain/2019/03/22/historical/2019/03/22'
        URL_1 = 'https://omnieq.com/underlyings/NYSE/GME/chain/'
        URL_3 = '/historical/'
        row = []

        fri_list = get_fridays(start=self.ex_start, end=self.ex_end)
        weekday_list = get_weekdays(start=self.day_start, end=self.day_end)

        for expiry in fri_list:
            driver.get(f"{URL_1}{expiry.strftime('%Y/%m/%d')}")
            # td_list allows for timedelta values that correspond to Thursday, Wednesday,
            # Monday, and Tuesday surrounding the typical Friday expiry
            search_ct, td_list = 0, [-1, -1, 5, 1]
            while driver.title == 'Page Not Found' and search_ct < 5:
                expiry += timedelta(days=td_list[search_ct])
                driver.get(f"{URL_1}{expiry.strftime('%Y/%m/%d')}")
                search_ct += 1

            if driver.title == 'Page Not Found':
                raise ValueError('The URL for an expiry was not found.')

            for weekday in weekday_list:
                driver.get(f"{URL_1}{expiry.strftime('%Y/%m/%d')}{URL_3}{weekday.strftime('%Y/%m/%d')}")
                if driver.title != 'Page Not Found' and weekday < expiry:
                    data = driver.find_elements(By.TAG_NAME, 'td')
                    ct = 0
                    for datum in data:
                        if datum.text == '':
                            row.append(None)
                            if ct in [4, 6]:
                                row.append(None)
                                ct += 1
                            ct += 1
                            continue
                        mod_1 = datum.text.replace(',', '')
                        if ct in [0, 1]:
                            row.append(mod_1)
                        elif ct in [2, 11, 12, 13, 14, 15]:
                            row.append(float(mod_1))
                        elif ct == 3:
                            last = float(mod_1.replace('$', ''))
                            row.append(last)
                        elif ct in [4, 6]:
                            basize1 = mod_1.replace('$', '')
                            basize2 = basize1.replace(' ','')
                            b_a = float(basize2.split('/')[0])
                            size = float(basize2.split('/')[1])
                            row.append(b_a)
                            row.append(size)
                            ct += 1 # Additional count since it's split into 2 datapoints
                        elif ct in [8, 9]:
                            vol_IO = int(mod_1)
                            row.append(vol_IO)
                        elif ct == 10:
                            iv = float(mod_1.replace('%', ''))
                            row.append(iv)
                        ct += 1

                        if len(row) == 16:
                            # The following 2 lines of code convert the weekday and expiry to Unix so it can be
                            # stored in the SQLite database as an integer.
                            # It is important to remember this is 16 not because we have added date and expiry
                            # but because we are splitting bid/size and ask/size into 2 columns each.
                            row.insert(0, time.mktime(weekday.timetuple()))
                            row.insert(0, time.mktime(expiry.timetuple()))
                            c.execute(
                                """INSERT INTO gme
                                (expiry, date, symbol, type, strike, last, bid, b_size,
                                ask, a_size, volume, OI, IV, delta, theta, gamma, vega, rho)
                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                row)
                            conn.commit()
                            row = []
                            ct = 0

        driver.quit()

        conn.close()

