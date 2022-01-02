from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, sqlite3

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
        wkday_list = get_weekdays(start=self.start, end=self.end)

        for expiry in fri_list:
            empty_ct = 0
            # driver.get(URL_1+)
            elem = driver.find_elements(By.TAG_NAME, 'td')
            for i in elem:
                print(i.text)

        driver.quit()

        # use friday list as starting point.  if nothing is found then adjust the days until finds expiration then
        # continue and try every weekday for open days

        # conn.commit()

        # conn.close()

        # datatypes: NULL, INTEGER, REAL, TEXT, BLOB

