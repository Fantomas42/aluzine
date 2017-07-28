import os

from datetime import datetime


class Lock(object):

    def __init__(self):
        self.date = datetime.now().date()
        self.path = os.path.join(
            '/', 'var', 'lock', 'aluzine',
            self.date.strftime('%Y-%m-%d')
        )

    def exist(self):
        return os.path.isfile(self.path)

    def create(self):
        base_dir = os.path.dirname(self.path)

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        open(self.path, 'a').close()
