import traceback
from typing import Union, List, Dict

import aiohttp
from parser.config import url_league, url_event, url_odds, url_sport, url_bookmaker
from parser.data_for_bet import find_name_league, find_country_league, find_name_event, find_display_name
from program_state import GLOBAL_STATE


async def get_bookmakers() -> dict[str, int]:  # function returns dict for bookmaker_id searching
    async with aiohttp.ClientSession() as session:
        async with session.get(url_bookmaker, headers=GLOBAL_STATE.HEADERS) as resp:
            bookmakers = await resp.json()
    # bookmakers = requests.get(url_bookmaker, headers=GLOBAL_STATE.HEADERS).json()
    return {
        bookmaker.get('name'): bookmaker.get('id')
        for bookmaker in bookmakers
    }


async def get_sports() -> dict[str, int]:  # function returns dict for sport_id searching
    # sports = requests.get(url_sport, headers=GLOBAL_STATE.HEADERS).json()
    async with aiohttp.ClientSession() as session:
        async with session.get(url_sport, headers=GLOBAL_STATE.HEADERS) as resp:
            sports = await resp.json()
    return {
        sport.get('name'): sport.get('id')
        for sport in sports
    }


async def get_leagues(sport_id: int) -> List[Dict]:  # function returns dict for league_id searching
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{url_league}{sport_id}/1/', headers=GLOBAL_STATE.HEADERS) as resp:
            return await resp.json()
    # return requests.get(f'{url_league}{sport_id}/1/', headers=GLOBAL_STATE.HEADERS).json()


def get_league_id(leagues: list, html_text: str) -> int:    # function returns league_id
    country_name = find_country_league(html_text)
    league_name = find_name_league(html_text)
    for row in leagues:
        if row.get('country') == country_name and row.get('name') == league_name:
            return row.get('id')


async def get_events(sport_id: int, league_id: int) -> List[Dict]:     # function returns dict for event_id searching
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url_event}{sport_id}/{league_id}', headers=GLOBAL_STATE.HEADERS) as resp:
                return await resp.json()
        # return requests.get(f'{url_event}{sport_id}/{league_id}', headers=GLOBAL_STATE.HEADERS).json()
    except Exception as e:
        traceback.print_exc()
        return []


def get_event_id(events: list, html_text: str) -> Union[int, None]:    # function returns events_id
    try:
        teams = str(find_name_event(html_text)).split(' - ')  # split 2 teams
        team1 = str(teams[0])
        team2 = str(teams[1])

        for row in events:
            if row.get('team1') == team1 and row.get('team2') == team2:
                return row.get('id')
    except Exception as e:
        traceback.print_exc()
        return None


async def get_odds(event_id: int) -> List[Dict]:      # function returns dict for odd_id searching
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{url_odds}{event_id}', headers=GLOBAL_STATE.HEADERS) as resp:
                return await resp.json()
        # resp = requests.get(f'{url_odds}{event_id}', headers=GLOBAL_STATE.HEADERS)
        # return resp.json()
    except:
        traceback.print_exc()
        return []


def get_odds_id(odds: list, html_text: str) -> int:  # function returns odds_id
    for row in odds:
        if row.get('displayName') == find_display_name(html_text):
            return row.get('id')


def topic_id(bet: dict) -> Union[int, str, None]:    # function returns topic_id
    return bet['topicAddon']['topicId']


