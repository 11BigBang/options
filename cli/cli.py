import os, time

from analyze.query import Query
from scrape.scrape import ScrapeChain
from scrape.qaqc import check_dates

class CLI():
    def __init__(self):
        while True:
            self.mm()
            self.clear()
            self.continue_menu()
            self.clear()

    def clear(self):
        os.system('cls')

    def mm(self):
        mm_sel = input("""
        
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
          
Main menu
------------
1. Analyze
2. QAQC
3. Scrape
4. Quit

Please enter 1-3:  
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
            ans = input("Would you like to return to the main menu or quit? (m/q)")
            if ans == 'q':
                quit()
            elif ans == 'm':
                break
            else:
                print("Please enter either 'm' for main menu or 'q' for quit.")

    def go_analyze(self):
        ans = input('What metric would you like to search?')
        if ans == 'bid':
            start, end = self.ask_dates()

            print(self.query.get_data(metric=ans, start=start, end=end))
        elif ans == 'q':
            quit()

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
            scrape = ScrapeChain(start=start, end=end)
            scrape.driver.quit()
            scrape.conn.close()

    def ask_dates(self):
        start = input("What date would you like to start?\nEx: 1986-07-27\n")
        print("\n")
        end = input('What date would you like to end?\nEx: 1986-07-27\n')
        print("\n")

        return start, end
