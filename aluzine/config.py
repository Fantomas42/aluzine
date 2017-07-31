import os

from ConfigParser import SafeConfigParser


config = SafeConfigParser()

config_read = config.read(os.path.expanduser('~/.aluzine'))

login = config.get('user', 'login')
password = config.get('user', 'password')
domain = config.get('user', 'domain')
