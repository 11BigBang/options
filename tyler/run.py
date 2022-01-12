from query import get_data

ans = input('What would you like to search?')

if ans == 'bid':
    start_date = input("What date to start?\nEx: 1986-07-27\n")
    end_date = input('What date to end?\nEx: 1986-07-27\n')

    print(get_data(metric=ans,start=start_date,end=end_date))
elif ans == 'q':
    quit()
else:
    print('Thanks for playing')