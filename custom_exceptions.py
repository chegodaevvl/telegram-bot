class NegativeValue(BaseException):
    """
    Ошибка: отрицательное значение
    """
    def __init__(self):
        self.message = 'NegativeValue'


class ValueOverLimit(BaseException):
    """
    Ошибка: значение превышает верхнюю границу интервала
    """
    def __init__(self):
        self.message = 'ValueOverLimit'


class CityNotFound(BaseException):
    """
    Ошибка: Город не найден
    """
    def __init__(self):
        self.message = 'CityNotFound'


class DateIsEarly(BaseException):
    """
    Ошибка: Слишком ранняя дата
    """
    def __init__(self):
        self.message = 'DateIsEarly'


class WrongType(BaseException):
    """
    Ошибка: Неверный тип данных
    """
    def __init__(self):
        self.message = 'WrongType'


class ServiceUnavailable(BaseException):
    """
    Ошибка: Сервис недоступен
    """
    def __init__(self):
        self.message = 'ServiceUnavailable'


class HotelsNotFound(BaseException):
    """
    Ошибка: Отели не надены
    """
    def __init__(self):
        self.message = 'HotelsNotFound'


class HistoryIsEmpty(BaseException):
    """
    Ошибка: История пока не велась
    """
    def __init__(self):
        self.message = 'HistoryIsEmpty'
