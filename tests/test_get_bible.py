#!/usr/bin/env python3
# coding=utf-8

from unittest.mock import patch

from tests import YVSTestCase
from utilities.add_language import get_bible

VERSIONS = [
    {"id": 234, "name": "ABC"},
    {"id": 123, "name": "DEF"},
    {"id": 456, "name": "GHI"},
    {"id": 345, "name": "JKL"},
]
BOOKS = [
    {"id": "gen", "name": "Genesis"},
    {"id": "1sa", "name": "1 Samuel"},
    {"id": "jhn", "name": "John"},
]


class TestGetBible(YVSTestCase):
    @patch("utilities.book_parser.get_books", return_value=BOOKS)
    @patch("utilities.version_parser.get_versions", return_value=VERSIONS)
    def test_get_bible_default_version_explicit(self, get_versions, get_books):
        """should store explicitly-supplied default version into Bible data"""
        language_id = "spa"
        language_name = "Español"
        default_version = 345
        bible = get_bible(language_id, language_name, default_version)
        get_versions.assert_called_once_with(language_id)
        self.assertEqual(bible["books"], BOOKS)
        self.assertEqual(bible["default_version"], default_version)
        self.assertEqual(bible["language"], {"id": language_id, "name": language_name})
        self.assertEqual(bible["versions"], VERSIONS)

    @patch("utilities.book_parser.get_books", return_value=BOOKS)
    @patch("utilities.version_parser.get_versions", return_value=VERSIONS)
    def test_get_bible_default_version_implicit(self, get_versions, get_books):
        """should retrieve implicit default version if none is explicitly given"""
        bible = get_bible(language_id="spa", language_name="Español")
        self.assertEqual(bible["books"], BOOKS)
        self.assertEqual(bible["default_version"], 123)
        self.assertEqual(bible["language"], {"id": "spa", "name": "Español"})
        self.assertEqual(bible["versions"], VERSIONS)

    @patch("utilities.book_parser.get_books", return_value=BOOKS)
    @patch("utilities.version_parser.get_versions", return_value=VERSIONS)
    def test_get_bible_default_version_nonexistent(self, get_versions, get_books):
        """should raise error if given default version does not exist in list"""
        with self.assertRaises(RuntimeError):
            get_bible(language_id="spa", language_name="Español", default_version=999)
