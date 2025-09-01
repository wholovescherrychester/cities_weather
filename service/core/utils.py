from .weather_apies import get_current_city, city_data_api, get_icon

from celery import shared_task

import math


@shared_task
def get_city_data(city_name):
    # city = get_current_city()
    # if city is None:
    #     return "Выключите vpn"
    data = city_data_api(city_name)
    return data


def get_rad(value:float | int):
    ''' Переводит градусы в радианы '''
    return (value * math.pi) / 180


def get_dist(lon1:float | int ,lat1:float | int, lon2:float | int, lat2:float | int):
    '''Получает расстояние (в км) между двумя точками Земли по широте и долготе'''

    # Переводим координаты в радианы
    fi_1 = get_rad(lat1)
    lambda_1 = get_rad(lon1)
    fi_2 = get_rad(lat2)
    lambda_2 = get_rad(lon2)
    delta_lambda = lambda_2 - lambda_1

    # Получаем косинусы и синусы для формулы гаверсинусов
    cos_lon_1 = math.cos(fi_1)
    cos_lon_2 = math.cos(fi_2)
    sin_lon_1 = math.sin(fi_1)
    sin_lon_2 = math.sin(fi_2)
    
    cos_delta = math.cos(delta_lambda)
    sin_delta = math.sin(delta_lambda)

    # Вычисляем числитель и знаменатель по отдельности
    numerator = math.sqrt(
            (cos_lon_2*sin_delta)**2 + (cos_lon_1*sin_lon_2 - sin_lon_1*cos_lon_2*cos_delta)**2
    )
    denominator = sin_lon_1*sin_lon_2 + cos_lon_1*cos_lon_2*cos_delta

    # Получаем угловую разницу
    delta_sigma = math.atan2(numerator,denominator)

    # Получаем расстояние в километрах
    dist = round((delta_sigma * 6372795) / 1000)

    return dist


def get_weather_icon(icon_tag:str):
    return get_icon(icon_tag)