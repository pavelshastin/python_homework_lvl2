"""

"""

from socket import socket, AF_INET, SOCK_STREAM
import json
import time
import sys


class User:
    def __init__(self, name, password):
        self.__name = name
        self.__password = password


    def presence(self):
        to_send = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user": {
                "account_name": self.__name.title(),
                "status": "Yes, I'm here"
            }
        }

        return json.dumps(to_send)

    def message(self, to, msg):
        to_send = {
            "action": "msg",
            "time": time.time(),
            "to": to.title(),
            "from": self.__name.title(),
            "encoding": "ascii",
            "message": msg
        }

        return json.dumps(to_send)




if __name__ == "__main__":

    args = sys.argv[1:]
    try:
        addr = str(args[0])
        port = int(args[1])
    except:
        port = 7777

    address = (addr, port)



    user = User("pavel", "Sh1pvonk")

    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)
        sock.send(user.presence().encode("ascii"))

        msg, addr = sock.recvfrom(1024)
        print(json.loads(msg.decode("ascii")))


