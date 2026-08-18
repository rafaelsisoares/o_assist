import requests
import os
import math
from dotenv import load_dotenv


load_dotenv()


def get_coordinates(city):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')

    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    return None, None


def get_weather(city):
    lat, lon = get_coordinates(city)
    if not lat or not lon:
        return None

    api_key = os.getenv('OPENWEATHERMAP_API_KEY')

    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=pt_br'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': data['name'],
            'weather': data['weather'],
            'temperature': math.ceil(data['main']['temp']),
            'visibility': data['visibility'],
            'description': data['weather'][0]['description'],
        }
        print(weather_info)
        return weather_info
    else:
        return None


def build_bot_response(content):
    weather = get_weather(content)
    if not weather:
        return "Desculpe, não encontrei esse local, vamos tentar de novo."
    return (
        f'O clima em {content.capitalize()} é {weather["description"]}, '
        f'a temperatura média para hoje é {weather["temperature"]} °C '
        f'e a visibilidade é de {weather["visibility"] / 1000} km.'
    )
