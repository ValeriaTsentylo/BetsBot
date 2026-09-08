import os

ENCODING = "utf-8"

# Path to the CSV holding the mailbox credentials (git-ignored, see .env.example).
PATH_TO_EMAIL_DATA = os.getenv("PATH_TO_EMAIL_DATA", "./login_to_mail.csv")

# IMAP server polled for new notification e-mails. Provider-agnostic:
# set IMAP_SERVER / IMAP_PORT in the environment, see .env.example.
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.example.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", "993"))
