import pytest
import time
import json

from client import User

address = ("localhost", 7777)


class TestUser:

    def setup(self):
        self.user = User("Pavel", "password")

    def teardown(self):
        del self.user


    def test_presence(self):
        to_send = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user": {
                "account_name": 'Pavel',
                "status": "Yes, I'm here"
            }
        }

        assert json.dumps(to_send) == self.user.presence()


    def test_message(self):
        to_send = {
            "action": "msg",
            "time": time.time(),
            "to": "Admin",
            "from": "Pavel",
            "encoding": "ascii",
            "message": "First message"
        }

        assert json.dumps(to_send) == self.user.message("admin", "First message")