#!/usr/bin/env python3
# coding=utf-8

import json
from unittest.mock import Mock, NonCallableMock, patch

import httpx

from tests import YVSTestCase
from utilities.language_parser import get_language_name, get_languages_json

with open("tests/json/languages.json") as json_file:
    json_dict = json.load(json_file)
    patch_requests_get = patch(
        "httpx.get",
        return_value=NonCallableMock(json=Mock(return_value=json_dict)),
    )


class TestGetLanguageName(YVSTestCase):
    def setUp(self):
        patch_requests_get.start()
        super().setUp()

    def tearDown(self):
        patch_requests_get.stop()
        super().tearDown()
        get_languages_json.cache_clear()

    def test_get_language_name(self):
        """should fetch language name for the given language ID"""
        language_name = get_language_name("spa_es")
        self.assertEqual(language_name, "Español (España)")

    def test_get_language_name_cache(self):
        """should cache languages HTML after initial fetch"""
        if hasattr(get_languages_json, "cache_clear"):
            get_languages_json.cache_clear()
        get_language_name("spa")
        language_name = get_language_name("fra")
        httpx.get.assert_called_once()
        self.assertEqual(language_name, "Français")

    @patch("httpx.get", return_value=NonCallableMock(json=Mock(return_value={})))
    def test_get_language_name_no_data(self, requests_get):
        """should raise error when language list cannot be found"""
        with self.assertRaises(RuntimeError):
            get_language_name(language_id="eng")

    def test_get_language_name_nonexistent(self):
        """should raise error when language name cannot be found"""
        with self.assertRaises(RuntimeError):
            get_language_name(language_id="xyz")
