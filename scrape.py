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

            if expiry.weekday() != 4:
                print(expiry)

            for weekday in weekday_list:
                driver.get(f"{URL_1}{expiry.strftime('%Y/%m/%d')}{URL_3}{weekday.strftime('%Y/%m/%d')}")
                if driver.title != 'Page Not Found':
                    data = driver.find_elements(By.TAG_NAME, 'td')
                    ct = 0
                    for datum in data:
                        row.append(datum.text)
                        if ct % 14 == 0:
                            c.execute(
                                #TODO: change below to insert into table and modify creation.py to reflect
                                "INSERT INTO NYSE_Threshold_Securities "
                                "(Symbol, Security_Name, Trade_Date, Market)"
                                " VALUES(%s,%s,%s,%s)",
                                row)
                            row = []

                        ct += 1

        driver.quit()

        # use friday list as starting point.  if nothing is found then adjust the days until finds expiration then
        # continue and try every weekday for open days

        # conn.commit()

        # conn.close()

        # datatypes: NULL, INTEGER, REAL, TEXT, BLOB

