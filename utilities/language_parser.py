#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import requests

from utilities.yv_parser import YVParser


# Finds on the YouVersion website the language name associated with the given
# language code
class LanguageParser(YVParser):

    # Associates the given language ID with this parser instance
    def __init__(self, language_id):
        YVParser.__init__(self)
        self.language_url_suffix = '/languages/{}'.format(language_id)

    # Resets parser variables (implicitly called on instantiation)
    def reset(self):
        YVParser.reset(self)
        self.depth = 0
        self.in_language = False
        self.language_depth = 0
        self.language_name = None
        self.language_name_parts = []

    # Detects the start of a language link
    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.depth += 1
        if ('href' in attr_dict and
                attr_dict['href'].endswith(self.language_url_suffix)):
            self.in_language = True
            self.language_depth = self.depth

    # Detects the end of a language link
    def handle_endtag(self, tag):
        if self.in_language and self.depth == self.language_depth:
            self.in_language = False
            self.language_name = ''.join(self.language_name_parts).strip()
            # Empty the list containing the language name parts
            del self.language_name_parts[:]
        self.depth -= 1

    # Handles the language name contained within the current language link
    def handle_data(self, data):
        if self.in_language:
            self.language_name_parts.append(data)


# Retrieves the language with
def get_language_name(language_id):

    entry_key = 'languages.html'
    page_html = requests.get(
        'https://www.bible.com/languages'.format(language_id)).text

    parser = LanguageParser(language_id)
    parser.feed(page_html)

    return parser.language_name
