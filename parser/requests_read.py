import requests
from parser.config import url_league, url_sport, url_event, url_bet, url_odds, url_odd, headers, headers_for_post
from dict import sport_id, league_id, event_id, odds_id
from data import name_event, coefficient, MaxValue, displayName
json = {"id": None, "blog": {"id": 19994}, "title": str(name_event), "content": "", "price": 0,
        "publish": True, "closeComment": False,
        "bet": {"bookmakerId": 1, "sportId": str(sport_id), "leagueId": str(league_id), "eventId": str(event_id),
                "oddId": str(odds_id), "value": 0, "isHidden": False, "coefficient": str(coefficient),
                "analytic": False, "maxValue": str(MaxValue), "displayName": str(displayName), "selectedRecords": [],
                "wantStakeAmount": 0}, "mediaIds": [], "confirmBet": False, "pinn": False, "hardOpen": False}

sport_choose = requests.get(url_sport + str(sport_id), headers=headers)
league_choose = requests.get(url_league + str(sport_id) + str('/1'), headers=headers)
event_choose = requests.get(url_event + str(sport_id) + '/' + str(league_id), headers=headers)
odds_choose = requests.get(url_odds + str(event_id))
odd_choose = requests.get(url_odd + str(odds_id))
bet = requests.post(url_bet, json=json, headers=headers_for_post)
print(sport_choose.status_code)
print(league_choose.status_code)
print(event_choose.status_code)
print(odds_choose.status_code)
print(odd_choose.status_code)
print(bet.status_code)
print(bet.text)
