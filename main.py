# Телеграм-бот v.004
import json
from gettext import find
from io import BytesIO
from time import sleep

import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import requests
import bs4
import BotGames  # бот-игры, файл BotGames.py
from menuBot import Menu, Users  # в этом модуле есть код, создающий экземпляры классов описывающих моё меню
import DZ  # домашнее задание от первого урока

bot = telebot.TeleBot('5228642369:AAGQJwrL9paeUtQ1U4T-CqZOlJ3Bb0haZsw')  # !!! Oleg4TestBot
game21 = None  # класс игры в 21, экземпляр создаём только при начале игры

# --------GLOBAL VAR-------------

# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message, res=False):
    txt_message = f"Привет! Я ботик"
    bot.send_message(message.chat.id, text=txt_message, reply_markup=Menu.getMenu("Главное меню").markup)


# -----------------------------------------------------------------------
# Получение сообщений от юзера

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text
    global game21

    cur_user = Users.getUser(chat_id)
    if cur_user == None:
        cur_user = Users(chat_id, message.json["from"])

    result = goto_menu(chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if result == True:
        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu != None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню
        cur_user.set_cur_menu(ms_text)
        if ms_text == "Хозяин":
            send_help(chat_id)

        elif ms_text == "Прислать погоду":
            bot.send_message(chat_id, text='Погода в СПб на - '+get_weather())

        elif ms_text == "Прислать енота":
            bot.send_photo(chat_id, photo=get_raccoonURL(), caption="Лови енота")

        elif ms_text == "Прислать курс эфира":
            get_eth()
            bot.send_message(chat_id, text=get_eth())


        elif ms_text == "Прислать стоимость газа":
            get_gas()
            bot.send_message(chat_id, text=get_gas())

        elif ms_text == "Прислать фильм":
            send_film(chat_id)

        elif ms_text == "Угадай кто?":
            get_ManOrNot(chat_id)

        elif ms_text == "Карту!":
            if game21 == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                goto_menu(chat_id, "Выход")
                return

            text_game = game21.get_cards(1)
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

            if game21.status != None:  # выход, если игра закончена
                goto_menu(chat_id, "Выход")
                return

        elif ms_text == "Стоп!":
            game21 = None
            goto_menu(chat_id, "Выход")
            return

        elif ms_text in BotGames.GameRPS.values:  # реализация игры Камень-ножницы-бумага
            bot.send_message(chat_id, text="Ждем игрока")
            for _ in range(5):
                text_game = ""
                for user in Users.activeUsers.values():
                    if cur_user.get_cur_enemy():
                        user = cur_user.get_cur_enemy()
                    if user.id != cur_user.id and user.get_cur_menu() in BotGames.GameRPS.values:
                        user.set_cur_enemy(cur_user)
                        enemy_value = user.get_cur_menu()
                        bot.send_message(chat_id, text="Твой друган - @{enemy}".format(enemy=user.userName))
                        gameRSP = BotGames.getGame(chat_id)
                        if gameRSP == None:  # если мы случайно попали в это меню, а объекта с игрой нет
                            goto_menu(chat_id, "Выход")
                            return
                        text_game = gameRSP.player_vs_player_choice(ms_text, enemy_value)
                        bot.send_message(chat_id, text=text_game)
                        gameRSP.newGame()
                        break
                if text_game:
                    break
                sleep(1)
            if not text_game:
                bot.send_message(chat_id, text="Друган не найден :С")
            sleep(1)
            cur_user.set_cur_menu("")
            cur_user.set_cur_enemy("")


        elif ms_text == "Задание 1":

            DZ.dz1(bot, chat_id)

        elif ms_text == "Задание 2":

            DZ.dz2(bot, chat_id)

        elif ms_text == "Задание 3":

            DZ.dz3(bot, chat_id)

        elif ms_text == "Задание 4,5":

            DZ.dz45(bot, chat_id)

        elif ms_text == "Задание 6":

            DZ.dz6(bot, chat_id)

        elif ms_text == "Задание 7.1":

            DZ.dz7n(bot, chat_id)

        elif ms_text == "Задание 7.2":

            DZ.dz7a(bot, chat_id)

        elif ms_text == "Задание 8":

            DZ.dz8(bot, chat_id)

        elif ms_text == "Задание 9.1":

            DZ.dz91(bot, chat_id)

        elif ms_text == "Задание 9.2":

            DZ.dz92(bot, chat_id)

        elif ms_text == "Задание 10":

            DZ.dz10(bot, chat_id)

    else:  # ...........................................................................................................
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        goto_menu(chat_id, "Главное меню")


# -----------------------------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # если требуется передать параметр или несколько параметров в обработчик кнопки, использовать методы Menu.getExtPar() и Menu.setExtPar()
    pass
    # if call.data == "ManOrNot_GoToSite": #call.data это callback_data, которую мы указали при объявлении InLine-кнопки
    #
    #     # После обработки каждого запроса нужно вызвать метод answer_callback_query, чтобы Telegram понял, что запрос обработан.
    #     bot.answer_callback_query(call.id)


# -----------------------------------------------------------------------
def goto_menu(chat_id, name_menu):
    # получение нужного элемента меню
    cur_menu = Menu.getCurMenu(chat_id)
    if name_menu == "Выход" and cur_menu != None and cur_menu.parent != None:
        target_menu = Menu.getMenu(chat_id, cur_menu.parent.name)
    else:
        target_menu = Menu.getMenu(chat_id, name_menu)

    if target_menu != None:
        bot.send_message(chat_id, text=target_menu.name, reply_markup=target_menu.markup)

        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if target_menu.name == "Игра в 21":
            game21 = BotGames.newGame(chat_id, BotGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=getMediaCards(game21))  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif target_menu.name == "Камень, ножницы, бумага":
            gameRSP = BotGames.newGame(chat_id, BotGames.GameRPS())  # создаём новый экземпляр игры
            text_game = "<b>Победитель определяется по следующим правилам:</b>\n" \
                        "1. Камень побеждает ножницы\n" \
                        "2. Бумага побеждает камень\n" \
                        "3. Ножницы побеждают бумагу"

        return True
    else:
        return False


# -----------------------------------------------------------------------
def getMediaCards(game21):
    medias = []
    for url in game21.arr_cards_URL:
        medias.append(types.InputMediaPhoto(url))
    return medias


# -----------------------------------------------------------------------
def send_help(chat_id):
    global bot
    bot.send_message(chat_id, "Я крутой\nhttps://linktr.ee/koyshem")

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in Users.activeUsers:
        bot.send_message(chat_id, Users.activeUsers[el].getUserHTML(), parse_mode='HTML')

# -----------------------------------------------------------------------
def send_film(chat_id):
    film = get_randomFilm()
    info_str = f"<b>{film['Наименование']}</b>\n" \
               f"Год: {film['Год']}\n" \
               f"Страна: {film['Страна']}\n" \
               f"Жанр: {film['Жанр']}\n" \
               f"Продолжительность: {film['Продолжительность']}"
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Трейлер", url=film["Трейлер_url"])
    btn2 = types.InlineKeyboardButton(text="СМОТРЕТЬ онлайн", url=film["фильм_url"])
    markup.add(btn1, btn2)
    bot.send_photo(chat_id, photo=film['Обложка_url'], caption=info_str, parse_mode='HTML', reply_markup=markup)


# -----------------------------------------------------------------------

def get_raccoonURL():
    url = ""
    req = requests.get('https://some-random-api.ml/animal/raccoon')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
        # url.split("/")[-1]
    return url

def get_eth():
    url = requests.get('https://mainfin.ru/crypto/ethereum')
    b = bs4.BeautifulSoup(url.text, "html.parser")
    url1 = b.select(".crypto_curr_val")
    url_print = url1[0].getText()
    a = 'Средневзвешенный курс\nETH - '
    a = str(a + url_print)
    return a


def get_gas():
    url = requests.get('https://etherchain.org/tools/gasnow')  # подставляем url
    b = bs4.BeautifulSoup(url.text, "html.parser")
    url1 = b.select(".info-item-body")
    url_print = url1[0].getText()
    d = str(url_print)
    return d


# -----------------------------------------------------------------------
def get_weather():
    from yaweather import Russia, YaWeather

    y = YaWeather(
        api_key='7a4600f8-b028-4278-baf2-b06c443f01f4')  # Мой ключ АПИ, но лучше создай свой тут - https://developer.tech.yandex.ru/services/18

    res = y.forecast(Russia.SaintPetersburg)  # Указываешь местоположение

    for f in res.forecasts:
        day = f.parts.day_short
        b = (f'{f.date} | {day.temp} °C, {day.condition}')
        return b # То, что выведет функция


# -----------------------------------------------------------------------
def get_ManOrNot(chat_id):
    global bot

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Проверить",
                                      url="https://vc.ru/dev/58543-thispersondoesnotexist-sayt-generator-realistichnyh-lic")
    markup.add(btn1)

    req = requests.get("https://thispersondoesnotexist.com/image", allow_redirects=True)
    if req.status_code == 200:
        img = BytesIO(req.content)
        bot.send_photo(chat_id, photo=img, reply_markup=markup, caption="Этот человек реален?")


