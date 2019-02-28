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
        self.sock = s


    def get_conts(self):
        self.sock.send(self.get_contacts().encode("ascii"))

        contacts = self.sock.recv(1024).decode("ascii")
        return json.loads(contacts)
        # n = 0
        # q = -1
        #
        # while n != q:
        #     contact = self.sock.recv(1024).decode("ascii")
        #     c = json.loads(contact)
        #
        #     if c["response"] == 202:
        #         q = int(c["quantity"])
        #
        #     elif c["action"] == "contact_list":
        #         self.storage.add_contact(c["user_id"])
        #         n += 1



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
        contacts = self.storage.get_contacts()
        print("Contacts: ", contacts)

        while True:
            c = input("Would you like to add/del contact a/d/n: ").lower()

            if c != "n":
                if c == "a":
                    user = input("Enter user name to add: ").title()

                    self.sock.send(self.add_contact(user).encode("ascii"))

                    conf = self.sock.recv(1024).decode("ascii")
                    conf = json.loads(conf)
                    print("add", conf)
                    if conf["response"] == 202:
                        self.storage.add_contact(user)
                    else:
                        print("Can't add contact.")

                elif c == "d":
                    user = input("Enter user name to delete: ").title()

                    self.sock.send(self.add_contact(user).encode("ascii"))

                    conf = self.sock.recv(1024).decode("ascii")
                    conf = json.loads(conf)

                    if conf["response"] == 202:
                        self.storage.del_contact(user)
                    else:
                        print("Can't delete contact.")

                else:
                    print("Wrong enter")


            send_to = input("To: ")
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
    user.get_conts()



    if r:
        user.to_read()


    elif w:
        user.to_write()


