import asyncio

import aiohttp
import requests
from aiogram import Bot

from parser.config import url_bet, url_odd
from parser.data_for_bet import find_sport_name, find_name_event, find_display_name
from parser.dict import get_leagues, get_events, get_odds, get_league_id, get_event_id, get_odds_id, get_sports
from program_state import GLOBAL_STATE


async def make_bet(link: str, html_text: str, bot: Bot):
    # bookmakers = get_bookmakers()
    sports = await get_sports()
    print('sports done')
    name_sport = find_sport_name(html_text)
    if name_sport is None:
        return {'topicAddon': {'topicId': 'Could not find sport name or bet is forbidden'}}
    print('name_sport done')
    sport_id = sports.get(name_sport)  # get sport_id from sports
    print('sport_id done')
    leagues = await get_leagues(sport_id)
    print('leagues done')
    league_id = get_league_id(leagues, html_text)
    if league_id is None:
        return {'topicAddon': {'topicId': 'Could not find league_id'}}
    print('league_id done')
    name_event = find_name_event(html_text)
    print('name_event done')
    events = await get_events(sport_id, league_id)
    print('events done')
    event_id = get_event_id(events, html_text)
    if event_id is None:
        return {'topicAddon': {'topicId': 'Event is outdated'}}

    print('event_id done')
    odds = await get_odds(event_id)
    print('odds done')
    odds_id = get_odds_id(odds, html_text)
    print('odds_id done')
    display_name = find_display_name(html_text)
    print('display_name done')

    json = {
        "id": None,
        "blog": {"id": GLOBAL_STATE.BLOG_ID},
        "title": str(name_event),
        "content": "",
        "price": 0,
        "publish": True,
        "closeComment": False,
        "bet": {
            "bookmakerId": GLOBAL_STATE.BOOKMAKER_ID,
            "sportId": int(str(sport_id)) if sport_id else None,
            "leagueId": int(str(league_id)) if league_id else None,
            "eventId": int(str(event_id)) if event_id else None,
            "oddId": int(str(odds_id)) if odds_id else None,
            "value": 0,
            "isHidden": False,
            "analytic": False,
            "displayName": str(display_name),
            "selectedRecords": [],
            "wantStakeAmount": GLOBAL_STATE.STAKE_AMOUNT,
        },
        "mediaIds": [],
        "confirmBet": False,
        "pinn": False,
        "hardOpen": False
    }

    # odds_info = requests.get(f'{url_odd}{odds_id}', headers=GLOBAL_STATE.HEADERS)
    # odds_info_json = odds_info.json()
    async with aiohttp.ClientSession(headers=GLOBAL_STATE.HEADERS) as session:
        async with session.get(f'{url_odd}{odds_id}') as odds_info:
            odds_info_json = await odds_info.json()

    if 'maxValue' in odds_info_json:
        json['bet']['maxValue'] = odds_info_json['maxValue']
    if 'coefficient' in odds_info_json:
        json['bet']['coefficient'] = odds_info_json['coefficient']
    print('odds_info done', odds_info_json)
    print('next bet', json)
    bet = requests.post(url_bet, json=json, headers=GLOBAL_STATE.HEADERS_FOR_POST)
    print(bet.status_code)
    bet_json = bet.json()
    bet_status = bet.status_code
    bet_text = bet.text
    print('bet done', bet_status, bet_json)
    # async with aiohttp.ClientSession(headers=GLOBAL_STATE.HEADERS_FOR_POST) as session:
    #     async with session.post(url_bet, json=json) as bet:
    #         print(bet.status)
    #         bet_json = await bet.json()
    #         bet_status = bet.status
    #         bet_text = await bet.text()
    #         print('bet done', bet_status, bet_json)

    tries = 0
    while bet_status == 500:
        await asyncio.sleep(3)
        bet = requests.post(url_bet, json=json, headers=GLOBAL_STATE.HEADERS_FOR_POST)
        bet_json = bet.json()
        bet_status = bet.status_code
        bet_text = bet.text
        print(f'bet try {tries}', bet_status, bet_json)
        # async with aiohttp.ClientSession(headers=GLOBAL_STATE.HEADERS_FOR_POST) as session:
        #     async with session.post(url_bet, json=json) as bet:
        #         bet_json = await bet.json()
        #         bet_status = bet.status
        #         bet_text = await bet.text()
        #         print(f'bet try {tries}', bet_status, bet_json)
        tries += 1
        if tries > 10:
            await bot.send_message(
                chat_id=GLOBAL_STATE.USER_TELEGRAM_ID,
                text=f'Unprocessed link (with status code {bet_status}): {link}'
            )
            return {'topicAddon': {'topicId': 'Could not make a bet because of internal server error'}}

    if bet_status == 400:
        if bet_json['message'] == 'Ставка на этот матч уже размещена в выбраном блоге':
            return {'topicAddon': {'topicId': 'Ставка на этот матч уже размещена в выбранном блоге'}}
        elif bet_json['message'] == 'Проверьте введенные данные':
            await bot.send_message(
                chat_id=GLOBAL_STATE.USER_TELEGRAM_ID,
                text=f'Unprocessed link (with status code {bet_status}): {link}'
            )
            return {'topicAddon': {'topicId': 'Подписка на блог не активна'}}
        else:
            await bot.send_message(
                chat_id=GLOBAL_STATE.USER_TELEGRAM_ID,
                text=f'Unprocessed link (<b>UNKNOWN ERROR</b>!) '
                     f'(with status code {bet_status} '
                     f'and msg "{bet_text}"): {link}',
                parse_mode='HTML'
            )
            raise Exception(f'Error {bet_status}: {bet_text}')

    if bet_status == 403:
        GLOBAL_STATE.HEADERS_ARE_BROKEN = True
        await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text=f'Authorization expired. Please, relogin.')
        raise Exception(f'Error {bet_status}: {bet_text}')

    return bet_json
