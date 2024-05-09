from src.db import database as db


class User:
    def __init__(self, chat_id) -> None:
        self.chat_id = chat_id
        self.user = db.users.find_one({'_id': chat_id})
        self.state = self.user.get('state')  # Return None if not exist

    def get_current_question(self):
        user = db.users.find_one({"_id": self.chat_id})
        if (not user) or (not user.get('current_question')):
            return ''
        return '\n'.join(user['current_question'])

    def update_state(self, new_state):
        db.users.update_one({'_id': self.chat_id},
                            {"$set": {'state': new_state}})
        self.state = new_state
