from custom_exceptions import WrongType, NegativeValue, ValueOverLimit, DateIsEarly, CityNotFound
import request_data
import calculations


class Trip:
    """
        Класс с информацией о параметрах поездки
    """

    def __init__(self) -> None:
        """
            Инициализация класса с параметрами поездки
            Все параметры инициализмруются пустыми значениями или значениями по умолчанию
        """
        self.sort_order = ''
        self.city_name = ''
        self.city_id = ''
        self.hotels_count = 10
        self.checkin_date = ''
        self.checkout_date = ''
        self.persons_count = 1
        self.photos_count = 5

    @property
    def sort_order(self) -> str:
        """
            Геттер для получения значения порядка сортировки результатов
        :return: str - порядок сортировки результаов
        """
        return self.__sort_order

    @sort_order.setter
    def sort_order(self, msg_data: str) -> None:
        """
            Сеттер для задания порядка сортировки результатов
        :param msg_data: str - порядок сортировки результатов
        """
        self.__sort_order = msg_data

    @property
    def city_name(self) -> str:
        """
            Геттер для получения параметра город поездки
        :return: str - город поездки
        """
        return self.__city_name

    @city_name.setter
    def city_name(self, msg_data: str) -> None:
        """
            Сеттер для задания названия города поездки
        :param msg_data: str - Название города поездки
        """
        self.__city_name = msg_data
        self.city_id = msg_data

    @property
    def city_id(self) -> str:
        """
            Геттер для получения параметра идентификатор города поездки
        :return: str - идентификатор города поездки
        """
        return self.__city_id

    @city_id.setter
    def city_id(self, city_name: str) -> None:
        """
            Сеттер для задания идентификатора города поездки
        """
        if city_name == '':
            self.__city_id = 'city_name'
        else:
            try:
                self.__city_id = request_data.get_city_id(city_name)
            except CityNotFound:
                raise CityNotFound

    @property
    def hotels_count(self) -> int:
        """
            Геттер для получения информации о количестве отбираемых отелей
        :return: int - Количество отбираемых отелей
        """
        return self.__hotels_count

    @hotels_count.setter
    def hotels_count(self, msg_data: str) -> None:
        """
            Сеттер для задания параметра количество отбираемых отелей
        :param msg_data: str - Количество отбираемых отелей
        """
        try:
            self.__hotels_count = calculations.int_transformation(msg_data, 10)
        except WrongType:
            raise WrongType
        except NegativeValue:
            raise NegativeValue
        except ValueOverLimit:
            self.__hotels_count = 10

    @property
    def checkin_date(self) -> str:
        """
            Геттер для получения даты предполагаемой поездки
        :return: str - Дата предполагаемой поездки в строковом формате
        """
        return self.__check_in_date

    @checkin_date.setter
    def checkin_date(self, msg_data: str) -> None:
        """
            Сеттер для задания даты предполагаемой поездки
        :param msg_data: str
        """
        if msg_data == '':
            self.__check_in_date = msg_data
        else:
            try:
                self.__check_in_date = calculations.date_transformation(msg_data)
            except DateIsEarly:
                raise DateIsEarly
            except WrongType:
                raise WrongType

    @property
    def checkout_date(self) -> str:
        """
            Геттер для получения даты завершения поездки
        :return: str - Дата завершения в строковом формате
        """
        return self.__checkout_date

    @checkout_date.setter
    def checkout_date(self, msg_data: str) -> None:
        """
            Сеттер для задания даты окончания поездки через количество ночей
        :param msg_data: str - Количество ночей поездки
        """
        if msg_data == '':
            self.__checkout_date = msg_data
        else:
            try:
                nights_count = calculations.int_transformation(msg_data)
            except WrongType:
                raise WrongType
            except NegativeValue:
                raise NegativeValue
            else:
                self.__checkout_date = calculations.update_date(self.checkin_date, nights_count)

    @property
    def persons_count(self) -> int:
        """
            Геттер для получения информации о количестве туристов
        :return: int - Количество туристов
        """
        return self.__persons_count

    @persons_count.setter
    def persons_count(self, msg_data: str) -> None:
        """
            Сеттер для установления значения количества туристов
        :param msg_data: str - Количество туристов
        """
        try:
            self.__persons_count = calculations.int_transformation(msg_data)
        except WrongType:
            raise WrongType
        except NegativeValue:
            raise NegativeValue

    @property
    def photos_count(self) -> int:
        """
            Геттер для получения количества выгружаемых фотографий отеля
        :return: int - Количество выгружаемых фотографий
        """
        return self.__photos_count

    @photos_count.setter
    def photos_count(self, msg_data: str) -> None:
        """
            Сеттер для задания значения параметру Количество фотографий
        :param msg_data: str - Количество фотографий из сообщения
        """
        if msg_data == '0':
            self.__photos_count = 0
        else:
            try:
                self.__photos_count = calculations.int_transformation(msg_data, 5)
            except WrongType:
                raise WrongType
            except NegativeValue:
                raise NegativeValue
            except ValueOverLimit:
                self.__photos_count = 5


if __name__ == '__main__':
    pass
