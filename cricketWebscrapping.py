#Scrape espncricinfo 
#and save the player info
import requests 
from bs4 import BeautifulSoup 
import csv 
from pprint import pprint
import time
import timeit
import logging
import os

logging.basicConfig(filename='scrapper.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


classes = {"TEST": 1, "ODI": 2, "T20I": 3, "TOT": 11}
classes = {"ODI": 2}
# team_name = {1: "ENG", 2:  "AUS", 3: "SA", 4: "WI", 5: "NZ", 6: "IND", 7: "PAK", 8: "SL"}
team_name = {40:"Afghanistan",4058:"Africa XI",106:"Asia XI",2:"Australia",25:"Bangladesh",12:"Bermuda",17:"Canada",14:"East Africa",1:"England",19:"Hong Kong",140:"ICC World XI",6:"India",29:"Ireland",4083:"Jersey",26:"Kenya",28:"Namibia",32:"Nepal",15:"Netherlands",5:"New Zealand",37:"Oman",7:"Pakistan",20:"Papua New Guinea",30:"Scotland",3:"South Africa",8:"Sri Lanka",27:"United Arab Emirates",11:"United States of America",4:"West Indies",9:"Zimbabwe"}
teams = list(team_name.keys())
types = ["batting", "bowling", "fielding", "allround", "team", "aggregate"]
types = ["team"]
params = ""
file = "espncricinfo_data/espncricinfos"

def write_to_file(cls_name, filename, colums, stats):
    print(f"Creating file {filename} for class {cls_name}")
    print(f"colums = {colums}")
    print(f"stats = {stats}")
    if len(colums) == 0 or len(stats) == 0:
        return
    with open(filename, 'a', newline='') as f: 
        w = csv.DictWriter(f, colums) 
        if not os.path.isfile(filename):
            w.writeheader() 
        for stat in stats: 
            w.writerow(stat)
    print(f"File {filename} created !")

def create_data(team_name, cls, page, team, type):
    start = timeit.default_timer()
    params = f"class={cls};page={page};team={team};template=results;type={type}"
    URL = f"https://stats.espncricinfo.com/ci/engine/stats/index.html?{params}"
    print(f"Scrapping URL = {URL}")
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') 
    # time.sleep(1)
    table = soup.findAll('tr', attrs = {'class':'data1'})
    column_name = []
    stats = []
    for rows in table:
        try:
            row = rows.findAll('td')
            player_stats = {}
            player_stats['team'] = team_name
            if type == "batting":
                # player, span, match, innings, no, runs, hs, ave, bf, sr, r_100, r_50, r_0, r_4s, r_6s, _ = [td.text for td in row ]
                player, span, match, innings, no, runs, hs, ave, bf, sr, r_100, r_50, r_0, _ = [td.text for td in row ]
                # column_name = ['team', 'player', 'span', 'match', 'innings', 'no', 'runs', 'hs', 'average', 'bf', 'sr', '100', '50', '0', '4', '6']
                column_name = ['team', 'player', 'span', 'match', 'innings', 'no', 'runs', 'hs', 'average', 'bf', 'sr', '100', '50', '0']
                for i, col in enumerate(column_name[1:], 0):
                    player_stats[col] = [player, span, match, innings, no, runs, hs, ave, bf, sr, r_100, r_50, r_0][i]
            if type == "bowling":
                player, span, match, innings, overs, mdns, runs, wkts, bbi, bbm, ave, econ, sr, r_4, r_5, _ = [td.text for td in row ]
                column_name = ['team', 'player','span', 'match', 'innings', 'overs', 'mdns', 'runs', 'wkts', 'bbi', 'bbm', 'avg', 'econ', 'sr', '4', '5']
                for i, col in enumerate(column_name[1:], 0):
                    player_stats[col] = [player, span, match, innings, overs, mdns, runs, wkts, bbi, bbm, ave, econ, sr, r_5, r_5][i]
            if type == "fielding":
                player, span, match, innings, dis, ct, st, ct_wkts, md, di, _ = [td.text for td in row ]
                column_name = ['team', 'player','span', 'match', 'innings', "dis", 'ct', 'st', 'ct_wkts', 'md', 'di']
                for i, col in enumerate(column_name[1:], 0):
                    player_stats[col] = [player, span, match, innings, dis, ct, st, ct_wkts, md, di][i]
            if type == "allround":
                player, span, match, runs, hs, bat_avg, r_100, wkts, bbi, bowl_avg, r_5, ct, st, avg_diff, _ = [td.text for td in row ]
                column_name = ['team', 'player', 'span', 'match', 'runs', 'hs', 'bat_avg', 'r_100', 'wkts', 'bbi', 'bowl_avg', 'r_5', 'ct', 'st', 'avg_diff']
                for i, col in enumerate(column_name[1:], 0):
                    player_stats[col] = [player, span, match, runs, hs, bat_avg, r_100, wkts, bbi, bowl_avg, r_5, ct, st, avg_diff][i]
            if type == "team":
                team, span, match, won, lost, tied, nr, w_l, avg, rpo, innings, hs, ls, _ = [td.text for td in row ]
                column_name = ['team', 'team', 'span', 'match', 'won', 'lost', 'tied', 'nr', 'w_l', 'avg', 'rpo', 'innings', 'hs', 'ls']
                for i, col in enumerate(column_name[1:], 0):
                    player_stats[col] = [team, span, match, won, lost, tied, nr, w_l, avg, rpo, innings, hs, ls][i]
            if type == "aggregate":
                span, match, won, tied, draw, runs, wkts, balls, avg, rpo, _ = [td.text for td in row ]
                column_name = ['team', 'span', 'match', 'won', 'tied', 'draw', 'runs', 'wkts', 'balls', 'avg', 'rpo']
                for i, col in enumerate(column_name[1:], 0):
                    player_stats[col] = [span, match, won, tied, draw, runs, wkts, balls, avg, rpo][i]
            # print(f"player_stats : {player_stats}")
        except Exception as e:
            print(f"Someting happend like : {e}, and row value is : {row} and URL {URL}, lets continue!")
            continue
        stats.append(player_stats)
        # print(stats)
    end = timeit.default_timer()
    print(f"Total time taken to get data : {(end - start)/ 60:.2f}")
    return stats, column_name

def create_data_teams(cls, page, type, teams):
    start = timeit.default_timer()
    team = ''
    for t in teams:
        team += f'team={t};'
    params = f"class={cls};page={page};{team};template=results;type={type}"
    URL = f"https://stats.espncricinfo.com/ci/engine/stats/index.html?{params}"
    print(f"Scrapping URL = {URL}")
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib') 
    # time.sleep(1)
    table = soup.findAll('tr', attrs = {'class':'data1'})
    column_name = []
    stats = []
    for rows in table:
        try:
            row = rows.findAll('td')
            player_stats = {}
            team, span, match, won, lost, tied, nr, w_l, avg, rpo, innings, hs, ls, _ = [td.text for td in row ]
            column_name = ['team', 'span', 'match', 'won', 'lost', 'tied', 'nr', 'w_l', 'avg', 'rpo', 'innings', 'hs', 'ls']
            for i, col in enumerate(column_name[1:], 0):
                player_stats[col] = [team, span, match, won, lost, tied, nr, w_l, avg, rpo, innings, hs, ls][i]
        except Exception as e:
            print(f"Someting happend like : {e}, and row value is : {row} and URL {URL}, lets continue!")
            continue
        stats.append(player_stats)
        print(stats)
    end = timeit.default_timer()
    print(f"Total time taken to get data : {(end - start)/ 60:.2f}")
    return stats, column_name

def main():
    if types[0] == 'team':
        cls = 2
        type = 'team'
        file_name = f"{file}_{cls}_{type}.csv"
        for page in range(1, 20):
            stats, columns = create_data_teams(cls, page, type, teams)
            write_to_file(cls, file_name, columns, stats)
        return

    for cls in classes.values():
        print(f"Getting stat for class {cls}")
        for team in teams:
            teamname = team_name[team]
            print(f"Getting stat for team { teamname}")
            for type in types:
                print(f"Getting stat for type {type}")
                file_name = f"{file}_{cls}_{type}.csv"
                for page in range(1, 20):
                    print(f"Getting stat for page {page}")
                    stats, columns = create_data(teamname, cls, page, team, type)
                    write_to_file(cls, file_name, columns, stats)

if __name__ == '__main__':
    start = timeit.default_timer()
    main()
    end = timeit.default_timer()
    print(f"Total time taken for whole process : {(end - start)/ 60:.2f}")
