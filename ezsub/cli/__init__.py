#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import logging
from ezsub import const
from ezsub.utils import to_screen
from ezsub.cli.commands import (
    download, config, update, login, backup, history, info, clean, unzip
)
from ezsub.errors import (
    JobDone,
    WrongLineNumberError,
    NothingToCleanError,
    NoResultError
)

logging.basicConfig(
    filename=const.LOGFILE,
    filemode=const.LOGFILEMODE,
    level=const.LOGLEVEL,
    format=const.LOGFORMAT
)
logger = logging.getLogger()


def main():
    try:
        req = history(sys.argv[1:])

        if req.command not in ['update', 'u']:
            update(just_remind=True)

        if req.command in ['dl', 'd', 'download']:
            download(req)
        elif req.command in ['unzip', 'x']:
            unzip(req)
        elif req.command in ['config', 'cfg']:
            config(req)
        elif req.command in ['update', 'u']:
            update()
        elif req.command in ['login', 'l']:
            login()
        elif req.command in ['backup', 'b']:
            backup(req)
        elif req.command in ['info', 'i']:
            info(req)
        elif req.command in ['clean']:
            clean(req)
    except KeyboardInterrupt:
        to_screen("\nTerminated by user.")
    except NothingToCleanError:
        to_screen("Nothing to clean")
    except NoResultError:
        to_screen("No Result for this title.")
    except JobDone:
        pass
    except WrongLineNumberError:
        to_screen("Wrong line number")
    sys.exit(0)


if __name__ == "__main__":
    main()
