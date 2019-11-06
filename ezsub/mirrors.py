#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import traceback
from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

from ezsub import const
from ezsub.conf import UserConf
from ezsub.utils import to_screen
from ezsub.errors import (
    LoginFailedError,
    NoSiteIsAvailableError,
    GetContentFailed,
    NoResultError
)

cur = const.Curser
logger = logging.getLogger(__name__)

MDB = {
    'subscene': {
        "base_url": "https://subscene.com",
        "query_path": "/subtitles/searchbytitle",
        "method": requests.post,
        "login_path": '/account/login',
        "captcha": UserConf().get_captcha(),
        "selectors": {
            "title": "li div[class='title'] a",
            "link": "tr td[class='a1'] a",
            "btn": "a[id='downloadButton']"
        }
    },
    'hastisub': {
        "base_url": "http://hastisub.top",
        "query_path": "/subtitles/searchbytitle",
        "method": requests.get,
        "login_path": '',
        "captcha": '',
        "selectors": {
            "title": "li div[class='title'] a",
            "link": "tr td[class='a1'] a",
            "btn": "#downloadButton",
            "release": "li.release div",
            "author": "li.author a",
            "date": "#details ul li"
        }
    },
    'subf2m': {
        "base_url": "https://subf2m.co",
        "query_path": "/subtitles/searchbytitle",
        "method": requests.get,
        "login_path": '',
        "captcha": '',
        "selectors": {
            "title": "li div[class='title'] a",
            "link": "a[class='download icon-download']",
            "btn": "a[id='downloadButton']"
        }
    },
    'xyz': {
        "base_url": "https://subscene.xyz",
        "query_path": "/subtitles/searchbytitle",
        "method": requests.get,
        "login_path": '',
        "captcha": '',
        "selectors": {
            "title": "li div[class='title'] a",
            "link": "tr td[class='a1'] a",
            "btn": "a[id='downloadButton']"
        }
    }
}

def available(pagetext):
    for sign in const.SIGNS:
        if sign.lower() in str(pagetext).lower():
            # to_screen('\n[Warning] Temporary unavailable. Try again later or check the site in browser.')
            return False
    for sign in const.BAD:
        if sign.lower() in str(pagetext).lower():
            to_screen("\nBad request. maybe captcha is expired. login again with 'ezsub login'", style="warn")
            return False
    return True


