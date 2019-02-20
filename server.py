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


class Server(JIMServer):
    __responses = {
        200: {
            "response": 200,
            "time": time.time(),
            "alert": {}
        },
        402: {
            "response": 402,
            "time": time.time(),
            "error": "Wrong password or username"
        },
        409: {
            "response": 409,
            "time": time.time(),
            "error": "Someone has already connected with given username"
        }
    }

    __requests = {
        "probe": {
            "action": "probe",
            "time": time.time()
        }
    }


    def __init__(self, addr, port):
        self.address = (addr, port)
        self.clients = []
        super().__init__()

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
                requests[sock] = json.loads(data)



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

    server = Server(addr, port)
    server.run()

