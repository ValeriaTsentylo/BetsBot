import datetime as dt
import re
from typing import Union

import pandas as pd

from parser.config import path_bets_csv
from parser.data_for_bet import find_sport_name, find_name_event, find_name_league, find_country_league, \
    find_user_name, find_coefficient, find_display_name, find_max_value, find_date_bet
from parser.data_for_db import find_display_name2, find_coefficient2, find_max_value2, find_date_bet2, \
    find_date_match, find_new_user_name
from program_state import GLOBAL_STATE


def make_dict_bets(
        html_text: str,
        html_text2: Union[str, None],
        link: str,
        link2: Union[str, None],
        error_msg: Union[str, None]
):
    user_name = find_user_name(html_text)
    sport = find_sport_name(html_text)
    match_name = find_name_event(html_text)
    match_date = str(find_date_match(html_text))
    league = find_name_league(html_text)
    country = find_country_league(html_text)
    date2 = find_date_bet2(html_text)
    display_name2 = find_display_name2(html_text2)
    coefficient2 = find_coefficient2(html_text2)
    max_value2 = find_max_value2(html_text2)
    user_name_new = find_new_user_name(html_text)
    date_bet_taking_from = find_date_bet(html_text)
    display_name = find_display_name(html_text)
    coefficient = find_coefficient(html_text)
    max_value = find_max_value(html_text)

    try:
        match_month = re.sub(r'\s.+', '', match_date.split('.')[1])
        match_day = match_date.split('.')[0]
        match_time = match_date.split(' ')[1]
        match_year = dt.datetime.strptime(date_bet_taking_from, '%d.%m.%Y %H:%M').year
        match_date = f'{match_day}.{match_month}.{match_year} {match_time}'
    except:
        pass

    bets_db_dict = {
        'date_id': [dt.datetime.now()],
        'Sport': [sport],
        'Country': [country],
        'League': [league],
        'Match_name': [match_name],
        'Match_date': [match_date],
        'User_bet_taking_from': [user_name],
        'Date_bet_taking_from': [date_bet_taking_from],
        'Bet_taking_from': [display_name],
        'Coefficient_taking_from': [coefficient],
        'Max_value_taking_from': [max_value],
        'Link_taking_from': [link],
        'User_bet': [user_name_new],
        'Date_bet': [date2],
        'Bet': [display_name2],
        'Coefficient': [coefficient2],
        'Max_value': [max_value2],
        'Link': [link2 or error_msg or 'unknown error'],
        'Stake_amount': GLOBAL_STATE.STAKE_AMOUNT,
        'Result': None,
    }
    return bets_db_dict


def make_bets_csv(
        html_text: str,
        html_text2: Union[str, None],
        link: str,
        link2: Union[str, None],
        error_msg: Union[str, None]
):
    bets_db = make_dict_bets(html_text, html_text2, link, link2, error_msg)
    bets = pd.DataFrame(bets_db)
    bets.to_csv(path_bets_csv, mode='a', header=False, index=False)




