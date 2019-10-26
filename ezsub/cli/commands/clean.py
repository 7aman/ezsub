#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ezsub.cache import Cache, prune
from ezsub.errors import NoResultError, NothingToCleanError
from ezsub.utils import to_screen, select, parse_lngs, get_size, human_readable


def clean(req):
    cache = Cache()
    results = cache.search(req.title)
    if not results:
        raise NoResultError

    selected = select(results, req.auto_select)
    paths = [results[s-1]['path'] for s in selected]
    lngs = parse_lngs(req.lngs)
    to_clean = prune(paths, lngs)
    if not to_clean:
        raise NothingToCleanError

    files = [item['path'] for item in to_clean]

    size_before = get_size(cache.subtitles)
    if req.zero:
        action = cache.zero(files)
    else:
        action = cache.delete(files)

    cache.delete_empty_folders()
    size_after = get_size(cache.subtitles)
    to_screen(f"\n{human_readable(size_before-size_after)} freed by {action} files.\n", style='warn')

    return None
