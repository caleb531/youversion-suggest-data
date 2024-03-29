#!/usr/bin/env python3
# coding=utf-8


from unittest.mock import patch

import utilities.update_languages as update_langs
from tests import YVSTestCase
from tests.decorators import redirect_stdout


class TestUpdateLanguages(YVSTestCase):

    @patch("utilities.update_languages.update_language")
    @redirect_stdout
    def test_update_languages(self, out, update_language):
        """should update all languages"""
        update_langs.update_languages()
        self.assertGreaterEqual(out.getvalue().count("\n"), 20)
        self.assertGreaterEqual(update_language.call_count, 20)
        update_language.assert_any_call("eng")
        update_language.assert_any_call("swe")
        update_language.assert_any_call("deu")

    @patch("utilities.update_languages.update_languages", side_effect=KeyboardInterrupt)
    @redirect_stdout
    def test_main_keyboardinterrupt(self, out, update_languages):
        """main function should quit gracefully when ^C is pressed"""
        # AttributeError: '_io.StringIO' object has no attribute 'assertIsNone'
        self.assertIsNone(update_langs.main())
