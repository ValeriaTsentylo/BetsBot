import requests
from bs4 import BeautifulSoup
from requests_read import bet_dict
from dict import topic_id
from config import url_ex


link2 = f'{url_ex}{topic_id(bet_dict)}'  # new link
print(link2)


def find_display_name2():    # function return displayName
    try:
        html_text = requests.get(link2).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('span', class_='bet-type-title').next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_coefficient2():     # function returns coefficient
    try:
        html_text = requests.get(link2).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('span', class_='bet-type-k').next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_max_value2():   # function return MaxValue
    try:
        html_text = requests.get(link2).text
        soup = BeautifulSoup(html_text, 'html.parser')
        values = soup.find_all('span', class_=None)
        return values[8].next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_date_bet2():
    try:
        html_text = requests.get(link2).text
        soup = BeautifulSoup(html_text, 'html.parser')
        values = soup.find_all('span', class_=None)
        return values[9].next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_date_match():
    try:
        html_text = requests.get(link2).text
        soup = BeautifulSoup(html_text, 'html.parser')
        values = soup.find('span', class_='bet-game-time').next_element
        return values
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_new_user_name():
    try:
        html_text = requests.get(link2).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('a', class_='mr-2').next_element
    except Exception as exp:
        print("text from html err", exp)
        return False
