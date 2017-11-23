#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import nose.tools as nose
from mock import NonCallableMock, patch

import tests
import utilities.book_parser as book_parser

with open('tests/html/books.html') as html_file:
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
def test_get_books():
    """should fetch book list in proper format"""
    books = book_parser.get_books(default_version=75)
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
@patch('requests.get', return_value=NonCallableMock(text=html_content))
def test_get_books_url(requests_get):
    """should fetch book list for the given default version"""
    default_version = 75
    book_parser.get_books(default_version)
    requests_get.assert_called_once_with(
        'https://www.bible.com/bible/{}/jhn.1'.format(default_version))


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text='abc'))
def test_get_books_nonexistent(requests_get):
    """should raise error when book list cannot be found"""
    with nose.assert_raises(RuntimeError):
        book_parser.get_books(default_version=123)


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text=html_content))
@patch('utilities.book_parser.get_chapter_data', return_value={})
def test_get_books_empty(get_chapter_data, requests_get):
    """should raise error when book list is empty"""
    with nose.assert_raises(RuntimeError):
        book_parser.get_books(default_version=123)
