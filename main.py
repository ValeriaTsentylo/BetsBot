from time import sleep
from datetime import datetime as dt
from mails.get_new_emails import get_new_emails
import telebot
from telegram.config import token, user_id

bot = telebot.TeleBot(token)

while True:
    bot.send_message(chat_id=user_id, text='The program has been started')

    def email_checker():    # read new emails and add links to the global new_topics
        bot.send_message(chat_id=user_id, text=f'kindly checking new emails at {dt.today()}')
        global new_topics
        new_topics = []
        try:
            new_topics.append(get_new_emails())
        except Exception as exp:
            bot.send_message(chat_id=user_id, text=f'{exp}')
        return (new_topics)

    if len(email_checker()) == 0:
        bot.send_message(chat_id=user_id, text='There is not new emails')
        sleep(360)
    else:
        def make_link():  #  найти ссылку в новой переменной, заюзать для ставки  и удалить ее из глобальной переменной
            try:
                for i in new_topics:
                    link = i
                    return link
            except Exception as exp:
                bot.send_message(chat_id=user_id, text=f'{exp}')

    bot.polling(none_stop=True, interval=0)


