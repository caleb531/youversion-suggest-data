#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import nose.tools as nose
import requests
from mock import NonCallableMock, patch

import tests
from utilities.language_parser import get_language_name, get_languages_json

with open('tests/json/languages.json') as json_file:
    json_content = json_file.read().decode('utf-8')
    patch_requests_get = patch(
        'requests.get', return_value=NonCallableMock(
            text=json_content))


def set_up():
    patch_requests_get.start()
    tests.set_up()


def tear_down():
    patch_requests_get.stop()
    tests.tear_down()
    get_languages_json.cache_clear()


@nose.with_setup(set_up, tear_down)
def test_get_language_name():
    """should fetch language name for the given language ID"""
    language_name = get_language_name('spa_es')
    nose.assert_equal(language_name, 'Español (España)')


@nose.with_setup(set_up, tear_down)
def test_get_language_name_cache():
    """should cache languages HTML after initial fetch"""
    if hasattr(get_languages_json, 'cache_clear'):
        get_languages_json.cache_clear()
    get_language_name('spa')
    language_name = get_language_name('fra')
    requests.get.assert_called_once()
    nose.assert_equal(language_name, 'Français')


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text='{}'))
def test_get_language_name_no_data(requests_get):
    """should raise error when language list cannot be found"""
    with nose.assert_raises(RuntimeError):
        get_language_name(language_id='eng')


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text='{"items":[]}'))
def test_get_language_name_empty(requests_get):
    """should raise error when language list is empty"""
    with nose.assert_raises(RuntimeError):
        get_language_name(language_id='eng')


@nose.with_setup(set_up, tear_down)
def test_get_language_name_nonexistent():
    """should raise error when language name cannot be found"""
    with nose.assert_raises(RuntimeError):
        get_language_name(language_id='xyz')
