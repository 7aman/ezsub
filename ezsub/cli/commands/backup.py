#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil

from ezsub import const
from ezsub.cache import Cache
from ezsub.utils import to_screen
from ezsub.destination import Destination


cur = const.Curser

def backup(req):
    # does not need '.zip' extension
    file_name = f"{const.PROGRAMNAME}-{const.TODAY_TIMEADD}"
    destination = Destination(req.destination, req.group, req.open_after)
    to_file = destination.get_child(file_name, mk_parents=True)
    cache = Cache()
    try:
        to_screen(f"Backup {const.PROGRAMNAME} cache directory to:")
        to_screen(f"    {to_file.resolve()}.zip", style="info")
        to_screen("started...", end='')
        shutil.make_archive(to_file, 'zip', root_dir=cache.root, base_dir=cache.root)
        to_screen(f"\r{cur.CL}Done.", style="ok")
        destination.open()
    except KeyboardInterrupt:
        out_file = to_file.with_suffix('.zip')
        if out_file.exists():
            to_screen(f"\nRemoving incomplete backup file '{out_file.name}' from destination...", style="warn")
            out_file.unlink()
            to_screen("Done!", style="ok")
        raise KeyboardInterrupt
    return None
