import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, mean_squared_error 


def onehot_data(data):
    team1_col = data[['one1', 'one2', 'one3', 'one4', 'one5']]
    team2_col = data[['two1', 'two2', 'two3', 'two4', 'two5']]
    team1_features = pd.get_dummies(team1_col, prefix='t1')
    team2_features = pd.get_dummies(team2_col, prefix='t2')
    data = pd.merge(left=data, right=team1_features, left_index=True,right_index=True)
    data = pd.merge(left=data, right=team2_features, left_index=True,right_index=True)
    data = data.groupby(data.columns, axis=1).sum()
    data = data.drop(['one1', 'one2', 'one3', 'one4', 'one5','two1', 'two2', 'two3', 'two4', 'two5'], axis=1)
    return data

def train_model(data):
    print(data.head())
    features = data.drop(['win'], axis=1)
    label = data['win']
    x_train, x_test, y_train, y_test = train_test_split(features, label, test_size=0.10)
    model = DecisionTreeClassifier()
    model.fit(x_train, y_train)
    y_predict = model.predict(x_test)
    print('MSE: ' + str(mean_squared_error(y_test, y_predict)))
    print('Accuracy: ' + str(accuracy_score(y_test, y_predict))) 


def get_good_data():
    data = pd.read_csv('match_data.csv')
    data = onehot_data(data)
    print(data.head())
    data.to_csv('good_match_data.csv')

def main():
    #data = pd.read_csv('good_match_data.csv')
    #for col in data.columns:
        #print(col)
    print(train_model(pd.read_csv('good_match_data.csv')))

if __name__ == '__main__':
    main()