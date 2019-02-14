import pytest
import socket

from server import Server

address = ("", 7777)
test_server = Server(*address)


@pytest.yield_fixture
def my_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)
    yield s
    print("Finalizing my_socket")
    s.close()



def test_new_listen_socket(my_socket):
    try:
        s = test_server.new_listen_socket(address)
    except OSError:
        assert 1 == 1



