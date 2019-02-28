import json

from Chat import Chat
from ServerStorage import ServerStorage
from JIMServer import JIMServer

class MessageHandler(JIMServer):
    def __init__(self):
        self.chats = []
        self.storage = ServerStorage()

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

            if msg["action"] == "add_contact":
                add = self.storage.add_contact(msg["user_id"], msg["from"])
                if add:
                    return self.accept("Accepted")
                else:
                    return self.not_authed()

            elif msg["action"] == "get_contacts":

                conts = self.storage.get_contacts(msg["from"])
                return self.contact(conts)

            for ch in self.chats:

                if ch.name == msg["to"]:

                    ch.add_message(msg["message"], msg["from"])

                    return self.OK(ch.get_messages(msg["from"]))


        else:
            return msg


    def add_user(self, name, info):
        self.storage.add_user(name, info)


    def __verify_req(self, msg):
        if isinstance(msg, dict):
            return True
        else:
            return False
