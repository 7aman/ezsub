#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests_futures.sessions import FuturesSession

from ezsub import const
from ezsub.conf import UserConf
from ezsub.utils import to_screen
from ezsub.errors import InvalidSiteError, LoginFailedError


def available(pagetext):
    for sign in const.SIGNS:
        if sign.lower() in str(pagetext).lower():
            # to_screen('\n[Warning] Temporary unavailable. Try again later or check the site in browser.')
            return False
    for sign in const.BAD:
        if sign.lower() in str(pagetext).lower():
            to_screen(
                '\n[Warning] Bad request. maybe captcha is expired. login again with "ezsub login"\n')
            return False
    return True


class Mirror(object):
    def __init__(self, names=const.SITE):
        '''names is a space separated site names in preferred order.'''
        self.names = names.split()
        self._try_these = const.MIRRORS

    def select_first_responding(self, timeout=const.TIMEOUT, silent=False):
        for name in self.names:
            self._fill_attributes(name)
            if self._is_responding(timeout):
                break
            else:
                self._try_these.remove(self.name)
        else:
            to_screen(
                '[warning] your preferred sites are not accessible. check others.', silent)
            for name in self._try_these:
                self._fill_attributes(name)
                if self._is_responding(timeout):
                    break
            else:
                to_screen(
                    'Mirror: [error] any site is accessible. check internet connection.', silent)
                sys.exit()

    def get_sub_details(self, page_text):
        btn = BeautifulSoup(page_text, 'html.parser').select_one(
            self.selectors['btn'])
        if btn:
            return {
                'download_link': btn['href']
            }
        else:
            return False

    def search(self, title, silent=False):
        path = self.query_path
        data = None
        if self.method == requests.get:
            path += f"?query={title}&l=''"
        elif self.method == requests.post:
            data = {'query': title, 'l': '',
                    'g-recaptcha-response': self.captcha}
        to_screen(f'[Search] {self.base_url}{path}', silent)
        page_text = self._get_page_text(path, data=data)
        titles = BeautifulSoup(page_text, 'html.parser').select(
            self.selectors['title'])
        aggregated = {title.attrs['href']: title.text for title in titles}
        return [{'path': p, 'title': t} for p, t in aggregated.items()]

    def get_subs(self, path):
        page_text = self._get_page_text(path)
        subs = BeautifulSoup(page_text, 'html.parser').select(
            self.selectors['link'])
        return {sub['href'] for sub in subs}

    def _get_page_text(self, path, data=None, timeout=const.TIMEOUT, silent=False):
        try:
            page = self.method(self.base_url + path,
                               data=data, timeout=timeout)
            page.encoding = 'utf-8'
            return page.text
        except requests.exceptions.ConnectTimeout:
            to_screen('[error] site is not reachable. (Timeout Error)', silent)
            return ''
        except requests.exceptions.ConnectionError:
            to_screen('[error] Connection Error', silent)
            return ''
        except Exception as e:
            to_screen('[error] unknown error', silent)
            to_screen(e, silent)
            return ''

    def is_online(self):
        return self._is_responding(silent=True)

    def _is_responding(self, timeout=const.TIMEOUT, silent=False):
        try:
            if self.name not in const.MIRRORS:
                raise InvalidSiteError
            to_screen(f"[{self.name}] {self.base_url}/ is ",
                      silent, flush=True, end='')
            r = requests.head(self.base_url, timeout=timeout)
            if r.status_code == requests.codes['ok']:
                to_screen('OK', silent)
                return True
            else:
                to_screen(f'down? (status: {r.status_code})', silent)
                return False
        except requests.exceptions.ConnectTimeout:
            to_screen('not reachable. (Timeout Error)', silent)
            return False
        except requests.exceptions.ConnectionError:
            to_screen('down? (Connection Error)', silent)
            return False
        except InvalidSiteError:
            to_screen(
                f'[warning] Mirror: invalid site name: {self.name}', silent)
            return False
        except Exception as e:
            to_screen('down?', silent)
            to_screen(e, silent)
            return False

    def mass_request(self, links):
        session = FuturesSession(max_workers=const.MAX_WORKERS)
        n = len(links)
        no_links = []
        to_download = []
        requests = [session.get(self.base_url + link) for link in links]
        for i, path in enumerate(links):
            to_screen(f'\r[new links] {i+1}/{n}',
                      flush=True, end='')  # progress stats
            page_text = requests[i].result().text
            link = self.get_sub_details(page_text)
            url = self.base_url + path
            if link:
                to_download.append(
                    {'path': path, 'url': url, 'dlink': link['download_link']})
            else:  # no link is found
                no_links.append(url)
        else:
            to_screen()  # go to new line for ending progress stats
        if no_links:
            to_screen(
                '\n[Warning] Getting download links for these urls was not successful:')
            for link in no_links:
                to_screen(f'       {link}')
            to_screen()
        return to_download

    def mass_download(self, to_download, silent=False):
        session = FuturesSession(max_workers=const.MAX_WORKERS)
        all_requests = [session.get(self.base_url + sub['dlink'])
                        for sub in to_download]
        n = len(to_download)
        to_extract = []
        for i, subtitle in enumerate(to_download):
            file = subtitle['path']
            file.parent.mkdir(parents=True, exist_ok=True)
            to_screen(f"\r[download] {i+1}/{n}", silent,
                      flush=True, end='')  # progress stats
            with open(file, "w+b") as f:
                file_content = all_requests[i].result().content
                f.write(file_content)
            to_extract.append(subtitle)
        else:
            to_screen()  # go to new line for ending progress stats
        return to_extract

    def login(self, timeout=const.TIMEOUT):
        session = requests.Session()
        try:
            session.get(self.base_url + self.login_path, timeout=timeout)
            return session.cookies.get_dict()['idsrv.xsrf']
        except:
            raise LoginFailedError

    def _fill_attributes(self, name):
        self.name = name
        if self.name == 'subscene':
            self.base_url = "https://subscene.com"
            self.query_path = "/subtitles/searchbytitle"
            self.method = requests.post
            self.login_path = '/account/login'
            self.captcha = UserConf().get_captcha()
            self.selectors = {
                "title": "li div[class='title'] a",
                "link": "tr td[class='a1'] a",
                "btn": "a[id='downloadButton']"
            }
        elif self.name == 'hastisub':
            self.base_url = "http://hastisub.top"
            self.query_path = "/subtitles/searchbytitle"
            self.method = requests.get
            self.login_path = ''
            self.selectors = {
                "title": "li div[class='title'] a",
                "link": "tr td[class='a1'] a",
                "btn": "#downloadButton",
                "release": "li.release div",
                "author": "li.author a",
                "date": "#details ul li"
            }
        elif self.name == 'subf2m':
            self.base_url = "https://subf2m.co"
            self.query_path = "/subtitles/searchbytitle"
            self.method = requests.get
            self.login_path = ''
            self.selectors = {
                "title": "li div[class='title'] a",
                "link": "a[class='download icon-download']",
                "btn": "a[id='downloadButton']"
            }
        elif self.name == 'xyz':
            self.base_url = "https://subscene.xyz"
            self.query_path = "/subtitles/searchbytitle"
            self.method = requests.get
            self.login_path = ''
            self.selectors = {
                "title": "li div[class='title'] a",
                "link": "tr td[class='a1'] a",
                "btn": "a[id='downloadButton']"
            }


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
