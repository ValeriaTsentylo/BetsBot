import re
import traceback
from typing import Union

from bs4 import BeautifulSoup


def find_display_name2(html_text: Union[str, None]):    # function return displayName
    if html_text is None:
        return None
    try:
        # html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('span', class_='bet-type-title').next_element
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return ''


def find_coefficient2(html_text: Union[str, None]):     # function returns coefficient
    if html_text is None:
        return None
    try:
        # html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('span', class_='bet-type-k').next_element
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return None


def find_max_value2(html_text: Union[str, None]):   # function return MaxValue
    if html_text is None:
        return None
    try:
        # html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        values = soup.find_all('span', class_=None)
        return values[8].next_element
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return None


def find_date_bet2(html_text: Union[str, None]):
    if html_text is None:
        return None
    try:
        # html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        values = soup.find_all('span', class_=None)
        return values[9].next_element
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return None


def find_date_match(html_text: Union[str, None]):
    if html_text is None:
        return None
    try:
        # html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        values = soup.find('span', class_='bet-game-time').next_element
        return values
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return None


def find_new_user_name(html_text: Union[str, None]):
    if html_text is None:
        return None
    try:
        # html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('a', class_='mr-2').next_element
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return None


def find_result(html_text: str):
    if not html_text:
        return None
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        test = re.sub(r'\s*', '', soup.find('table').find_all('tr')[6].find_all('td')[0].text or '')
        print(test, test == 'Статус:')
        if test == 'Статус:':
            return None
        else:
            test2 = re.sub(r'\s*', '', soup.find('table').find_all('tr')[6].find_all('td')[1].text or '')
            print(test2)
            return test2
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return None
