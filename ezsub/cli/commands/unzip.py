#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ezsub.cache import Cache, prune
from ezsub.destination import Destination
from ezsub.utils import select, parse_lngs
from ezsub.errors import NoResultError


def unzip(req):
    destination = Destination(req.destination, req.group, req.open_after)
    cache = Cache()
    if req.exact:
        results, selected = cache.exact_search(req.exact)
    else:  # use title
        results = cache.search(req.title)
        selected = select(results, req.auto_select)

    if not selected:
        raise NoResultError

    paths = [results[s-1]['path'] for s in selected]
    lngs = parse_lngs(req.lngs)
    to_extract = prune(paths, lngs)
    destination.extract(to_extract)
    return None
