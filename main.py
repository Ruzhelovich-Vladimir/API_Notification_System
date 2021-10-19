from config.config import settings

import log
from request_sql import Request
from telegram import TelegramClass

if __name__ == '__main__':

    logger = log.init()

    control_list = settings.CONTROL_SUPPLIER

    for control_supplier in control_list:
        logger.info(f'Обработка поставщика: {control_supplier["supplier_name"]}')

        BOT_TOKEN = settings.BOT_TOKEN if 'BOT_TOKEN' not in control_supplier else control_supplier.BOT_TOKEN
        SQL = settings.SQL if 'SQL' not in control_supplier else control_supplier.SQL

        sql_query = SQL.replace('@supplier_id', f'{control_supplier["supplier_id"]}')

        control_supplier['sql_query'] = sql_query

        orders = Request(control_supplier).run()

        # Подготовка сообщения
        text = f'Новые уведомления по {control_supplier["supplier_name"]}:'
        for inx, order in enumerate(orders):
            text_order = '\n'.join([f'{key.capitalize()}: {value}' for key, value in order.items()])
            text = f'{text}\n{"*"*10}Уведомление №{inx+1}{"*"*10}\n{text_order}'

        # Отправка сообщение в группы телеграмм
        if text != f'Новые уведомления по {control_supplier["supplier_name"]}:':
            for chat in control_supplier["chats"]:
                TelegramClass(BOT_TOKEN).send_to_chat(f'{chat}', text)
