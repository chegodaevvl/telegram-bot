import telebot
from telebot import types
import request_data
import history
import trip
from custom_exceptions import WrongType, NegativeValue, DateIsEarly, CityNotFound, ServiceUnavailable
from custom_exceptions import HistoryIsEmpty, HotelsNotFound
from decouple import config


assistant_bot = telebot.TeleBot(config('bot_uid'))


@assistant_bot.message_handler(content_types=['text'])
def get_text_message(message) -> None:
    """
        Функция для обработки команд отправляемых боту
    :param message : Сообщение, получаемое ботом
    """
    welcome_msg = 'Привет, мир! Агентство Too Easy Travel готово организовать отдых вашей мечты!'
    greeting_msg = 'Здравствуйте. Введите /help, чтобы посмотреть перечень доступных команд.'
    command_list = '/lowprice - топ самых дешевых отелей города\n'
    command_list += '/highprice - топ самых дорогих отелей города\n'
    command_list += '/bestdeal - топ отелей, оптимальных по цене и расположению от центра города\n'
    command_list += '/history - просмотр истории поисковых запросов пользователя'
    if message.text.lower() == '/hello-world':
        assistant_bot.send_message(message.from_user.id, welcome_msg)
    elif message.text.lower() == 'привет':
        assistant_bot.send_message(message.from_user.id, greeting_msg)
    elif message.text.lower() == '/help':
        assistant_bot.send_message(message.from_user.id, command_list)
    elif message.text.lower() == '/lowprice':
        trip_info.sort_order = 'PRICE'
        start(message)
    elif message.text.lower() == '/highprice':
        trip_info.sort_order = 'PRICE_HIGHEST_FIRST'
        start(message)
    elif message.text.lower() == '/bestdeal':
        trip_info.sort_order = 'BEST_SELLER'
        start(message)
    elif message.text.lower() == '/history':
        try:
            history_output = session_history.get_history(message.from_user.id)
        except HistoryIsEmpty:
            assistant_bot.send_message(message.from_user.id, 'Вы еще не проводили поиск отелей с моей помощью.')
        else:
            assistant_bot.send_message(message.from_user.id, history_output)
    else:
        assistant_bot.send_message(message.from_user.id, "Я вас не понимаю, введите команду 'Привет'")


def start(message):
    """
        Функция запуска получения данных о поездке
    :param message:
    """
    assistant_bot.send_message(message.from_user.id, "В какой город поедете?")
    assistant_bot.register_next_step_handler(message, get_town)


def get_town(message):
    """
        Функция фиксации информации о городе путешествия
    :param message:
    """
    try:
        trip_info.city_name = message.text
    except CityNotFound:
        assistant_bot.send_message(message.from_user.id, "Мы не знаем такого города. Введите город заново.")
        assistant_bot.register_next_step_handler(message, get_town)
    else:
        assistant_bot.send_message(message.from_user.id, "Введите дату начала поездки (в формате dd.mm.yyyy).")
        assistant_bot.register_next_step_handler(message, get_start_date)


def get_start_date(message):
    """
        Функция фиксации планируемой даты прибытия в город
    :param message:
    """
    try:
        trip_info.checkin_date = message.text
    except DateIsEarly:
        assistant_bot.send_message(message.from_user.id, "Введите дату из будущего периода")
        assistant_bot.register_next_step_handler(message, get_start_date)
    except WrongType:
        assistant_bot.send_message(message.from_user.id, "Введена дата в неверном формате. Введите заново.")
        assistant_bot.register_next_step_handler(message, get_start_date)
    else:
        assistant_bot.send_message(message.from_user.id, "Сколько ночей планируете провести в городе {}?".format(
            trip_info.city_name
        ))
        assistant_bot.register_next_step_handler(message, get_night_count)


def get_night_count(message):
    """
        Функция фиксации количества ночей
    :param message:
    """
    try:
        trip_info.checkout_date = message.text
    except WrongType:
        assistant_bot.send_message(message.from_user.id, 'Введено не число')
        assistant_bot.register_next_step_handler(message, get_night_count)
    except NegativeValue:
        assistant_bot.send_message(message.from_user.id, 'Введено отрицательное число')
        assistant_bot.register_next_step_handler(message, get_night_count)
    else:
        assistant_bot.send_message(message.from_user.id, 'Количество гостей?')
        assistant_bot.register_next_step_handler(message, get_adult_guest_count)


