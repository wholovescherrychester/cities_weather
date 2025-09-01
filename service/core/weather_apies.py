import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()


def get_current_city():
    url = "https://get.geojs.io/v1/ip/geo.json"
    response = requests.get(url).text
    data = json.loads(response)
    city = data.get('city', None)
    return city


def city_data_api(city:str):
    url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&appid={os.getenv('OpenWeatherApiKey')}"
    response = requests.get(url).text
    return response


def get_icon(icon_tag:str):
    url = f"https://openweathermap.org/img/wn/{icon_tag}@2x.png"
    return url
