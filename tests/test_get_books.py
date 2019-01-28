#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import nose.tools as nose
from mock import NonCallableMock, patch

import tests
from utilities.book_parser import get_books

with open('tests/json/books.json') as json_file:
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


@nose.with_setup(set_up, tear_down)
def test_get_books():
    """should fetch book list in proper format"""
    books = get_books(default_version=75)
    nose.assert_equal(len(books), 3)
    nose.assert_list_equal(books, [
        {
            'id': 'gen',
            'name': 'Genesis',
        },
        {
            'id': '1sa',
            'name': '1 Samuël',
        },
        {
            'id': 'jhn',
            'name': 'Johannes',
        }
    ])


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text=json_content))
def test_get_books_url(requests_get):
    """should fetch book list for the given default version"""
    default_version = 75
    get_books(default_version)
    requests_get.assert_called_once_with(
        'https://www.bible.com/json/bible/books/{}'.format(default_version))


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text='{}'))
def test_get_books_nonexistent(requests_get):
    """should raise error when book list cannot be found"""
    with nose.assert_raises(RuntimeError):
        get_books(default_version=123)


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text=json_content))
@patch('utilities.book_parser.get_bible_metadata', return_value={'books': {}})
def test_get_books_empty(get_bible_metadata, requests_get):
    """should raise error when book list is empty"""
    with nose.assert_raises(RuntimeError):
        get_books(default_version=123)
