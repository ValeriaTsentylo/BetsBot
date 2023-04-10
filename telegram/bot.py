import imaplib
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from telegram.config import token, path_user_id, path_excel, path_data_for_header, path_mail
from parser.config import path_bets_csv
from aiogram.dispatcher import FSMContext
from telegram.states import DatePeriod, DataHeaders, LoginMail


bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])    # starts bot, save user_id to cvs, displays buttons
async def start(message):
    user_id = message.from_user.id
    users_id = {
        'user_id': [user_id]
    }
    data = pd.DataFrame(users_id)
    data.to_csv(path_user_id, mode='a', header=False, index=False)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Change data for request')
    button2 = types.KeyboardButton('Change login to mail')
    button3 = types.KeyboardButton('Get bets DB')
    button4 = types.KeyboardButton('/help')
    markup.row(button1, button2)
    markup.row(button3, button4)

    await bot.send_message(message.chat.id, 'Welcome to Bets bot', reply_markup=markup)
    await bot.send_message(message.chat.id, 'Choose your option:', reply_markup=markup)


@dp.message_handler(commands=['help'])
async def need_help(message):
    await bot.send_message(message.chat.id, 'If something goes wrong with the bot or the bets, please contact the maintainer')


@dp.message_handler(content_types=['text'])
async def login_to_mail(message):
    if message.text == 'Change login to mail':
        await bot.send_message(message.chat.id, 'Please put your login to mail below:', reply_markup=types.ReplyKeyboardRemove())
        await LoginMail.login.set()
    elif message.text == 'Change data for request':
        await bot.send_message(message.chat.id, 'Please put your Cookies below:', reply_markup=types.ReplyKeyboardRemove())
        await DataHeaders.cookies.set()
    elif message.text == 'Get bets DB':
        await bot.send_message(message.chat.id, 'Please put start date below in format yyyy-mm-dd:', reply_markup=types.ReplyKeyboardRemove())
        await DatePeriod.start_date.set()


@dp.message_handler(state=LoginMail.login)
async def get_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Please put your password below")
    await LoginMail.next()


@dp.message_handler(state=LoginMail.password)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='question1_yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='No', callback_data='question1_no')
    keyboard.add(key_no)
    question = f'Your login is: {data["login"]} and \n ' \
               f'your password is: {data["password"]}?'
    await bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    await LoginMail.next()


@dp.message_handler(state=DataHeaders.cookies)
async def get_cookies(message: types.Message, state: FSMContext):
    await state.update_data(cookies=message.text)
    await message.answer("Please put your Content-Length param below")
    await DataHeaders.next()


@dp.message_handler(state=DataHeaders.content_length)
async def get_content_length(message: types.Message, state: FSMContext):
    await state.update_data(content_length=message.text)
    await message.answer("Please put your token param below")
    await DataHeaders.next()


@dp.message_handler(state=DataHeaders.token_req)
async def get_token_req(message: types.Message, state: FSMContext):
    await state.update_data(token_req=message.text)
    data = await state.get_data()
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='question2_yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='No', callback_data='question2_no')
    keyboard.add(key_no)
    question = f'Your cookies is: {data["cookies"]}, \n ' \
               f'your content_length is: {data["content_length"]}\n' \
               f'your token is {data["token_req"]}?'
    await bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    await DataHeaders.next()


@dp.message_handler(state=DatePeriod.start_date)
async def get_start_date(message: types.Message, state: FSMContext):
    await state.update_data(start_date=message.text)
    await message.answer('Please put end date below in format yyyy-mm-dd:')
    await DatePeriod.next()


@dp.message_handler(state=DatePeriod.end_date)
async def get_end_date(message: types.Message, state: FSMContext):
    await state.update_data(end_date=message.text)
    data = await state.get_data()
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Yes', callback_data='question3_yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='No', callback_data='question3_no')
    keyboard.add(key_no)
    question = f'Do you need information about bets from {data["start_date"]} to {data["end_date"]} period?'
    await bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    await DatePeriod.next()


@dp.callback_query_handler(lambda call: call.data.startswith('question2'), state=DataHeaders.calltest)
async def callback_worker_1(call, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    if call.data.endswith('yes'):
        if len(data['cookies']) == 189 and len(data['content_length']) == 3 and len(data['token_req']) == 36:
            await bot.send_message(call.message.chat.id, 'Your data has been updated')
            new_cookies = data['cookies']
            new_content_length = data['content_length']
            new_token = data['token_req']
            dict_data = {
                'Cookie': [new_cookies],
                'Content-Length': [new_content_length],
                'X-CSRF-TOKEN': [new_token],
            }
            data = pd.DataFrame(dict_data)
            data.to_csv(path_data_for_header, mode='a', header=False, index=False)
        else:
            await bot.send_message(call.message.chat.id, 'There is a mistake in your data. Please, try again!')
            await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
    elif call.data.endswith('no'):
        await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
    await state.reset_state()


@dp.callback_query_handler(lambda call: call.data.startswith('question3'), state=DatePeriod.calltest)
async def callback_worker_1(call, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    if call.data.endswith('yes'):
        df = pd.read_csv(path_bets_csv, sep=",")
        file = df.loc[(df['date_id'] >= data['start_date']) & (df['date_id'] <= data['end_date'] + ' 23:59:59')]
        file.to_excel(path_excel, header=True)
        await bot.send_message(call.message.chat.id, 'Here if your file with data for the period')
        f = open(path_excel, "rb")
        await bot.send_document(call.message.chat.id, f)
        await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
    elif call.data.endswith('no'):
        await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
    await state.reset_state()


@dp.callback_query_handler(lambda call: call.data.startswith('question1'), state=LoginMail.calltest)
async def callback_worker_1(call, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    if call.data.endswith('yes'):
        imap_server = "imap.example.com"
        try:
            port = 993
            imap = imaplib.IMAP4_SSL(imap_server, port)
            sts, res = imap.login(data['login'], data['password'])
            if sts == "OK":
                await bot.send_message(call.message.chat.id, 'Your data has been updated')
                new_login = data['login']
                new_password = data['password']
                dict_data = {
                    'USERNAME1': [new_login],
                    'MAIL_PASS1': [new_password],
                }
                await bot.send_message(call.message.chat.id, f'New login is: {new_login} and \n'
                                                             f'new password is: {new_password}')
                data = pd.DataFrame(dict_data)
                data.to_csv(path_mail, mode='a', header=False, index=False)
        except Exception as exp:
            await bot.send_message(call.message.chat.id, f'{exp}')
            await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
    elif call.data.endswith('no'):
        await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
    await state.reset_state()
