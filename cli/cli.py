import os, time
from datetime import datetime as dt

from analyze.query import Query
from scrape.scrape import ScrapeChain
from scrape.qaqc import check_dates

class CLI():
    def __init__(self):
        self.show_start()
        while True:
            self.mm()
            self.continue_menu()
            self.clear()

    def clear(self):
        os.system('cls')

    def show_start(self):
        print("""
        
  /$$$$$$              /$$     /$$                              
 /$$__  $$            | $$    |__/                              
| $$  \ $$  /$$$$$$  /$$$$$$   /$$  /$$$$$$  /$$$$$$$   /$$$$$$$
| $$  | $$ /$$__  $$|_  $$_/  | $$ /$$__  $$| $$__  $$ /$$_____/
| $$  | $$| $$  \ $$  | $$    | $$| $$  \ $$| $$  \ $$|  $$$$$$ 
| $$  | $$| $$  | $$  | $$ /$$| $$| $$  | $$| $$  | $$ \____  $$
|  $$$$$$/| $$$$$$$/  |  $$$$/| $$|  $$$$$$/| $$  | $$ /$$$$$$$/
 \______/ | $$____/    \___/  |__/ \______/ |__/  |__/|_______/ 
          | $$                                                  
          | $$                                                  
          |__/   
""")

    def mm(self):
        mm_sel = input(""" 
          
Main menu
------------
1. Analyze
2. QAQC
3. Scrape
4. Quit

Please enter 1-4:  
""")

        self.query = Query()
        self.clear()

        if mm_sel == '1':
            self.go_analyze()

        elif mm_sel == '2':
            self.go_qaqc()

        elif mm_sel == '3':
            self.go_scrape()

        elif mm_sel == '4':
            print('Goodbye!')
            quit()

        else:
            print("Please enter a number 1-4 corresponding to the menu option.")
            time.sleep(5)

    def continue_menu(self):
        ans = ''
        while ans != 'm' or 'q':
            ans = input("\nWould you like to return to the main menu or quit? (m/q)")
            if ans == 'q':
                quit()
            elif ans == 'm':
                break
            else:
                print("\nPlease enter either 'm' for main menu or 'q' for quit.")

    def go_analyze(self):
        while True:
            metric_list = ['expiry', 'date', 'symbol', 'type', 'strike', 'last', 'bid', 'b_size', 'ask',
                         'a_size', 'volume', 'OI', 'IV', 'delta', 'theta', 'gamma', 'vega', 'rho']
            print("Metrics\n----------------")
            for i in metric_list:
                print(i)
            ans = input('\nWhat metric would you like to search?\n')
            if ans in metric_list:
                start, end = self.ask_dates()
                print(self.query.get_data(metric=ans, start=start, end=end))
                break
            else:
                self.clear()
                print(f"\nERROR\n{ans} is not a valid choice from the list of metrics.")
                time.sleep(5)

    def go_qaqc(self):
        start, end = self.ask_dates()
        check_dates(start=start, end=end)

    def go_scrape(self):
        start, end = self.query.suggest_dates()
        print(f"""May I suggest the following dates?\nStart: {start}\nEnd: {end}\n""")
        sug = input("Would like to proceed with the following dates?(y/n)")

        if sug == 'n':
            start, end = self.ask_dates()

        if sug == 'n' or 'y':
            confirm = input(f"Are you sure you would like to scrape the following dates?\nStart: {start}\nEnd: {end} (y/n)")
            if confirm == 'y':
                scrape = ScrapeChain(start=start, end=end)
                scrape.driver.quit()
                scrape.conn.close()

    def ask_dates(self):
        while True:
            start = input("\nWhat date would you like to start?\nEx: 1986-07-27\n")
            if self.is_valid_date(start):
                break
        while True:
            end = input('\nWhat date would you like to end?\nEx: 1986-07-27\n')
            if self.is_valid_date(end):
                break

        return start, end

    def is_valid_date(self, date_str):
        format = "%Y-%m-%d"
        valid = False
        try:
            dt.strptime(date_str, format)
            valid = True
        except ValueError:
            print("ERROR!\nThis is the incorrect date string format. It should be YYYY-MM-DD.\n")

        return valid
