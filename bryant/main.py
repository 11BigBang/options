from scrape import ScrapeChain
from datetime import datetime as dt

begin = dt.now()
print(begin)
scrape = ScrapeChain(start='2021-02-18', end='2021-02-19')
scrape.driver.quit()
scrape.conn.close()
print(f'Finished {dt.now()}, Run time was {dt.now() - begin}')
