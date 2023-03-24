import telebot
import openpyxl
from config import token
from telebot import types
import imaplib
import pandas as pd


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup()
        button1 = types.KeyboardButton('Change data for request')
        button2 = types.KeyboardButton('Change login to mail')
        button3 = types.KeyboardButton('Get bets DB')
        button4 = types.KeyboardButton('/help')

        markup.row(button1, button2)
        markup.row(button3, button4)

        bot.send_message(message.chat.id, 'Welcome to Bets bot', reply_markup=markup)
        bot.send_message(message.chat.id, 'Choose your option:', reply_markup=markup)

    @bot.message_handler(commands=['help'])
    def need_help(message):
        bot.send_message(message.chat.id, 'If something goes wrong with the bot or the bets, please contact the maintainer')

    @bot.message_handler(content_types=['stop'])
    def stop(message):
        bot.send_message(message.chat.id, 'Thank you for using our bot!')
        bot.stop_polling()

    @bot.message_handler(content_types=['text'])
    def login_to_mail(message):
        if message.text == 'Change login to mail':
            bot.send_message(message.chat.id, 'Please put your login to mail below:')
            bot.register_next_step_handler(message, get_login)
        elif message.text == 'Change data for request':
            bot.send_message(message.chat.id, 'Please put your Cookies below:')
            bot.register_next_step_handler(message, get_cookies)
        elif message.text == 'Get bets DB':
            bot.send_message(message.chat.id, 'Please put start date below in format yyyy-mm-dd:')
            bot.register_next_step_handler(message, get_start_date)

    def get_login(message):
        global login
        login = message.text
        bot.send_message(message.from_user.id, 'Please put your password below')
        bot.register_next_step_handler(message, get_password)

    def get_password(message):
        global password
        password = message.text
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Yes', callback_data='question1_yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='No', callback_data='question1_no')
        keyboard.add(key_no)
        question = f'Your login is: {login} and your password is: {password}?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    def get_cookies(message):
        global cookies
        cookies = message.text
        bot.send_message(message.from_user.id, 'Please put your Content-Length param below')
        bot.register_next_step_handler(message, get_content_length)

    def get_content_length(message):
        global content_length
        content_length = message.text
        bot.send_message(message.from_user.id, 'Please put your token param below')
        bot.register_next_step_handler(message, get_token)

    def get_token(message):
        global token_req
        token_req = message.text
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Yes', callback_data='question2_yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='No', callback_data='question2_no')
        keyboard.add(key_no)
        question = f'Your cookies is: {cookies}, \n your content_length is: {content_length} \n your token is {token_req}?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    def get_start_date(message):
        global start_date
        start_date = message.text
        bot.send_message(message.from_user.id, 'Please put end date below in format yyyy-mm-dd:')
        bot.register_next_step_handler(message, get_end_date)

    def get_end_date(message):
        global end_date
        end_date = message.text
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Yes', callback_data='question3_yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='No', callback_data='question3_no')
        keyboard.add(key_no)
        question = f'Do you need information about bets from {start_date} to {end_date} period?'
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('question1'))
    def callback_worker(call):
        if call.data.endswith('yes'):
            username = login
            mail_pass = password
            imap_server = "imap.example.com"
            try:
                port = 993
                imap = imaplib.IMAP4_SSL(imap_server, port)
                sts, res = imap.login(username, mail_pass)
                if sts == "OK":
                    bot.send_message(call.message.chat.id, 'Your data has been updated')
                    new_login = login
                    new_password = password
                    dict_data = {
                        'USERNAME1': [new_login],
                        'MAIL_PASS1': [new_password],
                    }
                    bot.send_message(call.message.chat.id, f'New login is: {new_login} and new password is: {new_password}')
                    path = './login_to_mail.csv'
                    data = pd.DataFrame(dict_data)
                    data.to_csv(path, mode='a', header=False, index=False)
            except Exception as exp:
                bot.send_message(call.message.chat.id, f'{exp}')
        elif call.data.endswith('no'):
            bot.send_message(call.message.chat.id, 'Choose your option:')

    @bot.callback_query_handler(lambda call: call.data.startswith('question2'))
    def callback_worker_1(call):
        if call.data.endswith('yes'):
            if len(cookies) == 181 and len(content_length) == 3 and len(token_req) == 36:
                bot.send_message(call.message.chat.id, 'Your data has been updated')
                path = './infromation_for_header.csv'
                new_cookies = cookies
                new_content_length = content_length
                new_token = token_req
                dict_data = {
                    'Cookie': [new_cookies],
                    'Content-Length': [new_content_length],
                    'X-CSRF-TOKEN': [new_token],
                }
                path = './infromation_for_header.csv'
                data = pd.DataFrame(dict_data)
                data.to_csv(path, mode='a', header=False, index=False)
            else:
                bot.send_message(call.message.chat.id, 'There is a mistake in your data. Please, try again!')
        elif call.data.endswith('no'):
            bot.send_message(call.message.chat.id, 'Choose your option:')

    @bot.callback_query_handler(lambda call: call.data.startswith('question3'))
    def callback_worker_1(call):
        if call.data.endswith('yes'):
            path = './bets_csv.csv'
            df = pd.read_csv(path, sep=",")
            file = df.query(f"'{start_date}' <= date_id <= '{end_date}'")
            file.to_excel(r'./Bets_DB_Telegram.xlsx', header=True)
            bot.send_message(call.message.chat.id, 'Here if your file with data for the period')
            f = open("./Bets_DB_Telegram.xlsx", "rb")
            bot.send_document(call.message.chat.id, f)
        elif call.data.endswith('no'):
            bot.send_message(call.message.chat.id, 'Choose your option:')

    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    telegram_bot(token)
