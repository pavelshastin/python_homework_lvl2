"""

"""

from socket import socket, AF_INET, SOCK_STREAM
import json
import time
import sys

from JIMClient import JIMClient

class Client(JIMClient):
    def __init__(self, name, password):
        super().__init__(name, password)

        self.__name = name
        self.__password = password


    def send_message(self):
        pass



if __name__ == "__main__":

    args = sys.argv


    try:
        addr = str(args[args.index("-a") + 1]) if args.count("-a") else "localhost"
        port = str(args[args.index("-p") + 1]) if args.count("-p") else 7777
        w = True if args.count("-w") else False
        r = True if args.count("-r") else False
        username = str(args[args.index("-un") + 1]) if args.count("-un") else "Pavel"
        pswd = str(args[args.index("-pw") + 1]) if args.count("-pw") else "PaSsw0rd"
        #print(w, r)
    except:
        port = 7777

    address = (addr, port)
    #print(addr, port, w, r)


    user = Client(username, pswd)


    if r:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(address)

            while True:

                msg = sock.recv(1024).decode("ascii")

                if msg:
                    form = json.loads(msg)

                    if form["response"] == 200:
                        for m in form["alert"]:
                            dt = time.ctime(m["time"])
                            fr = m["from"]
                            ms = m["message"]
                            print("{} From: {} Message: {}".format(dt, fr, ms))

    elif w:

        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(address)

            while True:
                send_to = input("To: ")
                msg = input("Message: ")

                if msg == "quit" or send_to == "quit":
                    sock.close()
                    break

                sock.send(user.to_user(send_to, msg).encode("ascii"))

