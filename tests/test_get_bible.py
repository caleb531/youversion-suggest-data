#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import nose.tools as nose
from mock import patch

from tests import set_up, tear_down
from utilities.add_language import get_bible

VERSIONS = [
    {'id': 234, 'name': 'ABC'},
    {'id': 123, 'name': 'DEF'},
    {'id': 456, 'name': 'GHI'},
    {'id': 345, 'name': 'JKL'}
]
BOOKS = [
    {'id': 'gen', 'name': 'Genesis'},
    {'id': '1sa', 'name': '1 Samuel'},
    {'id': 'jhn', 'name': 'John'}
]


@nose.with_setup(set_up, tear_down)
@patch('utilities.book_parser.get_books', return_value=BOOKS)
@patch('utilities.version_parser.get_versions', return_value=VERSIONS)
def test_get_bible_default_version_explicit(get_versions, get_books):
    """should store explicitly-supplied default version into Bible data"""
    language_id = 'spa'
    language_name = 'Español'
    default_version = 345
    bible = get_bible(language_id, language_name, default_version)
    get_versions.assert_called_once_with(language_id)
    nose.assert_equal(bible['books'], BOOKS)
    nose.assert_equal(bible['default_version'], default_version)
    nose.assert_equal(bible['language'], {
        'id': language_id,
        'name': language_name
    })
    nose.assert_equal(bible['versions'], VERSIONS)


@nose.with_setup(set_up, tear_down)
@patch('utilities.book_parser.get_books', return_value=BOOKS)
@patch('utilities.version_parser.get_versions', return_value=VERSIONS)
def test_get_bible_default_version_implicit(get_versions, get_books):
    """should retrieve implicit default version if none is explicitly given"""
    bible = get_bible(language_id='spa', language_name='Español')
    nose.assert_equal(bible['books'], BOOKS)
    nose.assert_equal(bible['default_version'], 123)
    nose.assert_equal(bible['language'], {
        'id': 'spa',
        'name': 'Español'
    })
    nose.assert_equal(bible['versions'], VERSIONS)


@nose.with_setup(set_up, tear_down)
@patch('utilities.book_parser.get_books', return_value=BOOKS)
@patch('utilities.version_parser.get_versions', return_value=VERSIONS)
def test_get_bible_default_version_nonexistent(get_versions, get_books):
    """should raise error if given default version does not exist in list"""
    with nose.assert_raises(RuntimeError):
        get_bible(
            language_id='spa',
            language_name='Español',
            default_version=999)
