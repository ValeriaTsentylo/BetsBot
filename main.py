import traceback
from datetime import datetime
from typing import List

import aiohttp
import pandas as pd

from mails.get_new_emails import get_new_emails
from parser.bets_db import make_bets_csv
from parser.config import url_ex, path_bets_csv
from parser.data_for_db import find_result
from parser.dict import topic_id
from parser.requests_read import make_bet
from program_state import GLOBAL_STATE
from telegram.bot import bot, dp
from aiogram.utils import executor
import asyncio


async def results_updater():
    print('update results started')
    all_data = pd.read_csv('bets_csv.csv', sep=',')
    no_result_data = all_data.loc[all_data['Result'].isna() & all_data['Link'].notna()]
    # iterate over all Links in no_result_data
    links: List[str] = [link for link in no_result_data['Link'].unique().tolist() if link.startswith('https://')]
    async with aiohttp.ClientSession() as session:
        for i, link in enumerate(links):
            print(f'update {i} of {len(links)}. {link}')
            try:
                async with session.get(link, headers=GLOBAL_STATE.HEADERS) as resp:
                    if resp.status != 200:
                        print(f'update {i} of {len(links)} failed. {link} {resp.status}')
                        continue
                    result = find_result(await resp.content.read())
                    all_data.loc[all_data['Link'] == link, 'Result'] = result
            except Exception as exp:
                traceback.print_exc()
                await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text=f'main:36 {exp}')

    print('saving update results')
    all_data.to_csv(path_bets_csv, index=False, sep=',', mode='w', header=True)
    print('update results finished')


async def email_checker() -> List[str]:  # read new emails and add links to the global new_topics
    new_topics: List[str] = []
    try:
        new_topics.extend(get_new_emails())
    except Exception as exp:
        traceback.print_exc()
        await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text=f'main:16 {exp}')
    return new_topics


async def timed_messages_worker():
    if GLOBAL_STATE.USER_TELEGRAM_ID is None:
        print('waiting for user to start')

    while GLOBAL_STATE.USER_TELEGRAM_ID is None:
        await asyncio.sleep(1)

    await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text='The program has been started')
    unprocessed_topics: List[str] = []
    while True:
        # ----------------- check if headers are working -----------------
        if GLOBAL_STATE.HEADERS_ARE_BROKEN:
            await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text='Headers are broken!')
            while GLOBAL_STATE.HEADERS_ARE_BROKEN:
                await asyncio.sleep(1)
            continue

        # ----------------- check if email data is set -----------------
        if not GLOBAL_STATE.EMAIL_DATA_IS_SET:
            await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text='Email data is not set!')
            while not GLOBAL_STATE.EMAIL_DATA_IS_SET:
                await asyncio.sleep(1)
            continue

        # ----------------- check if blog id is set -----------------
        if GLOBAL_STATE.BLOG_ID is None:
            await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text='Blog id is not set!')
            while GLOBAL_STATE.BLOG_ID is None:
                await asyncio.sleep(1)
            continue

        # ----------------- check if program is on pause -----------------
        if GLOBAL_STATE.PAUSE:
            await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text='The program is paused')
            while GLOBAL_STATE.PAUSE:
                await asyncio.sleep(1)
            continue

        if GLOBAL_STATE.UPDATE_RESULTS or datetime.today().hour == 14:
            await results_updater()
            GLOBAL_STATE.UPDATE_RESULTS = False

        print(f'while start: {len(unprocessed_topics)} unprocessed topics')
        try:
            unprocessed_topics.extend([
                link for link in await email_checker()
                if isinstance(link, str) and link.startswith('https://') and link not in unprocessed_topics
            ])
        except Exception as exp:
            traceback.print_exc()
            await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text=f'main:27 {exp}')
            continue

        if len(unprocessed_topics) == 0:
            # await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text='There are no new emails')
            await asyncio.sleep(GLOBAL_STATE.WAITING_TIME)
            continue

        print('new unprocessed topics length: ', len(unprocessed_topics))
        for i, link in enumerate(unprocessed_topics.copy()):
            try:
                print('link: ', link)
                async with aiohttp.ClientSession() as session:
                    async with session.get(link) as resp:
                        html_text = await resp.text()
                print('make_bet starts')
                bet_dict = await make_bet(link, html_text, bot)
            except Exception as exp:
                traceback.print_exc()
                # await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text=f'main:33 {exp}')
                unprocessed_topics.pop(unprocessed_topics.index(link))
                unprocessed_topics.append(link)
                print(f'link {i} was not processed: {link}; {len(unprocessed_topics)} unprocessed topics left')
                continue

            topic_id_link = topic_id(bet_dict)
            error_msg = None
            if isinstance(topic_id_link, str):
                error_msg = topic_id_link
                link2 = None
            else:
                link2 = f'{url_ex}{topic_id_link}' if topic_id_link else None

            try:
                print('link2: ', link2)
                html_text2 = None
                if link2:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(link2) as resp:
                            html_text2 = await resp.text()

                print('make_bets_csv starts')
                make_bets_csv(html_text, html_text2, link, link2, error_msg)
                print('make_bets_csv ends')
            except Exception as exp:
                traceback.print_exc()
                # await bot.send_message(chat_id=GLOBAL_STATE.USER_TELEGRAM_ID, text=f'main:40 {exp}')
                unprocessed_topics.pop(unprocessed_topics.index(link))
                unprocessed_topics.append(link)
                print(f'link {i} was not processed: {link}; {len(unprocessed_topics)} unprocessed topics left')
                continue

            unprocessed_topics.pop(unprocessed_topics.index(link))
            print(f'link {i} processed: {link}; {len(unprocessed_topics)} unprocessed topics left')
            await asyncio.sleep(GLOBAL_STATE.BET_WAITING_TIME)

        print(f'Unprocessed topics: {len(unprocessed_topics)}')
        await asyncio.sleep(GLOBAL_STATE.WAITING_TIME)
        print('while end')
    print('end of function timed_messages_worker()')


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        task = loop.create_task(timed_messages_worker())
        executor.start_polling(dp)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()
