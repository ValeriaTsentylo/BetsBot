import os

token = os.getenv("TELEGRAM_BOT_TOKEN", "")
if not token:
    raise RuntimeError(
        "TELEGRAM_BOT_TOKEN is not set. Copy .env.example to .env and fill it in."
    )
path_user_id = './user_id.csv'
path_excel = './Bets_DB_Telegram.xlsx'
path_data_for_header = './infromation_for_header.csv'
path_mail = './login_to_mail.csv'


# with open(path_user_id, 'r') as f:  # looking for user_id for sending mails to telegram bot
#     reader = csv.reader(f)
#     rows = list(reader)
#     last_row = rows[-1]

# user_id = str(last_row[0])



