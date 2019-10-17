#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import logging
import configparser
from datetime import datetime

from ezsub import const
from ezsub.utils import to_screen

logger = logging.getLogger(__name__)


def display_configs(path):
    lines = list()
    with open(path, 'r') as config_file:
        content = config_file.read()
        for line in content.splitlines():
            if line:
                if line[0] == ';':  # skip comments
                    continue
                elif line[0] == '[':  # add a line before sections
                    lines.append('')
                lines.append(line)
    lines.append('')
    to_screen('')
    to_screen(f"-------user.conf----------")
    to_screen('\n'.join(lines))
    to_screen(f"-------user.conf----------")


def new_parser():
    parser = configparser.ConfigParser(
        allow_no_value=True,
        comment_prefixes=('#',),
        delimiters=('='),
        empty_lines_in_values=True
    )
    parser.BOOLEAN_STATES = const.BOOLEAN_STATES
    parser.optionxform = str
    return parser


def fresh_configs():
    configs = new_parser()

    YESNO = "{" + ", ".join(const.BOOLEAN_STATES.keys()) + "}"
    ALL_LNGS = "{" + ", ".join(const.SUPPORTED_LNGS) + "}"
    SITES = "{" + ", ".join(const.MIRRORS) + "}"

    configs.add_section('Defaults')
    configs['Defaults'] = {
        ';; open_after:    Open destination folder after job is done. [boolean]': None,
        ';; auto_select:   Auto select best match in title search i.e. first title. [boolean]': None,
        ';; group:         Group subtitles in folders like this: "./destination/title/language/". [boolean]': None,
        f';;                for booleans choose from {YESNO}': None,
        ';; site:          Site to download from.': None,
        f';;                supported sites: {SITES}': None,
        ';; languages:     Language(s) you interested to. Use space separated values.': None,
        f';;                supported languages: {ALL_LNGS}': None,
        ';; destination:   Set a path for destination folder. Can be relative.': None,
        'open_after': const.OPEN_AFTER,
        'auto_select': const.AUTO_SELECT,
        'group': const.GROUP,
        'site': const.SITE,
        'languages': const.LNGS,
        'destination': const.DESTINATION
    }

    configs.add_section('Login')
    configs['Login'] = {
        ";; Do not change manually else you know what are you doing.": None,
        "captcha": 'run ezsub login to fill this'
    }

    configs.add_section('Update')
    configs['Update'] = {
        ";; Do not change manually else you know what are you doing.": None,
        "remind_every": const.PERIOD,
        "last_check": const.TODAY_STAMP
    }

    return configs


def add_section(configs, section):
    configs.add_section(section)
    configs[section] = fresh_configs()[section]
    return configs


def reset_option(configs, section, option):
    """replace a an option in a section with its default value"""
    configs[section][option] = fresh_configs()[section][option]
    return configs


def validate_section(configs, section):
    if configs.has_section(section):
        configs = validate_options(configs, section)
    else:
        configs = add_section(configs, section)
        logger.warning(
            f"in user.conf, section '{section}' is missing. Added with default values.")
    return configs


def validate(configs):
    for section in const.SETTINGS_SKELETON.keys():
        configs = validate_section(configs, section)
    return configs


def validate_options(configs, section):
    for option, validator_approves in const.SETTINGS_SKELETON[section].items():
        if configs.has_option(section, option):
            value = configs[section][option]
            if not validator_approves(value):
                logger.warning(
                    f"in user.conf, option '{option}' in section '{section}' is invalid. reset to default value.")
                logger.debug(f"                 value was: {value}")
                configs = reset_option(configs, section, option)
        else:
            logger.warning(
                f"in user.conf, option '{option}' in section '{section}' is missing. set to default value.")
            configs = reset_option(configs, section, option)
    return configs


class UserConf:
    def __init__(self):
        self.path = const.CONFIGFILE

    def read(self):
        is_changed = False
        configs = new_parser()
        if self.path.exists():
            configs.read(self.path)
            configs_before = copy.deepcopy(configs)
            configs = validate(configs)
            is_changed = (configs != configs_before)
        else:
            logger.warning(
                "file 'user.conf' does not exist. creating with default values.")
            configs = fresh_configs()
            is_changed = True

        self.configs = configs
        self.open_after = configs['Defaults'].getboolean('open_after')
        self.auto_select = configs['Defaults'].getboolean('auto_select')
        self.group = configs['Defaults'].getboolean('group')
        self.site = configs['Defaults'].get('site')
        self.lngs = configs['Defaults'].get('languages')
        self.destination = configs['Defaults'].get('destination')
        self.captcha = configs['Login'].get('captcha')
        self.last_check = configs['Update'].get('last_check')
        self.reminder = configs['Update'].get('remind_every')
        if is_changed:
            self.write()

    def write(self):
        with open(self.path, 'w') as file_to_write:
            self.configs.write(file_to_write)

    def get_last_check(self):
        configs = new_parser()
        configs.read(self.path)
        last_check = configs['Update']['last_check']
        return datetime.fromtimestamp(int(last_check))

    def set_last_check(self):
        configs = new_parser()
        configs.read(self.path)
        configs['Update']['last_check'] = const.TODAY_STAMP
        self.configs = configs
        self.write()

    def get_captcha(self):
        configs = new_parser()
        configs.read(self.path)
        return configs['Login']['captcha']

    def set_captcha(self, value):
        configs = new_parser()
        configs.read(self.path)
        configs['Login']['captcha'] = value
        self.configs = configs
        self.write()

    def set_option(self, section, option, value):
        configs = new_parser()
        configs.read(self.path)
        changed = False
        section = section.title()
        option = option.lower()
        if section in const.SETTINGS_SKELETON.keys():
            if option in const.SETTINGS_SKELETON[section].keys():
                if value == '-':
                    configs = reset_option(configs, section, option)
                    to_screen(f"user.conf ::: option is reset successfully.")
                    changed = True
                else:
                    if const.SETTINGS_SKELETON[section][option](value):
                        configs[section][option] = value
                        to_screen(f"user.conf ::: option is set successfully.")
                        changed = True
                    else:
                        to_screen(
                            f"user.conf ::: value '{value}' is invalid for this option. ignored.")
            else:
                to_screen(
                    f"user.conf ::: no option named '{option}' in section '{section}'. ignored.")
        else:
            to_screen(f"user.conf ::: no section named '{section}'. ignored")
        self.configs = configs
        if changed:
            to_screen(f"user.conf ::: write changes to file.")
            self.write()
