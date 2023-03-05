import telebot
import requests
from conf import *

bot = telebot.TeleBot(TOKEN2)

user = {}
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привіт! Введіть своє ім'я користувача:")
    bot.register_next_step_handler(message, ask_password)

def ask_password(message):
    username = message.text
    user['username'] = username
    bot.reply_to(message, "Дякую! Тепер, будь ласка, введіть свій пароль:")
    bot.register_next_step_handler(message, save_password)

def save_password(message):
    password = message.text
    user['password'] = password
    user['telegram_id'] = message.chat.id
    bot.reply_to(message, 'Дякую! Ваші дані для входу збережено. Щоб ми могли повідомити вас про покупку ваших/інших акаунтів надішліть повідомлення "/start" цьому боту: http://t.me/n0tlflcatl0ns_bot')
    bot.reply_to(message, " Якщо ви успішно продали свій продукт, надішліть мені його назву, але майте на увазі, щоб користуватись цією функцією покупець акаунту повинен перший підтвердити покупку.")
    requests.post('http://127.0.0.1:8000/users/', user)

@bot.message_handler(commands=['buyed'])
def ask_name(message):
    bot.reply_to(message, "Введіть назву облікового запису який ви хочете купити:")
    bot.register_next_step_handler(message, check_account)

def check_account(message):
    requests.get(f'http://127.0.0.1:8000/sel_prod/{message.text}')
    bot.reply_to(message, "Дякую! Обліковий запис додано до категорії проданих")

@bot.message_handler(commands=['report'])
def ask_name(message):
    bot.reply_to(message, "Будь ласка, введіть ім'я користувача, який вас ошукав")
    bot.register_next_step_handler(message, check_profile)

def check_profile(message):
    requests.get(f'http://127.0.0.1:8000/report/{message.text}')
    bot.reply_to(message, "Дякую за інформацію я відправив скаргу на цього користувача.")

@bot.message_handler(func=lambda m: True)
def delete_product(message):
    r = requests.get(f'http://127.0.0.1:8000/del_prod/{message.chat.id}/{message.text}')
    if r.text == '400':
        bot.reply_to(message, "Невірне ім'я")
    elif r.text == '401':
        bot.reply_to(message, "Покупець акаунту ще не підтвердив цю покупку")
    else:
        bot.reply_to(message, 'Успішно продано.')
# start the bot
bot.polling()
