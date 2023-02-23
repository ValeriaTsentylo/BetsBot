import requests
from parser.config import headers
from config import url_league, url_event, url_odds
from data import name_sport, name_league, league_country, team1, team2, displayName

sports = {  # dict with sport_id
    "Football": 1,
    "Tennis": 2,
    "Basketball": 3,
    "Baseball": 4,
    "E Sports": 18,
    "American Football": 21,
    "Hockey": 25,
}

sport_id = sports.get(name_sport)   # get sport_id from sports


def get_leagues():    # function returns dict for league_id searching
    return requests.get(url_league + str(sport_id) + '/1/', headers=headers).json()


leagues = get_leagues()    # dict with id_league


def get_league_id():    # function returns league_id
    for row in leagues:
        if row.get('country') == league_country and row.get('name') == name_league:
            return row.get('id')


league_id = get_league_id()


def get_events():     # function returns dict for event_id searching
    return requests.get(url_event + str(sport_id) + '/' + str(league_id), headers=headers).json()


events = get_events()


def get_event_id():    # function returns events_id
    for row in events:
        if row.get('team1') == team1 and row.get('team2') == team2:
            return row.get('id')


event_id = get_event_id()


def get_odds_dict():      # function returns dict for odd_id searching
    return requests.get(url_odds + str(event_id), headers=headers).json()


odds = get_odds_dict()


def get_odds_id():  # function returns odds_id
    for row in odds:
        if row.get('displayName') == str(displayName):
            return row.get('id')


odds_id = get_odds_id()
