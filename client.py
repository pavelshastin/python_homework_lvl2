"""

"""

from socket import socket, AF_INET, SOCK_STREAM
import json
import datetime as time
import sys


from JIMClient import JIMClient
from MetaClient import MetaClient
from ClientStorage import ClientStorage

class Client(JIMClient, metaclass=MetaClient):

    def __init__(self, name, password):
        super().__init__(name, password)

        self.__name = name
        self.__password = password
        self.storage = ClientStorage(name)


    def connect(self, address):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(address)
        self.sock =  s


    def to_read(self):
        while True:
            msg = self.sock.recv(1024).decode("ascii")

            if msg:
                form = json.loads(msg)

                if form["response"] == 200:
                    for m in form["alert"][0]:
                        dt = time.datetime.fromtimestamp(form["time"])
                        fr = m[0]
                        ms = m[1]
                        self.storage.add_message(dt, fr, ms)
                        print("{} From: {} Message: {}".format(time.datetime.ctime(dt), fr, ms))

    def to_write(self):
        while True:
            send_to = input("To Chat: ")
            msg = input("Message: ")

            if msg == "quit" or send_to == "quit":
                self.sock.close()
                break

            try:
                self.sock.send(self.to_chat(send_to, msg).encode("ascii"))
            except:
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
    user.join("new")

    user.connect(address)

    if r:
        user.to_read()


    elif w:
        user.to_write()


