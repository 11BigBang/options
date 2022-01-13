from scrape import ScrapeChain

scrape = ScrapeChain(start='2021-07-27', end='2021-07-27')
scrape.driver.quit()
scrape.conn.close()