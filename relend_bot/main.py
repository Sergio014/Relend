import telebot

bot = telebot.TeleBot('6295344637:AAE92oTYx_MMyfR-8alyLgNa_goxi0ulTSw')

# define a dictionary to store the username and password for each user
users = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi there! Please enter your username:")
    bot.register_next_step_handler(message, ask_password)

def ask_password(message):
    username = message.text
    chat_id = message.chat.id
    users[chat_id] = {'username': username}
    bot.reply_to(message, "Thanks! Now please enter your password:")
    bot.register_next_step_handler(message, save_password)

def save_password(message):
    password = message.text
    chat_id = message.chat.id
    users[chat_id]['password'] = password
    bot.reply_to(message, "Thanks! Your login information has been saved.")
    print(users)

# start the bot
bot.polling()
