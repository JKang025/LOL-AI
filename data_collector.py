import requests
import time
import pandas as pd
import traceback
import my_utils

MY_PUUID = '51pKOAjVvVFCP77maBPpiMCeSeQrKFLjFLa9Wo9mngMGqYSgS0CbFfnYjuMcn7uBYXalM5DBWcF0Fg'
API_KEY = 'RGAPI-de3f1231-ea52-4344-b6da-438dd521fbe8'

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
    dcrawl = datacrawler(my_utils.txt_to_set('test_matchid_list.txt'), set())
    dcrawl.gather_data('test_match_data.csv')


def main():
    """
    dcrawl = datacrawler()
    rawd = dcrawl.get_match_data('NA1_4264715107')
    print(rawd['info']['participants'])
    a = dcrawl.get_relevant_data(rawd)
    print(a)
    """
    get_data()


if __name__ == '__main__':
    main()
    

