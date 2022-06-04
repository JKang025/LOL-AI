from numpy import setdiff1d
import requests
import time
import pandas as pd
import traceback
import my_utils

MY_PUUID = '51pKOAjVvVFCP77maBPpiMCeSeQrKFLjFLa9Wo9mngMGqYSgS0CbFfnYjuMcn7uBYXalM5DBWcF0Fg'
API_KEY = 'RGAPI-7949a1de-dae5-4b3f-ac6b-0a315d58f37b'

class playerobj: 
    """
    class that has a players puuid and 10 matchid of recent games
    """
    def __init__(self, puuid, num_games):
        self.puuid = puuid
        response = requests.get('https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/' + \
                                puuid + '/ids?type=ranked&start=0&count=' + str(num_games) + '&api_key=' + API_KEY)
        self.matches = list(response.json())

class datacrawler:

    def __init__(self, matchid_set = set(), puuid_set = set()):
        self.matchid_set = matchid_set
        self.puuid_set = puuid_set
        self.requests = 0

    def get_match_data(self, matchid):
        self.request_handler()
        response = requests.get('https://americas.api.riotgames.com/lol/match/v5/matches/' + matchid + '?api_key=' + API_KEY)
        return response.json()

    def get_player_puuid_in_match(self, dict, ignorepuuid):
        participants = dict['info']['participants']
        players_puuid = []
        for player in participants:
            if player['puuid'] != ignorepuuid:
                players_puuid.append(player['puuid'])
        return players_puuid

    def get_relevant_data(self, dict):
        result = {}
        participants = dict['info']['participants']
        win = 0 # 1 if first team wins
        if str(participants[0]['win']) == 'True':
            win = 1
        result.update({'win':win})
        result.update({'one1':participants[0]['championName']})
        result.update({'one2':participants[1]['championName']})
        result.update({'one3':participants[2]['championName']})
        result.update({'one4':participants[3]['championName']})
        result.update({'one5':participants[4]['championName']})
        result.update({'two1':participants[5]['championName']})
        result.update({'two2':participants[6]['championName']})
        result.update({'two3':participants[7]['championName']})
        result.update({'two4':participants[8]['championName']})
        result.update({'two5':participants[9]['championName']})
        return result
    
    def request_handler(self):
        if self.requests == 99:
            print('waitlong')
            time.sleep(116)
            self.requests = 0
        if (self.requests % 20 == 0) and (self.requests != 0):
            time.sleep(1)
            print('waitshort')
        self.requests += 1
        print(self.requests)
    

    def datacrawl(self, player, layer, max_layer):
        matches = player.matches
        index = len(matches) - 1
        try:
            if (layer < max_layer) and index >= 0:
                self.request_handler()
                data = self.get_match_data(matches[index])
                players = self.get_player_puuid_in_match(data, player.puuid)
                self.puuid_set.update(players)
                for x in range(3):
                    self.request_handler()
                    p = playerobj(players[x], 2)
                    self.datacrawl(p, layer + 1, max_layer)
        except Exception as e: 
            traceback.print_exc()
            print(self.get_match_data(matches[index]))
    
    
    def find_matchids(self, games_per_player):
        for id in self.puuid_set:
            try:
                self.request_handler()
                p = playerobj(id, games_per_player)
                if 'status' not in p.matches:
                    self.matchid_set.update(p.matches)
            except Exception as e:
                traceback.print_exc()
    
    def gather_data(self, filename):
        data = []
        for match in self.matchid_set:
            try:
                match_data = self.get_relevant_data(self.get_match_data(match)) 
                data.append(match_data)
            except Exception as e:
                traceback.print_exc()
        df = pd.DataFrame(data)
        df.to_csv(filename)
    ######################################################################################################################
    #code after in this class is for research question 3, slightly aleterd versions of some previous methods
    def get_relevant_player_data(self, dict, player_puuid):
        result = {}
        participants = dict['info']['participants']
        win = 0 # 1 if first team wins
        if str(participants[0]['win']) == 'True':
            win = 1
        for i in range(10):
            if participants[i]['puuid'] == player_puuid:
                if i < 5:
                    result.update({'player_team': 1})
                else:
                    result.update({'player_team': 0})
        result.update({'win':win})
        result.update({'one1':participants[0]['championName']})
        result.update({'one2':participants[1]['championName']})
        result.update({'one3':participants[2]['championName']})
        result.update({'one4':participants[3]['championName']})
        result.update({'one5':participants[4]['championName']})
        result.update({'two1':participants[5]['championName']})
        result.update({'two2':participants[6]['championName']})
        result.update({'two3':participants[7]['championName']})
        result.update({'two4':participants[8]['championName']})
        result.update({'two5':participants[9]['championName']})
        return result
    
    def gather_player_data(self, filename, player_puuid):
        data = []
        for match in self.matchid_set:
            try:
                match_data = self.get_relevant_player_data(self.get_match_data(match), player_puuid) 
                data.append(match_data)
            except Exception as e:
                traceback.print_exc()
        df = pd.DataFrame(data)
        df.to_csv(filename)


