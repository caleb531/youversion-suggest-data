#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import json
import os.path

import requests

# The pattern used to identify the <script> tag containing the relevant Bible
# data
raw_books_patt = r'window\.Bible\.__INITIAL_STATE__ = ({(?:.*?)});'


# Retrieves metadata for every book of the Bible
def get_bible_metadata():

    bible_metadata_path = os.path.join('bible', 'metadata.json')
    with open(bible_metadata_path, 'r') as bible_metadata_file:
        return json.load(bible_metadata_file)


# Convert the given raw book JSON to a schema-compliant dictionary
def get_book(raw_book):
    return {
        'id': raw_book['usfm'].lower().strip(),
        # Do not use human_long
        'name': raw_book['human'].strip()
    }


# Retrieve only the books for which this project has associated chapter data;
# this project has chosen to only include books from the Biblical Canon
def get_canon_books(books):
    bible_metadata = get_bible_metadata()
    return [book for book in books if book['id'] in bible_metadata['books']]


# Retrieves all books listed on the chapter page in the given default version
def get_books(default_version):

    books_url = 'https://www.bible.com/json/bible/books/{}'.format(
        default_version)
    raw_books = json.loads(requests.get(books_url).text)

    if not raw_books:
        raise RuntimeError('Cannot fetch book list')

    books = get_canon_books(
        get_book(raw_book) for raw_book in raw_books['items'])
    if not books:
        raise RuntimeError('Book list is empty')

    return books
