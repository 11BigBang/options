from scrape import ScrapeChain
from datetime import datetime as dt

begin = dt.now()
scrape = ScrapeChain(start='2020-12-01', end='2020-12-14')
scrape.driver.quit()
scrape.conn.close()
print(f'Run time was {dt.now() - begin}')
