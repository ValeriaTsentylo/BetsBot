import imaplib
import traceback
from datetime import datetime

import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup

from parser.config import path_bets_csv
from program_state import GLOBAL_STATE
from telegram.config import token, path_user_id, path_excel, path_data_for_header, path_mail
from telegram.states import DatePeriod, DataHeaders, LoginMail, AccountSetup

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

BASIC_MARKUP = ReplyKeyboardMarkup(resize_keyboard=True)
BASIC_MARKUP.row(
    types.KeyboardButton('Change headers data'),
    types.KeyboardButton('Change e-mail data'),
    types.KeyboardButton('Change account data')
)
BASIC_MARKUP.row(types.KeyboardButton('Get bets DB'), types.KeyboardButton('/commands'))


@dp.message_handler(commands=['start'])    # starts bot, save user_id to cvs, displays buttons
async def start(message):
    user_id = message.from_user.id
    GLOBAL_STATE.USER_TELEGRAM_ID = user_id
    # markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # button1 = types.KeyboardButton('Change headers data')
    # button2 = types.KeyboardButton('Change e-mail data')
    # button3 = types.KeyboardButton('Get bets DB')
    # button4 = types.KeyboardButton('/help')
    # markup.row(button1, button2)
    # markup.row(button3, button4)

    await bot.send_message(
        message.chat.id,
        'Welcome to Bets bot, type /commands to see all available commands or choose your option:',
        reply_markup=BASIC_MARKUP
    )
    # await bot.send_message(message.chat.id, 'Choose your option:', reply_markup=BASIC_MARKUP)


@dp.message_handler(commands=['help'])
async def need_help(message):
    await bot.send_message(message.chat.id, 'If something goes wrong with the bot or the bets, please contact the maintainer')


@dp.message_handler(commands=['pause'])
async def need_help(message):
    GLOBAL_STATE.PAUSE = True
    await bot.send_message(message.chat.id, 'Program will be paused starting with the next cycle of e-mail checking')


@dp.message_handler(commands=['unpause'])
async def need_help(message):
    GLOBAL_STATE.PAUSE = False
    await bot.send_message(message.chat.id, 'Program soon will be resumed')


@dp.message_handler(commands=['commands'])
async def need_help(message):
    commands_with_description = {
        '/start': 'Starts communication with bot',
        '/help': 'Get some help',
        '/pause': 'Program will be paused starting with the next cycle of e-mail checking',
        '/unpause': 'Program soon will be resumed',
        '/commands': 'Displays all commands',
    }
    commands = 'List of commands:\n' + '\n'.join(
        [f'{key}: {value}' for key, value in commands_with_description.items()]
    )
    await bot.send_message(message.chat.id, commands)


@dp.message_handler(content_types=['text'])
async def login_to_mail(message):
    if message.text == 'Change e-mail data':
        await bot.send_message(message.chat.id, 'Please put your login to mail below:', reply_markup=types.ReplyKeyboardRemove())
        await LoginMail.login.set()
    elif message.text == 'Change headers data':
        await bot.send_message(message.chat.id, 'Please put your Cookies below:', reply_markup=types.ReplyKeyboardRemove())
        await DataHeaders.cookies.set()
    elif message.text == 'Get bets DB':
        await bot.send_message(message.chat.id, 'Please put start date below in format yyyy-mm-dd:', reply_markup=types.ReplyKeyboardRemove())
        await DatePeriod.start_date.set()
    elif message.text == 'Change account data':
        await bot.send_message(message.chat.id, f'Please put blog id below (or "skip" to left the {GLOBAL_STATE.BLOG_ID}):', reply_markup=types.ReplyKeyboardRemove())
        await AccountSetup.blog_id.set()


@dp.message_handler(state=LoginMail.login)
async def get_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Please put your password below")
    await LoginMail.next()


@dp.message_handler(state=LoginMail.password)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    # data = await state.get_data()
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Confirm', callback_data='question1_yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Cancel', callback_data='question1_no')
    keyboard.add(key_no)
    question = f'Confirm your data, please'
    await bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)
    await LoginMail.next()


@dp.message_handler(state=AccountSetup.blog_id)
async def get_blog_id(message: types.Message, state: FSMContext):
    if message.text == 'skip':
        await state.update_data(blog_id=GLOBAL_STATE.BLOG_ID)
    else:
        try:
            blog_id = int(message.text)
            if blog_id <= 0:
                raise ValueError
            await state.update_data(blog_id=blog_id)
        except ValueError:
            await message.answer(f"Blog id must be a positive integer, please try again")
            return
    await message.answer(f"Please put desirable stake amount below or 'skip' to left the {GLOBAL_STATE.STAKE_AMOUNT}")
    await AccountSetup.next()


@dp.message_handler(state=AccountSetup.stake_amount)
async def get_stake_amount(message: types.Message, state: FSMContext):
    if message.text == 'skip':
        await state.update_data(stake_amount=GLOBAL_STATE.STAKE_AMOUNT)
    else:
        try:
            stake_amount = float(message.text)
            if stake_amount < 0:
                raise ValueError
            await state.update_data(stake_amount=stake_amount)
        except ValueError:
            await message.answer(f"Stake amount must be a positive number, please try again")
            return
    await message.answer(
        f"Please put desirable waiting time for new e-mail checks below "
        f"or 'skip' to left the {GLOBAL_STATE.WAITING_TIME} seconds"
    )
    await AccountSetup.next()