# ---------------------------------------------------------------------
def get_randomFilm():
    url = 'https://randomfilm.ru/'
    infoFilm = {}
    req_film = requests.get(url)
    soup = bs4.BeautifulSoup(req_film.text, "html.parser")
    result_find = soup.find('div', align="center", style="width: 100%")
    infoFilm["Наименование"] = result_find.find("h2").getText()
    names = infoFilm["Наименование"].split(" / ")
    infoFilm["Наименование_rus"] = names[0].strip()
    if len(names) > 1:
        infoFilm["Наименование_eng"] = names[1].strip()

    images = []
    for img in result_find.findAll('img'):
        images.append(url + img.get('src'))
    infoFilm["Обложка_url"] = images[0]

    details = result_find.findAll('td')
    infoFilm["Год"] = details[0].contents[1].strip()
    infoFilm["Страна"] = details[1].contents[1].strip()
    infoFilm["Жанр"] = details[2].contents[1].strip()
    infoFilm["Продолжительность"] = details[3].contents[1].strip()
    infoFilm["Режиссёр"] = details[4].contents[1].strip()
    infoFilm["Актёры"] = details[5].contents[1].strip()
    infoFilm["Трейлер_url"] = url + details[6].contents[0]["href"]
    infoFilm["фильм_url"] = url + details[7].contents[0]["href"]

    return infoFilm


# ---------------------------------------------------------------------


bot.polling(none_stop=True, interval=0)  # Запускаем бота

print()
