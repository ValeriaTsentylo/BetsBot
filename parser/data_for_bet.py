import requests
from bs4 import BeautifulSoup


def find_sport_name(link):     # function returns sport from url
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('span', class_='bet-game-sport').next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_country_league(link):  # function returns country for searching league_id
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('span', class_='bet-game-league').next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_name_league(link):  # function returns name dor searching league_id
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        league = soup.find('div', class_='bet-game').find_all('span')
        return league[3].next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_name_event(link):  # function return name_event for searching event_id
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('h1', class_='h1 fn title').next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_display_name(link):    # function return displayName for searching odds_id
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('span', class_='bet-type-title').next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_coefficient(link):     # function return displayName for searching odds_id
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        values = soup.find_all('span', class_=None)
        return values[6].next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_max_value(link):   # function return MaxValue for searching odds_id
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        values = soup.find_all('span', class_=None)
        return values[8].next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_user_name(link):
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.find('a', class_='mr-2').next_element
    except Exception as exp:
        print("text from html err", exp)
        return False


def find_date_bet(link):
    try:
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        values = soup.find_all('span', class_=None)
        return values[9].next_element
    except Exception as exp:
        print("text from html err", exp)
        return False






