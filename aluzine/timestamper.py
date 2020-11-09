from datetime import date

from aluzine.config import domain
from aluzine.config import login
from aluzine.config import password

from bs4 import BeautifulSoup

import requests


class TimeStamperException(Exception):
    pass


class TimeStamper(object):
    BASE_URL = '%s/open/login'
    LOGIN_URL = '%s/open/j_spring_security_check'
    HOMEPAGE_URL = '%s/open/homepage?ACTION=intranet&asked=1&header=0'
    BADGING_URL = '%s/open/webgtp/badge'
    DECLARATION_URL = '%s/open/homepage?ACTION=intranet&asked=7&header=0'

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

    DECLARATION_FORM = {
        'ACTION': 'CHANGER_APPLI',
        'ACTION_SWITCH': '',
        'module': 'gtp.name',
        'choixApplication': '7',
        'application': '10',
        'eltOidDemande': '',
        'isPourTiers': 'false',
        'etatDemandeTransfert': '0',
        'dateDebut': '',
        'dateFin': '',
        'selectionnerToutLISTE_DEMANDE_TRANSFERT_DE_COMPTE': 'true',
        'colonneTriLISTE_DEMANDE_TRANSFERT_DE_COMPTE': 'DATE_EXECUTION',
        'ordreTriLISTE_DEMANDE_TRANSFERT_DE_COMPTE': 'CROISSANT',
        '_csrf_bodet': ''
    }

    def __init__(self):
        self.login = login
        self.password = password
        self.domain = domain

        self.BASE_URL = self.BASE_URL % self.domain
        self.LOGIN_URL = self.LOGIN_URL % self.domain
        self.BADGING_URL = self.BADGING_URL % self.domain
        self.DECLARATION_URL = self.DECLARATION_URL % self.domain
        self.HOMEPAGE_URL = self.HOMEPAGE_URL % self.domain

    def ping(self):
        with requests.Session() as s:
            s.headers.update({'User-Agent': 'Aluzine v1.0'})

            splash = s.get(self.BASE_URL)

            token = self.get_token(splash.text)
            self.CREDENTIALS_FORM['_csrf_bodet'] = token
            self.CREDENTIALS_FORM['username'] = self.login
            self.CREDENTIALS_FORM['password'] = self.password

            s.post(self.LOGIN_URL, data=self.CREDENTIALS_FORM)
            homepage = s.get(self.HOMEPAGE_URL)

            token = self.get_token(homepage.text)
            jeton = self.get_jeton(homepage.text)

            self.BADGING_FORM['_csrf_bodet'] = token
            self.BADGING_FORM['JETON_INTRANET'] = jeton

            badging = s.post(self.BADGING_URL, data=self.BADGING_FORM)

            if 'class="alerte"' in badging.text:
                return False

            return True

    def check_previous(self):
        with requests.Session() as s:
            s.headers.update({'User-Agent': 'Aluzine v1.0'})

            splash = s.get(self.BASE_URL)

            token = self.get_token(splash.text)
            self.CREDENTIALS_FORM['_csrf_bodet'] = token
            self.CREDENTIALS_FORM['username'] = self.login
            self.CREDENTIALS_FORM['password'] = self.password

            s.post(self.LOGIN_URL, data=self.CREDENTIALS_FORM)
            declaration = s.get(self.DECLARATION_URL)

            previous_declaration = self.get_previous_declaration(
                declaration.text
            )

            return previous_declaration

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

    def get_previous_declaration(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        current_date = date.today().strftime('%d/%m/%Y')

        try:
            value = soup.find(
                'input', id='%s_heure1' % current_date
            ).get('value')
        except:
            raise TimeStamperException('Cannot find declaration row')

        return value
