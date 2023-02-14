import telebot
import config
import os
import time
import write_text as wt
import csv
import sys


from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    if message.content_type != 'text':
        error(message)
    else:
        received_message = bot.send_message(
            message.chat.id, f"Привет, {message.from_user.first_name}!\nЯ телеграм бот, который нанесёт текст на валентинку\nНапиши \'/next\', чтобы начать")
        bot.register_next_step_handler(received_message, get_from_to_text)


@bot.message_handler(commands=['next'])
def get_from_to_text(message):
    if message.content_type != 'text':
        error(message)
    else:
        write_in_file = True
        with open("users.csv", "r", encoding="utf-8") as file:
            readerder = csv.reader(file, delimiter=",")
            for row in readerder:
                if row[1] == str(message.from_user.id):
                    write_in_file = False
        if write_in_file:
            print(
                f"Новый пользователь -> {message.from_user.first_name} -> ID: {message.from_user.id}")
            with open("users.csv", "a", newline="", encoding="utf-8") as file:
                printer = csv.writer(file, delimiter=",")
                printer.writerow([
                    message.from_user.first_name,
                    message.from_user.id,
                    message.chat.id
                ])
        markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
        if message.from_user.id == 765103434:
            markup.add(types.KeyboardButton("Send_GoodBye"))
        received_message = bot.send_message(
            message.chat.id, "Итак напиши мне КОМУ валентинка, ОТ КОГО она и КАКОЙ на ней должен быть ТЕКСТ, обязательно соблюдай следующий формат иначе получится некрасиво)\n\nФОРМАТ:\nПолине_Вовы_Я тебя люблю\n\n !Без смайликов!(Иначе будут ??? вместо них)\nТакже не пиши слишком большое сообщение, иначе будет не очень красиво)\nНижние подчёркивания обязательно!(Маше_Пети_)", reply_markup=markup)
        bot.register_next_step_handler(received_message, write_and_send)


def write_and_send(message):
    if message.content_type != 'text':
        error(message)
    else:
        if message.text == "Send_GoodBye":
            send_goodbye(message)
        else:
            if not wt.check_input_format(message.text):
                error(message)
            else:
                max_len = 16  # поменять макс длинну
                help_tup = wt.separation_text(message.text)
                if len(help_tup[2]) > 95:
                    error(message)
                else:
                    try:
                        file_path = wt.write_on_image(
                            f"{help_tup[0]}_{help_tup[1]}_{wt.check_lenght_str(help_tup[2], max_len)}", int(message.from_user.id))
                        with open(file_path, "rb") as img:
                            bot.send_document(message.chat.id, img)
                            print(
                                f"File: {file_path}; Text: {message.text}; User: {message.from_user.first_name}; User_ID: {message.from_user.id}")
                        os.remove(file_path)
                        welcome(message)
                    except:
                        error(message)


def error(message):
    if message.content_type != 'text':
        bot.send_message(
            message.chat.id, "Не нужно мне отправлять что-то не похожее на текст пожалуйста\n*робот злиться*")
    received_message = bot.send_message(
        message.chat.id, "Произошла ошибочка. Возможно:\n1) Ты отправил(а), что-то не то\n2) Ты отправил(а) не в правильном формате\n3) Слишком большой текс поздравления\n\nНапиши '/start', чтобы продолжить")
    bot.register_next_step_handler(received_message, welcome)


def send_goodbye(message):
    if message.content_type != 'text':
        error(message)
    else:
        if message.from_user.id == 765103434:
            with open("send_goodbye.txt", "r", encoding="utf-8") as file:
                text = ""
                for line in file:
                    text += line
            with open("users.csv", "r", encoding="utf-8") as file:
                readerder = csv.reader(file, delimiter=",")
                for row in readerder:
                    try:
                        bot.send_message(row[2], text)
                        print(f"Send goodbye to {row[2]}")
                    except:
                        pass
        else:
            error(message)


while True:
    try:
        print("Bot Start!")
        bot.infinity_polling()
    except:
        print("Some problem, restart")
        time.sleep(10)
