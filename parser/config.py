path_bets_csv = './bets_csv.csv'

# with open(path_data_for_header, 'r') as f:  # looking for param for headers for requests
#     reader = csv.reader(f)
#     rows = list(reader)
#     last_row = rows[-1]
#
# Cookie = str(last_row[0])
# Content_Length = str(last_row[1])
# X_CSRF_TOKEN = str(last_row[2])
#
# headers = {'Cookie': Cookie}
# headers_for_post = {
#     'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate, br',
#     'Accept-Language': 'uk-UA,uk;q=0.9,ru-UA;q=0.8,ru;q=0.7,en-US;q=0.6,en;q=0.5',
#     'Connection': 'keep-alive',
#     'Content-Length': Content_Length,
#     'Content-Type': 'application/json; charset=UTF-8',
#     'Cookie': Cookie,
#     'Host': 'expari.com',
#     'Origin': 'https://expari.com',
#     'Referer': 'https://expari.com/topic/create',
#     'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
#     'sec-ch-ua-mobile': '?0',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
#     'X-CSRF-TOKEN': X_CSRF_TOKEN
# }
url_bookmaker = 'https://expari.com/api/bet/bookmakers'
url_bet = 'https://expari.com/api/topics'
url_sport = 'https://expari.com/api/bet/sports/1'
url_league = 'https://expari.com/api/bet/leagues/'
url_event = 'https://expari.com/api/bet/events/'
url_odds = 'https://expari.com/api/bet/odds/'
url_odd = 'https://expari.com/api/bet/odd/'
url_ex = 'https://expari.com/topic/'

# The upstream API (expari.com) is a Russian-language service and returns its
# error messages and page labels verbatim in Russian. The constants below mirror
# those raw upstream strings so the responses can be matched; they are written as
# escape sequences to keep this source tree free of non-Latin text, and they are
# never shown to the user.
API_ERROR_BET_ALREADY_PLACED = (
    '\u0421\u0442\u0430\u0432\u043a\u0430 \u043d\u0430 \u044d\u0442\u043e\u0442 '
    '\u043c\u0430\u0442\u0447 \u0443\u0436\u0435 \u0440\u0430\u0437\u043c\u0435'
    '\u0449\u0435\u043d\u0430 \u0432 \u0432\u044b\u0431\u0440\u0430\u043d\u043e\u043c '
    '\u0431\u043b\u043e\u0433\u0435'
)
API_ERROR_CHECK_INPUT_DATA = (
    '\u041f\u0440\u043e\u0432\u0435\u0440\u044c\u0442\u0435 \u0432\u0432\u0435'
    '\u0434\u0435\u043d\u043d\u044b\u0435 \u0434\u0430\u043d\u043d\u044b\u0435'
)
PAGE_LABEL_STATUS = '\u0421\u0442\u0430\u0442\u0443\u0441:'
