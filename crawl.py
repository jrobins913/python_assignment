from bs4 import BeautifulSoup
import requests
from db import *

db_type = 'sqllite'
# db_type = 'postgres'
page_link = 'https://d1baseball.com/conference/big-ten-conference/2018/'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}

# open main page to get the list of teams
page_response = requests.get(page_link, timeout=5, headers=headers)
page_content = BeautifulSoup(page_response.content, "html.parser")

# find the team class looping over each team to get the link content for each team stats page
batting_table = []
pitching_table = []
for tag in page_content.find_all('td', class_='team'):
    team_link = tag.find('a')['href']
    team_page = 'https://d1baseball.com'+team_link+'/2018/stats'
    # open the team stats page
    t_page_resp = requests.get(team_page, timeout=6, headers=headers)
    t_page_content = BeautifulSoup(t_page_resp.content, "html.parser")

    # find the batting-stats table and place the cell data in a matrix

    for table_tag in t_page_content.find_all('table', {'id': 'batting-stats'}):
        for tr in table_tag.find_all('tr'):
            row = []
            for td in tr.find_all('td'):
                row.append(td.text)
            # skip the title row
            if len(row) > 0:
                batting_table.append(row)

    # find the pitching stats table

    for table_tag in t_page_content.find_all('table', {'id': 'pitching-stats'}):
        for tr in table_tag.find_all('tr'):
            row = []
            for td in tr.find_all('td'):
                row.append(td.text)
            # skip the title row
            if len(row) > 0:
                pitching_table.append(row)

# Create tables and insert data
db = get_connection(db_type)
player_model = get_player_model(db)
pitcher_model = get_pitcher_model(db)
db.drop_tables([player_model, pitcher_model])
db.create_tables([player_model, pitcher_model])

# Create tuples of data from the table matrix so we can bulk insert in single transaction
hitting_data = []
for row in batting_table:
    hitting_data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[8]))

pitching_data = []
for row in pitching_table:
    pitching_data.append((row[0], row[1], row[2], row[3], row[4], row[10]))

# bulk insert in transaction
with db.atomic():
    player_model.insert_many(hitting_data, get_player_fields(db)).execute()

with db.atomic():
    pitcher_model.insert_many(pitching_data, get_pitcher_fields(db)).execute()



