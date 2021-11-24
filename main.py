from config.config import settings

import log
from request_sql import Request
from telegram_api import TelegramClass

from tabulate import tabulate

if __name__ == '__main__':

    logger = log.init()

    control_list = settings.CONTROL_SUPPLIER

    for control_supplier in control_list:
        logger.info(
            f'Обработка поставщика: {control_supplier["supplier_name"]}')

        BOT_TOKEN = settings.BOT_TOKEN if 'BOT_TOKEN' not in control_supplier else control_supplier.BOT_TOKEN
        SQL = settings.SQL if 'SQL' not in control_supplier else control_supplier.SQL

        sql_query = SQL.replace(
            '@supplier_id', f'{control_supplier["supplier_id"]}')

        control_supplier['sql_query'] = sql_query

        orders = Request(control_supplier).run()
        if len(orders) == 0:
            continue

        # Подготовка сообщения
        text = f'УВЕДОМЛЕНИЯ {control_supplier["supplier_name"]}:'

        if 'table_mode' in control_supplier and control_supplier['table_mode'].lower() == 'yes':
            col_cnt = len(orders[0])
            len_field = int(60 / col_cnt)

            data = [{key.title().replace(' ', '')[:len_field]: str(value).title().replace(' ', '')
                     for key, value in elem.items()} for elem in orders]
            msg = tabulate(data, headers='keys', stralign='center')
        else:
            key_max_len = max((len(key.capitalize()) for key in orders[0].keys()))
            msg = ''
            for inx, order in enumerate(orders):
                text_order = '\n'.join([f'{key.capitalize()}{" "*(key_max_len-len(key.capitalize()))}: {value}'
                                        for key, value in order.items()])
                msg = f'{msg}\n{"*"*10}Уведомление №{inx+1}{"*"*10}\n{text_order}'

        text = f"{text}\n```{msg}```"  # {text}<br>
        # Отправка сообщение в группы телеграмм
        if text != f'УВЕДОМЛЕНИЯ {control_supplier["supplier_name"]}:':
            for chat in control_supplier["chats"]:
                TelegramClass(BOT_TOKEN).send_to_chat(chat, text)
