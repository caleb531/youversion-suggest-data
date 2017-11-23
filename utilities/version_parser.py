#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import itertools
import re
from operator import itemgetter

import requests
from pyquery import PyQuery as pq


# Parse the numeric version ID from the given version element
def get_version_id(version_elem):
    patt = r'(?<=/versions/)(\d+)-([a-z]+\d*)'
    matches = re.search(patt, version_elem.attr.href, flags=re.UNICODE)
    if not matches:
        raise RuntimeError('Cannot parse version ID')
    return int(matches.group(1))


# Parse the version name from the given version element
def get_version_name(version_elem):
    matches = re.search(r'\(\s*([^\)]+)\s*\)\s*$', version_elem.text())
    if not matches:
        raise RuntimeError('Cannot parse version name')
    return matches.group(1)


# Convert the given version element to a JSON dictionary
def get_version(version_elem):
    return {
        'id': get_version_id(pq(version_elem)),
        'name': get_version_name(pq(version_elem))
    }


# Returns a copy of the given version list with duplicates removed
def get_unique_versions(versions):

    unique_versions = []
    for name, group in itertools.groupby(versions, key=itemgetter('name')):
        # When duplicates are encountered, favor the version with the lowest ID
        version = min(group, key=itemgetter('id'))
        unique_versions.append(version)

    return unique_versions


# Retrieves all versions listed on the chapter page in the given language code
def get_versions(language_id):

    d = pq(requests.get(
        'https://www.bible.com/languages/{}'.format(language_id)).text)
    version_elems = d('a[href*="/versions/"]')

    versions = [get_version(elem) for elem in version_elems]
    if not versions:
        raise RuntimeError('Cannot retrieve version data')

    versions.sort(key=itemgetter('id'))
    unique_versions = get_unique_versions(versions)

    return unique_versions
