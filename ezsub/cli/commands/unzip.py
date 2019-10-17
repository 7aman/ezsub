#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ezsub.cache import Cache
from ezsub.destination import Destination
from ezsub.errors import NoResultError
from ezsub.utils import to_screen, select, parse_lngs


def unzip(req):
    destination = Destination(req.destination, req.group, req.open_after)
    cache = Cache()
    results = cache.search(req.title)
    selected = select(results, req.auto_select)
    if not selected:
        raise NoResultError
    paths = [results[s-1]['path'] for s in selected]
    lngs = parse_lngs(req.lngs)
    folders = cache._filter_langs(paths, lngs)
    to_extract = [
        {'url': '', 'path': child}
        for folder in folders
        for child in folder.iterdir()
    ]
    destination.extract(to_extract)
