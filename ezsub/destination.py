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
from ezsub.errors import EmptyArchiveError, BadCompressedFileError

logger = logging.getLogger(__name__)


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
            return None
        empty_files = 0
        unrar_missing = False
        bad_files = list()
        destinations = set()
        n = len(to_extract)
        for i, item in enumerate(to_extract):
            to_screen(f'\r[extract] {i+1}/{n}', flush=True, end='')
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
        to_screen()
        complain(empty_files, destinations, unrar_missing, bad_files)
        self.open()

    def open(self):
        if not self.root.exists():
            logger.warn("path '%s' not exists to open. Ignored.",
                        self.root.resolve())
            return None

        if self.open_after:
            path = str(self.root.resolve())
            apps = {
                'Windows': 'explorer',
                'Darwin': 'open',
                'Others': 'xdg-open'
            }
            try:
                app = apps[const.OS]
            except:
                app = apps['Others']
            subprocess.Popen([app, path])

    def make_destination(self, filepath):
        dest = self.root
        if self.group:
            dest = self.root.joinpath(*filepath.parts[-3:-1])
        dest.mkdir(parents=True, exist_ok=True)
        return dest

    def get_child(self, child, mk_parents=False):
        if str(child).startswith('/'):
            child = f".{child}"
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


def extract_members(dest, file, archive):
    for member in archive.infolist():
        if hasattr(member, 'is_dir'):
            if member.is_dir():
                continue
        elif hasattr(member, 'isdir'):
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


def get_name(file, dest, item):
    filename = dest.joinpath(item)
    lng = str(file).split('/')[-2]
    name_options = {
        "1": filename,
        "2": filename.with_suffix(f'.{lng}{filename.suffix}'),
        "3": filename.parent.joinpath(f"{file.stem}.{lng}.{filename.name}")
    }
    preferred = "2"
    filename = name_options[preferred]
    if filename.exists():
        _rand = str(uuid.uuid4())[0:3]
        new_name = filename.with_suffix(f'.{_rand}{filename.suffix}')
        filename.rename(new_name)

    return filename


def complain(empty=False, dest_list=None, no_unrar=None, bad_files=None):
    to_screen()
    if empty:
        to_screen(f'[Warning] empty archives: {empty}')

    files_removed = remove_same(dest_list)
    if files_removed:
        to_screen(f'[Warning] removed duplicate subtitles: {files_removed}')

    if no_unrar:
        to_screen(
            '[Warning] Some rar archives are found but unrar executable is missing.')

    if bad_files:
        to_screen(
            '[Warning] Some files are not zip nor rar.So these are considered as text files:')
        for item in bad_files:
            to_screen(f"       {item['path']}")
            if item['url']:
                to_screen(f"           downloaded from: {item['url']}")
            shutil.copy2(str(item['path']), str(item['dest']))


def remove_same(paths):
    if not paths:
        return 0
    to_remove = []
    for path in paths:
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


def test_path(folder, name):
    try:
        filepath = folder.joinpath(name)
        filepath.exists()
        return name
    except OSError:
        # windows has some limitations on file names.
        # '/' might be in namelist because dome compressed file have folders.
        illegals = r'<>:"\|?*'
        name = "".join([c for c in name if c not in illegals]).rstrip()
        return name
