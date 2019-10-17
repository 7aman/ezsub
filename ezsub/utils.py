#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import zipfile
import subprocess

from ezsub import const

logger = logging.getLogger(__name__)


def to_screen(msg='', silent=False, **kwargs):
    if not silent:
        print(str(msg), **kwargs)
    return None


def full2abbr(language):
    for key, value in const.LANGUAGE_PAIRS.items():
        if value == language:
            return key
    else:
        raise ValueError(f"language '{language}' is not supported.")


def get_lang(file_path):
    language = file_path.parent.name
    if language == 'farsi_persian':
        language = 'farsi'
    return language


def abbr2full(lng):
    return const.LANGUAGE_PAIRS[lng]


def is_valid_lng(lng):
    return lng in const.SUPPORTED_LNGS


def parse_lngs(lngs_string, silent=False):
    lngs = lngs_string.split()
    parsed = {}
    for lng in lngs:
        if is_valid_lng(lng):
            parsed[lng] = abbr2full(lng)
        else:
            logger.warn(f"'{lng}' is not a valid language abbr. Ignored.")
            to_screen(
                f"'{lng}' is not a valid language abbr. Ignored.", silent)
    return parsed or {'en': 'english'}


def is_valid_integer(i):
    try:
        int(i)
        return True
    except ValueError:
        return False


def filter_valid_choice(text, maximum):
    numbers = text.split(',')
    numbers = [int(n) for n in numbers if is_valid_integer(n)]
    return list(set([n for n in numbers if (0 < n < 1+maximum)]))


def get_user_choice(results):
    mx = len(results)
    if mx == 1:
        text = "  Press Enter to select only result"
    else:
        text = "  Select titles, comma separated numbers"

    while True:
        try:
            selected = input(f'{text} [1]: ') or '1'
            answer = filter_valid_choice(selected, mx)
            if answer:
                return answer
            else:
                raise IndexError
        except IndexError:
            to_screen("    Oops! not valid. Try again.")


def show_to_select(results):
    to_screen('\n[Results]')
    to_screen("  -----------------------------------------------")
    max_width = len(str(len(results)))
    for i, res in enumerate(results):
        to_screen(f"    {str(i+1).rjust(max_width, ' ')} - {res['title']}")
    to_screen("  -----------------------------------------------")


def select(results, auto_select):
    if not results:
        return []
    else:
        show_to_select(results)
        if auto_select:
            to_screen('    auto select: 1')
            selected = [1, ]
        else:
            selected = get_user_choice(results)
        return selected


def windows_size(path):
    size = subprocess.check_output([
        'powershell',
        '-noprofile',
        '-command',
        f"ls {path} -r | measure -s Length | select -ExpandProperty Sum"
    ])
    return int(size)


def unix_size(path):
    size = subprocess.check_output(['du', '-s', '-B 1', path])
    return int(size.split()[0].decode('utf-8'))


def human_readable(size):
    for unit in ['', 'K', 'M', 'G', 'T']:
        if size < 1024.0:
            return f"{size:03.2f} {unit}B"
        size = size / 1024.0


def machine_readable(size):
    units = {"B": 1, "KB": 1024, "MB": 1024**2, "GB": 1024**3, "TB": 1024**4}
    number, unit = size.split()
    return int(float(number)*units[unit])


def get_size(path, form='machine'):
    if const.OS == "Windows":
        size = windows_size(path)
    else:
        size = unix_size(path)
    if form == 'human':
        return human_readable(size)  # string
    elif form == 'machine':
        return size  # int


def get_title(path):
    return " ".join(path.name.split('-')).title()


def count_children(path, count, generation=1):
    '''
    generation 1 means direct children only
    generetion 2 means children of children only - children are excluded.
    generetion 3 ....
    '''
    if generation == 1:
        return count + len([child for child in path.iterdir()])
    else:
        for child in path.iterdir():
            count = count_children(child, count, generation-1)
    return count
