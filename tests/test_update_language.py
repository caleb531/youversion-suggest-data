#!/usr/bin/env python3
# coding=utf-8


from unittest.mock import patch

import utilities.update_language as update_lang
from tests import YVSTestCase
from tests.decorators import redirect_stdout


class TestUpdateLanguage(YVSTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @patch("utilities.update_language.add_language")
    @redirect_stdout
    def test_update_language(self, out, add_language):
        """should update language with correct default version"""
        update_lang.update_language("swe")
        self.assertIn("Updating language 'swe'", out.getvalue())
        add_language.assert_called_once_with(language_id="swe", default_version=154)

    @patch("sys.argv", [update_lang.__file__, "swe"])
    @patch("utilities.update_language.add_language")
    @redirect_stdout
    def test_main(self, out, add_language):
        """main function should pass correct arguments to add_language"""
        update_lang.main()
        add_language.assert_called_once_with(language_id="swe", default_version=154)

    @patch("sys.argv", [update_lang.__file__, "eng", "--default-version", "116"])
    @patch("utilities.update_language.add_language")
    @redirect_stdout
    def test_main_change_default_version(self, out, add_language):
        """main function should pass correct arguments to add_language"""
        update_lang.main()
        add_language.assert_called_once_with(language_id="eng", default_version=116)

    @patch("utilities.update_language.update_language", side_effect=KeyboardInterrupt)
    @patch("utilities.update_language.parse_cli_args")
    @redirect_stdout
    def test_main_keyboardinterrupt(self, out, parse_cli_args, update_language):
        """main function should quit gracefully when ^C is pressed"""
        self.assertIsNone(update_lang.main())