def get_adult_guest_count(message):
    """
        Функция фиксации количества гостей
    :param message:
    """
    try:
        trip_info.persons_count = message.text
    except NegativeValue:
        assistant_bot.send_message(message.from_user.id, 'Введено отрицательное число')
        assistant_bot.register_next_step_handler(message, get_adult_guest_count)
    except WrongType:
        assistant_bot.send_message(message.from_user.id, 'Введено не число')
        assistant_bot.register_next_step_handler(message, get_adult_guest_count)
    else:
        assistant_bot.send_message(message.from_user.id, 'Какое количество отелей показать? Не более 10.')
        assistant_bot.register_next_step_handler(message, get_hotel_count)


def get_hotel_count(message):
    """
        Функция фиксации количества отелей в выдаче и запрос на необходимость вывода фотографий
    :param message:
    """
    try:
        trip_info.hotels_count = message.text
    except WrongType:
        assistant_bot.send_message(message.from_user.id, 'Введено не число')
        assistant_bot.register_next_step_handler(message, get_hotel_count)
    except NegativeValue:
        assistant_bot.send_message(message.from_user.id, 'Введено отрицательное число')
        assistant_bot.register_next_step_handler(message, get_hotel_count)
    else:
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        question = 'Загружать фотографии отелей?'
        assistant_bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@assistant_bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    """
        Обработчик инлайн клавиатуры
    :param call:
    """
    if call.data == "no":
        assistant_bot.send_message(call.message.chat.id, 'Начинаем поиск.')
        trip_info.photos_count = '0'
        result_processing(call.message.chat.id)
    else:
        assistant_bot.send_message(call.message.chat.id, 'Количество фотографий для отеля? Не более 5.')
        assistant_bot.register_next_step_handler(call.message, get_photos_count)


def get_photos_count(message):
    """
        Фукнция фиксации количества выводимых фото
        :param message:
    """
    try:
        trip_info.photos_count = message.text
    except WrongType:
        assistant_bot.send_message(message.from_user.id, 'Количество фотографий для отеля? Не более 5.')
        assistant_bot.register_next_step_handler(message.from_user.id, get_photos_count)
    except NegativeValue:
        assistant_bot.send_message(message.from_user.id, 'Количество фотографий для отеля? Не более 5.')
        assistant_bot.register_next_step_handler(message.from_user.id, get_photos_count)
    else:
        assistant_bot.send_message(message.from_user.id, 'Начинаем поиск.')
        result_processing(message.from_user.id)


def result_processing(chat_id):
    """
        Функция вывода полученных результатов
    :param chat_id: Идентификатор чата с пользователем
    """
    history_record = history.HistoryRecord(chat_id, trip_info.sort_order)
    hotels_processed = 0
    try:
        for hotel in request_data.get_hotels(trip_info):
            if hotels_processed < trip_info.hotels_count:
                hotels_processed += 1
                history_record.add_hotel(hotel.hotel_name)
                msg_text = hotel.hotel_info().replace('№', '№{}'.format(hotels_processed))
                if trip_info.photos_count > 0:
                    msg_text += '\nФотографии отеля:'
                assistant_bot.send_message(chat_id, msg_text)
                if trip_info.photos_count != 0:
                    photo_shown = 0
                    for photo in hotel.photos:
                        if photo_shown < trip_info.photos_count:
                            try:
                                assistant_bot.send_photo(chat_id, photo)
                            except Exception:
                                pass
                            else:
                                photo_shown += 1
                        else:
                            break
    except HotelsNotFound:
        assistant_bot.send_message(chat_id, 'По вашим критериям ничего не найдено')
    except ServiceUnavailable:
        assistant_bot.send_message(chat_id, 'Сервис недоступен')
    session_history.add_record(history_record)


if __name__ == '__main__':
    session_history = history.History()
    trip_info = trip.Trip()
    assistant_bot.polling(none_stop=True, interval=0)
