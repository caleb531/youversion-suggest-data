#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function, unicode_literals

import itertools
import json
from operator import itemgetter

import requests


# Convert the given version element to a JSON dictionary
def get_version(raw_version):
    return {
        'id': raw_version['id'],
        'name': raw_version['local_abbreviation']
    }


# Returns a copy of the given version list with duplicates removed
def get_unique_versions(versions):

    unique_versions = []
    for name, group in itertools.groupby(versions, key=itemgetter('name')):
        # When multiple versions with the same name are encountered, favor the
        # version with the lowest ID
        version = min(group, key=itemgetter('id'))
        unique_versions.append(version)

    return unique_versions


# Retrieves all versions listed on the chapter page in the given language code
def get_versions(language_id):

    versions_url = 'https://www.bible.com/json/bible/versions/{}'.format(
        language_id)
    raw_versions = json.loads(requests.get(versions_url).text)

    if not raw_versions:
        raise RuntimeError('Cannot fetch version list')

    versions = [get_version(raw_version)
                for raw_version in raw_versions['items']]
    if not versions:
        raise RuntimeError('Version list is empty')

    unique_versions = get_unique_versions(versions)
    unique_versions.sort(key=itemgetter('id'))

    return unique_versions
