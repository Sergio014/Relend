from django.core.management.base import BaseCommand
from first_app import api

import dotenv
import json
import telebot
import os


dotenv.load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN1'))
user = {}

def send_to_buned_user(telegram_id):
    bot.send_message(telegram_id, 'Ваш акаунт був заблокований через погану поведінку')

def delete_message_after_button(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

def send_notification_to_owner(account, owner, buyer, status):
    keyboard = telebot.types.InlineKeyboardMarkup()
    sold = telebot.types.InlineKeyboardButton(
        text="ПРОДАНО", 
        callback_data=json.dumps({
            'buyer': buyer.id,
            'owner': owner.id,
            'account_id': account.id,
        })
    )
    report = telebot.types.InlineKeyboardButton(text=f"СКАРГА", 
                                                callback_data=json.dumps({'report_user': buyer.user.username}))
    keyboard.add(sold, report)
    
    bot.send_message(owner.telegram_id, parse_mode='HTML', reply_markup=keyboard,
                text=f"""Ваш продукт {account.name} хоче придбати цей користувач: <a href='tg://user?id={buyer.telegram_id}'>{buyer.user.username}</a> Рейтинг користувача: {status}""")
    
def send_notification_to_buyer(account, owner, buyer):
    keyboard = telebot.types.InlineKeyboardMarkup()
    sold = telebot.types.InlineKeyboardButton(text="Так", 
                                              callback_data=json.dumps({
                                                'confirmed': True,
                                                'account_id': account.id,
                                                }))
    report = telebot.types.InlineKeyboardButton(text=f"СКАРГА", callback_data=json.dumps({'report_user': owner.user.username}))
    keyboard.add(sold, report)

    bot.send_message(buyer.telegram_id, parse_mode='HTML', reply_markup=keyboard,
                text=f'''Ви купили {account.name} у цього користувача: <a href="tg://user?id={owner.telegram_id}">{owner.user.username}</a>?''')

def succesfully_sold(telegram_id):
    bot.send_message(telegram_id, 'Вітаю, ваш акаунт успішно продано :)')

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    delete_message_after_button(call)
    data = json.loads(call.data)
    if 'confirmed' in data:
        bot.send_message(call.message.chat.id, api.del_account(pk=data['account_id']))
    elif 'account_id' in data:
        bot.send_message(call.message.chat.id, 
                         api.confirm_sale(data['account_id'], data['buyer'], data['owner']))
    elif 'report_user' in data:
        bot.send_message(call.message.chat.id, api.report_user(username=data['report_user']))


@bot.message_handler(commands=['start'])
def get_username(message):
    bot.reply_to(message, "Привіт! Щоб авторизуватися, будь ласка, введіть своє ім'я користувача:")
    bot.register_next_step_handler(message, get_password)

def get_password(message):
    username = message.text
    user['username'] = username
    bot.reply_to(message, "Дякую! Тепер, будь ласка, введіть свій пароль:")
    bot.register_next_step_handler(message, check_data)

def check_data(message):
    password = message.text
    if api.register_telegram_user(user['username'], password, message.chat.id):
        bot.reply_to(message, '''Ви успішно увійшли у свій акаунт, можете спокійно повертатись до сайту.''')
    else:
        bot.reply_to("Неправильне ім'я або пароль, надішліть /start щоб спробувати знову")

class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'
    
    def handle(self, *args, **kwargs):
            bot.enable_save_next_step_handlers()
            bot.load_next_step_handlers()
            bot.infinity_polling()