#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class InvalidSiteError(Exception):
    pass


class NoResultError(Exception):
    pass


class LoginFailedError(Exception):
    pass


class NothingToCleanError(Exception):
    pass


class NothingToDownloadError(Exception):
    pass


class NothingToExtractError(Exception):
    pass


class EmptyArchiveError(Exception):
    pass


class BadCompressedFileError(Exception):
    pass


class JobDone(Exception):
    pass


class WrongLineNumberError(Exception):
    pass


class CacheIsEmptyError(Exception):
    pass


class NoSiteIsAvailableError(Exception):
    pass
