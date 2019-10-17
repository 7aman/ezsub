#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil

from ezsub import const
from ezsub.cache import Cache
from ezsub.utils import to_screen
from ezsub.destination import Destination


def backup(req):
    file_name = f"{const.PROGRAMNAME}-{const.TODAY_TIMEADD}" # does not need '.zip' extension
    destination = Destination(req.destination, req.group, req.open_after)
    to_file = destination.get_child(file_name, mk_parents=True)
    cache = Cache()
    try:
        to_screen(f"Backup {const.PROGRAMNAME} directory to:")
        to_screen(f"    {to_file.resolve()}.zip")
        to_screen("started...")
        shutil.make_archive(
            to_file, 'zip', root_dir=cache.root, base_dir=cache.root)
        to_screen("Done.")
        destination.open()
    except KeyboardInterrupt:
        to_screen("\nTerminated by user.")
        out_file = to_file.with_suffix('.zip')
        if out_file.exists():
            to_screen(f"Removing incomplete backup file '{out_file.name}' from destination...")
            out_file.unlink()
            to_screen("Done!")
