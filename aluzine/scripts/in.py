from aluzine.lock import Lock
from aluzine.timestamper import TimeStamper


def cmdline():
    lock = Lock()
    if lock.exist():
        return False

    lock.create()

    ts = TimeStamper()
    ts.ping()

    return True
