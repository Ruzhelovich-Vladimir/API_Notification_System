# import requests
from os.path import isfile

from telegram import Bot, ParseMode
import sys


class TelegramClass:

    def __init__(self, token):

        self._bot = Bot(token)

    def send_to_chat(self, chat, text_msg=None, file_path=None):

        parse_mode = ParseMode.MARKDOWN
        disable_web_page_preview = True
        reply_to_message_id = None

        try:
            if text_msg:
                self._bot.send_message(chat_id=str(chat), text=text_msg, parse_mode=parse_mode,
                                       disable_web_page_preview=disable_web_page_preview,
                                       reply_to_message_id=reply_to_message_id)
            if file_path and isfile(file_path):
                self._bot.send_photo(str(chat), photo=open(file_path, 'rb'))
        except Exception:
            exctype, value = sys.exc_info()[:2]
            print(exctype, value)


if __name__ == "__main__":

    msg = "Отчёт"
    path = "tmp/report.png"
    TelegramClass('1835821241:AAFkxmZzXWMN4m8veOl3RDDJo8HLvRpGFO0').send_to_chat(
        '-1001366099186', "Отчёт", "tmp/report.png")
