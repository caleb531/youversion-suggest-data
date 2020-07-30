#!/usr/bin/env python3
# coding=utf-8

from unittest.mock import patch

import nose.tools as nose

import utilities.update_languages as update_langs
from tests.decorators import redirect_stdout


@patch('utilities.update_languages.update_language')
@redirect_stdout
def test_update_languages(out, update_language):
    """should update all languages"""
    update_langs.update_languages()
    nose.assert_greater_equal(out.getvalue().count('\n'), 20)
    nose.assert_greater_equal(update_language.call_count, 20)
    update_language.assert_any_call('eng')
    update_language.assert_any_call('swe')
    update_language.assert_any_call('deu')


@patch('utilities.update_languages.update_languages',
       side_effect=KeyboardInterrupt)
@redirect_stdout
def test_main_keyboardinterrupt(out, update_languages):
    """main function should quit gracefully when ^C is pressed"""
    nose.assert_is_none(update_langs.main())
