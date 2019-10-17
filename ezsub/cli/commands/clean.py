#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ezsub.cache import Cache
from ezsub.errors import NoResultError, NothingToCleanError
from ezsub.utils import to_screen, select, parse_lngs, get_size, human_readable

def clean(req):
    cache = Cache()
    cache.delete_empty_children()
    results = cache.search(req.title, req.auto_select)
    selected = select(results, req.auto_select)
    if not selected:
        raise NoResultError
    paths = [results[s-1]['path'] for s in selected]
    lngs = parse_lngs(req.lngs)
    to_clean = cache._filter_langs(paths, lngs)
    if not to_clean:
        raise NothingToCleanError
    size_before = get_size(cache.subtitles)
    if req.zero:
        action = cache.zero(to_clean)
    else:
        action = cache.delete(to_clean, force=True)
    cache.delete_empty_children()
    size_after = get_size(cache.subtitles)
    to_screen(
        f"\n{human_readable(size_before-size_after)} freed by {action} files.\n")


