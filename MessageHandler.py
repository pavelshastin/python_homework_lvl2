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
                    return self.accepted("Accepted")
                else:
                    return self.not_authed()


            elif msg["action"] == "del_contact":
                dell = self.storage.del_contact(msg["user_id"], msg["from"])
                print("Delete: ", dell)
                if dell:
                    return self.accepted("Deleted")
                else:
                    return self.not_authed()


            elif msg["action"] == "get_contacts":

                conts = self.storage.get_contacts(msg["user_id"])
                cont_nums = len(conts)

                def gener(cont_nums, conts):
                    yield self.cont_quantity(cont_nums)

                    for cont in conts:
                        yield self.contact(cont)

                return gener(cont_nums, conts)


            elif msg["action"] == "get_potencials":

                potents = self.storage.get_potencials(msg["user_id"])
                pot_nums = len(potents)

                def gener(pot_nums, potents):
                    yield self.cont_quantity(pot_nums)

                    for p in potents:
                        yield self.potencial(p)

                return gener(pot_nums, potents)



            elif msg["action"] == "msg":

                return self.OK(msg["message"])


            elif msg["action"] == "authenticate":
                user_id = msg["user"]["account"]
                pswd = msg["user"]["password"]

                if self.storage.add_user(user_id, pswd):

                    return self.created("user added")
                else:
                    if self.storage.authenticate(user_id, pswd):

                        return self.OK("authenticated")
                    else:

                        return self.wrong_cridentials()



        else:
            return msg


    def add_user(self, name, info):
        self.storage.add_user(name, info)


    def __verify_req(self, msg):
        if isinstance(msg, dict):
            return True
        else:
            return False
