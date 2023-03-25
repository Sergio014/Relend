import telebot
import os

from dotenv import load_dotenv


load_dotenv()

bot = telebot.TeleBot(os.getenv('TOKEN1'))

def send_buyer(account, owner, buyer, status):
	bot.send_message(owner.telegram_id, parse_mode='HTML', text=f"Ваш продукт {account.name} хоче придбати цей користувач: <a href='tg://user?id={buyer.telegram_id}'>{buyer.user.username}</a> Рейтинг користувача: {status} Якщо ви продали свій обліковий запис, надішліть його ім'я цьому <a href='http://t.me/relend_bot'>боту</a>, або якщо вас ошукали, надішліть /report також цьому <a href='http://t.me/relend_bot'>боту</a>")
	bot.send_message(buyer.telegram_id, parse_mode='HTML', text=f'Ви купили {account.name} у цього користувача: <a href="tg://user?id={owner.telegram_id}">{owner.user.username}</a>? Якщо ви купили обліковий запис, надішліть /buyed цьому <a href="http://t.me/relend_bot">боту</a>, або якщо вас ошукали, надішліть /report також цьому <a href="http://t.me/relend_bot">боту</a>.')
