from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext as _
from django.core.cache import cache

from .utils import get_city_data, get_dist, get_weather_icon

import json
from datetime import datetime, timedelta, timezone
import pytz
from cities_light.models import City


def home_page(request):
    return render(request,'core/home.html')


def get_current_datetime(offset_seconds: int):
    tz = timezone(timedelta(seconds=offset_seconds))
    now = datetime.now(tz)

    current_time = now.time()
    current_date = now.date()

    return {'current_time':current_time,'current_date':current_date}


def temp_city_page(request, city_slug):
    city = get_object_or_404(City,slug=city_slug)

    weather_data = get_city_data.delay(city.name_ascii).get()
    weather_data = json.loads(weather_data)
    temperature = round(weather_data['main']['temp'])
    status = weather_data['weather'][0]['main']
    more_status = weather_data['weather'][0]['description']

    icon_tag = weather_data['weather'][0]['icon']
    weather_icon_url = get_weather_icon(icon_tag)

    offset_seconds = int(weather_data['timezone'])

    current_datetime = get_current_datetime(offset_seconds)

    current_time = current_datetime['current_time']
    current_date = current_datetime['current_date']
    

    context = {
        'city':city,
        'temp':temperature,
        'status':status, # Если хочется добавить картинки уже из статики (не используется в HTML шаблоне)
        'more_status':_(more_status),
        'icon_url':weather_icon_url,
        'current_time':current_time,
        'current_date':current_date,
    }

    return render(request,'core/city_page.html',context=context)


def cities_distance(request):
    name_city_from = request.GET.get('from',None)
    name_city_to = request.GET.get('to',None)

    if name_city_from is None or name_city_to is None:
        return HttpResponse('Выберите оба города')

    cache_distance = cache.get(f"{name_city_from}-{name_city_to}")
    cache_distance_reverse = cache.get(f"{name_city_to}-{name_city_from}")

    city_from = get_object_or_404(City,alternate_names=name_city_from)
    city_to = get_object_or_404(City,alternate_names=name_city_to)

    if city_from == city_to:
        distance = 0
    else:
        distance = cache_distance or cache_distance_reverse
        if not bool(distance):

            data_from = get_city_data.delay(city_from.name_ascii).get()
            data_to = get_city_data.delay(city_to.name_ascii).get()
            data_from = json.loads(data_from)
            data_to = json.loads(data_to)

            lon_from = data_from['coord']['lon']
            lat_from = data_from['coord']['lat']
            lon_to = data_to['coord']['lon']
            lat_to = data_to['coord']['lat']

            distance = get_dist(lon_from,lat_from,lon_to,lat_to)

            cache.set(f"{name_city_from}-{name_city_to}",distance,20)

    context = {
        'city_from':city_from,
        'city_to':city_to,
        'distance':distance,
    }
    return render(request,'core/distance_page.html',context=context)


# HTMX minor function
def get_cities(request,city_title):
    city = request.GET.get(city_title,'')
    if city == '':
        cities = []
    else:
        cities = City.objects.filter(alternate_names__icontains=city)
    return cities


# HTMX view
def city_list_temp(request):
    cities = get_cities(request,'city')
    return render(request,'core/includes/cities_temp.html',context={'cities':cities})


# HTMX view
def city_list_dist_1(request):
    cities = get_cities(request,'from')
    return render(request,'core/includes/cities_dist_1.html',context={'cities':cities})


# HTMX view
def city_list_dist_2(request):
    cities = get_cities(request,'to')
    return render(request,'core/includes/cities_dist_2.html',context={'cities':cities})