import telebot
import requests
from conf import *

bot = telebot.TeleBot(TOKEN2)

user = {}
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi there! Please enter your username:")
    bot.register_next_step_handler(message, ask_password)

def ask_password(message):
    username = message.text
    user['username'] = username
    bot.reply_to(message, "Thanks! Now please enter your password:")
    bot.register_next_step_handler(message, save_password)

def save_password(message):
    password = message.text
    user['password'] = password
    user['telegram_id'] = message.chat.id
    bot.reply_to(message, 'Thanks! Your login information has been saved. Please send "/start" message this bot: http://t.me/n0tlflcatl0ns_bot')
    bot.reply_to(message, " If you succesfuly selled your product send me it name")
    requests.post('http://127.0.0.1:8000/users/', user)
    
@bot.message_handler(func=lambda m: True)
def delete_product(message):
    requests.get(f'http://127.0.0.1:8000/del_prod/{message.text}')
    bot.reply_to(message, 'Succesfuly deleted')
# start the bot
bot.polling()
