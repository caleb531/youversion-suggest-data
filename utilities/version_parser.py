#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import re
import requests
from pyquery import PyQuery as pq


# Parse the numeric version ID from the given version element
def get_version_id(version_elem):
    patt = r'(?<=/versions/)(\d+)-([a-z]+\d*)'
    matches = re.search(patt, version_elem.attr.href, flags=re.UNICODE)
    if matches:
        return int(matches.group(1))
    else:
        return None


# Parse the version name from the given version element
def get_version_name(version_elem):
    matches = re.search(r'\(\s*([^\)]+)\s*\)\s*$', version_elem.text())
    if matches:
        return matches.group(1)
    else:
        return None


# Convert the given version element to a JSON dictionary
def get_version(version_elem):
    return {
        'id': get_version_id(pq(version_elem)),
        'name': get_version_name(pq(version_elem))
    }


# Retrieves all versions listed on the chapter page in the given language code
def get_versions(language_id):

    d = pq(requests.get(
        'https://www.bible.com/languages/{}'.format(language_id)).text)

    version_elems = d('a[href*="/versions/"]')

    return [get_version(version_elem)
            for version_elem in version_elems]
