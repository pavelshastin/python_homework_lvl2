"""

"""

from socket import socket, AF_INET, SOCK_STREAM
import json
import select
import sys
import time

import logging
import log_config as log
from JIMServer import JIMServer
from MessageHandler import MessageHandler
from Chat import Chat


class Server(JIMServer, MessageHandler):

    def __init__(self, addr, port):
        super().__init__()

        self.chats = []
        self.address = (addr, port)
        self.clients = []

        self.logger = logging.getLogger(self.__class__.__name__)
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        _format = logging.Formatter("%(asctime)s %(funcName)s %(message)s")
        ch.setFormatter(_format)
        self.logger.addHandler(ch)
        self.logger.info("Creating an instance of " + self.__class__.__name__)


    def new_listen_socket(self, address):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((addr, port))
        s.listen(5)
        s.settimeout(0.2)

        self.logger.info("Server is listening on %s port %d", addr, port)
        return s


    @log.log
    def read_requests(self, readables):
        requests = {}

        for sock in readables:
            try:
                data = sock.recv(1024).decode("ascii")

                if data:
                    requests[sock] = self.handle_request(json.loads(data))


            except OSError:
                self.logger.info("Client %s %s dropped connection", sock.fileno(), sock.getpeername())
                self.clients.remove(sock)
            except Exception as e:
                self.logger.error(str(e))

        return requests

    @log.log
    def write_response(self, requests, writables):

        for sock in writables:

            if len(requests) != 0:
                try:
                   msg = self.OK(list(requests.values()))

                   sock.send(msg.encode("ascii"))

                except OSError:
                    self.logger.info("Client %s %s dropped connection", sock.fileno(), sock.getpeername())
                    self.clients.remove(sock)

                except Exception as e:
                    self.logger.error(str(e))

    def add_listener(self, listener):
        self.listeners.append(listener)


    def run(self):
        sock = self.new_listen_socket(self.address)
        starttime = time.time()

        while True:
            try:
                conn, addr = sock.accept()

            except OSError as e:
                if str(e) != "timed out":
                    self.logger.critical(str(e))
            else:
               self.logger.info("Connection with %s", str(addr))
               self.clients.append(conn)
            finally:
                wait = 0
                w = []
                r = []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], wait)
                except:
                    pass

            requests = None
            if r:
                requests = self.read_requests(r)

            if w and requests:
                self.write_response(requests, w)
                requests = None




if __name__ == "__main__":
    addr = ""
    port = 7777

    try:
        addr = str(sys.argv[sys.argv.index("-a") + 1])
        port = int(sys.argv[sys.argv.index("-p") + 1])
    except:
        pass

    #Creating chat and adding 6 users with given name
    new_chat = Chat("new")
    new_chat.add_user("Pavel")
    new_chat.add_user("Sveta")
    new_chat.add_user("Alex")
    new_chat.add_user("Girl")
    new_chat.add_user("Pavel_2")
    new_chat.add_user("Me")


    server = Server(addr, port)
    server.add_chat(new_chat)

    server.run()

