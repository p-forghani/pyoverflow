from telebot import types
import emoji


def create_keyboard(
        *keys,
        row_width=2,
        resize_keyboard=True
):
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=resize_keyboard,
        row_width=row_width
    )
    keys = map(emoji.emojize, keys)
    buttons = map(types.KeyboardButton, keys)
    markup.add(*buttons)
    return markup
