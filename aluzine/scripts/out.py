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

    args = parser.parse_args()
    random_range = args.random_range

    lock = Lock()
    if not lock.exist():
        return False

    if random_range:
        sleep(randint(0, random_range) * 60)

    ts = TimeStamper()
    return not ts.ping()
