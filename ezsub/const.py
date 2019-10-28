#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import platform
from pathlib import Path
from datetime import datetime

__version__ = '2019.10.28'
SEMVER = '0.1.1'
CALVER = __version__
__author__ = 'Zaman'
__contact__ = '7amaaan@gmail.com'
__url__ = 'http://github.com/7aman/ezsub'
__license__ = 'MIT'


def get_root(OS):
    if OS == 'Windows':
        root = Path(os.environ['PROGRAMDATA']).joinpath('ezsub')
    elif OS == 'Linux':
        root = Path().home().joinpath('.ezsub')
    else:
        root = Path().home().joinpath('.ezsub')
    root.mkdir(parents=True, exist_ok=True)
    return root


def get_destination():
    return Path().home().joinpath('Downloads', 'ezsub').resolve()


PROGRAMNAME = 'ezsub'
OS = platform.system()
ROOT = get_root(OS)
HISTORY = ROOT.joinpath('history.txt')
CONFIGFILE = ROOT.joinpath('user.conf')
LOGFILE = ROOT.joinpath('ezsub.log')
LOGLEVEL = 'INFO'
LOGFILEMODE = 'w'
LOGFORMAT = "[%(asctime)s][%(levelname)s]{%(name)s:%(lineno)d}# %(message)s"
DESTINATION = get_destination()
MIRRORS = ['subscene', 'hastisub', 'subf2m', 'xyz']
SITE = MIRRORS[0]
AUTO_SELECT = False
OPEN_AFTER = True
GROUP = True
LNGS = 'en'
PERIOD = 7  # days delay to remind for update
BOOLEAN_STATES = {
    '0': False,
    'false': False,
    'False': False,
    'no': False,
    'No': False,
    '1': True,
    'true': True,
    'True': True,
    'yes': True,
    'Yes': True,
}
LANGUAGE_PAIRS = {
    "ar": "arabic",
    "da": "danish",
    "en": "english",
    "es": "spanish",
    "fa": "farsi_persian",
    "fr": "french",
    "he": "hebrew",
    "id": "indonesian",
    "it": "italian",
    "no": "norwegian",
    "sv": "swedish",
    "vi": "vietnamese",
    "big5": "big_5_code"
}
SUPPORTED_LNGS = list(LANGUAGE_PAIRS.keys())
TODAY = datetime.now()
TODAY_STAMP = str(int(TODAY.timestamp()))
TODAY_TIMEADD = TODAY.strftime('%Y%m%d-%H%M')


def valid_boolean(value):
    if value in BOOLEAN_STATES.keys():
        return True
    return False


def valid_site(value):
    """site value can be space separated site names"""
    sites = value.split()
    for site in sites:
        if site not in MIRRORS:
            return False
    return True


def valid_lngs_string(value):
    for lng in value.split():
        if lng not in SUPPORTED_LNGS:
            return False
    return True


def valid_destination(value):
    path = Path(value).resolve()
    if path.exists():
        if not path.is_dir():
            return False
    return True


def valid_captcha(value):
    return True


def valid_reminder(value):
    try:
        value = int(value)
        return value > 0
    except ValueError:
        return False


def valid_timestamp(value):
    try:
        value = int(value)
        return value > 0
    except ValueError:
        return False


SETTINGS_SKELETON = {
    'Defaults': {
        'open_after': valid_boolean,
        'auto_select': valid_boolean,
        'group': valid_boolean,
        'site': valid_site,
        'lngs': valid_lngs_string,
        'destination': valid_destination
    },
    'Login': {
        'captcha': valid_captcha
    },
    'Update': {
        "remind_every": valid_reminder,
        "last_check": valid_timestamp
    }
}

# requests timeout
TIMEOUT = 5
SIGNS = [
    "Temporary unavailable",
    "Request Timeout",
    "please retry a few minutes later.",
    'Backend server error',
    'many requests'
]
BAD = [
    "Bad request"
]
MAX_WORKERS = 8


# colors and text formats
class Style:
    END = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERSCORE = '\033[4m'
    URL = UNDERSCORE
    REVERSE = '\033[7m'
    TITLE = REVERSE
    CROSSED =  '\033[9m'
    OVERLINED = '\033[53m'
    BLUE = '\033[34m'
    RED = '\033[91m'
    FAIL = RED
    ERROR = RED
    GREEN = '\033[92m'
    SUCCESS = GREEN
    OK = GREEN
    YELLOW = '\033[93m'
    WARNING = YELLOW
    WARN = YELLOW
    INFO = '\033[94m'

    def __init__(self):
        if OS == "Windows":
            os.system('color')

    def demo(self):
        print("------start demo----")
        variables = dir(self)
        for a in variables:
            try:
                print(getattr(self, a) + a + self.END)
                print()
            except:
                break
        print("------stop demo----")

    def render(self, styles, text):
        ss = []
        for s in styles.split(';'):
            if hasattr(self, s.upper()):
                ss.append(getattr(self, s.upper()))
        ss.append(str(text))
        ss.append(self.END)
        return "".join(ss)

class Curser:
    LU = '\033[F'
    SAVE = '\033[s'
    RESTORE = '\033[u'
    CFH = '\033[0K'
    CTH= '\033[1K'
    CL = '\033[2K'