import base64
import imaplib
import quopri
import traceback

from bs4 import BeautifulSoup

from mails.config import IMAP_PORT, IMAP_SERVER
from program_state import GLOBAL_STATE


def connection():
    imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    sts, res = imap.login(GLOBAL_STATE.MAIL_USERNAME, GLOBAL_STATE.MAIL_PASS)
    if sts == "OK":
        return imap
    else:
        return False


def get_letter_text_from_html(body):
    body = body.replace("<p><p>", "<p>").replace("</p></p>", "</p>")
    try:
        soup = BeautifulSoup(body, "html.parser")
        paragraphs = soup.find_all("p")
        text = ""
        for paragraph in paragraphs:
            text += paragraph.text + "\n"
        return text.replace("\xa0", " ")
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return False


def letter_type(part):
    if part["Content-Transfer-Encoding"] in (None, "7bit", "8bit", "binary"):
        return part.get_payload()
    elif part["Content-Transfer-Encoding"] == "base64":
        encoding = part.get_content_charset()
        return base64.b64decode(part.get_payload()).decode(encoding)
    elif part["Content-Transfer-Encoding"] == "quoted-printable":
        encoding = part.get_content_charset()
        return quopri.decodestring(part.get_payload()).decode(encoding)
    else:  # all possible types: quoted-printable, base64, 7bit, 8bit, and binary
        return part.get_payload()


def get_letter_text(msg):
    if msg.is_multipart():
        for part in msg.walk():
            count = 0
            if part.get_content_maintype() == "text" and count == 0:
                extract_part = letter_type(part)
                if part.get_content_subtype() == "html":
                    letter_text = get_letter_text_from_html(extract_part)
                else:
                    letter_text = extract_part.rstrip().lstrip()
                count += 1
                return (
                    letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")
                )
    else:
        count = 0
        if msg.get_content_maintype() == "text" and count == 0:
            extract_part = letter_type(msg)
            if msg.get_content_subtype() == "html":
                letter_text = get_letter_text_from_html(extract_part)
            else:
                letter_text = extract_part
            count += 1
            return letter_text.replace("<", "").replace(">", "").replace("\xa0", " ")


def get_link_from_html(body):
    try:
        soup = BeautifulSoup(body, 'html.parser')
        links = soup.find_all('a')
        text = ''
        for link in links:
            if link.get('href').find('topic') > -1:
                text = link.get('href')
        return text
    except Exception as exp:
        print("text from html err", exp)
        traceback.print_exc()
        return None


def get_link(msg):
    if msg.is_multipart():
        for part in msg.walk():
            count = 0
            if part.get_content_maintype() == "text" and count == 0:
                extract_part = letter_type(part)
                if part.get_content_subtype() == "html":
                    letter_link: str = get_link_from_html(extract_part) or ''
                else:
                    letter_link = extract_part.rstrip().lstrip()
                count += 1
                return letter_link
    else:
        count = 0
        if msg.get_content_maintype() == "text" and count == 0:
            extract_part = letter_type(msg)
            if msg.get_content_subtype() == "html":
                letter_link = get_link_from_html(extract_part)
            else:
                letter_link = extract_part
            count += 1
            return letter_link
