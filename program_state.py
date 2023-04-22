import csv

import pandas as pd
import requests

from mails.config import PATH_TO_EMAIL_DATA
from parser.config import url_bet
from telegram.config import path_data_for_header, path_user_id


class ProgramState:
    BET_WAITING_TIME = 3
    WAITING_TIME = 60
    USER_TELEGRAM_ID: int = None

    MAIL_USERNAME: str = None
    MAIL_PASS: str = None

    STAKE_AMOUNT: float = 0.0
    BOOKMAKER_ID: int = 1
    BLOG_ID: int = None

    COOKIES: str = ''
    CONTENT_LENGTH: str = ''
    X_CSRF_TOKEN: str = ''
    HEADERS: dict = {}
    HEADERS_FOR_POST: dict = {
        'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'uk-UA,uk;q=0.9,ru-UA;q=0.8,ru;q=0.7,en-US;q=0.6,en;q=0.5',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json; charset=UTF-8',
        'Host': 'expari.com',
        'Origin': 'https://expari.com',
        'Referer': 'https://expari.com/topic/create',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        ),
    }
    HEADERS_ARE_BROKEN: bool = False
    PAUSE: bool = False
    UPDATE_RESULTS: bool = False

    @property
    def EMAIL_DATA_IS_SET(self):
        return self.MAIL_USERNAME is not None and self.MAIL_PASS is not None

    def __init__(self):
        with open(path_data_for_header, 'r') as f:  # looking for param for headers for requests
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                self.HEADERS_ARE_BROKEN = True
                return

            last_row = rows[-1]
            self.COOKIES = str(last_row[0])
            self.CONTENT_LENGTH = str(last_row[1])
            self.X_CSRF_TOKEN = str(last_row[2])

            self.HEADERS = {'Cookie': self.COOKIES}
            self.HEADERS_FOR_POST['Cookie'] = self.COOKIES
            self.HEADERS_FOR_POST['Content-Length'] = self.CONTENT_LENGTH
            self.HEADERS_FOR_POST['X-CSRF-TOKEN'] = self.X_CSRF_TOKEN
            self.headers_post_check()

        with open(PATH_TO_EMAIL_DATA, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            last_row = rows[-1]
            self.MAIL_USERNAME = str(last_row[0])
            self.MAIL_PASS = str(last_row[1])

        user_data = pd.read_csv(path_user_id, sep=',')
        if not user_data.empty:
            user_data = user_data.sort_values(by=['time_now'], ascending=[True]).to_dict('records')[-1]
            self.USER_TELEGRAM_ID = user_data['user_id']
            self.BLOG_ID = user_data['blog_id']
            self.WAITING_TIME = user_data['waiting_time']
            self.STAKE_AMOUNT = user_data['stake_amount']

    def update_headers(self, cookies: str, content_length: str, x_csrf_token: str):
        self.COOKIES = cookies
        self.CONTENT_LENGTH = content_length
        self.X_CSRF_TOKEN = x_csrf_token
        self.HEADERS = {'Cookie': self.COOKIES}
        self.HEADERS_FOR_POST['Cookie'] = self.COOKIES
        self.HEADERS_FOR_POST['Content-Length'] = self.CONTENT_LENGTH
        self.HEADERS_FOR_POST['X-CSRF-TOKEN'] = self.X_CSRF_TOKEN

    def headers_post_check(self, new_cookies: str = None, new_content_length: str = None, new_token: str = None):
        test_headers = {
            **self.HEADERS_FOR_POST,
            'Cookie': new_cookies or self.COOKIES,
            'Content-Length': new_content_length or self.CONTENT_LENGTH,
            'X-CSRF-TOKEN': new_token or self.X_CSRF_TOKEN,
        }
        resp = requests.post(url_bet, json={}, headers=test_headers)
        if resp.status_code == 403:
            print(f'Headers are broken with response "{resp.json()}"')
            self.HEADERS_ARE_BROKEN = True


GLOBAL_STATE = ProgramState()

