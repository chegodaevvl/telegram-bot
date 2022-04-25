class Hotel:
    """
    Класс с информацией об отеле.
    При инициации задается только название отеля
    Остальные параметры задаются пустыми значениями
    :param hotel_name: str - Название отеля
    """

    def __init__(self, hotel_name: str) -> None:
        """
        Функция инициации класса.
        При инициации задается только название отеля
        Остальные параметры задаются пустыми значениями
        :param hotel_name: str - Название отеля
        """
        self.hotel_name = hotel_name
        self.address = ''
        self.distance = ''
        self.price = ''
        self.photos = list()

    @property
    def hotel_name(self) -> str:
        """
        Геттер для получения значения атрибута Название отеля
        :return: str Название отеля
        """
        return self.__hotel_name

    @hotel_name.setter
    def hotel_name(self, hotel_name: str) -> None:
        """
        Сеттер для установки знаения атрибуту Название отеля
        :param hotel_name: str - Название отеля
        """
        self.__hotel_name = hotel_name

    @property
    def address(self) -> str:
        """
        Геттер для получения значения атрибута Адрес отеля
        :return: str - Адрес отеля
        """
        return self.__address

    @address.setter
    def address(self, address: str) -> None:
        """
        Сеттер для установки значения атрибута Адрес отеля
        :param address: str - Адрес отеля
        """
        self.__address = address

    @property
    def distance(self) -> str:
        """
        Геттер для получения значения отрибута Растояние до центра
        :return: str - Расстояние до центра
        """
        return self.__distance

    @distance.setter
    def distance(self, distance: str) -> None:
        """
        Cеттер для зания значения атрибуту расстояние до центра
        :param distance:  str - Расстояние до центра
        """
        self.__distance = distance

    @property
    def price(self) -> str:
        """
        Геттер для получения значения атрибута Стоимость за ночь
        :return: str - Стоимость номера за ночь
        """
        return self.__price

    @price.setter
    def price(self, price: str) -> None:
        """
        Сеттер для задания значения атрибуту Стоимость за ночь
        :param price: str - Стоимость за ночь
        """
        self.__price = price

    @property
    def photos(self) -> list:
        """
        Геттер для получения списка ссылок на фото отеля
        :return: list - Список с ссылками на фото отеля
        """
        return self.__photos

    @photos.setter
    def photos(self, photos: list) -> None:
        """
        Сеттер для задания списка со ссылками на фото отеля
        :param photos: list - Список с ссылками на фото отеля
        """
        self.__photos = photos

    def hotel_info(self) -> str:
        """
        Вывод информации об отеле в удобном виде для отправеки в сообщении.
        :return:
        """
        return "Отель №\nНазвание: {}\nАдрес: {}\nРасстояние до центра города: {}\nЦена за ночь: {}".format(
            self.hotel_name,
            self.address,
            self.distance,
            self.price
            )
