"""

"""

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import json
import select
import sys
import types
import time
from threading import Thread, Lock

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
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((addr, port))
        s.listen(5)
        # s.settimeout(0.2)

        self.logger.info("Server is listening on %s port %d", addr, port)
        return s


    @log(logger)
    def read_requests(self, readables):
        requests = {}
        print("readable", readables)
        for sock in readables:
            try:

                data = sock.recv(1024).decode("ascii")
                print("read_request", data)
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
        print(__name__, "--------------")

        for sock in writables:

            if len(requests) != 0:
                try:
                   msg = requests[sock]

                   if isinstance(msg, types.GeneratorType):
                       for i in msg:
                           print("msg", msg)
                           time.sleep(0.2)
                           sock.send(i.enconde("ascii"))
                   else:
                       print("msg", msg)
                       sock.send(msg.encode("ascii"))

                except OSError:
                    self.logger.info("Client %s %s dropped connection", sock.fileno(), sock.getpeername())
                    self.clients.remove(sock)

                except Exception as e:
                    self.logger.error(str(e))


    # def thread_socket(self, conn, addr):
    #     size=1024
    #
    #     while True:
    #         request = json.loads(conn.recv(size).decode("ascii"))
    #         print("request", request)
    #         response = self.handler.handle_request(request)
    #         print("response", response)
    #
    #         if isinstance(response, types.GeneratorType):
    #             for i in response:
    #                 time.sleep(0.2)
    #                 conn.send(i.encode("ascii"))
    #         else:
    #             conn.send(response.encode("ascii"))


    def run(self):
        sock = self.new_listen_socket(self.address)

        # while True:
        #     conn, addr = sock.accept()
        #
        #     try:
        #         Thread(target=self.thread_socket, args=(conn, addr)).start()
        #     except:
        #         print("Thread did not start")

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