def get_puuids():
    me = playerobj(MY_PUUID, 3)
    dcrawl = datacrawler()
    dcrawl.datacrawl(me, 0, 8)
    my_utils.set_to_txt(dcrawl.puuid_set)


def get_matchid():
    puuid_set = my_utils.txt_to_set('puuid_list.txt')   
    dcrawl = datacrawler(set(), puuid_set)
    dcrawl.find_matchids(10)
    matchids = dcrawl.matchid_set

    my_utils.set_to_txt(matchids, 'matchid_list.txt')


def get_data():
    dcrawl = datacrawler(my_utils.txt_to_set('matchid_list.txt'), set())
    dcrawl.gather_data('match_data.csv')

def onehot_data(data):
    team1_col = data[['one1', 'one2', 'one3', 'one4', 'one5']]
    team2_col = data[['two1', 'two2', 'two3', 'two4', 'two5']]
    team1_features = pd.get_dummies(team1_col, prefix='t1')
    team2_features = pd.get_dummies(team2_col, prefix='t2')
    data = pd.merge(left=data, right=team1_features, left_index=True,right_index=True)
    data = pd.merge(left=data, right=team2_features, left_index=True,right_index=True)
    data = data.groupby(data.columns, axis=1).sum()
    data = data.drop(['one1', 'one2', 'one3', 'one4', 'one5','two1', 'two2', 'two3', 'two4', 'two5', 'Unnamed: 0'], axis=1)
    return data

def get_good_data():
    data = pd.read_csv('match_data.csv')
    data = onehot_data(data)
    data.to_csv('good_match_data.csv')

def get_player_game_data():
    whole_dataset = pd.read_csv('good_match_data.csv')
    player = playerobj(MY_PUUID, 100)
    dcrawl = datacrawler(player.matches, set())
    dcrawl.gather_player_data('player_match_history.csv', MY_PUUID)
    data = pd.read_csv('player_match_history.csv')
    data = onehot_data(data)
    player_team = data['player_team']
    data = data.reindex(labels=whole_dataset.columns,axis=1)
    data = data.fillna(int(0))
    data = data.merge(right=player_team, left=data)
    data.to_csv('good_player_match_history.csv')

def main():
    #get_puuids()
    #get_matchid()
    #get_data()
    #get_good_data()
    #get_player_game_data()

    whole_dataset = pd.read_csv('good_match_data.csv')

    data = pd.read_csv('player_match_history.csv')
    data = onehot_data(data)
    player_team = data['player_team']
    data = data.reindex(labels=whole_dataset.columns,axis=1)
    data = data.fillna(int(0))
    data = pd.merge(right = player_team, left =data,left_index=True,right_index=True)
    data.to_csv('good_player_match_history.csv')


if __name__ == '__main__':
    main()
    

