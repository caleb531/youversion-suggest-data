#!/usr/bin/env python3
# coding=utf-8

import glob
import json

from tests import YVSTestCase


def get_book_metadata():
    with open("bible/book-metadata.json", "r") as book_metadata_file:
        return json.load(book_metadata_file)


def get_languages():
    with open("bible/languages.json", "r") as languages_file:
        return json.load(languages_file)


def get_language_bibles():
    for bible_path in glob.iglob("bible/bible-*.json"):
        with open(bible_path, "r") as bible_file:
            yield bible_path, json.load(bible_file)


class TestBibles(YVSTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_book_consistency(self):
        """should have books in language that also exist in book metadata"""
        metadata_book_ids = set(get_book_metadata().keys())
        for bible_path, bible in get_language_bibles():
            bible_book_ids = set(book["id"] for book in bible["books"])
            extra_books = bible_book_ids - metadata_book_ids
            fail_msg = "{} has extra books: {}".format(
                bible_path, ", ".join(extra_books)
            )
            yield self.assertEqual, len(extra_books), 0, fail_msg

    def test_consistent_language(self):
        """should have correct language data in bible"""
        languages = get_languages()
        for bible_path, bible in get_language_bibles():
            fail_msg = "{} has incorrect or missing language data".format(bible_path)
            yield self.assertIn, bible.get("language"), languages, fail_msg

    def test_valid_default_version(self):
        """should have a valid default version for that language"""
        for bible_path, bible in get_language_bibles():
            default_version = bible["default_version"]
            fail_msg = "{} has invalid default version: {}".format(
                bible_path, default_version
            )
            default_version_is_valid = any(
                version["id"] == default_version for version in bible["versions"]
            )
            yield self.assertTrue, default_version_is_valid, fail_msg
