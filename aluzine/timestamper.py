from aluzine.config import login
from aluzine.config import password

from bs4 import BeautifulSoup

import requests


class TimeStamperException(Exception):
    pass


class TimeStamper(object):
    BASE_URL = 'https://hiventy.bodet-software.com/open/login'
    LOGIN_URL = 'https://hiventy.bodet-software.com/open/j_spring_security_check'  # noqa
    BADGING_URL = 'https://hiventy.bodet-software.com/open/webgtp/badge'

    CREDENTIALS_FORM = {
        'username': '',
        'password': '',
        '_crsf_bodet': '',
        'ACTION': 'ACTION_VALIDER_LOGIN',
    }

    BADGING_FORM = {
        'ACTION': 'BADGER_ES',
        'ACTION_SWITCH': '',
        'module': 'gtp.name',
        'choixApplication': '1',
        'application': '1',
        'JETON_INTRANET': '',
        '_csrf_bodet': ''
    }

    def __init__(self):
        self.login = login
        self.password = password

    def ping(self):
        with requests.Session() as s:
            s.headers.update({'User-Agent': 'Aluzine v1.0'})

            splash = s.get(self.BASE_URL)

            token = self.get_token(splash.text)
            self.CREDENTIALS_FORM['_csrf_bodet'] = token
            self.CREDENTIALS_FORM['username'] = self.login
            self.CREDENTIALS_FORM['password'] = self.password

            logging = s.post(self.LOGIN_URL, data=self.CREDENTIALS_FORM)
            token = self.get_token(logging.text)
            jeton = self.get_jeton(logging.text)

            self.BADGING_FORM['_csrf_bodet'] = token
            self.BADGING_FORM['JETON_INTRANET'] = jeton

            badging = s.post(self.BADGING_URL, data=self.BADGING_FORM)

            if 'class="alerte"' in badging.text:
                return False

            return True

    def get_token(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        try:
            value = soup.find('input', {'name': '_csrf_bodet'}).get('value')
        except:
            raise TimeStamperException('Cannot find csrf')
        return value

    def get_jeton(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        try:
            value = soup.find('input', {'name': 'JETON_INTRANET'}).get('value')
        except:
            raise TimeStamperException('Cannot find Jeton')
        return value
