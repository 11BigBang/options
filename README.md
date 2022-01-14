## OPTIONS

### Current Status
The current program is fully functional for scraping options chains. 
It takes approximately 25 minutes per day.
#### Dates Scraped
12/1/2020 - 12/7/2020  

*Note:  07/27/2021 was also scraped as a test and is currently in the database.*

### Setup

1. Intall packages in requirements.txt file into your virtual environment.

2. Download chromedriver [here](https://chromedriver.chromium.org/downloads)
and save it in your Program Files (x86) folder.  You could save it somewhere
else but you would have to change the file path in the scrape module and this
is the recommended location.  You must also make sure that the chromedriver and 
   your Chrome browser versions match.

3. Download DB Browser for SQLite [here](https://sqlitebrowser.org/dl/). This 
will help you easily view your database or make minor changes without
having to write a bunch of SQL statements.

4. Run creation.py file to initialize database and tables.
