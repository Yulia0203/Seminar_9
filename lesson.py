import telebot
import requests
import time
import math, re
from telebot import types
import random
import logging

global num
global count
count = 0
num = random.randint(1,1000)

bot = telebot.TeleBot("TOKEN", parse_mode=None)

telebot.logger.setLevel(logging.INFO)

storage = dict()

def init_storage(user_id):
    storage[user_id] = dict(attempt=None, random_digit=None)

def set_data_storage(user_id, key, value):
    storage[user_id][key] = value

def get_data_storage(user_id):
    return storage[user_id]

   
@bot.message_handler(commands=['start', 'help', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing")

@bot.message_handler(content_types=["text"])
def hello_user(message):
    if 'привет' in message.text:
        bot.reply_to(message, 'привет, ' + message.from_user.first_name)
    elif message.text.lower() == 'как дела?':
        bot.send_message(message.chat.id, 'хорошо')
    # elif message.text == 'играть':
    #     bot.reply_to(message, 'хочешь поиграть?')
    elif message.text == 'погода':
        r = requests.get('https://wttr.in/?0T')
        bot.reply_to(message, r.text)
    elif message.text == 'котик':
        r = f'https://cataas.com/cat?t=${time.time()}'
        bot.send_photo(message.chat.id, r)
    elif message.text == 'собачка':
        r = f'https://images.dog.ceo/breeds/labradoodle/Cali.jpg'
        bot.send_photo(message.chat.id, r)
    elif message.text == 'файл':
        data = open('user_message.txt', encoding='utf-8')
        bot.send_document(message.chat.id, data)
        data.close()
    elif message.text.lower() == 'посчитать':
        r = bot.send_message(message.chat.id, 'Что нужно посчитать?')
        bot.register_next_step_handler(r, Calc)
    elif message.text.lower() == 'играть':
        r = bot.send_message(message.chat.id, 'Я загадал число от 1 до 1000, угадай число...)')
        bot.register_next_step_handler(r, Game)
    
def Calc(message):
    if '+' in message.text or '*' in message.text or '/' in message.text or '-' in message.text:
        do = str(eval(str(message.text)))
        bot.send_message(message.chat.id, f'{do}')
    else:
        bot.send_message(message.chat.id, 'Некорректный ввод')

def Game(message):
    global num
    global count
    count +=1
    if int(message.text) > num:        
        a = bot.send_message(message.chat.id, "Число должно быть меньше! Попробуй еще раз") 
        bot.register_next_step_handler(a, Game)
    elif int(message.text) < num:         
        b = bot.send_message(message.chat.id, "Число должно быть больше! Попробуй еще раз") 
        bot.register_next_step_handler(b, Game)
    else:         
        bot.send_message(message.chat.id, f"Ты угадал, это число = {num}, количество попыток {count}")     


# @bot.message_handler(func=lambda m: True)
# def echo_all(message):
   

bot.infinity_polling()


