# CSE163-LOL-AI

## API SETUP INSTRUCTIONS

This project gathers data from the RIOTAPI, created and maintained by the creators of League of Legends. To gain acess, first head to https://developer.riotgames.com/. There is a login button at the top-right corner, where you can use any riot account. If you do not have a riot account, simply create a free one by clicking on the create account link below the foward button on the login menu. After logging in, click on your profile in the top-right corner, then click dashboard. This should bring you to a page which contains a Development API Key section. Do the CAPTCHA and click on regenerate key, that is now an API key you can use until it expires at the time stated on the website. 

## PROGAM USE INSTRUCTIONS

The data_collector.py file will be the first file needed to gather the data from the API. Firstly, copy your API key into API_KEY global constant. Then run the file. This will take a long time due to API request limits (over 24hrs) and might not fully gather the data due to the API key expiring. Therefore, if you want to gather the full data, it is advised that you should run the functions get_puuids(), get_matchid(), and get_data() one at a time, and refresh the API key every time one of these functions complete. After getting the raw data, get_good_data() will generate good_match_data.csv which will be used for processing later on, and same for get_player_game_data() which uses the API but will take less than 2 minutes due to relativly small amount of requests. It should be noted that **the data will not exactly match the data given orginally** for the project, as the data gathering start point is the last few games from a specific player (my league account), and since I have played since I gathered the data, that means the players and games gathered from recursion will be different. In the grand scheme of things, however, this should not matter for the model once a large amount of datapoints is gathered.

The next file to run will be the data_analysis.py file to generate the models. The main method will run all the methods in the file, which will print out the infomration used for the report, all labeled, and create best_duos.txt and duo_data.txt which also contains infomraiton used in the report. It will also print out infomration on how the model predicts a certain player to do in his previous games determined by the data collected in the previous python file. However, running the main method with all the methods will likely take a long time as it includes the hyperparamater optimization methods, which go through many models and therefore will take a long time to run. Therefore, if you want to just see the information presented on the report quickly, do not run train_forest_hyperparam_grid() or train_forest_hyperparam_random(). Do know that you must run the data_collection.py methods in entirety, or various functions in this module will break. **all of the data collected in these instructions will be discussed and elborated on the report** 

Note: if you want to either generate data from a different starting point, or analyze a different player, change the MY_PUUID constant (to any valid PUUID) in data_collector.py and repeat the steps above. Information on getting PUUID can be found on this RIOTAPI page. https://developer.riotgames.com/apis#account-v1/GET_getByRiotId. 

Data guide:
'match_data.csv' : where around 50k datapoints of champions on each team and which team won
'good_match_data.csv' : same as above, but one hot encoded for the champions
'player_match_history.csv' : 100 datapoints of champions on each team, which team won, and which team the player analyzed is on
'good_player_match_history.csv' : same as above, but one hot encoded for the champions
'puuid_list.txt' : list of thousands of unique PUUIDS
'matchid_list.txt' : list of around 50k unique matchIDS
'duo_data.txt' : dictionary of botlane combos over 50 games played and their respective winrates
'best_duo.txt' : list of top 10 botlane, str includes names and winrate
-the rest of the non python files files used for testing
