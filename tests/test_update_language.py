#!/usr/bin/env python
# coding=utf-8

import nose.tools as nose
from mock import patch

import utilities.update_language as update_lang
from tests.decorators import redirect_stdout


@patch('utilities.update_language.add_language')
@redirect_stdout
def test_update_language(out, add_language):
    """should update language with correct default version"""
    update_lang.update_language('swe')
    nose.assert_in('Updating language \'swe\'', out.getvalue())
    add_language.assert_called_once_with(
        language_id='swe',
        default_version=154)


@patch('sys.argv', [update_lang.__file__, 'swe'])
@patch('utilities.update_language.add_language')
@redirect_stdout
def test_main(out, add_language):
    """main function should pass correct arguments to add_language"""
    update_lang.main()
    add_language.assert_called_once_with(
        language_id='swe', default_version=154)


@patch('utilities.update_language.update_language',
       side_effect=KeyboardInterrupt)
@patch('utilities.update_language.parse_cli_args')
@redirect_stdout
def test_main_keyboardinterrupt(out, parse_cli_args, update_language):
    """main function should quit gracefully when ^C is pressed"""
    nose.assert_is_none(update_lang.main())
