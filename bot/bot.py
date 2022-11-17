
import telebot
from telebot import types
import requests
import json
import datetime

token = '5364518161:AAGm_JkM-h6LFBb4ZOKaxt0StrabQE6RmxU'

weather_api_key = 'a20597ec83b5f2e21e30e41f03be89f9'

qstn = dict()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def hello_message(message):
    bot.send_message(message.chat.id, "шалом, православные")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'помоги себе сам\n Я умею узнавать погоду, администрировать чат \n Если взаимодействие требует запроса, нужно вызывать команду реплаем на сообщение с запросом', reply_to_message_id=message.message_id)
    bot.reply_to(message, '')

@bot.message_handler(commands=['get_out'])
def get_out_message(message):
    bot.send_message(message.chat.id, "пока")
    bot.leave_chat(message.chat.id)

@bot.message_handler(commands=['make_admin'])
def make_admin_message(message):
    if not message.reply_to_message:
        return bot.reply_to(message, 'Нужно отправить эту команду в ответ на сообщение пользователя, которого хотим сделать админом')
    bot.promote_chat_member(message.chat.id, message.reply_to_message.from_user.id, can_change_info=True, can_delete_messages=True, can_invite_users=True, can_restrict_members=True, can_pin_messages=True, can_promote_members=True)
    bot.send_message(message.chat.id, "шалом новому админу")

@bot.message_handler(commands=['ban'])
def ban_message(message):
    if not message.reply_to_message:
        return bot.reply_to(message, 'Нужно отправить эту команду в ответ на сообщение пользователя, которого хотим забанить')
    bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    bot.send_message(message.chat.id, "забанен")


@bot.message_handler(commands=['unban'])
def unban_message(message):
    if not message.reply_to_message:
        return bot.reply_to(message, 'Нужно отправить эту команду в ответ на сообщение пользователя, которого хотим разбанить')
    bot.unban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    bot.send_message(message.chat.id, "разбанен")

@bot.message_handler(commands=['stats'])
def stats_message(message):
    bot.send_message(message.chat.id, "всего пользователей: " + str(bot.get_chat_members_count(message.chat.id)))
    bot.send_message(message.chat.id, "всего админов: " + str(len(bot.get_chat_administrators(message.chat.id))))


@bot.message_handler(content_types=['new_chat_members'])
def new_member(message):
    res = bot.reply_to(message, "Шалом, " + message.new_chat_members[0].first_name + "!\n Сколько раз фраза Around the world была употреблена в треке Daft Punk - Around the world?")
    qstn[res.id] = message.new_chat_members[0].username


@bot.message_handler(commands=['set_photo'])
def set_photo_message(message):
    if not message.reply_to_message:
        return bot.reply_to(message, 'Нужно отправить эту команду в ответ на сообщение в котором будет фото чата')
    bot.set_chat_photo(message.chat.id, bot.get_file_url(message.reply_to_message.text))


@bot.message_handler(commands=['set_title'])
def set_title_message(message):
    if not message.reply_to_message:
        return bot.reply_to(message, 'Нужно отправить эту команду в ответ на сообщение в котором будет название чата')
    bot.set_chat_title(message.chat.id, message.reply_to_message.text)

@bot.message_handler(commands=['get_weather'])
def get_weather(message):
    if not message.reply_to_message:
        return bot.reply_to(message, 'Нужно отправить эту команду в ответ на сообщение в котором будет название города')
    res = json.loads(requests.get("http://api.openweathermap.org/data/2.5/weather?q=" + message.reply_to_message.text + "&appid=" + weather_api_key + "&units=metric").text)

    if 'weather' not in res:
        return bot.reply_to(message, 'Город не найден')

    response = 'Погода:' + res['weather'][0]['description'] + '\n' + 'Температура:' + str(res['main']['temp']) + '\n' + 'Влажность:' + str(res['main']['humidity']) + '%' + '\n' + 'Давление:' + str(res['main']['pressure']) + 'кПА \n' + 'Скорость ветра:' + str(res['wind']['speed']) + 'м/с \n'
    if 'rain' in res:
        response += 'Осадки(мм за последний час):' + str(res['rain']['1h'])
    if 'snow' in res:
        response += 'Снег(мм за последний час):' + str(res['snow']['1h'])
    if 'clouds' in res:
        response += 'Облачность:' + str(res['clouds']['all']) + '%' + '\n'
    if 'sys' in res:
        response += 'Восход по Гринвичу: ' + datetime.datetime.fromtimestamp(res['sys']['sunrise']).strftime('%Y-%m-%d %H:%M:%S') + '\n' + 'Закат по Гринвичу:' + datetime.datetime.fromtimestamp(res['sys']['sunset']).strftime('%Y-%m-%d %H:%M:%S')
    bot.reply_to(message, response)

@bot.message_handler(content_types='text')
def message_reply(message):
    if "Артём" in message.text or "артём" in message.text or "Артем" in message.text or "артем" in message.text:
        bot.send_message(message.chat.id, "дуралей")
    if message.reply_to_message and message.reply_to_message.id in qstn and qstn[message.reply_to_message.id] == message.from_user.username:
        if message.text == "144" or message.text == "144.":
            bot.reply_to(message, "Правильно! \n Work it harder, make it better \nDo it faster, makes us stronger \nMore than ever, hour after hour \n Work is never over")
            del qstn[message.reply_to_message.id]
        else:
            bot.reply_to(message, "Неправильно! \n It's not your fault I was being too demanding \n I must admit, it's my pride that made me distant \n All because I hoped that you'd be someone different")
            del qstn[message.reply_to_message.id]

bot.polling(none_stop=True, interval=0)
