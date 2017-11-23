#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
from mock import patch, NonCallableMock

import nose.tools as nose
import requests

import tests
import utilities.add_language as add_lang
import utilities.language_parser as lang_parser

with open('tests/html/languages.html') as html_file:
    html_content = html_file.read().decode('utf-8')
    patch_requests_get = patch(
        'requests.get', return_value=NonCallableMock(
            text=html_content))


def set_up():
    patch_requests_get.start()
    tests.set_up()


def tear_down():
    patch_requests_get.stop()
    tests.tear_down()


@nose.with_setup(set_up, tear_down)
def test_get_language_name():
    """should fetch language name for the given language ID"""
    language_name = add_lang.get_language_name('spa_es')
    nose.assert_equal(language_name, 'Español (España) - Spanish (Spain)')


@nose.with_setup(set_up, tear_down)
def test_get_language_name_cache():
    """should cache languages HTML after initial fetch"""
    if hasattr(lang_parser.get_languages_html, 'cache_clear'):
        lang_parser.get_languages_html.cache_clear()
    add_lang.get_language_name('spa')
    language_name = add_lang.get_language_name('fra')
    requests.get.assert_called_once()
    nose.assert_equal(language_name, 'Français - French')


@nose.with_setup(set_up, tear_down)
def test_get_language_name_nonexistent():
    """should raise error when language name cannot be found"""
    with nose.assert_raises(RuntimeError):
        add_lang.get_language_name(language_id='xyz')
