import csv


ENCODING = "utf-8"
# USERNAME1 = "user@example.com"  # UserMain in Expari
# MAIL_PASS1 = "***REMOVED***"
path = './login_to_mail.csv'
with open(path, 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)
    last_row = rows[-1]
    print(last_row)
USERNAME1 = last_row[0]
MAIL_PASS1 = last_row[1]
print(USERNAME1)
print(MAIL_PASS1)
USERNAME2 = "user2@example.com"         # User2 in Expari
MAIL_PASS2 = "***REMOVED***"


