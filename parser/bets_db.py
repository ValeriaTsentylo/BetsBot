from data_for_bet import find_sport_name, find_name_event, find_name_league, find_country_league, find_user_name, find_coefficient, find_display_name, find_max_value, find_date_bet
from data_for_db import find_display_name2, find_coefficient2, find_max_value2, link2, find_date_bet2, find_date_match, find_new_user_name
from mails.get_new_emails import link
import pandas as pd
import datetime as dt


def make_dict_bets():
    user_name = find_user_name()
    sport = find_sport_name()
    match_name = find_name_event()
    match_date = find_date_match()
    league = find_name_league()
    country = find_country_league()
    date2 = find_date_bet2()
    display_name2 = find_display_name2()
    coefficient2 = find_coefficient2()
    max_value2 = find_max_value2()
    user_name_new = find_new_user_name()
    date = find_date_bet()
    display_name = find_display_name()
    coefficient = find_coefficient()
    max_value = find_max_value()
    bets_db_dict = {
        'date_id': [dt.datetime.now()],
        'Sport': [sport],
        'Country': [country],
        'League': [league],
        'Match_name': [match_name],
        'Match_date': [match_date],
        'User_bet_taking_from': [user_name],
        'Date_bet_taking_from': [date],
        'Bet_taking_from': [display_name],
        'Coefficient_taking_from': [coefficient],
        'Max_value_taking_from': [max_value],
        'Link_taking_from': [link],
        'User_bet': [user_name_new],
        'Date_bet': [date2],
        'Bet': [display_name2],
        'Coefficient': [coefficient2],
        'Max_value': [max_value2],
        'Link': [link2],
    }
    return bets_db_dict


def make_bets_csv():
    bets_db = make_dict_bets()
    path = './bets_csv.csv'
    bets = pd.DataFrame(bets_db)
    bets.to_csv(path, mode='a', header=False, index=False)
    print('Your csv file has been updated')


make_bets_csv()