class Mirror(object):
    def __init__(self, names=const.SITE):
        '''names is a space separated site names in preferred order.'''
        self.names = names.split()

    def select_first_responding(self, timeout=const.TIMEOUT, ignore=''):
        not_checked = const.MIRRORS[:]
        for name in self.names:
            if name == ignore:
                not_checked.remove(name)
                continue
            self._fill_attributes(name)
            if self._is_responding(timeout):
                break
            else:
                not_checked.remove(self.name)
        else:
            # if still there are sites left to try
            if not_checked:
                to_screen("trying other mirrors...", style="yellow;italic")
            for name in not_checked:
                self._fill_attributes(name)
                if self._is_responding(timeout):
                    break
            else:
                raise NoSiteIsAvailableError
        return None

    def get_sub_details(self, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        btn = soup.select_one(self.selectors['btn'])
        if btn:
            return {'download_link': btn['href']}
        return False

    def search(self, title):
        path = self.query_path
        data = None
        if self.method == requests.get:
            path += f"?query={title}"
        elif self.method == requests.post:
            data = {
                'query': title,
                'l': '',
                'g-recaptcha-response': self.captcha
            }
        to_screen("  query: ", end='')
        to_screen(f"{self.base_url}{path}", style="italic;info")
        page_text = self._get_page_text(path, data=data)
        retry = const.RETRY
        while (not page_text) and retry:
            to_screen("current mirror is not responding. trying other mirrors...", style="warn")
            self.select_first_responding(ignore=self.name)
            self._get_page_text(path, data)
            retry = retry - 1
        if not page_text:
            raise GetContentFailed
        soup = BeautifulSoup(page_text, 'html.parser')
        titles = soup.select(self.selectors['title'])
        aggregated = {title.attrs['href']: title.text for title in titles}
        return [{'path': p, 'title': t} for p, t in aggregated.items()]

    @staticmethod
    def exact_search(title):
        return (
            [{'path': f"/subtitles/{title}", 'title': ''}], # results
            [1,]   # selected
        )

    def get_subs(self, path):
        page_text = self._get_page_text(path)
        soup = BeautifulSoup(page_text, 'html.parser')
        subs = soup.select(self.selectors['link'])
        return {sub['href'] for sub in subs}

    def _get_page_text(self, path, data=None, timeout=const.TIMEOUT, retry=const.RETRY):
        while retry:
            try:
                page = self.method(self.base_url + path, data=data, timeout=timeout)
                page.encoding = 'utf-8'
                return page.text
            except Exception as e:
                to_screen("getting page content failed. for more info see log.", style="warn")
                logger.warn(e)
                logger.debug(traceback.format_exc())
            retry = retry - 1
            timeout = 2 * timeout  # double timeout
            if retry:
                to_screen("retry with timeout doubled...", style="warn")
        raise GetContentFailed

    def _is_responding(self, timeout=const.TIMEOUT):
        try:
            to_screen(f"checking '{self.name}': ", end='')
            to_screen(f"{self.base_url}/", style="info", end='')
            to_screen(" is ", end='')
            r = requests.head(self.base_url, timeout=timeout)
            if r.status_code == requests.codes['ok']:
                to_screen('OK', style="bold;ok")
                return True
            else:
                to_screen(f"not responding (status: {r.status_code})", style="warn")
        except Exception as e:
            to_screen("failed with error. see log. trying next mirror...", style="warn")
            logger.warn(e)
            logger.debug(traceback.format_exc())
        return False

    def mass_request(self, paths):
        session = FuturesSession(max_workers=const.MAX_WORKERS)
        n = len(paths)
        no_links = []
        to_download = []
        requests = [session.get(self.base_url + path) for path in paths]
        for i, path in enumerate(paths):
            page_text = requests[i].result().text
            link = self.get_sub_details(page_text)
            url = self.base_url + path
            to_screen(f"\rgetting subtitles info... {i+1}/{n}", end='')  # progress
            if link:
                item = {
                    'path': path,
                    'url': url,
                    'dlink': link['download_link']
                }
                to_download.append(item)
            else:  # no link is found
                no_links.append(url)
        else:
            to_screen("\rgetting subtitles info... ", end='')
            to_screen(f"{cur.CFH}done!", style="ok")

        if no_links:
            to_screen("\nno download link is found for these urls:", style="warning")
            for link in no_links:
                to_screen(f'       {link}', style="info")
        return to_download

    def mass_download(self, to_download):
        session = FuturesSession(max_workers=const.MAX_WORKERS)
        all_requests = [session.get(self.base_url + sub['dlink']) for sub in to_download]
        n = len(to_download)
        to_extract = []
        for i, subtitle in enumerate(to_download):
            file = subtitle['path']
            to_screen(f"\rdownloading... {i+1}/{n}", end='')  # progress
            with open(file, "w+b") as f:
                file_content = all_requests[i].result().content
                f.write(file_content)
            to_extract.append(subtitle)
        else:
            to_screen("\rdownloading... ", end='')
            to_screen(f"{cur.CFH}done!", style="ok")
        return to_extract

    def login(self, timeout=const.TIMEOUT):
        session = requests.Session()
        try:
            session.get(self.base_url + self.login_path, timeout=timeout)
            return session.cookies.get_dict()['idsrv.xsrf']
        except:
            raise LoginFailedError

    def _fill_attributes(self, name):
        if name not in const.MIRRORS:
            to_screen(f"\r[site] ignoring invalid site '{name}' and using '{const.SITE}' instead.", style="warning")
            name = const.SITE
        self.name = name
        self.base_url = MDB[name]['base_url']
        self.query_path = MDB[name]['query_path']
        self.method = MDB[name]['method']
        self.login_path = MDB[name]['login_path']
        self.captcha = MDB[name]['captcha']
        self.selectors = MDB[name]['selectors']


def get_soup(url):
    session = FuturesSession(max_workers=const.MAX_WORKERS)
    req = session.get(url)
    r = req.result()
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'html.parser')


def get_subtitle_info(soup, selectors, url):
    '''get soup of subtitle download page and returns info'''
    info = dict()
    info["url"] = url
    info["language"] = url.split('/')[-2]
    info["author"] = soup.select_one(selectors.author).text.strip()
    releases = soup.select(selectors.release)
    info["releases"] = [div.text.strip() for div in releases]
    info['download'] = soup.select_one(selectors.btn)['href']
    upload_date = " ".join(soup.select_one(selectors.date).text.split()[1:4])
    info["date"] = datetime.strptime(upload_date, '%m/%d/%Y %I:%M %p')
    return info


def get_all_subtitle_urls(soup):
    '''get soup of title page or filtered language and returns all subtitles download page url'''
    subs = soup.select("tbody tr td[class='a1'] a")
    return {a['href'] for a in subs}


def get_available_languages(soup):
    '''get soup of a title page and returns all available languages for that title'''
    language_rows = soup.select('tbody tr td[colspan="5"]')
    return [row['id'] for row in language_rows if row.has_attr('id')]


