from scrape import ScrapeChain

start = '2022-01-10'
end = '2022-01-14'

if __name__ == '__main__':
    scrape = ScrapeChain(start=start, end=end)
    scrape.driver.quit()
    scrape.conn.close()
