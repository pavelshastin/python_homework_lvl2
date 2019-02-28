"""

"""

from socket import socket, AF_INET, SOCK_STREAM, SOCK_DGRAM
import json
import select
import sys
import time


from log_config import logger, log
from JIMServer import JIMServer
from MessageHandler import MessageHandler
from Chat import Chat
from MetaServer import MetaServer



class Server(JIMServer, metaclass=MetaServer):
    logger = logger(__name__)


    def __init__(self, addr, handler):
        super().__init__()

        self.handler = handler
        self.address = addr
        self.clients = []

        self.logger.info("Creating an instance of " + self.__class__.__name__)


    def new_listen_socket(self, address):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((addr, port))
        s.listen(5)
        s.settimeout(0.2)

        self.logger.info("Server is listening on %s port %d", addr, port)
        return s


    @log(logger)
    def read_requests(self, readables):
        requests = {}

        for sock in readables:
            try:
                data = sock.recv(1024).decode("ascii")

                if data:
                    requests[sock] = self.handler.handle_request(json.loads(data))


            except OSError:
                self.logger.info("Client %s %s dropped connection", sock.fileno(), sock.getpeername())
                self.clients.remove(sock)
            except Exception as e:
                self.logger.error(str(e))

        return requests

    @log(logger)
    def write_response(self, requests, writables):

        for sock in writables:

            if len(requests) != 0:
                try:
                   msg = requests[sock]

                   sock.send(msg.encode("ascii"))

                except OSError:
                    self.logger.info("Client %s %s dropped connection", sock.fileno(), sock.getpeername())
                    self.clients.remove(sock)

                except Exception as e:
                    self.logger.error(str(e))


    def run(self):
        sock = self.new_listen_socket(self.address)


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
    # new_chat = Chat("new")
    # new_chat.add_user("Pavel")
    # new_chat.add_user("Sveta")
    # new_chat.add_user("Alex")
    # new_chat.add_user("Girl")
    # new_chat.add_user("Pavel_2")
    # new_chat.add_user("Me")

    req_handler = MessageHandler()
    # req_handler.add_chat(new_chat)

    req_handler.add_user("Pavel", "Password")
    req_handler.add_user("Sveta", "Password")
    req_handler.add_user("Alex", "Password")
    req_handler.add_user("Girl", "Password")
    req_handler.add_user("Pavel_2", "Password")
    req_handler.add_user("Me", "Password")

    server = Server((addr, port), req_handler)

    server.run()

