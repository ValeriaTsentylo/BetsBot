import traceback

from bs4 import BeautifulSoup


def find_bookmaker(html_text: str):  # function returns bookmaker from url
    try:
        # html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, 'html.parser')
        img_src = soup.find('div', class_='bookmaker-bet-logo').find('img').get('src')
        if isinstance(img_src, list) or img_src is None:
            raise Exception('img_src shouldn\'t be a list or None')

        elif 'pinnacle' in img_src:
            return 'pinnacle'
        else:
            return 'vodds'
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return False


def find_sport_name(html_text: str):     # function returns sport from url
    # html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    element = soup.find('span', class_='bet-game-sport')
    if element:
        return element.next_element
    else:
        return None


def find_country_league(html_text: str):  # function returns country for searching league_id
    # html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    element = soup.find('span', class_='bet-game-league')
    if element:
        return element.next_element
    else:
        return None


def find_name_league(html_text: str):  # function returns name dor searching league_id
    # html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    league = soup.find('div', class_='bet-game').find_all('span')
    if league:
        return league[3].next_element
    else:
        return None


def find_name_event(html_text: str):  # function return name_event for searching event_id
    # html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    element = soup.find('h1', class_='h1 fn title')
    if element:
        return element.next_element
    else:
        return None


def find_display_name(html_text: str):    # function return displayName for searching odds_id
    # html_text = requests.get(link, timeout=20).text
    soup = BeautifulSoup(html_text, 'html.parser')
    element = soup.find('span', class_='bet-type-title')
    if element:
        return element.next_element
    else:
        return None


def find_coefficient(html_text: str):     # function return displayName for searching odds_id
    # html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    values = soup.find_all('span', class_=None)
    if values:
        return values[6].next_element
    else:
        return None


def find_max_value(html_text: str):   # function return MaxValue for searching odds_id
    # html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    values = soup.find_all('span', class_=None)
    if values:
        return values[8].next_element
    else:
        return None


def find_user_name(html_text: str):
    # html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    element = soup.find('a', class_='mr-2')
    if element:
        return element.next_element
    else:
        return None


def find_date_bet(html_text: str):
    # html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, 'html.parser')
    values = soup.find_all('span', class_=None)
    if values:
        return values[9].next_element
    else:
        return None






