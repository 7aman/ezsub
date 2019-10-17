#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from ezsub import const
from ezsub.cache import Cache
from ezsub.utils import to_screen, get_size, get_title, machine_readable, count_children

def info(req):
    cache = Cache()
    path = cache.subtitles
    if not os.listdir(path):
        to_screen('\n' + "[Exit] Cache folder is empty." + '\n')
    else:
        size = get_size(path, 'human')
        children = count_children(path, 0, generation=1)
        total = count_children(path, 0, generation=3)
        basic_info(path, size, children, total)
        to_screen()
        if req.verbosity >= 1:
            level_one(path, req.sort)
        to_screen()


LANGMAX = 15
SIZEMAX = 10
COUNTMAX = 6
SPACING = 3
BAR = 41
SYMBOL = '#'


def basic_info(path, size, children, total):
    to_screen(f"\nezsub ver {const.__version__}")
    to_screen('\n[basic info]')
    TAB = 2
    to_screen(f'{" "*TAB}Path:       {path}')
    to_screen(f'{" "*TAB}Size:       {size}')
    to_screen(f'{" "*TAB}Titles:     {children}')
    to_screen(f'{" "*TAB}Subtitles:  {total}')


def level_one(path, sort_key):
    items = get_sorted_items(path, sort_key)
    tick = {'s': '', 'n': '', 't': ''}
    tick[sort_key] = SYMBOL
    headers = [
        f'{tick["n"]}Files'.rjust(COUNTMAX),
        f'{tick["s"]}Size'.rjust(SIZEMAX),
        f'{tick["t"]}Title'
    ]
    header = (' '*SPACING).join(headers)
    subheaders = ["="*COUNTMAX, "="*SIZEMAX, "="*BAR]
    subheader = (" "*SPACING).join(subheaders)
    to_screen(header)
    to_screen(subheader)
    for item in items:
        row_items = [
            str(item['n']).rjust(COUNTMAX),
            item['s'].rjust(SIZEMAX),
            item['t']
        ]
        to_screen((' '*SPACING).join(row_items))
    to_screen(subheader)
    to_screen(header)
    to_screen(f'\nnotice: results are sorted by {SYMBOL} marked column\n')


def get_sorted_items(path, sort_key):
    items = list()
    for child in path.iterdir():
        items.append({
            't': get_title(child),
            's': get_size(child, 'human'),
            'n': count_children(child, 0, generation=2)
        })

    def key(x):
        if sort_key == 's':
            return machine_readable(x[sort_key])
        else:
            return x[sort_key]

    reverse = False if sort_key == 't' else True
    return sorted(items, key=key, reverse=reverse)
