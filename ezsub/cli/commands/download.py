#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from ezsub.cache import Cache
from ezsub.mirrors import Mirror
from ezsub.errors import NoResultError
from ezsub.destination import Destination
from ezsub.utils import to_screen, select, parse_lngs


def download(req):
    site = Mirror(req.site)
    site.select_first_responding()
    cache = Cache()
    destination = Destination(req.destination, req.group, req.open_after)
    results = site.search(req.title)
    selected = select(results, req.auto_select)
    if not selected:
        raise NoResultError
    paths = [results[s-1]['path'] for s in selected]
    lngs = parse_lngs(req.lngs)
    new_subs = []
    for path in paths:
        new_subs = new_subs[:] + prune(path, lngs, site, cache)[:]

    if req.simulation:
        n = len(new_subs)
        for i, path in enumerate(new_subs):
            file = cache.get_child(f'{path}.zip')
            to_screen(
                f"\r[simulate] {i+1}/{n}",
                flush=True, end='')  # progress stats
            cache.empty_zipfile(file)
        else:
            to_screen('\n\n')  # go to new line for ending progress stats
    else:
        to_download = site.mass_request(new_subs)
        for index, item in enumerate(to_download):
            to_download[index]['path'] = cache.get_child(f"{item['path']}.zip")
        to_extract = site.mass_download(to_download)
        destination.extract(to_extract)


def prune(path, lngs, site, cache, silent=False):
    to_screen(f'\ngetting {site.base_url}{path}', silent)
    links = site.get_subs(path)
    results = [
        link
        for link in links
        if link.split('/')[-2] in lngs.values()
    ]
    splitted = count_each_language(results, lngs)
    to_screen(f'all: {splitted}', silent)
    new_subs = [
        path
        for path in results
        if not cache.exists(f'.{path}.zip')
    ]
    splitted = count_each_language(new_subs, lngs)
    to_screen(f'new: {splitted}', silent)
    return new_subs


def count_each_language(results, lngs):
    splitted = {lng: 0 for lng in lngs.keys()}
    mapper = {language: lng for lng, language in lngs.items()}
    for link in results:
        language = link.split('/')[-2]
        splitted[mapper[language]] += 1
    return splitted
