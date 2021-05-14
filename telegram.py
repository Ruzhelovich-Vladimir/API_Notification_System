import requests

class TelegramClass:

    def __init__(self, token):
        self.token = token

    def send_to_chat(self, chat_id, msg):
        return requests.get(f'https://api.telegram.org/bot{self.token}/sendMessage',
                            params=dict(chat_id=chat_id, text=msg))

if __name__ == "__main__":
    TelegramClass('1835821241:AAFkxmZzXWMN4m8veOl3RDDJo8HLvRpGFO0').send_to_chat('@b2b_test', 'Тест')
