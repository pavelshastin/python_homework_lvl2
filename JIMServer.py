import json
import time


class JIMServer:
    def __init__(self):
        pass

    def probe(self):
        to_send = {
            "action": "probe",
            "time": time.time()
        }

        return json.dumps(to_send)

    def basic(self):
        to_send = {
            "response": 100,
            "time": time.time(),
            "alert": "basic response"
        }
        return json.dumps(to_send)

    def warning(self):
        to_send = {
            "response": 101,
            "time": time.time(),
            "alert": "warning response"
        }
        return json.dumps(to_send)


    def OK(self, msg):
        to_send = {
            "response": 200,
            "time": time.time(),
            "alert": msg
        }
        return json.dumps(to_send)

    def created(self, msg):
        to_send = {
            "response": 201,
            "time": time.time(),
            "alert": msg
        }
        return json.dumps(to_send)

    def accepted(self, msg):
        to_send = {
            "response": 202,
            "time": time.time(),
            "alert": msg
        }
        return json.dumps(to_send)

    def wrong_req(self):
        to_send = {
            "response": 400,
            "time": time.time(),
            "alert": "wrong request or JSON object"
        }
        return json.dumps(to_send)

    def not_authed(self):
        to_send = {
            "response": 401,
            "time": time.time(),
            "alert": "The user is not authorized"
        }
        return json.dumps(to_send)

    def wrong_cridentials(self):
        to_send = {
            "response": 402,
            "time": time.time(),
            "alert": "Wrong login or password"
        }
        return json.dumps(to_send)

    def forbidden(self):
        to_send = {
            "response": 403,
            "time": time.time(),
            "alert": "The user is forbidden"
        }
        return json.dumps(to_send)

    def not_found(self):
        to_send = {
            "response": 404,
            "time": time.time(),
            "alert": "The user or the chat are not located on server"
        }
        return json.dumps(to_send)

    def conflict(self):
        to_send = {
            "response": 409,
            "time": time.time(),
            "alert": "The server has already connection with given credencials"
        }
        return json.dumps(to_send)

    def gone(self):
        to_send = {
            "response": 410,
            "time": time.time(),
            "alert": "The used has leave the chat"
        }
        return json.dumps(to_send)

    def server_error(self):
        to_send = {
            "response": 500,
            "time": time.time(),
            "alert": "The server error"
        }
        return json.dumps(to_send)

    def contact(self, user_id):
        to_send = {
            "action": "contact_list",
            "user_id": user_id
        }

        return json.dumps(to_send)

    def cont_quantity(self, quant):
        to_send = {
            "response": 202,
            "quantity": quant
        }

        return json.dumps(to_send)