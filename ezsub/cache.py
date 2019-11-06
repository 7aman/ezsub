#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile

from ezsub import const
from ezsub.errors import CacheIsEmptyError
from ezsub.utils import get_title, to_screen


class Cache(object):
    def __init__(self, root=const.ROOT):
        self.root = root
        self.subtitles = root.joinpath('subtitles')
        self.subtitles.mkdir(parents=True, exist_ok=True)

    def search(self, title):
        to_screen("[cache] ", end='')
        to_screen(f"{self.subtitles}", style="info")
        self.delete_empty_folders()
        if self.is_empty(self.subtitles):
            raise CacheIsEmptyError

        max_score = 1
        titles = list()
        for child in self.subtitles.iterdir():
            score = self._get_match_score(title, child.name)
            item = {
                'path': child.resolve(),
                'title': get_title(child)
            }
            if score > max_score:
                max_score = score
                titles = [item, ]
            elif score == max_score:
                titles.append(item)
        return titles

    def exact_search(self, title):
        return (
            [{'path': self.subtitles.joinpath(title).resolve(), 'title': ''}],  # results
            [1, ]   # selected
        )

    def exists(self, path):
        return self.root.joinpath(path).exists()

    def get_child(self, child, mk_parents=False):
        if str(child).startswith('/'):
            child = f".{child}"
        path = self.root.joinpath(child)
        if mk_parents:
            path.parent.mkdir(parents=True, exist_ok=True)
        return path.resolve()

    def delete_empty_folders(self, root=None):
        if not root:
            root = self.subtitles
        for child in root.iterdir():
            if child.is_dir():
                if self.is_empty(child):
                    child.rmdir()
                else:
                    self.delete_empty_folders(child)
            else:
                return None
        return None

    @staticmethod
    def _get_match_score(title, target):
        # TODO: add partial word score
        title_words = set(title.lower().replace('+', ' ').replace('-', ' ').split())
        score = 0
        for word in title_words:
            if str(target).__contains__(word):
                score += 1
        return score

    @staticmethod
    def empty_zipfile(path):
        with zipfile.ZipFile(path, 'w'):
            pass
        return None

    def zero(self, files):
        for file in files:
            self.empty_zipfile(file)
        return 'emptying'

    @staticmethod
    def delete(files):
        for file in files:
            file.unlink()
        return 'deleting'

    @staticmethod
    def is_empty(path):
        if path.is_dir():
            return not os.listdir(path)
        return False


def filter_langs(path, lngs):
    final_paths = list()
    for language in lngs.values():
        p = path.joinpath(language)
        if p.exists():
            final_paths.append(p)
    return final_paths


def count_each_language(result, lngs):
    splitted = {lng: 0 for lng in lngs.keys()}
    mapper = {language: lng for lng, language in lngs.items()}
    for file in result:
        language = file['path'].parent.name
        splitted[mapper[language]] += 1
    return splitted


def prune(paths, lngs):
    pruned = []
    for path in paths:
        folders = filter_langs(path, lngs)
        result = [
            {'url': '', 'path': child}
            for folder in folders
            for child in folder.iterdir()
        ]
        splitted = count_each_language(result, lngs)
        to_screen("\n    path: ", end='')
        to_screen(f"{path.resolve()}", style="info")
        to_screen("   found: ", end='')
        to_screen(splitted, style="ok")
        pruned = pruned[:] + result[:]
    splitted = count_each_language(pruned, lngs)
    to_screen("\ntotal: ", end='')
    to_screen(splitted, style="ok")
    return pruned
