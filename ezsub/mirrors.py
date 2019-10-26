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
from ezsub.errors import InvalidSiteError, LoginFailedError, NoSiteIsAvailableError

cur = const.Curser

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
        self._try_these = const.MIRRORS

    def select_first_responding(self, timeout=const.TIMEOUT):
        for name in self.names:
            self._fill_attributes(name)
            if self._is_responding(timeout):
                break
            else:
                self._try_these.remove(self.name)
        else:
            if self._try_these:  # if still site left to try
                to_screen(" your preferred sites are not accessible. trying others...", style="yellow;italic")
            for name in self._try_these:
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
        soup = BeautifulSoup(page_text, 'html.parser')
        titles = soup.select(self.selectors['title'])
        aggregated = {title.attrs['href']: title.text for title in titles}
        return [{'path': p, 'title': t} for p, t in aggregated.items()]

    def get_subs(self, path):
        page_text = self._get_page_text(path)
        soup = BeautifulSoup(page_text, 'html.parser')
        subs = soup.select(self.selectors['link'])
        return {sub['href'] for sub in subs}

    def _get_page_text(self, path, data=None, timeout=const.TIMEOUT):
        try:
            page = self.method(self.base_url + path, data=data, timeout=timeout)
            page.encoding = 'utf-8'
            return page.text
        except requests.exceptions.ConnectTimeout:
            to_screen("[error] site is not reachable. (Timeout Error)", style="red")
        except requests.exceptions.ConnectionError:
            to_screen("[error] Connection Error", style="red")
        except Exception as e:
            to_screen("[error] unknown error", style="red")
            to_screen(e, style="red")
        return ''

    def _is_responding(self, timeout=const.TIMEOUT):
        try:
            if self.name not in const.MIRRORS:
                raise InvalidSiteError
            to_screen(f"[site] ", end='')
            to_screen(f"{self.base_url}/", style="info", end='')
            to_screen(" is ", end='')
            r = requests.head(self.base_url, timeout=timeout)
            if r.status_code == requests.codes['ok']:
                to_screen('OK', style="bold;ok")
                return True
            else:
                to_screen(f"down? (status: {r.status_code})", style="red")
        except requests.exceptions.ConnectTimeout:
            to_screen("not reachable. (Timeout Error)", style="red")
        except requests.exceptions.ConnectionError:
            to_screen("down? (Connection Error)", style="red")
        except InvalidSiteError:
            to_screen(f"\r[site] invalid site name: {self.name}", style="warning")
        except Exception as e:
            to_screen("down?", style="red")
            to_screen(e, style="red")
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
        return None


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
