import os
import requests
from bs4 import BeautifulSoup
import time
import csv

# Strikers finishing
# 2023-2024 Big 5 European Leagues Defensive Action Stats
# For the other seasons:
# https://fbref.com/en/comps/Big5/2022-2023/shooting/2022-2023-Big-5-European-Leagues-Stats

# URls Collection for Shooting data
def get_shooting_data():
    cur_yr = 2024
    urls = ["https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats"]
    for i in range(14):
        prvy = cur_yr - 1
        pprvy = cur_yr - 2
        cur_yr = prvy
        url = f"https://fbref.com/en/comps/Big5/{pprvy}-{prvy}/shooting/players/{pprvy}-{prvy}-Big-5-European-Leagues-Stats"
        urls.append(url)

    response = requests.get(urls[0])
    extracted_data = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract the  Header
        table = soup.find('table', {'id': 'stats_shooting'})
        # The header that contains the data column names
        t_header = table.find('thead').find_all('tr')[1]
        columns = t_header.find_all('th')
        columns_info = [column.get('aria-label', None) for column in columns]
        table_header = [column.get_text(strip=True) for column in columns]
        # make a dictionary of data names and column info
        shooting_schema = {name: info for name, info in zip(table_header, columns_info)}
        # extract the tables
        for url in urls:
            print(f'sraping  {url}')
            if response.status_code == 200:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                table = soup.find('table', {'id': 'stats_shooting'})
                # extract the table body
                table_body = table.find('tbody')
                # exclude the header rows
                rows_to_exclude = table_body.find_all('tr', class_='thead rowSum')
                for row in rows_to_exclude:
                    row.decompose()
                rows = table_body.find_all('tr')
                data = []
                # get the data values from the first element being a th and the following being td
                for row in rows:
                    stats = row.find_all(['th', 'td'])
                    for stat in stats:
                        # handling Na values
                        data.append('Na' if stat.text == '' else stat.text)
                extracted_data.append(data)
                # delay before the next request
                time.sleep(10)

            else:
                print(f'Failed to retrieve the web page for URL: {url}')

        # store data
        file_path = 'data/shooting_data.csv'
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # create shooting_data.csv
        with open(file_path, 'w', newline='') as csvfile:
            # Create a CSV writer
            csvwriter = csv.writer(csvfile)

            # Write the header
            csvwriter.writerow(table_header)

            # Write the data
            csvwriter.writerows(extracted_data)
            print('Success: Your shooting data is under "data/shooting_data.csv')


    else:
        print('failed to retreive the web page.')
