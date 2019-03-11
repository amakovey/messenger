import logging
import time
t = time.strftime("%Y-%m-%d", time.localtime())
name = t+".log"
logging.basicConfig(

    filename = name,
    format = "%(levelname)-10s %(asctime)s %(module)s %(message)s",
    level = logging.DEBUG
)
def log(what):
    def wrap(*args):
        obj_what=what(*args)
        log = logging.getLogger("app")
        args = (what.__name__) + str(args)
        log.debug(args)
        return obj_what
    return wrap