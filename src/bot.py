import os
import telebot


BOT = telebot.TeleBot(
    os.environ['STRANGER_BOT_TOKEN'], parse_mode='HTML'
)