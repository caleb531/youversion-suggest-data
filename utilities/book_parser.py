#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import json
import re

import requests
from pyquery import PyQuery as pq


# The pattern used to identify the <script> tag containing the relevant Bible
# data
bible_data_patt = r'window\.Bible\.__INITIAL_STATE__ = ({(?:.*?)});'


# Find the script element among the given set that contains the Bible data
def find_bible_data(script_elems):
    for script_elem in script_elems:
        matches = re.search(bible_data_patt, pq(script_elem).text(),
                            re.UNICODE | re.DOTALL)
        if matches:
            return json.loads(matches.group(1))
    return None


# Convert the given raw book JSON to a schema-compliant dictionary
def get_book(raw_book):
    return {
        'id': raw_book['usfm'].lower().strip(),
        # Do not use human_long
        'name': raw_book['human'].strip()
    }


# Retrieves all books listed on the chapter page in the given default version
def get_books(default_version):

    d = pq(requests.get(
        'https://www.bible.com/bible/{}/jhn.1'.format(default_version)).text)

    script_elems = d('script')
    bible_data = find_bible_data(script_elems)
    if bible_data:
        return [get_book(raw_book)
                for raw_book in bible_data['bibleReader']['books']['all']]

    return None
