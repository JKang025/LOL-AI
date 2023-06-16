# LOL-AI

The objective of this project is to create a model that can accurately predict League of Legends matches given the team composition of each team.

Furthermore, using this model I hope to be able to determine whether a player contributes positively or negatively to their team composition.

### Background
League of Legends is a five versus five competitive multiplayer game. Each player chooses a character--usually referred to as a champion--that has drastically different abilities, roles, and strengths. There is a common consensus in the community that team composition is a factor in the outcome of a match (although the degree of impact remains uncertain), as certain champions play well with others while certain champions are well suited to counter other champions. Furthermore, some champions are just generally considered stronger than others in any given version of the game. As such, intuitively, it makes sense that statistical models should be able to make these connections to accurately predict outcomes of matches to some degree given enough data.

## Methodology and Implementation
### Data collection 
The data collection and processing all occurred in data_collector.py. The RIOT API does not allow you to immediately query a large number of games easily. As such, the data is collected through a convoluted process:
1. start with a player
2. pick one of their recent games, find the other player
3. choose Y other players in the game you choose, and repeat steps 1-3 until you have a sufficient number of unique players
4. Then get data of the last X games of each unique player

X and Y are controlled so you can get a sufficient amount of games from a sufficiently diverse population while also not taking too many requests. This process is also slow, as they only allow 100 requests every 2 minutes.
### Data processing

The data collected on team composition and which team won is all the raw data needed. However, this is currently not able to be processed by models, so I simply used **one hot encoding**, which is basically adding a column with each champion's name, and 1 if it was on the team, and 0 otherwise. This is done twice, as there is a distinction between what team the champion is on.

### Model training

After the data is processed, a variety of models are trained on the data, including an MLP Classifier (neural network), tree classifier, and forest classifier. I determined that the forest classifier had the highest accuracy with default parameters.

Therefore, I began to do **hyperparameter tuning** on the forest classifier. I first used a testing function that input random parameters into the forest classifier to find the general optimal range. Then I used grid hyperparameter tuning on the general range found with the random method. Using this, I found the optimal parameters to use with a forest classifier.

### Model validation
To test the models, to ensure there was no overfitting I did the general 80/20 division of training versus test data. All the results are from the test data.
## Results
My best model was a hyperparameter tuned forest classifier, with a 53% accuracy. While this is certainly low, it is statistically significant. I believe that this model can be easily improved with more data, which admittedly is very annoying to obtain.

I also tried to use the model on myself for fun. The model predicts my team had better team composition 62% of the time, while my actual win rate is 65%. Out of the games I have won, the model predicted me to win 68% of the time

## Roadmap and Improvements
I hope to return to this project with more data and try to use a neural network instead. I believe that, theoretically, it should be good at this, as it will be able to identify the connections of synergy, counters, and roles in literally countless different permutations of team compositions.
## Usage
### Setup
There are a few packages that this program requires, outlined in the provided requirements.txt.
```
pip3 install -r requirements.txt
```

### API 
If you want to collect the up-to-date data yourself, you must set up a [RIOT API account and key]([https://developer.riotgames.com/ (https://developer.riotgames.com/)). Then copy the key into the API_KEY global constant in data_collector.py. Note that the general RIOT API account's keys only last for a day and have limited requests, which is a large limiting factor in data collection.

### Starting Node/Player
As mentioned previously, the data is gathered starting from a specific player's id, dubbed the PUUID. Currently, it uses my personal PUUID as a starting point, but if you wish to change that, simply [find the PUUID of the player you wish to start with](https://developer.riotgames.com/apis#account-v1/GET_getByRiotId) and enter that in the MY_PUUID constant in data_collector.py.

### Running the program yourself
To run the data collection,  run
```
py data_collector.py
```
Note that due the limited requests of the general RIOT API account, this process will take over 24 hours. As such, as the key expires in 24 hours, it is suggested to run get_puuids(), get_matchid(), get_data() seperately.

Afterwards, you can process the data and find the results of the models yourself by running 
```
py data_analysis.py
```
Note that the hyperparamater training is disabled by default, as the optimal hyperparamaters have already been inserted in the functon, and the training takes a long time, but if you want to find the optimal hyperparamaters yourself, just uncomment train_forest_hyperparam_random(), train_forest_hyperparam_grid()

### Data guide
*  'match_data.csv' : 50,000~ datapoints of champions on each team and which team won 

* 'good_match_data.csv' : same as above, but one hot encoded for the champions

 * 'player_match_history.csv' : 100 datapoints of champions on each team, which team won, and which team the player analyzed is on 
 * 'good_player_match_history.csv' : same as above, but one hot encoded for the champions 
 * 'puuid_list.txt' : list of thousands of unique PUUIDS 
 * 'matchid_list.txt' : list of around 50k unique matchIDS 
 * 'duo_data.txt' : dictionary of botlane combos over 50 games played and their respective winrates 
 * 'best_duo.txt' : list of top 10 botlane, str includes names and winrate 