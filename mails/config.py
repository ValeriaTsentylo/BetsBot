import csv

ENCODING = "utf-8"
path = './login_to_mail.csv'
with open(path, 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)
    last_row = rows[-1]
USERNAME1 = str(last_row[0])
MAIL_PASS1 = str(last_row[1])


# USERNAME1 = "user@example.com"  # UserMain in Expari
# MAIL_PASS1 = "***REMOVED***"
USERNAME2 = "user2@example.com"         # User2 in Expari
MAIL_PASS2 = "***REMOVED***"


