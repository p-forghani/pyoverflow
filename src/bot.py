import os
import telebot


BOT = telebot.TeleBot(
    os.environ['PYOVERFLOW_BOT_TOKEN'], parse_mode='HTML'
)
