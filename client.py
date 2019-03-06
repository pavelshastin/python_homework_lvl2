"""

"""

from socket import socket, AF_INET, SOCK_STREAM
import json
import datetime as time
import sys
from threading import Thread, Lock
from select import select

from JIMClient import JIMClient
from MetaClient import MetaClient
from ClientStorage import ClientStorage

class Client(JIMClient, metaclass=MetaClient):

    def __init__(self, name, password):
        super().__init__(name, password)

        self.__name = name
        self.__password = password
        self.storage = ClientStorage(name)
        self.lock = Lock()




    def connect(self, address):
        s = socket(AF_INET, SOCK_STREAM)
        s.connect(address)

        self.sock = s

        # t_read = Thread(target=self.to_read)
        # t_read.start()
        # t_read.join()
        #
        self.to_write()



    # def get_conts(self):
    #     self.acquire()
    #     self.sock.send(self.get_contacts().encode("ascii"))
    #     print("contacts getting")
    #     cont_num = json.loads(self.sock.recv(1024).decode("ascii"))
    #     self.release()
    #
    #     q = int(cont_num["quantity"])
    #     print("q", q)
    #     n = 1
    #     while True:
    #         contact = self.sock.recv(1024).decode("ascii")
    #
    #         contact = json.loads(contact)
    #         print("contact", contact)
    #         if contact["action"] == "contact_list":
    #             self.storage.add_contact(contact["user_id"])
    #
    #         if n == q:
    #             break
    #
    #         n += 1



    def to_read(self):
        while True:
            self.lock.acquire()
            msg = self.sock.recv(1024).decode("ascii")

            print(__name__, msg)
            if msg:
                form = json.loads(msg)

                if form["response"] == 200:
                    for m in form["alert"][0]:
                        dt = time.datetime.fromtimestamp(form["time"])
                        fr = m[0]
                        ms = m[1]
                        self.storage.add_message(dt, fr, ms)
                        print("{} From: {} Message: {}".format(time.datetime.ctime(dt), fr, ms))
            self.lock.release()

    def to_write(self):
        # contacts = self.storage.get_contacts()
        # contacts = [u.user_id for u in contacts]
        # print("Contacts: ", contacts)

        while True:
            c = input("Would you like to add/del contact a/d/n: ").lower()

            if c == "a":
                user = input("Enter user name to add: ").title()

                self.sock.send(self.add_contact(user).encode("ascii"))

                # # conf = self.sock.recv(1024).decode("ascii")
                # conf = json.loads(conf)
                # print("add", conf)
                # if conf["response"] == 202:
                #     self.storage.add_contact(user)
                # else:
                #     print("Can't add contact.")

            elif c == "d":
                user = input("Enter user name to delete: ").title()

                self.sock.send(self.add_contact(user).encode("ascii"))

                # conf = self.sock.recv(1024).decode("ascii")
                # conf = json.loads(conf)
                #
                # if conf["response"] == 202:
                #     self.storage.del_contact(user)
                # else:
                #     print("Can't delete contact.")

            elif c == "n":
                break

            else:
                print("Wrong enter")



        while True:
            # self.lock.release()
            # send_to = input("To: ")
            # msg = input("Message: ")
            #
            #
            # if msg == "quit" or send_to == "quit":
            #     self.sock.close()
            #     break
            #
            # try:
            #     # self.lock.acquire()
            #     self.sock.send(self.to_user(send_to, msg).encode("ascii"))
            #     # self.lock.release()
            #     self.lock.acquire()
            # except:
            #     print("The message haven't send")

            sockets_list = [sys.stdin, self.sock]

            read_sockets, write_socket, errsocket = select(sockets_list, [], [])

            for sock in read_sockets:
                if sock == self.sock:
                    print("one")

                    message = self.sock.recv(1024).encode("ascii")
                    
                    sys.stdout.write(message)
                    sys.stdout.flush()
                else:
                    message = sys.stdin.readline()
                    mes = self.to_user("Pavel", message).encode("ascii")

                    self.sock.send(mes)

                    sys.stdout.write("Pavel")

                    sys.stdout.flush()


if __name__ == "__main__":

    args = sys.argv


    try:
        addr = str(args[args.index("-a") + 1]) if args.count("-a") else "localhost"
        port = str(args[args.index("-p") + 1]) if args.count("-p") else 7777
        # w = True if args.count("-w") else False
        # r = True if args.count("-r") else False
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

    # user.get_conts()




    # if r:
    #     user.to_read()
    #
    #
    # elif w:
    #     user.to_write()


