# tests.test_add_language.test_get_books
# coding=utf-8

from __future__ import unicode_literals
from mock import patch, NonCallableMock

import nose.tools as nose

import tests
import utilities.add_language as add_lang

with open('tests/html/books.html') as html_file:
    html_content = html_file.read().decode('utf-8')
    patch_urlopen = patch(
        'requests.get', return_value=NonCallableMock(
            text=html_content.decode('utf-8')))


def set_up():
    patch_urlopen.start()
    tests.set_up()


def tear_down():
    patch_urlopen.stop()
    tests.tear_down()


@nose.with_setup(set_up, tear_down)
def test_get_books():
    """should fetch book list in proper format"""
    books = add_lang.get_books(default_version=75)
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
def test_get_books_url(get_url_content):
    """should fetch book list for the given default version"""
    default_version = 75
    add_lang.get_books(default_version)
    get_url_content.assert_called_once_with(
        'https://www.bible.com/bible/{}/jhn.1'.format(default_version))


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text='abc'))
def test_get_books_nonexistent(get_url_content):
    """should raise error when book list cannot be found"""
    with nose.assert_raises(RuntimeError):
        add_lang.get_books(default_version=123)


@nose.with_setup(set_up, tear_down)
@patch('requests.get', return_value=NonCallableMock(text=html_content))
@patch('utilities.add_language.get_chapter_data', return_value={})
def test_get_books_empty(get_chapter_data, get_url_content):
    """should raise error when book list is empty"""
    with nose.assert_raises(RuntimeError):
        add_lang.get_books(default_version=123)
