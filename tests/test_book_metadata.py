#!/usr/bin/env python3
# coding=utf-8

import json

import pytest


def get_book_metadata():
    with open("bible/book-metadata.json", "r") as book_metadata_file:
        return json.load(book_metadata_file)


@pytest.mark.parametrize(("book_id", "book_metadata_item"), get_book_metadata().items())
def test_chapter_verse_correspondence(book_id, book_metadata_item):
    """should have a verse count for every chapter in the metadata store"""
    chapter_count = book_metadata_item["chapters"]
    verse_count = len(book_metadata_item["verses"])
    fail_msg = "book {} has {} chapters but {} verse counts found".format(
        book_id, chapter_count, verse_count
    )
    assert verse_count == chapter_count, fail_msg
