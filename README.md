## OPTIONS

### Table of Contents
[Current Status](#Current-Status)  
[Setup](#Setup)  
[QAQC](#QAQC)

### Current Status
The current program is fully functional for scraping options chains. 
It takes approximately 25 minutes per day.
#### Dates Scraped
12/01/2020 - 01/15/2021  

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

### QAQC
If you would like to ensure all dates between a range have been scraped,
run the 'qaqc.py' module after entering start and end dates into the function
at the bottom.  

*IMPORTANT:  This module just checks to make sure a single row is in the 
database for that date.  It doesn't necessarily mean that it took in all of
the data from that date.*
