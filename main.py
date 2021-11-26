import os.path
from config.config import settings

import log
from request_sql import Request
from telegram_api import TelegramClass

import pandas as pd
import dataframe_image as dfi


report_path = './tmp/report.png'

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

        data_list = Request(control_supplier).run()
        if len(data_list) == 0:
            continue

        # Подготовка сообщения
        text = f'УВЕДОМЛЕНИЯ {control_supplier["supplier_name"]}:'
        if 'table_mode' in control_supplier and control_supplier['table_mode'].lower() == 'yes':
            # col_cnt = len(data_list[0])
            # len_field = int(60 / col_cnt)
            #
            # data = [{key.title().replace(' ', '')[:len_field]: str(value).title().replace(' ', '')
            #          for key, value in elem.items()} for elem in data_list]
            # msg = tabulate(data, headers='keys', stralign='center')
            text = None
            for elem in data_list:
                elem['Уведомления'] = control_supplier["supplier_name"]
            df = pd.DataFrame(data_list)
            dfi.export(df, report_path)
        else:
            key_max_len = max((len(key.capitalize()) for key in data_list[0].keys()))
            msg = ''
            for inx, order in enumerate(data_list):
                text_order = '\n'.join([f'{key.capitalize()}{" "*(key_max_len-len(key.capitalize()))}: {value}'
                                        for key, value in order.items()])
                msg = f'{msg}\n{"*"*10}Уведомление №{inx+1}{"*"*10}\n{text_order}'
            text = f"{text}\n```{msg}```"  # {text}<br>
            # Отправка сообщение в группы телеграмм
        for chat in control_supplier["chats"]:
            TelegramClass(BOT_TOKEN).send_to_chat(chat, text, report_path)
        if os.path.isfile(report_path):
            os.remove(report_path)
