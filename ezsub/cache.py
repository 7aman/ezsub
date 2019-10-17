#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile

from ezsub import const
from ezsub.utils import to_screen, select, get_title
from ezsub.errors import NoResultError, NothingToCleanError


class Cache(object):
    def __init__(self, root=const.ROOT):
        self.root = root
        self.subtitles = root.joinpath('subtitles')
        self.subtitles.mkdir(parents=True, exist_ok=True)

    def search(self, title, silent=False):
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

    def exists(self, path):
        return self.root.joinpath(path).exists()

    def get_child(self, child, mk_parents=False):
        if str(child).startswith('/'):
            child = f".{child}"
        path = self.root.joinpath(child)
        if mk_parents:
            path.parent.mkdir(parents=True, exist_ok=True)
        return path.resolve()

    def empty_zipfile(self, child):
        path = self.root.joinpath('.', child)
        with zipfile.ZipFile(path, 'w'):
            pass

    def delete_empty_children(self):
        for title in self.subtitles.iterdir():
            for langs in title.iterdir():
                self.delete([langs], force=False)
            self.delete([title], force=False)
        to_screen()

    @staticmethod
    def _get_match_score(title, target):
        title_words = set(str(title).lower().replace(
            '+', ' ').replace('-', ' ').split())
        score = 0
        for word in title_words:
            if str(target).__contains__(word):
                score += 1
        return score

    @staticmethod
    def _filter_langs(paths, lngs):
        final_paths = list()
        for path in paths:
            for language in lngs.values():
                p = path.joinpath(language)
                if p.exists():
                    final_paths.append(p)
                else:
                    to_screen(
                        ' '*4 + f"no result for: {language} in {path.resolve()}")
        to_screen()
        return final_paths
    @staticmethod
    def zero(folders):
        cache = Cache()
        action = 'emptying'
        to_screen(f'\n[{action}]')
        for folder in folders:
            for child in folder.iterdir():
                cache.empty_zipfile(child)
                to_screen(f'emptied: {child.resolve()}')
        return action

    @staticmethod
    def delete(folders, force=False):
        action = 'deleting'
        for folder in folders:
            if force:
                shutil.rmtree(folder)
                to_screen(f'deleted: {folder.resolve()}')
            else:
                if not os.listdir(folder):
                    to_screen(f'deleted: [empty folder] {folder.resolve()}')
                    folder.rmdir()
        return action