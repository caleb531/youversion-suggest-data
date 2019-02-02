#!/usr/bin/env python3

import glob
import json
import re

import nose.tools as nose


def get_book_metadata():
    with open('bible/book-metadata.json', 'r') as book_metadata_file:
        return json.load(book_metadata_file)


def get_language_bibles():
    for file_path in glob.iglob('bible/language-*.json'):
        with open(file_path, 'r') as language_file:
            language_id = re.search('language-(.*?).json', file_path).group(1)
            yield language_id, json.load(language_file)


def test_book_consistency():
    metadata_book_ids = set(get_book_metadata().iterkeys())
    """should have books in language that also exist in book metadata"""
    for language_id, bible in get_language_bibles():
        bible_book_ids = set(book['id'] for book in bible['books'])
        extra_books = bible_book_ids - metadata_book_ids
        fail_msg = 'language \'{}\' has extra books: {}'.format(
            language_id, ', '.join(extra_books))
        yield nose.assert_equal, len(extra_books), 0, fail_msg


def test_valid_default_version():
    """should have a valid default version for that language"""
    for language_id, bible in get_language_bibles():
        default_version = bible['default_version']
        fail_msg = 'language \'{}\' has invalid default version: {}'.format(
            language_id, default_version)
        default_version_is_valid = any(
            version['id'] == default_version for version in bible['versions'])
        yield nose.assert_true, default_version_is_valid, fail_msg
