from scrape import ScrapeChain
from datetime import datetime as dt

begin = dt.now()
print(begin)
scrape = ScrapeChain(start='2020-12-14', end='2020-12-18')
scrape.driver.quit()
scrape.conn.close()
print(f'Finished {dt.now()}, Run time was {dt.now() - begin}')
