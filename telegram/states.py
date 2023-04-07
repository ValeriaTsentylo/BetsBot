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
    start_date = State()
    end_date = State()
    calltest = State()  # this state is for callback_query_handler
