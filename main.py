from get_data import *
from merge_data import *
from scrape_transfers import *

def main():
    get_shooting_data()
    merge_shooting_data()
    get_opponent_passing()
    merge_opp_pass_data()
    scrape_transfers()
    merge_transfers_data()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
