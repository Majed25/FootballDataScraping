from bs4 import BeautifulSoup
import requests
import json
import time
import csv

HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}
"""
session = requests.session()
session.headers.update(HEADERS)
"""

LEAGUES = {'laliga': 'ES1',
           'bundesliga': 'L1',
           'serie-a': 'IT1',
           'premier-league': 'GB1',
           'ligue-1': 'FR1'
           }
SEASONS = [yr for yr in range(2009, 2024)]
URLS = []
for league, lg in LEAGUES.items():
    for season in SEASONS:
        url = f'https://www.transfermarkt.com/{league}/transfers/wettbewerb/{lg}/plus/?saison_id={season}&s_w=&leihe=1&intern=0&intern=1'
        URLS.append(url)

#scrping 1 example table
html_content = requests.get(URLS[1])

if html_content.status_code == 200:
    print('Success')
    soup = BeautifulSoup(html_content.text, 'html.parser')
    team_tags_html = soup.find_all('h2',
                                   class_="content-box-headline content-box-headline--inverted content-box-headline--logo")
    team_names = []
    for team_tag in team_tags_html:
        team_name = team_tag.find_all('a')[1]
        if team_name:
            team_names.append(team_name.text.strip())

    # getting the tables
    tables = soup.find_all('div', class_='responsive-table')
    tables = tables[::2]
    soup = BeautifulSoup(str(tables), 'html.parser')
    target_tables = soup.find_all('table')
    # open csv file
    csv_file_path = 'temp_data/team_transfer.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        # Create a CSV writer object
        csv_writer = csv.writer(csv_file)

        # write the table header
        headers = [col.text.strip() for col in target_tables[0].find('thead').find('tr').find_all('th')]
        print(headers)

        # I need to duplicate the column in my header because it contains 2 elements.
        LEFT_index = headers.index('Left')
        my_headers = headers[:LEFT_index + 1]
        my_headers.append('previous_team')
        my_headers = my_headers + headers[LEFT_index + 1:]
        my_headers.append('current_team')
        csv_writer.writerow(my_headers)

        # parse the table data
        for table, team in zip(target_tables, team_names):

            # get the tr tags "rows"
            rows_tags = [tr for tr in table.find('tbody').find_all('tr')]
            for tr in rows_tags:
                soup = BeautifulSoup(str(tr), 'html.parser')
                data = [dt.text.strip() if dt.text else 'Nan' for dt in soup.find_all('td')]
                data.append(team)
                csv_writer.writerow(data)


else:
    print(html_content.status_code)



# empty




