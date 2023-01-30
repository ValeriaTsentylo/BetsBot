import email
from typing import Iterable

from mails.config import ENCODING
from mails.helpers import get_letter_text, connection


def get_new_emails() -> Iterable[str]:
    imap = connection()
    if not imap:
        return

    status, messages = imap.select("INBOX")  # папка входящие
    res, unseen_msg = imap.uid("search", "UNSEEN", "ALL")
    unseen_msg = unseen_msg[0].decode(ENCODING).split(" ")

    if unseen_msg[0]:
        for letter in unseen_msg:
            res, msg = imap.uid("fetch", letter, "(RFC822)")
            if res == "OK":
                msg = email.message_from_bytes(msg[0][1])
                letter_text = get_letter_text(msg)
                yield letter_text
        imap.logout()
    else:
        imap.logout()
        return

