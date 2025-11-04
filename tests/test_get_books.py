#!/usr/bin/env python3
# coding=utf-8

import json
from unittest.mock import Mock, NonCallableMock, patch

import pytest

from utilities.book_parser import get_books

with open("tests/json/books.json") as json_file:
    json_dict = json.load(json_file)
    patch_requests_get = patch(
        "httpx.get", return_value=NonCallableMock(json=Mock(return_value=json_dict))
    )


@pytest.fixture
def patched_books_response():
    with patch_requests_get:
        yield


def test_get_books(patched_books_response):
    """should fetch book list in proper format"""
    books = get_books(default_version=75)
    assert len(books) == 3
    assert books == [
        {
            "id": "gen",
            "name": "Genesis",
        },
        {
            "id": "1sa",
            "name": "1 Samuël",
        },
        {
            "id": "jhn",
            "name": "Johannes",
        },
    ]


@patch("httpx.get", return_value=NonCallableMock(json=Mock(return_value=json_dict)))
def test_get_books_url(requests_get):
    """should fetch book list for the given default version"""
    default_version = 75
    get_books(default_version)
    requests_get.assert_called_once_with(
        "https://www.bible.com/api/bible/version/{}".format(default_version),
        headers={"user-agent": "YouVersion Suggest"},
    )


@patch("httpx.get", return_value=NonCallableMock(json=Mock(return_value={})))
def test_get_books_nonexistent(requests_get):
    """should raise error when book list cannot be found"""
    with pytest.raises(RuntimeError):
        get_books(default_version=123)


@patch("httpx.get", return_value=NonCallableMock(json=Mock(return_value=json_dict)))
@patch("utilities.book_parser.get_book_metadata", return_value={"books": {}})
def test_get_books_empty(get_book_metadata, requests_get):
    """should raise error when book list is empty"""
    with pytest.raises(RuntimeError):
        get_books(default_version=123)
