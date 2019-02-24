import logging
import time
import inspect
from functools import wraps

logging.basicConfig(
    filename="server_log.log",
    format="%(asctime)s %(levelname)-10s %(module)s %(funcName)s %(message)s",
    level=logging.INFO,
    filemode="a"
)


def logger(name):
    logger = logging.getLogger(name)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    _format = logging.Formatter("%(asctime)s %(funcName)s %(message)s")
    ch.setFormatter(_format)

    logger.addHandler(ch)

    return logger



def log(logger):
    def set_logger(func):

        @wraps(func)
        def logged(*args, **kwargs):

            caller = inspect.stack()[1].function

            logger.info("Start %s. Caller %s", func.__name__, caller)

            res = func(*args, **kwargs)

            logger.info("%s result %s", func.__name__, res)

            return res

        return logged

    return set_logger



# def log(func):
#     def logged(*args, **kwargs):
#         with open("server_log.log", "a", encoding="UTF-8") as f:
#             dt = time.ctime(time.time())
#             name = func.__name__
#             caller = inspect.stack()[1].function
#
#             f.write("{} Function {} is called by {}-function\n".format(dt, name, caller))
#
#             res = func(*args, **kwargs)
#
#             f.write("{} Function {} finished with result: {}\n".format(dt, name, res))
#
#         return res
#
#
#     return logged

