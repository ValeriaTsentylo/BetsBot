import requests
from parser.config import headers
from config import url_league, url_event, url_odds
from data_for_bet import find_name_league, find_country_league, find_name_event, find_display_name


def get_leagues(sport_id: int):  # function returns dict for league_id searching
    return requests.get(f'{url_league}{sport_id}/1/', headers=headers).json()


def get_league_id(leagues: list):    # function returns league_id
    for row in leagues:
        if row.get('country') == find_country_league() and row.get('name') == find_name_league():
            return row.get('id')


def get_events(sport_id: int, league_id: int):     # function returns dict for event_id searching
    return requests.get(f'{url_event}{sport_id}/{league_id}', headers=headers).json()


def get_event_id(events: list):    # function returns events_id
    teams = str(find_name_event()).split(' - ')  # split 2 teams
    team1 = str(teams[0])
    team2 = str(teams[1])
    for row in events:
        if row.get('team1') == team1 and row.get('team2') == team2:
            return row.get('id')


def get_odds(event_id: int):      # function returns dict for odd_id searching
    return requests.get(f'{url_odds}{event_id}', headers=headers).json()


def get_odds_id(odds: list):  # function returns odds_id
    for row in odds:
        if row.get('displayName') == find_display_name():
            return row.get('id')


def topic_id(bet: dict):    # function returns topic_id
    return bet['topicAddon']['topicId']


