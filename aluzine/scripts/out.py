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

    parser.add_argument(
        '--check-previous',
        action='store_true',
        help='By pass lock checking and check previous ping in the day')

    args = parser.parse_args()
    no_lock = args.no_lock
    check_previous = args.check_previous
    random_range = args.random_range

    if not (no_lock or check_previous):
        lock = Lock()
        if not lock.exist():
            return False

    if random_range:
        sleep(randint(0, random_range) * 60)

    ts = TimeStamper()
    if check_previous:
        if not ts.check_previous():
            return 1

    return not ts.ping()
