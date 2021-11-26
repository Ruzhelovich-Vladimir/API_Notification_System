from requests import Session

from urllib.parse import quote
from bs4 import BeautifulSoup

USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 YaBrowser/20.11.3.268 (beta) Yowser/2.5 Safari/537.36'

"""
Входные данны словарь:
        base_url - url adminer
        server - sql сервер
        login - логин 
        password - пароль
        db - база данных
        ns - пользователь dbo
        sql_query - sql-запрос
Выходные данные:
список словарей результата запроса [{"наименование поля":значение,..},...]
"""


class Request:

    def __init__(self, request):

        # Запрос
        self.request = request
        # Создаём сессию
        self.__session = Session()
        # Ответ, получае куки в заголовке
        self.response = self.__get_cookie()

    def run(self):

        # Выполняем запросы
        if self.response.status_code == 200:
            return self.execute_request()
        else:
            print(f'Ошибка:{self.response["status_code"]}')
            return

    # Получение кука
    def __get_cookie(self):
        return self.__session.get(
            self.request['base_url'], headers={'UserAgent': USER_AGENT})

    def __get_token(self):
        """Получаем токен формы
        Returns:
            [string]: [Токен формы]
        """
        result = ''
        try:
            selector_result = BeautifulSoup(
                self.response.text, 'lxml').select('input[name="token"]')
        except Exception as e:
            print(e)
            return result

        if selector_result:
            result = selector_result[len(selector_result)-1].attrs['value']
        else:
            result = ''
        return result

    def __preparation(self, url):
        """Подготавливаем запрос

        Args:
            url ([строка]): [адрес заспроса]
        """
        # На всякий случай восстанавливаем агента
        self.__updateHeaders('User-Agent', USER_AGENT)
        # Иногда требуется указывать атрибут backUrl
        self.__updateHeaders('backUrl', url)
        self.__updateHeaders('referer', url)

    def __updateHeaders(self, key, value):
        """Обновляем  значения атрибут в заголовках
        Args:
            key ([строка]): [Наименование атрибута]
            value ([строка]): [Значение]
        """
        self.__session.headers.update({
            key: value
        })

    def execute_request(self):

        result = []
        request = {}
        base_url = self.request['base_url']
        server = self.request['server']
        username = self.request['login']
        password = self.request['password']
        db = self.request['db']
        ns = self.request['ns']
        # Получаем url
        query_url = quote(self.request['sql_query'])
        url = f'{base_url}?mssql={server}&username={username}&db={db}&ns={ns}&sql={query_url}'
        # Заполняем атрибуты данные
        request['data'] = {}
        # Заполняем атрибут запроса
        request['data']['query'] = self.request['sql_query']
        # Получаем текущий токен формы или пустую строку
        request['data']['token'] = self.__get_token()
        request['data']['limit'] = ''
        request['data']['auth[server]'] = server
        request['data']['auth[username]'] = username
        request['data']['auth[password]'] = password
        request['data']['auth[db]'] = db
        request['data']['auth[ns]'] = ns

        self.__preparation(url)
        # Выполняем запрос
        self.response = self.__session.post(
            url, data=request['data'])

        # Получение таблицы в разметки html
        soup = BeautifulSoup(self.response.text, "lxml")
        rows = soup.findAll("tr")

        # Получение заголовок таблицы
        if len(rows) > 0:
            headers = [col.text for col in rows[0]]
            rows.pop(0)
            # Получение результата запроса
            result = [{headers[inx]:value.text for inx, value in enumerate(row)} for row in rows]

        return result