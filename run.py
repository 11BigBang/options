from analyze.query import Query

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

query = Query()

if mm_sel == '1':
    ans = input('What would you like to search?')
    if ans == 'bid':
        start_date = input("What date to start?\nEx: 1986-07-27\n")
        end_date = input('What date to end?\nEx: 1986-07-27\n')

        print(query.get_data(metric=ans,start=start_date,end=end_date))
    elif ans == 'q':
        quit()

elif mm_sel == '3':
    start, end = query.suggest_dates()
    print(start)
    print(end)

else:
    print('Thanks for playing')