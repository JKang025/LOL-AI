import requests
import numpy as np
import os
import time
import pandas as pd
import traceback

import my_utils

MY_PUUID = '51pKOAjVvVFCP77maBPpiMCeSeQrKFLjFLa9Wo9mngMGqYSgS0CbFfnYjuMcn7uBYXalM5DBWcF0Fg'
API_KEY = 'RGAPI-a7b06e50-6c8c-49c9-bb2e-1c2c3d6a077f'

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
        response = requests.get('https://americas.api.riotgames.com/lol/match/v5/matches/' + matchid + '?api_key=' + API_KEY)
        self.requests += 1
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
        if participants[0]['win'] == 'true':
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
                    self.requests += 1
                    self.datacrawl(p, layer + 1, max_layer)
        except Exception as e: 
            traceback.print_exc()
            print(self.get_match_data(matches[index]))
                
def main():
    me = playerobj(MY_PUUID, 5)
    #print(a.matches)                         
    #dc = datacrawler()
    #data = dc.get_match_data('NA1_4317076649')
    #print(len(dc.get_player_puuid_in_match(data, MY_PUUID)))
    #print(dc.get_relevant_data(data))
    #a = set()
    #a.update(['john', 'james', 'jill', 'jack'])
    #my_utils.set_to_txt(a, 'matchid_list.txt')
    #print(my_utils.txt_to_set('matchid_list.txt'))
    test = datacrawler()
    test.datacrawl(me, 0, 7)
    my_utils.set_to_txt(test.puuid_set, 'puuid_list.txt')


if __name__ == '__main__':
    main()
    

