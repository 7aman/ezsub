#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
from pkg_resources import parse_version

import requests

from ezsub import const
from ezsub.conf import UserConf
from ezsub.utils import to_screen


def update(just_remind=False):
    if just_remind:
        remind_to_update()
        return None
    current = const.__version__
    to_screen(
        f"Checking for {const.PROGRAMNAME} update. It take some seconds.")
    to_screen(f'    Current: {current}')
    to_screen(f'    Latest : ', flush=True, end='')
    remote = remote_version()
    if remote:
        to_screen(f'{remote}')
        if parse_version(remote) > parse_version(current):
            to_screen(f'There is a new version.')
            install(remote, action='Upgrade')
        elif parse_version(remote) < parse_version(current):
            to_screen(f'You are ahead of the latest version.')
            install(remote, action='Downgrade')
        else:
            to_screen(f'You are using the latest version.')
        config = UserConf()
        config.set_last_check()
    else:
        to_screen('unknown')
        to_screen(f"{const.PROGRAMNAME} can not reach pypi api server")


def install(remote, action='Upgrade'):
    answer = input(f'{action}? [y]/n: ') or 'y'
    if answer.lower() == 'y':
        to_screen(f"Installing {const.PROGRAMNAME} version {remote} silently...")
        subprocess.check_call([
            sys.executable,
            '-m', 'pip', 'install', '-U', '--user', '-q',
            f'{const.PROGRAMNAME}=={remote}'], stdout=None)
        to_screen("Done!")
    else:
        to_screen('skipped.')


def remote_version():
    TIMEOUT = const.TIMEOUT * 2 # pypi is a bit slower
    url = f"https://pypi.org/pypi/{const.PROGRAMNAME}/json/"
    try:
        r = requests.get(url, timeout=TIMEOUT).json()
        return r['info']['version']
    except requests.exceptions.ConnectTimeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    return False

def remind_to_update():
    configs = UserConf()
    configs.read() # to get reminder
    days_past = (const.TODAY - configs.get_last_check()).days
    if days_past > int(configs.reminder):
        to_screen(f"\n[update] It's been {days_past} days or more since last check for {const.PROGRAMNAME} update.")
        to_screen(f"         Check if there is an update available with: '{const.PROGRAMNAME} update'\n")