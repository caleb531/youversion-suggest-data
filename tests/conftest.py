#!/usr/bin/env python3
# coding=utf-8

import os
import shutil
from unittest.mock import patch

import pytest

import utilities


@pytest.fixture(autouse=True)
def packaged_data_dir(tmp_path_factory):
    """Provide an isolated packaged data directory for each test."""
    original_value = utilities.PACKAGED_DATA_DIR_PATH
    temp_dir = os.fspath(tmp_path_factory.mktemp("yvs-core"))
    patched_path = os.path.join(temp_dir, "data")
    os.makedirs(patched_path, exist_ok=True)
    shutil.copytree(
        os.path.join(original_value, "bible"),
        os.path.join(patched_path, "bible"),
    )
    try:
        with patch.object(utilities, "PACKAGED_DATA_DIR_PATH", patched_path):
            yield
    finally:
        shutil.rmtree(patched_path, ignore_errors=True)
