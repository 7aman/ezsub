#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from ezsub import const
from ezsub.cache import Cache
from ezsub.mirrors import Mirror
from ezsub.errors import NoResultError, NothingToDownloadError
from ezsub.destination import Destination
from ezsub.utils import to_screen, select, parse_lngs


cur = const.Curser

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
    new_subs = prune(paths, lngs, site, cache)
    if not new_subs:
        raise NothingToDownloadError

    if req.simulation:
        n = len(new_subs)
        for i, path in enumerate(new_subs):
            file = cache.get_child(f'{path}.zip', mk_parents=True)
            to_screen(f"\rcreating empty zip files... {i+1}/{n}", end='')  # progress stats
            cache.empty_zipfile(file)
        else:
            to_screen("\rcreating empty zip files... ", end='')
            to_screen(f"{cur.CFH}done", style='ok')
    else:
        to_download = site.mass_request(new_subs)
        for index, item in enumerate(to_download):
            to_download[index]['path'] = cache.get_child(f"{item['path']}.zip", mk_parents=True)
        to_extract = site.mass_download(to_download)
        destination.extract(to_extract)
    return None


def prune(paths, lngs, site, cache):
    pruned = []
    for path in paths:
        to_screen("\n     url: ", end='')
        to_screen(f"{site.base_url}{path}", style="info")
        links = site.get_subs(path)
        results = [
            link
            for link in links
            if link.split('/')[-2] in lngs.values()  # filter language
        ]
        splitted = count_each_language(results, lngs)
        to_screen("     all: ", end='')
        to_screen(splitted, style="ok")
        new_subs = [
            path
            for path in results
            if not cache.exists(f'.{path}.zip')  # filter already downloaded
        ]
        splitted = count_each_language(new_subs, lngs)
        to_screen("     new: ", end='')
        to_screen(splitted, style="ok")
        pruned = pruned[:] + new_subs[:]

    splitted = count_each_language(pruned, lngs)
    to_screen("\ntotal: ", end='')
    to_screen(splitted, style="ok")
    return pruned


def count_each_language(results, lngs):
    splitted = {lng: 0 for lng in lngs.keys()}
    mapper = {language: lng for lng, language in lngs.items()}
    for link in results:
        language = link.split('/')[-2]
        splitted[mapper[language]] += 1
    return splitted
