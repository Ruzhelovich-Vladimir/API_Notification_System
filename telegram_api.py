# import requests
from telegram import Bot, ParseMode
import sys


class TelegramClass:

    def __init__(self, token):

        self._bot = Bot(token)

    def send_to_chat(self, chat, msg):

        parse_mode = ParseMode.MARKDOWN
        disable_web_page_preview = True
        reply_to_message_id = None

        try:
            # logger.debug("Message to send:(chat:%s,text:%s,parse_mode:%s,disable_preview:%s,keyboard:%s, reply_to_message_id:%s" %
            #                 (chat_id, msg[0], parse_mode, disable_web_page_preview, msg[1], reply_to_message_id))
            self._bot.send_message(chat_id=str(chat), text=msg, parse_mode=parse_mode,
                                   disable_web_page_preview=disable_web_page_preview,
                                   reply_to_message_id=reply_to_message_id)
            # logger.debug("Message sent OK:(chat:%s,text:%s,parse_mode:%s,disable_preview:%s,reply_keyboard:%s, reply_to_message_id:%s" %
            #                 (chat_id, msg[0], parse_mode, disable_web_page_preview, msg[1], reply_to_message_id))
        except:
            exctype, value = sys.exc_info()[:2]
            print(value)
            # print("""Error trying to send message:(chat:%s,text:%s,parse_mode:%s,disable_preview:%s,
            #                 reply_keyboard:%s, reply_to_message_id:%s): %s:%s""" %
            #       (chat, msg, parse_mode, disable_web_page_preview, msg, reply_to_message_id, exctype, value))
            # logger.error("""Error trying to send message:(chat:%s,text:%s,parse_mode:%s,disable_preview:%s,
            #                 reply_keyboard:%s, reply_to_message_id:%s): %s:%s""" %
            #                 (chat_id, msg[0], parse_mode, disable_web_page_preview, msg[1], reply_to_message_id, exctype, value))

        # bot = Bot(self.token)
        # try:
        #     bot.send_message(chat_id=chat, text=msg, parse_mode=ParseMode.HTML)
        # except Exception as err:
        #     print(err)

        # return requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage',
        #                     params=dict(chat_id=chat_id, text=msg, parse_mode=''))


if __name__ == "__main__":

    msg = """
|           Сообщение            |   Код поставщика |         Поставтащик          |   Всего привязано к поставщику |   С каталогом поставщика |  Доля с каталогом  |   С портфелем ABIE |
|:------------------------------:|-----------------:|:----------------------------:|-------------------------------:|-------------------------:|:------------------:|-------------------:|
| Доля каталогов в базе < 50.00% |                4 | Триал Восток - Сады придонья |                           2287 |                      591 |       25.84%       |               2287 |
| Доля каталогов в базе < 50.00% |                5 |        ВиасПКФ - Марс        |                           3864 |                     1296 |       33.54%       |               3841 |
| Доля каталогов в базе < 50.00% |               17 | Триал Восток - Сады придонья |                            471 |                        0 |       0.00%        |                248 |
</pre>
"""
    TelegramClass('1835821241:AAFkxmZzXWMN4m8veOl3RDDJo8HLvRpGFO0').send_to_chat(
        '-1001366099186', msg)
