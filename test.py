import requests
import bs4


# Функция, которая показывает курс BNB (криптовалюты)

def get_bnb():
    url = requests.get('https://markets-today.ru/calculator/bnb/')  # Указываем сайт с которого будем вытаскивать ину
    b = bs4.BeautifulSoup(url.text, "html.parser")
    url1 = b.select(".col-12")  # Выбираем место откуда будет вытаскиваться текст
    url_print = url1[0].getText()
    a = 'Курс BNB'
    a = str(a + url_print)
    return a  # То, что выведет функция


print(get_bnb())


def get_weather():
    from yaweather import Russia, YaWeather

    y = YaWeather(
        api_key='7a4600f8-b028-4278-baf2-b06c443f01f4')  # Мой ключ АПИ, но лучше создай свой тут - https://developer.tech.yandex.ru/services/18

    res = y.forecast(Russia.SaintPetersburg)  # Указываешь местоположение

    for f in res.forecasts:
        day = f.parts.day_short
        b = (f'{f.date} | {day.temp} °C, {day.condition}')
        return b # То, что выведет функция


print('Погода в СПб на - '+get_weather())
