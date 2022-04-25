import requests
from typing import List, Iterable
from custom_exceptions import CityNotFound, ServiceUnavailable, HotelsNotFound
from hotels import Hotel
from trip import Trip
from decouple import config


def get_city_id(city_name: str) -> str:
    """
        Функция для получения id города по его названию
    :param city_name: Название города
    :return: идентификатор города
    """
    result = ''
    url = "https://hotels4.p.rapidapi.com/locations/search"
    querystring = {"query": city_name,
                   "locale": "ru_RU"}
    response = requests.request("GET", url, headers=headers, params=querystring)
    for search_results in response.json()['suggestions']:
        if search_results['group'] == 'CITY_GROUP':
            for search_result in search_results['entities']:
                if search_result['name'] == city_name:
                    result = search_result['destinationId']
                    break
            else:
                raise CityNotFound
    return result


def get_hotels(trip_info: Trip) -> Iterable:
    """
        Функция-генератор для формирования и вывода списка отелей по заданному городу
    :param  trip_info: Trip -  Класс, с информацией о параметрах путешествия
    :return: Класс с информацией об отеле
    """
    querystring = {"destinationId": trip_info.city_id,
                   "pageNumber": "1",
                   "pageSize": str(trip_info.hotels_count),
                   "checkIn": trip_info.checkin_date,
                   "checkOut": trip_info.checkout_date,
                   "adults1": str(trip_info.persons_count),
                   "sortOrder": trip_info.sort_order,
                   "locale": "ru_RU",
                   "currency": "RUB"}
    url = "https://hotels4.p.rapidapi.com/properties/list"
    response = requests.request("GET", url, headers=headers, params=querystring)
    request_result = response.json()
    if request_result['result'] == 'OK':
        if len(request_result['data']['body']['searchResults']['results']) > 0:
            for hotel_record in request_result['data']['body']['searchResults']['results']:
                hotel = Hotel(hotel_record['name'])
                hotel.address = hotel_record['address']['streetAddress']
                for landmark in hotel_record['landmarks']:
                    if landmark['label'] == 'Центр города' or landmark['label'] == 'City center':
                        hotel.distance = landmark['distance']
                hotel.price = hotel_record['ratePlan']['price']['current'].replace('RUB', 'рублей')
                if trip_info.photos_count != 0:
                    hotel.photos = get_hotel_photos(hotel_record['id'])
                yield hotel
        else:
            raise HotelsNotFound
    else:
        raise ServiceUnavailable
    return


def get_hotel_photos(hotel_id: str) -> List:
    """
        Функция получения списка фотографий отеля по его id
    :param hotel_id: str - Идетификатор отеля
    :return: Список URL на фотографии отеля.
    """
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    querystring = {"id": hotel_id}
    response = requests.request("GET", url, headers=headers, params=querystring)
    request_result = response.json()
    photos = request_result['hotelImages']
    return list(photo_record['baseUrl'].replace('_{size}', '') for photo_record in photos)


if __name__ != '__main__':
    headers = {
        'x-rapidapi-host': config('host'),
        'x-rapidapi-key': config('key')
    }
