import pandas as pd
from cse163_utils import assert_equals


def test_data_to_csv():
    """
    tests if test_match_data.csv has the right data
    """
    data = pd.read_csv('test_match_data.csv').to_dict('records')
    actual_value = [{'Unnamed: 0': 0, 'win': 1, 'one1': 'Garen',
                     'one2': 'Amumu', 'one3': 'Orianna',
                     'one4': 'Swain', 'one5': 'Ziggs',
                     'two1': 'Kayle', 'two2': 'Shyvana',
                     'two3': 'Teemo', 'two4': 'MissFortune',
                     'two5': 'Lux'},
                    {'Unnamed: 0': 1, 'win': 0, 'one1': 'Illaoi',
                     'one2': 'Taliyah', 'one3': 'Graves', 'one4': 'Kaisa',
                     'one5': 'Renata',
                     'two1': 'Kled', 'two2': 'Elise', 'two3': 'Pantheon',
                     'two4': 'Vayne', 'two5': 'Senna'}]
    assert_equals(actual_value, data)


def test_good_match_data():
    """
    test if number of features in good_match_data.csv
    is correct
    """
    data = pd.read_csv('good_match_data.csv')
    assert_equals(320, len(data.columns))
    # num champs * 2 + 1(win) + 1(unanmed)


def test_good_player_match_history():
    """
    test if number of features in
    good_player_match_history.csv
    is correct
    """
    data = pd.read_csv('good_player_match_history.csv')
    assert_equals(322, len(data.columns))
    # num champs * 2 + 1(win) + 1(player_team) + 2(unanmed)


def main():
    """
    runs aforementioned functions
    """
    test_data_to_csv()
    test_good_match_data()
    test_good_player_match_history()


if __name__ == '__main__':
    main()
