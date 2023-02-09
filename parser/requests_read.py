import requests

headers = {
    'Cookie': 'SESSION=OTM1ZWMyOWUtZDM1Yi00MjRhLThkNDktZjUzMDMwZTNiMWJi; _ga=GA1.2.1918142767.1675961520; _gid=GA1.2.541953671.1675961520; _ym_uid=16759615201049564383; _ym_d=1675961520; _ym_isad=1; _gat=1'}

# res = requests.get('https://expari.com/api/bet/leagues/1/1', headers=headers)
# res = requests.get('https://expari.com/api/bet/events/1/35', headers=headers)

# print(res.status_code)
#
# leages = res.json()
# for leage in leages:
#     print(type(leage), leage)

data = {"id": None, "blog": {"id": 19994}, "title": "Western Sydney Wanderers - Sydney FC", "content": "", "price": 0,
        "publish": True, "closeComment": False,
        "bet": {"bookmakerId": 1, "sportId": 1, "leagueId": 35, "eventId": 5078742, "oddId": 60175093180, "value": 0,
                "isHidden": False, "coefficient": 2.81, "analytic": False, "maxValue": 838.73,
                "displayName": "(1x2) Хозяева", "selectedRecords": [], "wantStakeAmount": 0}, "mediaIds": [],
        "confirmBet": False, "pinn": False, "hardOpen": False}
res = requests.post('https://expari.com/api/topics', data=data, headers=headers)
print(res.status_code)
print(res.text)
