from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, sqlite3
from datetime import timedelta

from utils import get_fridays, get_weekdays

class ScrapeChain:
    def __init__(self, start, end):
        # conn = sqlite3.connect('options.db')
        #
        # c = conn.cursor()

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        service = Service('C:\Program Files (x86)\chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        time.sleep(5)

        self.start = start
        self.end = end

        # example URL 'https://omnieq.com/underlyings/NYSE/GME/chain/2019/03/22/historical/2019/03/22'
        URL_1 = 'https://omnieq.com/underlyings/NYSE/GME/chain/'
        URL_3 = '/historical/'

        fri_list = get_fridays(start=self.start, end=self.end)
        weekday_list = get_weekdays(start=self.start, end=self.end)

        for expiry in fri_list:
            driver.get(f"{URL_1}+{expiry.strftime('%Y/%m/%d')}")
            # td_list allows for timedelta values that correspond to Thursday, Wednesday,
            # Monday, and Tuesday surrounding the typical Friday expiry
            search_ct, td_list = 0, [-1, -1, 5, 1]
            while driver.title == 'Page Not Found' and search_ct < 5:
                expiry += timedelta(days=td_list[search_ct])
                driver.get(f"{URL_1}+{expiry.strftime('%Y/%m/%d')}")
                search_ct += 1

            if driver.title == 'Page Not Found':
                raise ValueError('The URL for an expiry was not found.')

            if expiry.weekday() != 4:
                print(expiry)

            # empty_ct = 0
            # # driver.get(URL_1+)
            # elem = driver.find_elements(By.TAG_NAME, 'td')
            # for i in elem:
            #     print(i.text)

        driver.quit()

        # use friday list as starting point.  if nothing is found then adjust the days until finds expiration then
        # continue and try every weekday for open days

        # conn.commit()

        # conn.close()

        # datatypes: NULL, INTEGER, REAL, TEXT, BLOB

