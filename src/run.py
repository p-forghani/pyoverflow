import telebot
from loguru import logger
from bot import BOT

from constants import keyboards
from filters import IsAdmin
from utils.io import write_json

class Bot:
    """Telegram bot to connect 2 strangers to randomly talk
    """
    def __init__(self, telebot: telebot.TeleBot):
        # Build the bot
        self.bot = telebot

        # Register the handlers
        self.handlers()

    def run(self):
        logger.info("Bot starting...")
        self.bot.infinity_polling()

    def handlers(self):
        @self.bot.message_handler(is_admin=True)
        def is_admin(message):
            self.bot.send_message(
                message.chat.id,
                'You are admin of this group!'
            )

        @self.bot.message_handler(func=lambda _: True)
        def echo_all(message: telebot.types.Message):
            """Send the user the message that recieve

            Args:
                message (_type_): the message that user sends the bot
            """
            logger.info('Message Recived!')
            self.send_message(
                message.chat.id,
                message.text,
                reply_markup=keyboards.main
            )
            logger.info('Message Sent!')

    def send_message(self, chat_id, text, reply_markup=None):
        self.bot.send_message(
            chat_id=chat_id, text=text, reply_markup=reply_markup
        )

if __name__ == '__main__':
    echo_bot = Bot(BOT)
    echo_bot.run()