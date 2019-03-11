"""

"""

from socket import socket, AF_INET, SOCK_STREAM
import json
import datetime as dt
import time
import sys
from threading import Thread, Event, Lock

from JIMClient import JIMClient
from MetaClient import MetaClient
from ClientStorage import ClientStorage

class Client(JIMClient, metaclass=MetaClient):

    def __init__(self, name, password):
        super().__init__(name, password)

        self.__name = name
        self.__password = password
        self.__msg = ""
        self.__send_to = ""
        self.__from = ""
        self.__from_msg = ""
        self.__potencials = []
        self.__quant = -1

        self.__authed = Event()
        self.__got_conts = Event()
        self.__got_potents = Event()
        self.__contacts = Event()
        self.__add_cont = Event()
        self.__del_cont = Event()
        self.lock = Lock()

        self.storage = ClientStorage(name)





    def connect(self, address):
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.connect(address)

        self.th_read = Thread(target=self.read_thread)
        self.th_read.daemon = True
        self.th_read.start()

        try:
            self.sock.send(self.auth().encode("ascii"))
            self.__authed.wait()

            self.sock.send(self.get_potencials().encode("ascii"))
            self.__got_potents.wait()

            self.sock.send(self.get_contacts().encode("ascii"))
            self.__got_conts.wait()
        except:
            print("Can't send message")


        self.th_cont = Thread(target=self.contact_thread)
        self.th_cont.daemon = True
        self.th_cont.start()

        self.th_write = Thread(target=self.write_thread)
        self.th_write.daemon = True
        self.th_write.start()

        self.th_inpt = Thread(target=self.input_thread)
        self.th_inpt.daemon = True
        self.th_inpt.start()

        self.th_cont.join()
        self.th_write.join()
        self.th_inpt.join()



    def read_thread(self):

        while True:

            msg = self.sock.recv(1024).decode("ascii")


            msg = json.loads(msg)
            try:
                response = msg["response"]
            except:
                response = ""

            try:
                action = msg["action"]
            except:
                action = ""

            print(msg)

            if response:
                if msg["response"] == 200 and msg["alert"] == "authenticated":
                    print("Authentication has passed")
                    self.__authed.set()
                    continue

                elif msg["response"] == 200 and msg["alert"] != "authenticated":
                    print("Authentication has passed")
                    self.__authed.set()
                    continue

                elif msg["response"] == 201 and msg["alert"] == "user added":
                    print("New user has been added to communication")
                    self.__authed.set()
                    continue

                elif msg["response"] == 402 and msg["alert"] == "Wrong login or password":
                    print("Authentication denied. Wrong password or login")
                    sys.exit()

                elif msg["response"] == 202 and msg["quantity"] != 0:
                    self.__quant = int(msg["quantity"])
                    continue

                elif msg["response"] == 202 and msg["quantity"] == 0:
                    if self.__got_potents.is_set():
                        self.__got_conts.set()
                        continue

                    self.__got_potents.set()
                    continue

                elif msg["response"] == 203 and msg["alert"] == "Accepted":
                    self.__add_cont.set()
                    continue

                elif msg["response"] == 203 and msg["alert"] == "Deleted":
                    self.__del_cont.set()
                    continue

                elif msg["response"] == 401 and msg["alert"] == "denied":
                    self.__del_cont.set()
                    continue


            elif action:

                if msg["action"] == "contact_list":
                    self.storage.add_contact(msg["user_id"])
                    self.__quant -= 1

                    if self.__quant == 0:
                        print("Available contacts: ", self.storage.get_contacts())
                        self.__got_conts.set()
                    continue

                elif msg["action"] == "potent_list":
                    self.__potencials.append(msg["user_id"])
                    self.__quant -= 1

                    if self.__quant == 0:
                        print("Available users to add", self.__potencials)
                        self.__got_potents.set()
                    continue



    def contact_thread(self):

        while True:
            c = input("Would you like to add/del contact a/d/n: ").lower()

            if c == "a":
                user = input("Enter user name to add: ").title()

                self.sock.send(self.add_contact(user).encode("ascii"))
                self.__add_cont.wait()

                self.storage.add_contact(user)
                print("Available contacts: ", self.storage.get_contacts())



            elif c == "d":
                user = input("Enter user name to delete: ").title()

                self.sock.send(self.del_contact(user).encode("ascii"))

                self.__del_cont.wait()
                self.storage.del_contact(user)
                print("Available contacts: ", self.storage.get_contacts())


            elif c == "n":
                self.__contacts.set()
                break

            else:
                print("Wrong enter")



    def write_thread(self):
        self.__contacts.wait()

        while True:
            if self.__authed is True:

                if self.__msg != "" and self.__send_to != "":
                    try:
                        self.sock.send(self.to_user(self.__send_to, self.__msg).encode("ascii"))
                        self.__msg = ""
                        self.__send_to = ""
                    except:
                        print("The message haven't send")


    def input_thread(self):
        self.__contacts.wait()

        while True:

            if self.__from != "" and self.__from_msg != "":
                print("{}: {}".format(self.__from, self.__from_msg))
                self.__from = ""
                self.__from_msg = ""
                continue

            self.__send_to = input("To: ")
            self.__msg = input("Message: ")

            if self.__msg == "quit" or self.__send_to == "quit":
                sys.exit()




if __name__ == "__main__":

    args = sys.argv


    try:
        addr = str(args[args.index("-a") + 1]) if args.count("-a") else "localhost"
        port = str(args[args.index("-p") + 1]) if args.count("-p") else 7777
        username = str(args[args.index("-un") + 1]) if args.count("-un") else "Pavel"
        pswd = str(args[args.index("-pw") + 1]) if args.count("-pw") else "PaSsw0rd"

    except:
        port = 7777

    address = (addr, port)

    user = Client(username, pswd)

    user.connect(address)








