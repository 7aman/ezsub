#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ezsub import const
from ezsub.conf import UserConf
from ezsub.mirrors import Mirror
from ezsub.utils import to_screen
from ezsub.errors import LoginFailedError


def login():
    """This function is for subscene only. Other mirrors do not have login page"""
    timeout = 3 * const.TIMEOUT
    site = Mirror('subscene')
    site.select_first_responding(timeout)
    to_screen("It takes some seconds. In success, it will display new token.")
    try:
        token = site.login(timeout)
        to_screen(f"token:", end='')
        to_screen(token, style='ok')
        configs = UserConf()
        configs.set_captcha(token)
        to_screen("saved new token to user.conf", style='ok')
    except LoginFailedError:
        to_screen("Login failed.", style='red')
    return None
