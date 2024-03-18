import telebot
from bot import BOT

class IsAdmin(telebot.custom_filters.SimpleCustomFilter):
    # class will check whether the user is admin or creator in group or not
    key = 'is_admin'
    @staticmethod
    def check(message: telebot.types.Message):
        return BOT.get_chat_member(
            message.chat.id, message.from_user.id
        ).status in ['adminstrator', 'creator']