import requests
import os
import math
from dotenv import load_dotenv
from .weather_info_codes import WEATHER_INFO_CODES


load_dotenv()


def get_weather(city):
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=pt_br'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            'city': data['name'],
            'weather': data['weather'],
            'temperature': math.ceil(data['main']['temp']),
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
        f'a temperatura atual é {weather["temperature"]} °C.'
    )
