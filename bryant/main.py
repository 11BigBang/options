from scrape import ScrapeChain
from datetime import datetime as dt

begin = dt.now()
scrape = ScrapeChain(start='2021-07-27', end='2021-07-27')
scrape.driver.quit()
scrape.conn.close()
print(f'Run time was {dt.now() - begin}')