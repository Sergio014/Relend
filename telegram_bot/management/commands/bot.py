from django.core.management.base import BaseCommand
from first_app import api
from .text import text_dict 
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
import dotenv
import json
import telebot
from telebot import types
import os


dotenv.load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN1'))
user = {}

def send_to_buned_user(telegram_id, language):
    bot.send_message(telegram_id, text_dict[language]['account_blocked'])

def delete_message_after_button(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

def send_notification_to_owner(account, owner, buyer, status):
    lan = owner.language
    keyboard = telebot.types.InlineKeyboardMarkup()
    sold = telebot.types.InlineKeyboardButton(
        text="✅", 
        callback_data=json.dumps({
            'buyer': buyer.id,
            'owner': owner.id,
            'account_id': account.id,
        })
    )
    back = telebot.types.InlineKeyboardButton(
        text="❌", 
        callback_data=json.dumps({
            'back': True,
        })
    )
    report = telebot.types.InlineKeyboardButton(text=f"REPORT", 
                                                callback_data=json.dumps({'report_user': buyer.user.username, 'lan': owner.language}))
    keyboard.add(sold, report, back)
    
    bot.send_message(owner.telegram_id, parse_mode='HTML', reply_markup=keyboard,
                text=text_dict[lan]['owner'].format(account=account, buyer=buyer, status=status))
    
def send_notification_to_buyer(account, owner, buyer):
    lan = buyer.language
    keyboard = telebot.types.InlineKeyboardMarkup()
    sold = telebot.types.InlineKeyboardButton(text="✅", 
                                              callback_data=json.dumps({
                                                'confirmed': True,
                                                'account_id': account.id,
                                                }))
    back = telebot.types.InlineKeyboardButton(
        text="❌", 
        callback_data=json.dumps({
            'back': True,
        })
    )
    report = telebot.types.InlineKeyboardButton(text=f"Report", callback_data=json.dumps({'report_user': owner.user.username, 'lan': buyer.language}))
    keyboard.add(sold, report, back)

    bot.send_message(buyer.telegram_id, parse_mode='HTML', reply_markup=keyboard,
                text=text_dict[lan]['buyer'].format(account=account, owner=owner))

def succesfully_sold(telegram_id, language):
    bot.send_message(telegram_id, text_dict[language]['sold_message'])

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
        bot.send_message(call.message.chat.id, api.report_user(username=data['report_user'], language=data['lan']))
    elif 'back' in data:
        pass


@bot.message_handler(commands=['start'])
def get_language(message):
    markup = ReplyKeyboardMarkup(row_width=2)
    markup.add(KeyboardButton('English'), KeyboardButton('Українська'), KeyboardButton('Руский'))
    bot.send_message(message.chat.id, "Please select a language:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text.startswith('Українська'))
def get_username_ua(message):
    bot.reply_to(message, "Привіт! Щоб авторизуватися, будь ласка, введіть своє ім'я користувача", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_password_ua)

def get_password_ua(message):
    username = message.text
    user['username'] = username
    bot.reply_to(message, "Дякую! Тепер, будь ласка, введіть свій пароль:")
    bot.register_next_step_handler(message, check_data_ua)

def check_data_ua(message):
    password = message.text
    if api.register_telegram_user(user['username'], password, message.chat.id, 'ua'):
        bot.reply_to(message, '''Ви успішно увійшли у свій акаунт, можете спокійно повертатись до сайту.''')
    else:
        bot.reply_to(message, "Неправильне ім'я або пароль, надішліть /start щоб спробувати знову")

@bot.message_handler(func=lambda message: message.text.startswith('English'))
def get_username(message):
    bot.reply_to(message, "Hello! To authorize, please enter your username:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_password_en)

def get_password_en(message):
    username = message.text
    user['username'] = username
    bot.reply_to(message, "Thank you! Now, please enter your password:")
    bot.register_next_step_handler(message, check_data_en)

def check_data_en(message):
    password = message.text
    if api.register_telegram_user(user['username'], password, message.chat.id, 'en'):
        bot.reply_to(message, '''You have successfully logged into your account, you can safely return to the site.''')
    else:
        bot.reply_to(message, "Incorrect username or password, send /start to try again")

@bot.message_handler(func=lambda message: message.text.startswith('Руский'))
def get_username(message):
    bot.reply_to(message, "Привет! Чтобы авторизоваться, пожалуйста, введите свое имя пользователя:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, get_password_ru)

def get_password_ru(message):
    username = message.text
    user['username'] = username
    bot.reply_to(message, "Спасибо! Теперь, пожалуйста, введите свой пароль:")
    bot.register_next_step_handler(message, check_data_ru)

def check_data_ru(message):
    password = message.text
    if api.register_telegram_user(user['username'], password, message.chat.id, 'ru'):
        bot.reply_to(message, '''Вы успешно вошли в свою учетную запись, можете смело возвращаться на сайт.''')
    else:
        bot.reply_to(message, "Неправильное имя или пароль, отправьте /start чтобы попробовать снова")

class Command(BaseCommand):
    help = 'Implemented to Django application telegram bot setup command'
    
    def handle(self, *args, **kwargs):
            bot.enable_save_next_step_handlers()
            bot.load_next_step_handlers()
            bot.infinity_polling()