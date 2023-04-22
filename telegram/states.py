from aiogram.dispatcher.filters.state import State, StatesGroup


class DataHeaders(StatesGroup):
    cookies = State()
    content_length = State()
    token_req = State()
    calltest = State()  # this state is for callback_query_handler


class LoginMail(StatesGroup):
    login = State()
    password = State()
    calltest = State()  # this state is for callback_query_handler


class DatePeriod(StatesGroup):
    date_period = State()
    calltest = State()  # this state is for callback_query_handler


class AccountSetup(StatesGroup):
    blog_id = State()
    stake_amount = State()
    waiting_time = State()
    calltest = State()  # this state is for callback_query_handler

