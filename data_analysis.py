import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, mean_squared_error 
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
import json
from operator import itemgetter



OG_DATA_PATH = 'match_data.csv'
GOOD_DATA_PATH = 'good_match_data.csv'


def train_treeclassifier(data):
    features = data.drop(['win'], axis=1)
    label = data['win']
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.15)
    model = DecisionTreeRegressor()
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    ytrain_predict = model.predict(x_train)
    print('MSE: ' + str(mean_squared_error(y_test, y_predict)))
    print('Accuracy: ' + str(accuracy_score(y_test, y_predict))) 
    print('MSEtrain: ' + str(mean_squared_error(y_train, ytrain_predict)))
    print('Accuracytrain: ' + str(accuracy_score(y_train, ytrain_predict))) 


def train_neural_model(data):
    features = data.drop(['win'], axis=1)
    label = data['win']
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.15)
    model = MLPClassifier()
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    ytrain_predict = model.predict(x_train)
    print('MSE: ' + str(mean_squared_error(y_test, y_predict)))
    print('Accuracy: ' + str(accuracy_score(y_test, y_predict))) 
    print('MSEtrain: ' + str(mean_squared_error(y_train, ytrain_predict)))
    print('Accuracytrain: ' + str(accuracy_score(y_train, ytrain_predict))) 
    print(classification_report(y_test,y_predict))
    return model

def train_forest_default(data):
    features = data.drop(['win'], axis=1)
    label = data['win']
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.15)
    model = RandomForestClassifier()
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    ytrain_predict = model.predict(x_train)
    print('MSE: ' + str(mean_squared_error(y_test, y_predict)))
    print('Accuracy: ' + str(accuracy_score(y_test, y_predict))) 
    print('MSEtrain: ' + str(mean_squared_error(y_train, ytrain_predict)))
    print('Accuracytrain: ' + str(accuracy_score(y_train, ytrain_predict))) 
    return model

def train_forest_hyperparam_random(data):
    features = data.drop(['win'], axis=1)
    label = data['win']
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.15)
    random_grid = {'n_estimators': [10, 100, 200, 300, 400, 500, 700, 900, 1100, 1500, 1900],
               'max_features': ['auto', 'sqrt'],
               'max_depth': [5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
               'min_samples_split': [2, 5, 10, 50, 100, 200, 400],
               'min_samples_leaf': [1, 2, 4, 10, 50, 100, 200, 400],
               'bootstrap': [True, False]}
    model = RandomForestClassifier()
    model_random = RandomizedSearchCV(estimator=model, param_distributions=random_grid, n_iter=100, cv=3, verbose=2, random_state=42, n_jobs=-1)
    model_random.fit(x_train,y_train)
    best_model = model_random.best_estimator_
    print(model_random.best_params_)
    return best_model

def train_forest_hyperparam_grid(data):
    features = data.drop(['win'], axis=1)
    label = data['win']
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.15)
    grid = {'n_estimators': [300,400,500,600,700],
               'max_features': ['auto'],
               'max_depth': [50,60,70,80],
               'min_samples_split': [150,200,250],
               'min_samples_leaf': [3,4,5],
               'bootstrap': [True]}

    model = RandomForestClassifier()
    grid_search = GridSearchCV(estimator = model, param_grid = grid, 
                          cv = 3, n_jobs = -1, verbose = 2)
    grid_search.fit(x_train, y_train)
    print(grid_search.best_params_)
    best_model = grid_search.best_estimator_
    y_predict = best_model.predict(x_test)
    ytrain_predict = best_model.predict(x_train)
    print('MSE: ' + str(mean_squared_error(y_test, y_predict)))
    print('Accuracy: ' + str(accuracy_score(y_test, y_predict))) 
    print('MSEtrain: ' + str(mean_squared_error(y_train, ytrain_predict)))
    print('Accuracytrain: ' + str(accuracy_score(y_train, ytrain_predict))) 
    return best_model

