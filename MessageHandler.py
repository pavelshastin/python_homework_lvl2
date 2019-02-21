import json

from Chat import Chat


class MessageHandler:
    def __init__(self):
        self.chats = []

    def add_chat(self, chat):
        if isinstance(chat, Chat):
            if chat.name in self.chats:
                raise ValueError("The chat with given name already exists")
            else:
                self.chats.append(chat)
        else:
            raise TypeError("The given argument is not instance of Chat")


    def handle_request(self, msg):
        if self.__verify_req(msg):

            if msg["action"]:
                for ch in self.chats:

                    if ch.name == msg["to"]:

                        ch.add_message(msg["message"], msg["from"])

                        return ch.get_messages(msg["from"])

        else:
            return msg


    def __verify_req(self, msg):
        if isinstance(msg, dict):
            return True
        else:
            return False
