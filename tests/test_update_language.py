#!/usr/bin/env python3
# coding=utf-8


from unittest.mock import patch

import utilities.update_language as update_lang


@patch("utilities.update_language.add_language")
def test_update_language(add_language, capsys):
    """should update language with correct default version"""
    update_lang.update_language("swe")
    captured = capsys.readouterr()
    assert "Updating language 'swe'" in captured.out
    add_language.assert_called_once_with(language_id="swe", default_version=154)


@patch("sys.argv", [update_lang.__file__, "swe"])
@patch("utilities.update_language.add_language")
def test_main(add_language):
    """main function should pass correct arguments to add_language"""
    update_lang.main()
    add_language.assert_called_once_with(language_id="swe", default_version=154)


@patch("sys.argv", [update_lang.__file__, "eng", "--default-version", "116"])
@patch("utilities.update_language.add_language")
def test_main_change_default_version(add_language):
    """main function should pass correct arguments to add_language"""
    update_lang.main()
    add_language.assert_called_once_with(language_id="eng", default_version=116)


@patch("utilities.update_language.update_language", side_effect=KeyboardInterrupt)
@patch("utilities.update_language.parse_cli_args")
def test_main_keyboardinterrupt(parse_cli_args, update_language):
    """main function should quit gracefully when ^C is pressed"""
    assert update_lang.main() is None
