from aluzine.config import login
from aluzine.config import password


class TimeStamper(object):

    def __init__(self):
        self.login = login
        self.password = password

    def ping(self):
        print 'PING'
