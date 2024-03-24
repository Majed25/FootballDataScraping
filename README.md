# Football Data Scraping

## Objective

The objective of this project is to scrape football data for analysis, specifically to investigate whether striker transfers affect their performance in finishing.

## Data Sources

### FBref

- [Players Data (Big Five Leagues) for the Last 5 Years](https://fbref.com/en/comps/Big5/Big-5-European-Leagues-Stats)
- [Shooting Data (Big Five Leagues)](https://fbref.com/en/comps/Big5/shooting/players/Big-5-European-Leagues-Stats)
- [Defensive Action Stats (Big Five Leagues, 2023-2024)](https://fbref.com/en/comps/Big5/defense/players/Big-5-European-Leagues-Stats)
- [Goal and Shot Creation Stats (Big Five Leagues, 2023-2024)](https://fbref.com/en/comps/Big5/gca/players/Big-5-European-Leagues-Stats)

### Transfermarkt

- [Players Transfers](https://www.transfermarkt.com/)

## Steps

1. **Scraping Strikers' Shooting Data**
   - Utilize FBref's shooting data for the Big Five Leagues. 
   - The tables schema is not consistent throughout the seasons so they are separated to two parts (Seasons 09-16 / Seasons 17-24)
   - CSV file stored in "shooting_data/"

2. **Scraping Teams' Defensive Action And opposition passes Data**
   - Obtain defensive actions and opposition actions stats for the 2023-2024 season from FBref. In order to calculate
   - the (Passes per defensive actions allowed) PPDA, which is the number of opposition passes / number of devfensive
   - actions.
   - Storing data under "defensive_data/" and "opp_pass_data/"
   
   
4. **Scraping Transfer Data**
   - Start with scraping transfer data for the Premier League from Transfermarkt.
   - Data stored under "transfers_data/"


5. **Optimization and Data Preparation**
   - Add a year/team as a column to the tables help get the appropriate data later when analyzing the data.
   - Check if the tables schemas matching before merging the data.
   
   

## Legal Disclaimer

The data scraped from external sources, including FBref and Transfermarkt, is subject to the terms and conditions of the respective websites. While FBref permits scraping of their data with certain restrictions, Transfermarkt's policies may vary. I, Majid Menouar, am committed to adhering to fair use principles and respecting the terms of service of these websites.

It is important to ensure compliance with the policies and terms of each website before using the scraped data for analysis or any other purpose. By using this data, you acknowledge and agree to abide by the terms and conditions set forth by FBref and Transfermarkt.

