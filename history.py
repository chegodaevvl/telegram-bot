from datetime import datetime
from custom_exceptions import HistoryIsEmpty
from pathlib import Path
import sqlite3


class HistoryRecord:
    """
        Класс для создания записи, хранящей историю запроса о выполнении конкретной команды
    """

    def __init__(self, user_id, sort_order: str) -> None:
        """
            Функция инициализации экземпляра записи, хранящей историю выполнения команды
        :param user_id: str Идентификатор пользователя из чата Telegram
        :param sort_order: str Порядок сортировки выводимых данных в результате работы API запроса
        """
        self.__date_time = datetime.now()
        self.uid = user_id
        self.command = sort_order
        self.__hotels = list()

    @property
    def uid(self) -> str:
        """
            Геттер для получения значения параметра Идентификатор пользователя
        """
        return self.__uid

    @uid.setter
    def uid(self, user_id: str) -> None:
        """
            Сеттер для задания значения параметру Идентификатор пользователя
        :param user_id: str Идентификатор пользователя из чата Telegram
        """
        self.__uid = user_id

    @property
    def command(self) -> str:
        """
            Геттер для получения значения параметра Использованная команда
        """
        return self.__command

    @command.setter
    def command(self, sort_order: str) -> None:
        """
            Сеттер для задания значения параметру Использованная команда
        :param sort_order: str Порядок сортировки выводимых данных в результате работы API запроса
        """
        if sort_order == 'PRICE':
            self.__command = 'lowprice'
        elif sort_order == 'PRICE_HIGHEST_FIRST':
            self.__command = 'highprice'
        else:
            self.__command = 'bestdeal'

    def add_hotel(self, hotel_name: str) -> None:
        """
            Функция добавления названия отеля в запись истории поиска
        :param hotel_name: str - Название добовляемого отеля
        """
        self.__hotels.append(hotel_name)

    def get_hotels(self) -> str:
        """
            Геттер для получения перечня отелей, выведенных как результат поиска
        :return: список, содержащий перечень найденных отелей
        """
        return ', '.join(self.__hotels)

    def get_date(self) -> str:
        """
            Геттер для получения даты проведения сеанса поиска
        :return: str - Дата проведения сеанса поиска
        """
        return datetime.strftime(self.__date_time, '%d-%m-%Y')

    def get_time(self) -> str:
        """
            Геттер для получения времени проведения сеанса поиска
        :return: str - Время проведения сеанса поиска
        """
        return datetime.strftime(self.__date_time, '%H:%M')


class History:
    """
        Класс, содержащий историю выполнения команд поиска отелей
    """

    def __init__(self):
        """
            Функция инициализации базы данных, содержащей историю поиска отелей
        """
        if not Path('history_log').exists():
            Path('history_log').mkdir()
        history_path = Path('history_log').joinpath('history.db')
        self.__history_db = sqlite3.connect(history_path, check_same_thread=False)
        self.__cursor = self.__history_db.cursor()
        request = "CREATE TABLE IF NOT EXISTS history (user_id text, date_stamp text, time_stamp text, "
        request += "command text, hotels text)"
        self.__cursor.execute(request)

    def add_record(self, record: HistoryRecord) -> None:
        """
            Добавление записи выполненной команды в историю
        :param record: HistoryRecord Экземпляр класса, содержащего записи об истории поиска
        """
        request = "INSERT INTO history VALUES('{}', '{}', '{}', '{}', '{}')".format(str(record.uid),
                                                                                    str(record.get_date()),
                                                                                    str(record.get_time()),
                                                                                    str(record.command),
                                                                                    str(record.get_hotels()))
        self.__cursor.execute(request)
        self.__history_db.commit()

    def get_history(self, user_id: str) -> str:
        """
            Функция вывода истории поиска отелей
        :param: user_id: str - Идентификатор пользователя
        :return: История поиска отелей одной строкой
        """
        result = list()
        request = "SELECT date_stamp, time_stamp, command, hotels FROM history WHERE user_id=? and date_stamp="
        request += "(SELECT max(date_stamp) FROM history)"
        self.__cursor.execute(request, [user_id])
        history_raw = self.__cursor.fetchall()
        if len(history_raw) == 0:
            raise HistoryIsEmpty
        for line in history_raw:
            result.append('{}\n по команде {}\n были отобраны следующие отели: {}'.format(
                (line[0] + ' ' + line[1]),
                line[2],
                line[3]))
        return ('\n' + '=' * 40 + '\n').join(result)
