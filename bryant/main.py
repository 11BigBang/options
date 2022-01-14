from scrape import ScrapeChain
from datetime import datetime as dt

begin = dt.now()
scrape = ScrapeChain(start='2020-12-08', end='2020-12-09')
scrape.driver.quit()
scrape.conn.close()
print(f'Run time was {dt.now() - begin}')
