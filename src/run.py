import emoji
import telebot
from loguru import logger
from pymongo.collection import Collection

from src.bot import BOT
from src.constants import keys, states
from src.db import database
from src.user import User
from src.utils.keyboard import create_keyboard


class Bot:

    def __init__(self, telebot: telebot.TeleBot, database: Collection):
        # Build the bot
        self.bot = telebot
        self.db = database

        # Register the handlers
        self.handlers()

    def run(self):
        logger.info("Bot starting...")
        self.bot.infinity_polling()

    def handlers(self):

        @self.bot.message_handler(commands=['start'])
        def start(message):
            # Send the welcome message
            self.send_message(
                chat_id=message.from_user.id,
                text="Hello, Welcome to the PyOverflow bot. :heart_eyes:",
                reply_markup=create_keyboard(keys.ask_question),
            )

        @self.bot.message_handler(regexp=emoji.emojize(keys.cancel))
        def cancel(message):
            # Send user the proper message
            # Delete the current question array
            # Update state
            pass

        @self.bot.message_handler(regexp=emoji.emojize(keys.ask_question))
        def ask_question(message):
            logger.info("ask_question() called")
            # Send the how-to-ask text
            with open('../data/how_to_ask.html') as f:
                self.send_message(
                    chat_id=message.from_user.id,
                    text=f.read(),
                    parse_mode='HTML',
                    reply_markup=create_keyboard(keys.cancel)
                )
            # Update the user state to ask_question
            self.db.users.update_one(
                {"_id": message.from_user.id},
                {"$set": {"state": states.ask_question}},
                upsert=True
            )

        @self.bot.message_handler(regexp=emoji.emojize(keys.send_question))
        def send_question(message):
            # Get the current question using the user id
            current_question = User(message.from_user.id). \
                get_current_question()
            # Add the current question and the user id
            # to the questions collection
            self.db.questions.insert_one({
                "user_id": message.from_user.id,
                'text': current_question
            })
            # Empty current question array and update state of user
            self.db.users.update_one(
                {"_id": message.from_user.id},
                {"$set": {'current_question': [], 'state': states.main}}
            )
            self.send_message(
                message.from_user.id,
                "Your question stored!",
                reply_markup=create_keyboard(keys.ask_question)
            )

        @self.bot.message_handler(func=lambda _: True)
        def echo(message: telebot.types.Message):
            user = User(message.from_user.id)
            if user.state != states.ask_question:
                self.send_message(message.from_user.id,
                                  "Your state is not correct!")
                return
            # push the entry to the current question field
            self.db.users.update_one(
                {"_id": message.from_user.id},
                {"$push": {"current_question": message.text}}
            )
            # Send user the current question
            self.send_message(
                message.from_user.id,
                f"<strong>Question Preview</strong>\n\n"
                f"<code>{user.get_current_question()}</code>",
                reply_markup=create_keyboard(keys.send_question, keys.cancel)
            )

    def send_message(self, chat_id, text, *, emojize=True,
                     parse_mode=None, reply_markup=None, **kwargs):
        """A fork of telebot.send_message with option for emojization"""
        if emojize:
            text = emoji.emojize(text, language='alias')
        self.bot.send_message(chat_id, text, parse_mode=parse_mode,
                              reply_markup=reply_markup, **kwargs)


if __name__ == '__main__':
    echo_bot = Bot(BOT, database)
    echo_bot.run()
