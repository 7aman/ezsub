#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uuid
import shutil
import zipfile
import logging
import subprocess
from hashlib import md5
from pathlib import Path

import rarfile

from ezsub import const
from ezsub.utils import to_screen
from ezsub.errors import (
    EmptyArchiveError,
    BadCompressedFileError,
    NothingToExtractError
)

logger = logging.getLogger(__name__)
cur = const.Curser


def get_extracor(file):
    if zipfile.is_zipfile(file):
        return zipfile.ZipFile
    elif rarfile.is_rarfile(file):
        return rarfile.RarFile
    else:
        raise BadCompressedFileError


class Destination(object):
    def __init__(self, root=const.DESTINATION, group=const.GROUP, open_after=const.OPEN_AFTER):
        self.root = Path(root)
        self.group = group
        self.open_after = open_after

    def extract(self, to_extract):
        if not to_extract:
            logger.warn("nothing to extract")
            raise NothingToExtractError
        empty_files = 0
        unrar_missing = False
        bad_files = list()
        destinations = set()
        n = len(to_extract)
        for i, item in enumerate(to_extract):
            to_screen(f"\rextracting... {i+1}/{n}", end='')  # progress
            file = item['path']
            dest = self.make_destination(file)
            destinations.add(dest)
            try:
                extractor = get_extracor(file)
                _extract(file, extractor, dest)
            except EmptyArchiveError:
                empty_files += 1
            except BadCompressedFileError:
                name = '-'.join(item['path'].parts[-3:])
                item['dest'] = dest.joinpath(name).with_suffix('.txt')
                bad_files.append(item)
            except rarfile.RarCannotExec:
                unrar_missing = True
        else:
            to_screen("\rextracting... ", end='')
            to_screen(f"{cur.CFH}done!", style="ok")

        complain(empty_files, destinations, unrar_missing, bad_files)
        self.open()
        return None

    def open(self):
        if not self.root.exists():
            logger.warn("destination path '%s' not exists to open. Ignored.", self.root.resolve())
            return None

        if not self.open_after:
            return None

        path = str(self.root.resolve())
        if const.OS == 'Windows':
            app = 'explorer',
        elif const.OS == 'Darwin':
            app = 'open',
        else:
            app = 'xdg-open'
        to_screen("opening destination... ", end='')
        subprocess.Popen([app, path])
        to_screen(f"done!", style="ok")
        return None

    def make_destination(self, filepath):
        dest = self.root
        if self.group:
            dest = self.root.joinpath(*filepath.parts[-3:-1])
        dest.mkdir(parents=True, exist_ok=True)
        return dest

    def get_child(self, child, mk_parents=False):
        if str(child).startswith('/'):
            child = f".{child}"  # make it relative
        path = self.root.joinpath(child)
        if mk_parents:
            path.parent.mkdir(parents=True, exist_ok=True)
        return path.resolve()


def _extract(file, extractor, dest):
    with extractor(file) as archive:
        if archive.namelist():
            extract_members(dest, file, archive)
        else:
            raise EmptyArchiveError
    return None


def extract_members(dest, file, archive):
    for member in archive.infolist():
        if hasattr(member, 'is_dir'):  # zipfile
            if member.is_dir():
                continue
        elif hasattr(member, 'isdir'):  # rarfile
            if member.isdir():
                continue
        extracted_file = dest.joinpath(member.filename)
        try:
            extracted_file.exists()
        except OSError:
            # windows illegal characters in file name raise this error. skip this file.
            continue
        preferred_name = get_name(file, dest, member.filename)
        archive.extract(member.filename, str(dest))
        extracted_file.rename(preferred_name)
    return None


def get_language(file_path):
    language = file_path.parent.name
    if language == 'farsi_persian':
        language = 'farsi'
    return language


def get_name(file, dest, item):
    filename = dest.joinpath(item)
    language = get_language(file)
    name_options = {
        "1": filename,
        "2": filename.with_suffix(f'.{language}{filename.suffix}'),
        "3": filename.parent.joinpath(f"{file.stem}.{language}.{filename.name}")
    }
    preferred = "2"  # TODO: add argument to get name pattern from user
    filename = name_options[preferred]
    if filename.exists():
        _rand = str(uuid.uuid4())[0:3]
        new_name = filename.with_suffix(f'.{_rand}{filename.suffix}')
        filename.rename(new_name)

    return filename


def complain(empty=False, dest_list=None, no_unrar=None, bad_files=None):
    if empty:
        to_screen("found empty archives: ", end='')
        to_screen(empty, style="warn")

    files_removed = remove_same(dest_list)
    if files_removed:
        to_screen("removed duplicate subtitles: ", end='')
        to_screen(files_removed, style="warn")

    if no_unrar:
        to_screen("Some rar archives are found but unrar executable is missing.", style="warn")

    if bad_files:
        to_screen("Some files are not zip nor rar.So these are considered as text files:", style="warn")
        for item in bad_files:
            to_screen(f"       {item['path']}", style="info")
            if item['url']:
                to_screen(f"           downloaded from: {item['url']}", style="info")
            shutil.copy2(str(item['path']), str(item['dest']))


def remove_same(paths):
    if not paths:
        return 0
    to_remove = []
    for path in paths:
        # TODO: skip for known media types
        files = [
            {'file': item, 'md5': md5(item.read_bytes()).digest()}
            for item in path.iterdir() if item.is_file()
        ]
        i = 0
        for file1 in files:
            for file2 in files[i+1:]:
                if file1['md5'] == file2['md5']:
                    to_remove.append(file1['file'])
                    break
            i += 1

    for file in to_remove:
        file.unlink()

    return len(to_remove)


# TODO: use this function in case of illegal characters
def test_path(folder, name):
    try:
        filepath = folder.joinpath(name)
        filepath.exists()
    except OSError:
        # windows has some limitations on file names.
        # '/' might be in namelist because some compressed file have folders.
        illegals = r'<>:"\|?*'
        name = "".join([c for c in name if c not in illegals]).rstrip()
    return name