def train_forest_optimal(data):
    features = data.drop(['win'], axis=1)
    label = data['win']
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.15)
    model = RandomForestClassifier(bootstrap=True, max_depth=80, max_features='auto', min_samples_leaf=5, min_samples_split=200, n_estimators=300)
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    ytrain_predict = model.predict(x_train)
    print('MSE: ' + str(mean_squared_error(y_test, y_predict)))
    print('Accuracy: ' + str(accuracy_score(y_test, y_predict))) 
    print('MSEtrain: ' + str(mean_squared_error(y_train, ytrain_predict)))
    print('Accuracytrain: ' + str(accuracy_score(y_train, ytrain_predict))) 
    return model

def get_good_bot_duos():
    bot_duo_dict = {}
    dataset = pd.read_csv(OG_DATA_PATH)
    one = dataset[['one4', 'one5', 'win']]
    for i in range(len(one)):
        champ1 = one.at[i, 'one4']
        champ2 = one.at[i, 'one5']
        win = int(one.at[i, 'win'])
        key = [champ1, champ2]
        key.sort()
        key = ''.join(key)
        if key in bot_duo_dict:
            bot_duo_dict[key][0] += win
            bot_duo_dict[key][1] += 1
        else:
            bot_duo_dict.update({key: [win, 1]})
    two = dataset[['two4', 'two5', 'win']]
    for i in range(len(two)):
        champ1 = two.at[i, 'two4']
        champ2 = two.at[i, 'two5']
        win = int(two.at[i, 'win'])
        win = (win -1)  * -1
        key = [champ1, champ2]
        key.sort()
        key = ''.join(key)
        if key in bot_duo_dict:
            bot_duo_dict[key][0] += win
            bot_duo_dict[key][1] += 1
        else:
            bot_duo_dict.update({key: [win, 1]})
    duo_wr = {}
    for key in bot_duo_dict.keys():
        if bot_duo_dict[key][1] > 50:
            duo_wr.update({key: bot_duo_dict[key][0]/bot_duo_dict[key][1]})
    top_wr_duos = sorted(duo_wr, key=duo_wr.get, reverse=True)[:10]
    final = []
    for key in top_wr_duos:
        final.append(key + ' Winrate: ' + str(duo_wr[key]))
    with open('best_duos.txt', 'w') as convert_file:
        convert_file.write(json.dumps(final))
    with open('duo_data.txt', 'w') as convert_file:
        convert_file.write(json.dumps(duo_wr))

def player_predicted_wins():
    dataset = pd.read_csv(GOOD_DATA_PATH)
    model = train_forest_optimal(dataset)
    player_history = pd.read_csv('good_player_match_history.csv')
    features = player_history.drop(['player_team', 'win', 'Unnamed: 0'], axis=1)
    predict = list(model.predict(features))
    result = list(player_history['win'])
    player_team = list(player_history['player_team'])
    player_pred_win = 0
    player_won = 0
    pred_and_won = 0
    for i in range(len(predict)):
        if predict[i] == player_team[i]:
            player_pred_win += 1
        if player_team[i] == result[i]:
            player_won += 1
        if (player_team[i] == result[i]) and (predict[i] == player_team[i]):
            pred_and_won += 1

    print(predict)
    print(str(player_pred_win/len(predict)) + ' predicted')
    print(str(player_won/len(predict)) + ' wr')
    print(str(pred_and_won/player_won) + 'won and pred')
    
    


def main():
    """
    get_good_data()
    train_forest_optimal(pd.read_csv(GOOD_DATA_PATH))
    player_predicted_wins()
    """
    
    #train_treeclassifier_model(pd.read_csv('good_match_data.csv'))
    #train_neural_model(pd.read_csv('good_match_data.csv'))
    #train_forest(pd.read_csv('good_match_data.csv'))
    #train_forest_hyperparam_grid(pd.read_csv('good_match_data.csv'))
    #train_forest_optimal(pd.read_csv('good_match_data.csv'))
    
    #data = pd.read_csv('good_match_data.csv')
    #print(data['win'].value_counts())

    #test_neural_model(pd.read_csv('good_match_data.csv'))

    get_good_bot_duos()

if __name__ == '__main__':
    main()