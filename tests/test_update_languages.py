#!/usr/bin/env python3
# coding=utf-8


from unittest.mock import patch

import utilities.update_languages as update_langs


@patch("utilities.update_languages.update_language")
def test_update_languages(update_language, capsys):
    """should update all languages"""
    update_langs.update_languages()
    captured = capsys.readouterr()
    assert captured.out.count("\n") >= 20
    assert update_language.call_count >= 20
    update_language.assert_any_call("eng")
    update_language.assert_any_call("swe")
    update_language.assert_any_call("deu")


@patch("utilities.update_languages.update_languages", side_effect=KeyboardInterrupt)
def test_main_keyboardinterrupt(update_languages):
    """main function should quit gracefully when ^C is pressed"""
    # AttributeError: '_io.StringIO' object has no attribute 'assertIsNone'
    assert update_langs.main() is None
