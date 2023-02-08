import email
from typing import Iterable

from mails.config import ENCODING
from mails.helpers import get_letter_text, connection, get_link


def get_new_emails() -> list[dict[str, str]]:
    imap = connection()
    if not imap:
        return []

    status, messages = imap.select("INBOX")  # папка входящие
    res, unseen_msgs = imap.uid("search", "UNSEEN", "ALL")

    information = []
    for unseen_msg in unseen_msgs:
        unseen_msg = unseen_msg.decode(ENCODING).split(" ")
        if unseen_msg:
            for letter in unseen_msg:
                res, msg = imap.uid("fetch", letter, "(RFC822)")
                if res == "OK":
                    msg = email.message_from_bytes(msg[0][1])
                    letter_text = get_letter_text(msg)
                    letter_links = get_link(msg)
                    information.append({
                        'text': letter_text,
                        'link': letter_links,
                    })
        else:
            continue

    imap.logout()
    return information



