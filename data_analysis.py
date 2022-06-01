import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, mean_squared_error 
from sklearn.neural_network import MLPClassifier


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

def train_treeclassifier_model(data):
    features = data.drop(['win'], axis=1)
    label = data['win']
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.20)
    model = DecisionTreeClassifier()
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    ytrain_predict = model.predict(x_train)
    print('MSE: ' + str(mean_squared_error(y_test, y_predict)))
    print('Accuracy: ' + str(accuracy_score(y_test, y_predict))) 
    print('MSEt: ' + str(mean_squared_error(y_train, ytrain_predict)))
    print('Accuracyt: ' + str(accuracy_score(y_train, ytrain_predict))) 

def train_neural_model(data):
    features = data.drop(['win'], axis=1)
    label = data['win']
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.20)
    model = MLPClassifier(hidden_layer_sizes=(256, 128, 64))
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    print('MSE: ' + str(mean_squared_error(y_test, y_predict)))
    print('Accuracy: ' + str(accuracy_score(y_test, y_predict))) 

def get_good_data():
    data = pd.read_csv('match_data.csv')
    data = onehot_data(data)
    data.to_csv('good_match_data.csv')

def main():
    #get_good_data()
    #data = pd.read_csv('good_match_data.csv')
    #for col in data.columns:
        #print(col)
    
    train_treeclassifier_model(pd.read_csv('good_match_data.csv'))
    #train_neural_model(pd.read_csv('good_match_data.csv'))

if __name__ == '__main__':
    main()