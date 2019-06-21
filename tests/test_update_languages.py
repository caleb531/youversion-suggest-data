#!/usr/bin/env python
# coding=utf-8

import nose.tools as nose
from mock import patch

import utilities.update_languages as update_langs
from tests.decorators import redirect_stdout


@patch('utilities.update_languages.update_language')
@redirect_stdout
def test_update_language(out, update_language):
    """should update language with correct default version"""
    update_langs.update_languages()
    nose.assert_equal(out.getvalue().count('\n'), 24)
    nose.assert_equal(update_language.call_count, 24)
    update_language.assert_any_call('eng')
    update_language.assert_any_call('swe')
    update_language.assert_any_call('deu')


@patch('utilities.update_languages.update_languages',
       side_effect=KeyboardInterrupt)
@redirect_stdout
def test_main_keyboardinterrupt(out, update_languages):
    """main function should quit gracefully when ^C is pressed"""
    nose.assert_is_none(update_langs.main())
