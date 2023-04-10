from mails.get_new_emails import get_new_emails
from parser.bets_db import make_bets_csv
from parser.config import url_ex
from parser.dict import topic_id
from parser.requests_read import make_bet
from telegram.bot import bot, dp
from telegram.config import user_id
from aiogram.utils import executor
import asyncio


async def email_checker():  # read new emails and add links to the global new_topics
    new_topics = []
    try:
        new_topics.extend(get_new_emails())
    except Exception as exp:
        await bot.send_message(chat_id=user_id, text=f'{exp}')
    return new_topics


async def timed_messages_worker():
    await bot.send_message(chat_id=user_id, text='The program has been started')
    unprocessed_topics = []
    while True:
        unprocessed_topics.extend(await email_checker())
        if len(unprocessed_topics) == 0:
            await bot.send_message(chat_id=user_id, text='There is not new emails')
            await asyncio.sleep(360)
            continue
        for i, link in enumerate(unprocessed_topics.copy()):
            try:
                bet_dict = await make_bet(link, bot)
            except Exception as exp:
                print(exp)
                await bot.send_message(chat_id=user_id, text=f'{exp}')
                break
            link2 = f'{url_ex}{topic_id(bet_dict)}'
            try:
                await make_bets_csv(link, link2)
            except Exception as exp:
                await bot.send_message(chat_id=user_id, text=f'{exp}')
            unprocessed_topics.pop(i)
            await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        # asyncio.run(timed_messages_worker(loop=loop))
        task = loop.create_task(timed_messages_worker())
        executor.start_polling(dp)
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.stop()
        loop.close()
