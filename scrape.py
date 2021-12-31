from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, sqlite3

conn = sqlite3.connect('options.db')

c = conn.cursor()

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
service = Service('C:\Program Files (x86)\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

conn.commit()

conn.close()

# datatypes: NULL, INTEGER, REAL, TEXT, BLOB