import argparse

from random import randint
from time import sleep

from aluzine.lock import Lock
from aluzine.timestamper import TimeStamper


def cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--random-range',
        type=int,
        help='Range of minutes before pinging')

    parser.add_argument(
        '--no-lock',
        action='store_true',
        help='By pass lock checking')

    args = parser.parse_args()
    no_lock = args.no_lock
    random_range = args.random_range

    if not no_lock:
        lock = Lock()
        if not lock.exist():
            return False

    if random_range:
        sleep(randint(0, random_range) * 60)

    ts = TimeStamper()
    return not ts.ping()
