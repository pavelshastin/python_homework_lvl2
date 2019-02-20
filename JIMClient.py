import json
import time


class JIMClient:
    def __init__(self, name, pswd):
        self.__name = name
        self.__pswd = pswd
        self.__rooms = []

    def presence(self):
        to_send = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user": {
                "account": self.__name,
                "status": "Yes, I'm here"
            }
        }

        return json.dumps(to_send)

    def auth(self):
        to_send = {
            "action": "authenticate",
            "time": time.time(),
            "user": {
                "account": self.__name,
                "password": self.__pswd
            }
        }

        return json.dumps(to_send)

    def to_chat(self, room, msg):
        if room in self.__rooms:

            to_send = {
                "action": "msg",
                "time": time.time(),
                "to": room,
                "from": self.__name,
                "message": msg
            }

            return json.dumps(to_send)
        else:
            raise ValueError("You haven't join to the given chat room")

    def to_user(self, to, msg):
        to_send = {
            "action": "msg",
            "time": time.time(),
            "to": to,
            "from": self.__name,
            "message": msg
        }

        return json.dumps(to_send)


    def join(self, room):
        self.__rooms.append(room)

        to_send = {
            "action": "join",
            "time": time.time(),
            "room": room
        }

        return json.dumps(to_send)


    def leave(self, room):
        self.__rooms.remove(room)

        to_send = {
            "action": "join",
            "time": time.time(),
            "room": room
        }

        return json.dumps(to_send)


    def quit(self):
        to_send = {
            "action": "quit"
        }

        return json.dumps(to_send)