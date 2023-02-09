import telebot
import config
import os
import time
import write_text as wt

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    received_message = bot.send_message(
        message.chat.id, f"Привет, {message.from_user.first_name}!\nЯ телеграм бот, который нанести текст на валентинку\nНапиши \'/next\', чтобы начать")
    bot.register_next_step_handler(received_message, get_from_to_text)


@bot.message_handler(commands=['next'])
def get_from_to_text(message):
    received_message = bot.send_message(
        message.chat.id, "Итак напиши мне КОМУ валентинка, ОТ КОГО она и КАКОЙ на ней должен быть ТЕКСТ, обязательно соблюдай следующий формат иначе получится некрасиво)\n\nФОРМАТ:\nПОЛИНЕ_ВОВЫ_Я ТЕБЯ ЛЮБЛЮ\n\n !Без смайликов!(Иначе будут ??? вместо них)")
    bot.register_next_step_handler(received_message, write_and_send)


def write_and_send(message):
    max_len = 20  # поменять макс длинну
    help_tup = wt.separation_text(message.text)
    if len(help_tup[2]) <= max_len:
        try:
            file_path = wt.write_on_image(
                message.text, int(message.from_user.id))
            with open(file_path, "rb") as img:
                print(
                    f"File: {file_path}; Text: {message.text}; User: {message.from_user.first_name}; User_ID: {message.from_user.id}")
                bot.send_document(message.chat.id, img)
            os.remove(file_path)
        except:
            error(message)
        welcome(message)
    else:
        error(message)


def error(message):
    bot.send_message(
        message.chat.id, "Произошла ошибочка. Возможно:\n1) Ты отправил(а), что-то не то\n2)Слишком большая длина строки\n")
    welcome(message)


while True:
    try:
        print("Bot Start!")
        bot.polling(none_stop=True)
    except:
        print("Some problem, restart")
        time.sleep(15)
