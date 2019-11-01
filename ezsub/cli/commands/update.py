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
    to_screen(f"Checking for {const.PROGRAMNAME} update. It take some seconds.")
    to_screen(f'    Current: {current}')
    to_screen(f'    Latest : ', end='')
    remote = remote_version()
    if remote:
        to_screen(f'{remote}', style="ok")
        if parse_version(remote) > parse_version(current):
            to_screen(f'There is a new version.', style="warn")
            whats_new()
            install(remote, action='Upgrade')
        elif parse_version(remote) < parse_version(current):
            to_screen(f'You are ahead of the latest version.', style="warn")
            install(remote, action='Downgrade')
        else:
            to_screen(f'You are using the latest version.')
        config = UserConf()
        config.set_last_check()
    else:
        to_screen('unknown', style="red")
        to_screen(f"{const.PROGRAMNAME} can not reach pypi api server", style="warn")
    return None


def install(remote, action='Upgrade'):
    answer = input(f'{action}? [y]/n: ') or 'y'
    if answer.lower() == 'y':
        to_screen(f"Installing {const.PROGRAMNAME} version {remote} silently...", end='')
        subprocess.call([
            sys.executable,
            '-m', 'pip', 'install', '--user', '-q',
            f'{const.PROGRAMNAME}=={remote}'], stdout=None)
        to_screen("Done!", style="ok")
    else:
        to_screen('skipped.', style="warn")
    return None


def remote_version():
    TIMEOUT = const.TIMEOUT * 2  # pypi is a bit slower
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
    if configs.reminder == '0':
        # zero means never
        return None
    days_past = (const.TODAY - configs.get_last_check()).days
    if days_past > int(configs.reminder):
        to_screen("Update Reminder:", style="bold;italic;warn")
        to_screen(f"\rIt's been ", style="italic", end='')
        to_screen(f"{days_past} ", style="warn", end='')
        to_screen(f"days or more since last update check.", style="italic")
        to_screen(f"Check if there is a new version available with: ", style="italic", end='')
        to_screen(f"{const.PROGRAMNAME} update", style="ok")
        to_screen()
    return None


def get_changelog():
    TIMEOUT = const.TIMEOUT
    url = "https://raw.githubusercontent.com/7aman/ezsub/master/CHANGELOG"
    try:
        return requests.get(url, timeout=TIMEOUT).text
    except requests.exceptions.ConnectTimeout:
        return False
    except requests.exceptions.ConnectionError:
        return False
    return False


def whats_new():
    changelog = get_changelog().split('\n')
    curver = f"v{const.__version__}"  # vYYYY.MM.DD
    to_screen("what's new? ")
    for line in changelog:
        if line == curver:
            break
        to_screen(line, style="ok")
