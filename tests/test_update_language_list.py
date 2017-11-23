#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import os
import os.path
import json

import nose.tools as nose

import utilities
import utilities.add_language as add_lang
from tests import set_up, tear_down


def get_languages():
    """Retrieves a list of all supported languages"""
    languages_path = os.path.join(
        utilities.PACKAGED_DATA_DIR_PATH, 'bible', 'languages.json')
    with open(languages_path, 'r') as languages_file:
        return json.load(languages_file)


def get_language(languages, language_id):
    """Retrieve a language from the given language list with the given ID"""
    for language in languages:
        if language['id'] == language_id:
            return language
    return None


@nose.with_setup(set_up, tear_down)
def test_update_languge_list_add():
    """should add new languages to language list"""
    new_lang_id = 'kln'
    new_lang_name = 'Klingon'
    orig_num_langs = len(get_languages())
    add_lang.update_language_list(new_lang_id, new_lang_name)
    langs = get_languages()
    num_langs = len(langs)
    nose.assert_equal(num_langs, orig_num_langs + 1)
    new_lang = get_language(langs, new_lang_id)
    nose.assert_is_not_none(new_lang)
    nose.assert_equal(new_lang['name'], new_lang_name)


@nose.with_setup(set_up, tear_down)
def test_update_languge_list_update():
    """should update existing languages in language list"""
    updated_lang_id = 'spa'
    updated_lang_name = 'The Spanish Language'
    orig_num_langs = len(get_languages())
    add_lang.update_language_list(updated_lang_id, updated_lang_name)
    langs = get_languages()
    num_langs = len(langs)
    nose.assert_equal(num_langs, orig_num_langs)
    updated_lang = get_language(langs, updated_lang_id)
    nose.assert_is_not_none(updated_lang)
    nose.assert_equal(updated_lang['name'], updated_lang_name)
