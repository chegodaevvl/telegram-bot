from datetime import datetime, timedelta
from custom_exceptions import WrongType, NegativeValue, ValueOverLimit, DateIsEarly


def update_date(given_date: str, days_count: int) -> str:
    """
        Функция для увеличения заданной даты на заданное количество дней
    :param given_date: str - Заданная дата в строковом формате
    :param days_count: int - Заданное количество дней
    :return: str - Увеличенная дата в строковом формате
    """
    return (datetime.strptime(given_date, '%Y-%m-%d') + timedelta(days_count)).strftime('%Y-%m-%d')


def int_transformation(input_str: str, limit: int = 0) -> int:
    """
        Функция преобразования строкового значения в целочисленное.
        При преобразовании проверяется входимость в интервал от 1 до значения задаваемого параметром limit.
    :param input_str: Входная сторока
    :param limit: Верхняя граница интервала. По умолчанию равно 0 - Верхний лимит не задан
    :return: int - Целое число после преобразования
    """
    try:
        result = int(input_str)
    except Exception:
        raise WrongType
    else:
        if result < 1:
            raise NegativeValue
        elif (limit != 0) and (result > limit):
            raise ValueOverLimit
    return result


def date_transformation(input_str: str) -> str:
    """
        Преобразование строки в дату заданного формата с проверкой на корректность
    :param input_str: str - Входная строка, содержащая дату
    :return:
    """
    try:
        result = datetime.strptime(input_str, '%d.%m.%Y')
    except Exception:
        raise WrongType
    else:
        if result <= datetime.now():
            raise DateIsEarly
    return result.strftime('%Y-%m-%d')