@dp.message_handler(state=AccountSetup.waiting_time)
async def get_waiting_time(message: types.Message, state: FSMContext):
    if message.text == 'skip':
        await state.update_data(waiting_time=GLOBAL_STATE.WAITING_TIME)
    else:
        try:
            waiting_time = int(message.text)
            if waiting_time <= 0:
                raise ValueError
            await state.update_data(waiting_time=waiting_time)
        except ValueError:
            await message.answer(f"Waiting time must be a positive integer, please try again")
            return

    data = await state.get_data()
    GLOBAL_STATE.BLOG_ID = data['blog_id']
    GLOBAL_STATE.STAKE_AMOUNT = data['stake_amount']
    GLOBAL_STATE.WAITING_TIME = data['waiting_time']

    pd.DataFrame({
        'user_id': [GLOBAL_STATE.USER_TELEGRAM_ID],
        'telegram_name': [message.from_user.username],
        'time_now': [datetime.today()],
        'blog_id': [GLOBAL_STATE.BLOG_ID],
        'waiting_time': [GLOBAL_STATE.WAITING_TIME],
        'stake_amount': [GLOBAL_STATE.STAKE_AMOUNT],
    }).to_csv(path_user_id, mode='a', header=False, index=False, sep=',')

    await message.answer("Data successfully updated")
    await state.reset_state()


@dp.message_handler(state=DataHeaders.cookies)
async def get_cookies(message: types.Message, state: FSMContext):
    await state.update_data(cookies=message.text)
    await message.answer("Please put your Content-Length param below")
    await DataHeaders.next()


@dp.message_handler(state=DataHeaders.content_length)
async def get_content_length(message: types.Message, state: FSMContext):
    await state.update_data(content_length=message.text)
    await message.answer("Please put your X_CSRF_TOKEN param below")
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
    question = f'Your Cookies is: {data["cookies"]}\n ' \
               f'your Content-Length is: {data["content_length"]}\n' \
               f'your X_CSRF_TOKEN is {data["token_req"]}'
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
        try:
            new_cookies = data['cookies']
            new_content_length = data['content_length']
            new_token = data['token_req']
            GLOBAL_STATE.headers_post_check(new_cookies, new_content_length, new_token)
            if GLOBAL_STATE.HEADERS_ARE_BROKEN:
                raise Exception('Headers are not working')
        except Exception as exp:
            await bot.send_message(
                call.message.chat.id,
                f'Inserted data did not work with the error "{exp}". Please, try again!',
                reply_markup=BASIC_MARKUP
            )
            await state.reset_state()
            return
            # await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
        else:
            GLOBAL_STATE.update_headers(new_cookies, new_content_length, new_token)
            dict_data = {
                'Cookie': [new_cookies],
                'Content-Length': [new_content_length],
                'X-CSRF-TOKEN': [new_token],
            }
            data = pd.DataFrame(dict_data)
            data.to_csv(path_data_for_header, mode='w', header=False, index=False)

        # if len(data['cookies']) == 189 and len(data['token_req']) == 36:
        #     await bot.send_message(call.message.chat.id, 'Your data has been updated')
        #     new_cookies = data['cookies']
        #     new_content_length = data['content_length']
        #     new_token = data['token_req']
        #     dict_data = {
        #         'Cookie': [new_cookies],
        #         'Content-Length': [new_content_length],
        #         'X-CSRF-TOKEN': [new_token],
        #     }
        #     data = pd.DataFrame(dict_data)
        #     data.to_csv(path_data_for_header, mode='a', header=False, index=False)
        # else:
        #     await bot.send_message(call.message.chat.id, 'There is a mistake in your data. Please, try again!')
        #     await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
    elif call.data.endswith('no'):
        await bot.send_message(call.message.chat.id, 'Choose your option', reply_markup=BASIC_MARKUP)
    await state.reset_state()


@dp.callback_query_handler(lambda call: call.data.startswith('question3'), state=DatePeriod.calltest)
async def callback_worker_1(call, state: FSMContext):
    data = await state.get_data()
    await call.answer()
    if call.data.endswith('yes'):
        df = pd.read_csv(path_bets_csv, sep=",")
        file = df.loc[(df['date_id'] >= data['start_date']) & (df['date_id'] <= data['end_date'] + ' 23:59:59')]
        file.to_excel(path_excel, header=True)
        await bot.send_message(call.message.chat.id, 'Here is your file with data for the period')
        f = open(path_excel, "rb")
        await bot.send_document(call.message.chat.id, f)
        # await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
        await bot.send_message(call.message.chat.id, 'Choose your option', reply_markup=BASIC_MARKUP)
    elif call.data.endswith('no'):
        # await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
        await bot.send_message(call.message.chat.id, 'Choose your option', reply_markup=BASIC_MARKUP)
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
            traceback.print_exc()
            await bot.send_message(call.message.chat.id, f'bot:193 {exp}')
            # await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
            await bot.send_message(call.message.chat.id, 'Choose your option', reply_markup=BASIC_MARKUP)
    elif call.data.endswith('no'):
        # await bot.send_message(call.message.chat.id, 'To continue working with the bot press /start')
        await bot.send_message(call.message.chat.id, 'Choose your option', reply_markup=BASIC_MARKUP)
    await state.reset_state()
