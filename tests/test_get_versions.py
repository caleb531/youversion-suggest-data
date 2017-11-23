#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals
from mock import patch, NonCallableMock

import nose.tools as nose

import tests
import utilities.add_language as add_lang

with open('tests/html/versions.html') as html_file:
    html_content = html_file.read().decode('utf-8')
    patch_urlopen = patch(
        'requests.get', return_value=NonCallableMock(
            text=html_content))


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@nose.with_setup(set_up, tear_down)
def test_get_versions():
    """should fetch version list in proper format"""
    versions = add_lang.get_versions('deu')
    nose.assert_equal(len(versions), 5)
    nose.assert_list_equal(versions, [
        {
            'id': 8,
            'name': 'AMPC'
        },
        {
            'id': 206,
            'name': 'WEB-神'
        },
        {
            'id': 207,
            'name': 'WEB-上帝'
        },
        {
            'id': 477,
            'name': 'RV1885'
        },
        {
            'id': 877,
            'name': 'NBH'
        }
    ])


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text=html_content))
def test_get_versions_url(get_url_content):
    """should fetch version list for the given language ID"""
    language_id = 'nld'
    add_lang.get_versions(language_id)
    get_url_content.assert_called_once_with(
        'https://www.bible.com/languages/{}'.format(language_id))


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text='abc'))
def test_get_versions_nonexistent(get_url_content):
    """should raise error when version list cannot be found"""
    with nose.assert_raises(RuntimeError):
        add_lang.get_versions('xyz')
