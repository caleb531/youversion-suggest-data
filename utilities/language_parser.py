#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import cachetools.func
import requests
from pyquery import PyQuery as pq


# fetch to speed up subsequent requests
@cachetools.func.lru_cache(maxsize=1)
def get_languages_html():
    return requests.get('https://www.bible.com/languages').text


# Retrieves the language with
def get_language_name(language_id):

    d = pq(get_languages_html())
    lang_elem = d('a[href="/languages/{}"]'.format(language_id))

    language_name = lang_elem.text()
    if not language_name:
        raise RuntimeError('Cannot retrieve language data. Aborting.')

    return language_name
