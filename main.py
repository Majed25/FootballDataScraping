from get_data import get_shooting_data, get_defensive_style, get_opponent_passing
from merge_data import merge_defensive_data, merge_transfers_data, merge_opp_pass_data, load_params
from scrape_transfers import scrape_transfers
import logging

logging.basicConfig(filename='main.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



'''Uncomment the line to get the data needed'''

def main():
    params = load_params()
    #get_shooting_data(params)
    #merge_shooting_data(params)
    #get_opponent_passing(params)
    #merge_opp_pass_data(params)
    #get_defensive_style(params)
    #merge_defensive_data(params)
    #scrape_transfers(params)
    #merge_transfers_data()




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
