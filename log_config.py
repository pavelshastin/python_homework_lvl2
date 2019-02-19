import logging
import time
import inspect


logging.basicConfig(
    filename="server_log.log",
    format="%(asctime)s %(levelname)-10s %(module)s %(funcName)s %(message)s",
    level=logging.INFO,
    filemode="a"
)


def log(func):
    def logged(*args, **kwargs):
        with open("server_log.log", "a", encoding="UTF-8") as f:
            dt = time.ctime(time.time())
            name = func.__name__
            caller = inspect.stack()[1].function

            f.write("{} Function {} is called by {}-function\n".format(dt, name, caller))

            res = func(*args, **kwargs)

            f.write("{} Function {} finished with result: {}\n".format(dt, name, res))

        return res


    return logged

