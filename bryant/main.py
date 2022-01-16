from scrape import ScrapeChain
from datetime import datetime as dt

begin = dt.now()
print(begin)
scrape = ScrapeChain(start='2021-12-13', end='2021-12-17')
scrape.driver.quit()
scrape.conn.close()
print(f'Finished {dt.now()}, Run time was {dt.now() - begin}')
