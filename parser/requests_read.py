import requests
from telegram.config import user_id
from parser.config import url_league, url_sport, url_event, url_bet, url_odds, url_odd, headers, headers_for_post
from parser.dict import get_leagues, get_events, get_odds, get_league_id, get_event_id, get_odds_id
from parser.data_for_bet import find_sport_name, find_name_event, find_max_value, find_coefficient, find_display_name


async def make_bet(link, bot):
        sports = {  # dict with sport_id
                "Football": 1,
                "Tennis": 2,
                "Basketball": 3,
                "Baseball": 4,
                "E Sports": 18,
                "American Football": 21,
                "Hockey": 25,
                }
        name_sport = find_sport_name(link)
        sport_id = sports.get(name_sport)  # get sport_id from sports
        leagues = get_leagues(sport_id)
        league_id = get_league_id(leagues, link)
        name_event = find_name_event(link)
        events = get_events(sport_id, league_id)
        event_id = get_event_id(events, link)
        odds = get_odds(event_id)
        odds_id = get_odds_id(odds, link)
        display_name = find_display_name(link)
        coefficient = find_coefficient(link)
        max_value = find_max_value(link)

        json = {"id": None, "blog": {"id": 19994}, "title": str(name_event), "content": "", "price": 0,
                "publish": True, "closeComment": False,
                "bet": {"bookmakerId": 1, "sportId": str(sport_id), "leagueId": str(league_id),
                        "eventId": str(event_id), "oddId": str(odds_id), "value": 0, "isHidden": False,
                        "coefficient": str(coefficient),
                        "analytic": False,
                        # "maxValue": str(max_value),
                        "displayName": str(display_name),
                        "selectedRecords": [], "wantStakeAmount": 0}, "mediaIds": [], "confirmBet": False,
                "pinn": False, "hardOpen": False}

        requests.get(f'{url_sport}{sport_id}', headers=headers)
        requests.get(f'{url_league}{sport_id}/1', headers=headers)
        requests.get(f'{url_event}{sport_id}/{league_id}', headers=headers)
        requests.get(f'{url_odds}{event_id}', headers=headers)
        requests.get(f'{url_odd }{odds_id}', headers=headers)
        bet = requests.post(url_bet, json=json, headers=headers_for_post)
        if bet.status_code == 400:
                await bot.send_message(chat_id=user_id, text=f'{bet.status_code}')
                await bot.send_message(chat_id=user_id, text=f'{bet.text}')
        return bet.json()






