#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import logging
import argparse

from ezsub import const
from ezsub.utils import to_screen
from ezsub.cli.commands import (
    download, config, update, login, backup, history, info, clean, unzip
)
from ezsub.errors import (
    JobDone,
    WrongLineNumberError,
    NothingToCleanError,
    NothingToDownloadError,
    NothingToExtractError,
    NoResultError,
    CacheIsEmptyError,
    NoSiteIsAvailableError,
    GetContentFailed
)


def get_user_loglevel():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--loglevel")
    args, _ = parser.parse_known_args(sys.argv[1:])
    loglevel = args.loglevel
    if loglevel:
        numeric_level = getattr(logging, loglevel.upper(), None)
        if isinstance(numeric_level, int):
            to_screen(f"loglevel is set to {loglevel.upper()}", style="ok")
            return loglevel.upper()
        else:
            to_screen(f"Invalid log level {loglevel}. Ignored.", style="warn")
    return ''


logging.basicConfig(
    filename=const.LOGFILE,
    filemode=const.LOGFILEMODE,
    level=get_user_loglevel() or const.LOGLEVEL,
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
        to_screen("\nTerminated by user.", style="red;bold")
    except NothingToCleanError:
        to_screen("\nNothing to clean.", style="warn;bold")
    except NothingToExtractError:
        to_screen("\nNothing to extract.", style="warn;bold")
    except NothingToDownloadError:
        to_screen("\nNothing to download.", style="warn;bold")
    except NoResultError:
        to_screen("\nNo Result for this title.", style="warn;bold")
    except CacheIsEmptyError:
        to_screen("\nCache folder is empty.", style="warn;bold")
    except NoSiteIsAvailableError:
        to_screen("\nSites are not accessible. check internet connection.", style="red;bold")
    except GetContentFailed:
        to_screen("\nGetting page content is failed. try later.", style="red")
    except JobDone:
        pass
    except WrongLineNumberError:
        to_screen("\nWrong line number", style="warn;bold")
    to_screen('\a')
    sys.exit(0)


if __name__ == "__main__":
    main()
