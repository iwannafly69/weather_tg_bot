import telebot
import requests
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
from dotenv import load_dotenv

load_dotenv()

telegram_token = os.getenv('TELEGRAM_TOKEN')
weather_api_key = os.getenv('WEATHER_API_KEY')
url_api = 'https://api.openweathermap.org/data/2.5/weather'
EMOJI_CODE = {200: '⛈', 201: '⛈', 202: '⛈', 210: '🌩', 211: '🌩', 212: '🌩',
   221: '🌩', 230: '⛈', 231: '⛈', 232: '⛈', 301: '🌧', 302: '🌧', 310: '🌧',
   311: '🌧', 312: '🌧', 313: '🌧', 314: '🌧', 321: '🌧', 500: '🌧', 501: '🌧',
   502: '🌧', 503: '🌧', 504: '🌧', 511: '🌧', 520: '🌧', 521: '🌧', 522: '🌧',
   531: '🌧', 600: '🌨', 601: '🌨', 602: '🌨', 611: '🌨', 612: '🌨', 613: '🌨',
   615: '🌨', 616: '🌨', 620: '🌨', 621: '🌨', 622: '🌨', 701: '🌫', 711: '🌫',
   721: '🌫', 731: '🌫', 741: '🌫', 751: '🌫', 761: '🌫', 762: '🌫', 771: '🌫',
   781: '🌫', 800: '☀️', 801: '🌤', 802: '☁️', 803: '☁️', 804: '☁️'}

bot = telebot.TeleBot(telegram_token)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton('Получить погоду', request_location=True))
keyboard.add(KeyboardButton('О проекте'))


def get_weather(lat, lon):
    params = {'lat': lat, 'lon': lon, 'appid': weather_api_key, 'units': 'metric', 'lang': 'ru'}
    response = requests.get(url_api, params=params)

    if response.status_code == 200:
        data = response.json()
        city = data.get('name')
        description = data['weather'][0]['description']
        code = data['weather'][0]['id']
        temp = data['main']['temp']
        temp_feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        emoji = EMOJI_CODE[code]
        message = f'🏙 Погода в: {city}\n'
        message += f'{emoji} {description.capitalize()}.\n'
        message += f'🌡 Температура {temp}°C.\n'
        message += f'🌡 Ощущается {temp_feels_like}°C.\n'
        message += f'💧 Влажность {humidity}%.\n'
        return message
    else:
        print('Ошибка при выполнении запроса')


@bot.message_handler(content_types=["location"])
def send_weather(message):
    lon = message.location.longitude
    lat = message.location.latitude
    result = get_weather(lat, lon)
    if result:
        bot.send_message(message.chat.id, result, reply_markup=keyboard)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    text = 'Отправьте мне свое местоположение и я отправлю вам погоду!'
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


@bot.message_handler(regexp="О проекте")
def send_about(message):
    text = '''Бот позволяет получить погоду в текущем местоположении! 
Для получения погоды - отправь боту геопозицию. 
Погода берется с сайта https://openweathermap.org.'''
    bot.send_message(message.chat.id, text, reply_markup=keyboard)


bot.infinity_polling()
