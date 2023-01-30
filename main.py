from time import sleep
from datetime import datetime as dt

from mails.get_new_emails import get_new_emails


def email_checker():
    while True:
        print(f'kindly checking new emails at {dt.today()}')
        new_emails = get_new_emails()
        if not list(new_emails):
            print('no new emails :(')
        for i, email_text in enumerate(new_emails):
            print(i, ' ==> ', email_text)
            # тут будет какой-то экшн

        sleep(1*60)     # проверяем почту раз в минуту, может потом нужно будет увеличить


if __name__ == '__main__':
    email_checker()

