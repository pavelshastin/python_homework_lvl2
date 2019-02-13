"""

"""

from socket import socket, AF_INET, SOCK_STREAM
import json
import select
import sys
import time

args = sys.argv[1:]

addr = ""
port = 7777

try:
    addr = str(args[args.index("-a") + 1])
    port = int(args[args.index("-p") + 1])
except:
    pass


def my_func(x):
    return x*x


class Server:
    __responses = {
        200: {
            "response": 200,
            "alert": ""
        },
        402: {
            "response": 402,
            "error": "Wrong password or username"
        },
        409: {
            "response": 409,
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



    def __new_listen_socket(self, address):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind((addr, port))
        s.listen(5)
        s.settimeout(0.2)
        return s

    def __read_requests(self, readables):
        requests = {}

        for sock in readables:
            try:
                data = sock.recv(1024).decode("ascii")
                requests[sock] = json.loads(data)

            except:
                print("request", "Client {} {} dropped connection".format(sock.fileno(),
                                sock.getpeername()))

                clients.remove(sock)


        return requests

    def __write_response(self, requests, writables):

        for sock in writables:
            if sock in requests:
                try:
                   self.__responses[200]["Alert"] = requests[sock]

                   sock.send(json.dumps(self.__responses[200]).encode("ascii"))

                except:
                    print("response", "Client {} dropped connection".format(sock.getpeername()))
                    sock.close()
                    clients.remove(sock)


    def run(self):
        sock = self.__new_listen_socket(self.address)
        clients = []
        starttime = time.time()

        print("Server running...")

        while True:
            try:
                conn, addr = sock.accept()

            except OSError as e:
                pass
            else:
               print("Connection with {}".format(str(addr)))
               clients.append(conn)
            finally:
                wait = 0
                w = []
                r = []
                try:
                    r, w, e = select.select(clients, clients, [], wait)
                except:
                    pass


            requests = self.__read_requests(r)

            self.__write_response(requests, w)


if __name__ == "__main__":
    server = Server(addr, port)
    server.run()