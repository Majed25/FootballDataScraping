import os
import requests
from bs4 import BeautifulSoup
import time
import csv
import json
import re

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
        url = f"https://fbref.com/en/comps/Big5/{pprvy}-{prvy}/shooting/players/"\
            f"{pprvy}-{prvy}-Big-5-European-Leagues-Stats"
        urls.append(url)

    # extract the tables
    i = 0
    for url in urls[:1]:
        extracted_data = []
        response = requests.get(url)
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
            print(f'sraping  {url}')

            # extract the table body
            table = soup.find('table', {'id': 'stats_shooting'})
            table_body = table.find('tbody')
            # exclude the header rows
            rows_to_exclude = table_body.find_all('tr', class_='thead rowSum')
            for row in rows_to_exclude:
                row.decompose()
            rows = table_body.find_all('tr')

            # get the data values from the first element being a th and the following being td
            for row in rows:
                data = []
                stats = row.find_all(['th', 'td'])
                for stat in stats:
                    # handling Na values
                    data.append('Na' if stat.text == '' else stat.text)
                extracted_data.append(data)

            # store data
            file_path = f'temp_data/shooting_data{i}.csv'
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            # create shooting_data.csv
            with open(file_path, 'w', newline='') as csvfile:
                # Create a CSV writer
                csvwriter = csv.writer(csvfile)
                # Write the header
                print(len(table_header))
                csvwriter.writerow(table_header)
                # Write the data
                for row in extracted_data:
                    if len(row) != len(table_header):
                        print('lengths dont match len(row) len(header)', len(row), len(table_header))
                        break
                    else:
                        csvwriter.writerow(row)
                print(f'Success: Your shooting data is under {file_path}')
            # store schema
            file_path = f'temp_data/shooting_schema{i}.json'
            with open(file_path, 'w', newline='') as json_file:
                json.dump(shooting_schema, json_file, indent=2)

            i += 1
            time.sleep(10)

        else:
            print(f'Failed to retrieve the web page for URL: {url}')


def get_defensive_style():
    urls = ['https://fbref.com/en/comps/Big5/defense/squads/Big-5-European-Leagues-Stats']
    cur_yr = 2024
    for i in range(14):
        prvy = cur_yr - 1
        pprvy = cur_yr - 2
        cur_yr = prvy
        url = f'https://fbref.com/en/comps/Big5/{pprvy}-{prvy}/defense/squads/'\
              f'{pprvy}-{prvy}-Big-5-European-Leagues-Stats'
        urls.append(url)
    for url in urls:
        # store the season pattern
        pattern = re.search(r'/(\d{4}-\d{4})/', url)
        if pattern:
            season = pattern.group(1)
        else:
            season = '2023-2024'
        response = requests.get(url)
        extracted_data = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the  Header
            table = soup.find('table', {'id': 'stats_teams_defense_for'})
            # The header that contains the data column names
            t_header = table.find('thead').find_all('tr')[1]
            columns = t_header.find_all('th')
            columns_info = [column.get('aria-label', None) for column in columns]
            table_header = [column.get_text(strip=True) for column in columns]
            extracted_data.append(table_header)
            # make a dictionary of data names and column info
            defensive_schema = {name: info for name, info in zip(table_header, columns_info)}
            # store schema
            file_path = f'temp_data/defensive_schema{season}.json'
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(file_path, 'w', newline='') as json_file:
                json.dump(defensive_schema, json_file, indent=2)

            # extract the table body
            table_body = table.find('tbody')
            # exclude the header rows
            rows_to_exclude = table_body.find_all('tr', class_='thead rowSum')
            for row in rows_to_exclude:
                row.decompose()
            rows = table_body.find_all('tr')

            # get the data values from the first element being a th and the following being td
            for row in rows:
                data = []
                stats = row.find_all(['th', 'td'])
                for stat in stats:
                    # handling Na values
                    data.append('Na' if stat.text == '' else stat.text)
                extracted_data.append(data)

            # store the table in csv
            file_path = f'temp_data/defensive_data{season}.csv'
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            # create shooting_data.csv
            with open(file_path, 'w', newline='') as csvfile:
                # Create a CSV writer
                csvwriter = csv.writer(csvfile)
                # write data
                for row in extracted_data:
                    if len(row) != len(table_header):
                        print('lengths dont match len(row) len(header)', len(row), len(table_header))
                        break
                    else:
                        csvwriter.writerow(row)
                print(f'Success: Your shooting data is under {file_path}')
            time.sleep(10)

        else:
            print(f'Error fetching table from {url}')

def get_opponent_passing():
    urls = ['https://fbref.com/en/comps/Big5/passing/squads/Big-5-European-Leagues-Stats']
    cur_yr = 2024
    for i in range(14):
        prvy = cur_yr - 1
        pprvy = cur_yr - 2
        cur_yr = prvy
        url = f'https://fbref.com/en/comps/Big5/{pprvy}-{prvy}/passing/squads/'\
              f'{pprvy}-{prvy}-Big-5-European-Leagues-Stats'
    for url in urls:
        # store the season pattern
        pattern = re.search(r'/(\d{4}-\d{4})/', url)
        if pattern:
            season = pattern.group(1)
        else:
            season = '2023-2024'
        response = requests.get(url)
        extracted_data = []
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            # Extract the  Header
            table = soup.find('table', {'id': 'stats_teams_passing_against'})
            # The header that contains the data column names
            t_header = table.find('thead').find_all('tr')[1]
            columns = t_header.find_all('th')
            columns_info = [column.get('aria-label', None) for column in columns]
            table_header = [column.get_text(strip=True) for column in columns]
            extracted_data.append(table_header)
            # make a dictionary of data names and column info
            defensive_schema = {name: info for name, info in zip(table_header, columns_info)}
            # store schema
            file_path = f'temp_data/opp_pass_schema{season}.json'
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(file_path, 'w', newline='') as json_file:
                json.dump(defensive_schema, json_file, indent=2)

            # extract the table body
            table_body = table.find('tbody')
            # exclude the header rows
            rows_to_exclude = table_body.find_all('tr', class_='thead rowSum')
            for row in rows_to_exclude:
                row.decompose()
            rows = table_body.find_all('tr')

            # get the data values from the first element being a th and the following being td
            for row in rows:
                data = []
                stats = row.find_all(['th', 'td'])
                for stat in stats:
                    # handling Na values
                    data.append('Na' if stat.text == '' else stat.text)
                extracted_data.append(data)

            # store the table in csv
            file_path = f'temp_data/opp_pass_data{season}.csv'
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            # create shooting_data.csv
            with open(file_path, 'w', newline='') as csvfile:
                # Create a CSV writer
                csvwriter = csv.writer(csvfile)
                # write data
                for row in extracted_data:
                    if len(row) != len(table_header):
                        print('lengths dont match len(row) len(header)', len(row), len(table_header))
                        break
                    else:
                        csvwriter.writerow(row)
                print(f'Success: Your shooting data is under {file_path}')
            time.sleep(5)

        else:
            print(f'Error fetching table from {url}')
