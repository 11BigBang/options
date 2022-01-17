from scrape import ScrapeChain
from datetime import datetime as dt

begin = dt.now()
print(begin)
scrape = ScrapeChain(start='2022-01-03', end='2022-01-07')
scrape.driver.quit()
scrape.conn.close()
print(f'Finished {dt.now()}, Run time was {dt.now() - begin}')
