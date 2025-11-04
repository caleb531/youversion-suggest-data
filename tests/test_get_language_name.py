#!/usr/bin/env python3
# coding=utf-8

import json
from unittest.mock import Mock, NonCallableMock, patch

import httpx
import pytest

from utilities.language_parser import get_language_name, get_languages_json

with open("tests/json/languages.json") as json_file:
    json_dict = json.load(json_file)
    patch_requests_get = patch(
        "httpx.get",
        return_value=NonCallableMock(json=Mock(return_value=json_dict)),
    )


@pytest.fixture(autouse=True)
def clear_languages_cache():
    if hasattr(get_languages_json, "cache_clear"):
        get_languages_json.cache_clear()
    yield
    if hasattr(get_languages_json, "cache_clear"):
        get_languages_json.cache_clear()


@pytest.fixture
def patched_languages_response():
    with patch_requests_get:
        yield


def test_get_language_name(patched_languages_response):
    """should fetch language name for the given language ID"""
    language_name = get_language_name("spa_es")
    assert language_name == "Español (España)"


def test_get_language_name_cache(patched_languages_response):
    """should cache languages HTML after initial fetch"""
    get_language_name("spa")
    language_name = get_language_name("fra")
    assert httpx.get.call_count == 1
    assert language_name == "Français"


@patch("httpx.get", return_value=NonCallableMock(json=Mock(return_value={})))
def test_get_language_name_no_data(requests_get):
    """should raise error when language list cannot be found"""
    with pytest.raises(RuntimeError):
        get_language_name(language_id="eng")


def test_get_language_name_nonexistent(patched_languages_response):
    """should raise error when language name cannot be found"""
    with pytest.raises(RuntimeError):
        get_language_name(language_id="xyz")
