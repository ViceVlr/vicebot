import time

def dz1(bot, chat_id):
    dz1_ResponseHandler = lambda message: bot.send_message(chat_id, f'Привет, {message.text}!')
    my_input(bot, chat_id, 'Введите ваше имя:', dz1_ResponseHandler)

#-------------------------------------------------------------------------------------------------

def dz2(bot, chat_id):
    def dz2_ResponseHandler(bot, chat_id, age_int):
        bot.send_message(chat_id, text=f"Вам {age_int} лет!")

    my_inputInt(bot, chat_id, "Сколько вам лет?", dz2_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz3(bot, chat_id):
    dz3_ResponseHandler = lambda message: bot.send_message(chat_id, f"{message.text*5}")
    my_input(bot, chat_id, 'Введите ваше имя:', dz3_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz45(bot, chat_id):
    def dz45_ResponseHandler(bot, chat_id, age):
        if 0 < age < 7:
            bot.send_message(chat_id, "Почему ты не в садике")
        if 8 < age < 18:
            bot.send_message(chat_id, "Иди делай уроки <3")
        if age > 19:
            bot.send_message(chat_id, "Какого это жить в ваши " + str(age) + "?")

    my_inputInt(bot, chat_id, "Введите возраст.", dz45_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz6(bot, chat_id):
    dz6_ResponseHandler = lambda message: bot.send_message(chat_id, f"Привет, {message.text}! Смотри \n"
                                                                    f"{str(message.text[1:len(message.text) - 1:])}\n"
                                                                    f"{str(message.text[::-1])}\n"
                                                                    f"{str(message.text[-3::])}\n"
                                                                    f"{str(message.text[:5:])}\n")
    my_input(bot, chat_id, 'Введите ваше имя:', dz6_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz7n(bot, chat_id):
    dz7n_ResponseHandler = lambda message : bot.send_message(chat_id, f"Привет, {message.text}! Смотри \n"
                                                                      f"Длина вашего имени: " + f"{str(len(message.text))}\n")

    my_input(bot, chat_id, "Введите ваше имя: ", dz7n_ResponseHandler)


def dz7a(bot, chat_id):
    def dz7a_ResponseHandler(bot, chat_id, age):
        bot.send_message(chat_id, "Сумма символов в вашем имени: " + str((age // 10) + (age % 10)))
        bot.send_message(chat_id, "Произведение символов в вашем имени: " + str((age // 10) * (age % 10)))

    my_inputInt(bot, chat_id, "Введите возраст.", dz7a_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz8(bot, chat_id):
    dz8_ResponseHandler = lambda message : bot.send_message(chat_id, f"Привет, {message.text}! Смотри \n"
                                                                         f"{str.upper(message.text)}\n"
                                                                         f"{str.lower(message.text)}\n"
                                                                         f"{str.upper(message.text)[0:1:] + str.lower(message.text)[1::]}\n"
                                                                         f"{str.lower(message.text)[0:1:] + str.upper(message.text)[1::]}\n")
    my_input(bot, chat_id, 'Введите ваше имя:', dz8_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz92(bot, chat_id):
    def dz92_ResponseHandler(bot, chat_id, age):
        if age > 150 or age < 0 :
            bot.send_message(chat_id, 'Ошибка, такого возраста не существует!')
        else:
            bot.send_message(chat_id, 'В возрасте нет ошибок')

    my_inputInt(bot, chat_id, 'Введите возраст: ', dz92_ResponseHandler)

def dz91(bot, chat_id):
    def dz91_ResponseHandler(bot, chat_id, name):
        spaces = 0
        for i in range(0, len(name)) :
            if name[i] == ' ' :
                spaces += 1
                break
            else :
                spaces = 0
        if spaces == 0 :
            bot.send_message(chat_id, 'В имени нет ошибок')
        else :
            bot.send_message(chat_id, 'В имени есть ошибка.')

    my_inputStr(bot, chat_id, 'Введите имя: ', dz91_ResponseHandler)

#--------------------------------------------------------------------------------------------------

def dz10(bot, chat_id):
    bot.send_message(chat_id, 'Приветствую вас на шоу кто хочет стать миллионером!')
    bot.send_message(chat_id, 'Вопрос на миллион рублей:')
    bot.send_message(chat_id, '.')
    bot.send_message(chat_id, '..')
    bot.send_message(chat_id, '...')
    bot.send_message(chat_id, 'Сколько будет 2+2*2?')

    def dz10_ResponseHandler(bot, chat_id, ans):
        if ans == 6 :
            bot.send_message(chat_id, '.')
            bot.send_message(chat_id, '..')
            bot.send_message(chat_id, '...')
            bot.send_message(chat_id, '🧠Вы ответили верно! Ваше IQ больше 10! Поздравляю!🧠')
        elif ans == 8 :
            bot.send_message(chat_id, '.')
            bot.send_message(chat_id, '..')
            bot.send_message(chat_id, '...')
            bot.send_message(chat_id, "❌🧠 0_0")
        else :
            bot.send_message(chat_id, '.')
            bot.send_message(chat_id, '..')
            bot.send_message(chat_id, '...')
            bot.send_message(chat_id, 'Поздравляем! Ошибка 🥲')

    my_inputInt(bot, chat_id, "Иии ваш ответ???", dz10_ResponseHandler)
















#дописать
def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)

def my_inputInt(bot, chat_id, txt, ResponseHandler):

    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)

def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        var_int = int(message.text)
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                         text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)

def my_inputStr(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputStr_SecondPart, botQuestion=bot, txtQuestion=txt,
                                   ResponseHandler=ResponseHandler)

def my_inputStr_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id

    var_str = str(message.text)
    ResponseHandler(botQuestion, chat_id, var_str)
