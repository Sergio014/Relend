from django.core.management.base import BaseCommand

import dotenv
import telebot
import requests
import os

from first_app import api

dotenv.load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN1'))
user = {}

def send_buyer(account, owner, buyer, status):
	bot.send_message(owner.telegram_id, parse_mode='HTML', 
                text=f"""Ваш продукт {account.name} хоче придбати цей користувач: 
                <a href='tg://user?id={buyer.telegram_id}'>{buyer.user.username}</a> 
                Рейтинг користувача: {status} Якщо ви продали свій обліковий запис, просто
                надішліть його ім'я, або якщо вас ошукали, надішліть мені /report.""")
	bot.send_message(buyer.telegram_id, parse_mode='HTML', 
                text=f'''Ви купили {account.name} у цього користувача: 
		        <a href="tg://user?id={owner.telegram_id}">{owner.user.username}</a>? 
                Якщо ви купили обліковий запис, надішліть мені /buyed,
                або якщо вас ошукали, надішліть мені /report.''')

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
    if api.register_telegram_user(user['username'], password, message.chat.id):
        bot.reply_to(message, 'Дякую! Ваші дані для входу збережено. Щоб ми могли повідомити вас про покупку ваших/інших акаунтів надішліть повідомлення "/start" цьому боту: http://t.me/n0tlflcatl0ns_bot')
        bot.reply_to(message, " Якщо ви успішно продали свій продукт, надішліть мені його назву, але майте на увазі, щоб користуватись цією функцією покупець акаунту повинен перший підтвердити покупку.")
    else:
        bot.reply_to("Неправильне ім'я або пароль")

@bot.message_handler(commands=['buyed'])
def ask_name(message):
    bot.reply_to(message, "Введіть назву облікового запису який ви хочете купити:")
    bot.register_next_step_handler(message, check_account)

def check_account(message):
    api.add_sold_state(message.chat.id, message.text)
    bot.reply_to(message, "Дякую! Обліковий запис додано до категорії проданих")

@bot.message_handler(commands=['report'])
def ask_name(message):
    bot.reply_to(message, "Будь ласка, введіть ім'я користувача, який вас ошукав")
    bot.register_next_step_handler(message, check_profile)

def check_profile(message):
    api.report_user(message.text)
    bot.reply_to(message, "Дякую за інформацію я відправив скаргу на цього користувача.")

@bot.message_handler(func=lambda m: True)
def delete_account(message):
    bot.reply_to(message, )

class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'
    
    def handle(self, *args, **kwargs):
            bot.enable_save_next_step_handlers()
            bot.load_next_step_handlers()
            bot.infinity_polling()