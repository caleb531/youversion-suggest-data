#!/usr/bin/env python3
# coding=utf-8

import json
from unittest.mock import Mock, NonCallableMock, patch

from tests import YVSTestCase
from utilities.book_parser import get_books

with open("tests/json/books.json") as json_file:
    json_dict = json.load(json_file)
    patch_requests_get = patch(
        "httpx.get", return_value=NonCallableMock(json=Mock(return_value=json_dict))
    )


class TestGetBooks(YVSTestCase):
    def setUp(self):
        patch_requests_get.start()
        super().setUp()

    def tearDown(self):
        patch_requests_get.stop()
        super().tearDown()

    def test_get_books(self):
        """should fetch book list in proper format"""
        books = get_books(default_version=75)
        self.assertEqual(len(books), 3)
        self.assertListEqual(
            books,
            [
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
            ],
        )

    @patch("httpx.get", return_value=NonCallableMock(json=Mock(return_value=json_dict)))
    def test_get_books_url(self, requests_get):
        """should fetch book list for the given default version"""
        default_version = 75
        get_books(default_version)
        requests_get.assert_called_once_with(
            "https://www.bible.com/api/bible/version/{}".format(default_version),
            headers={"user-agent": "YouVersion Suggest"},
        )

    @patch("httpx.get", return_value=NonCallableMock(json=Mock(return_value={})))
    def test_get_books_nonexistent(self, requests_get):
        """should raise error when book list cannot be found"""
        with self.assertRaises(RuntimeError):
            get_books(default_version=123)

    @patch("httpx.get", return_value=NonCallableMock(json=Mock(return_value=json_dict)))
    @patch("utilities.book_parser.get_book_metadata", return_value={"books": {}})
    def test_get_books_empty(self, get_book_metadata, requests_get):
        """should raise error when book list is empty"""
        with self.assertRaises(RuntimeError):
            get_books(default_version=123)
