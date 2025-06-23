#!/usr/bin/env python3
# coding=utf-8

import os
import os.path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import utilities

temp_dir = tempfile.gettempdir()
packaged_data_dir_path_patcher = patch(
    "utilities.PACKAGED_DATA_DIR_PATH", os.path.join(temp_dir, "yvs-core")
)


class YVSTestCase(unittest.TestCase):
    def setUp(self):
        orig_packaged_data_dir_path = utilities.PACKAGED_DATA_DIR_PATH
        packaged_data_dir_path_patcher.start()
        try:
            shutil.copytree(
                os.path.join(orig_packaged_data_dir_path, "bible"),
                os.path.join(utilities.PACKAGED_DATA_DIR_PATH, "bible"),
            )
        except shutil.Error:
            pass

    def tearDown(self):
        try:
            shutil.rmtree(utilities.PACKAGED_DATA_DIR_PATH)
        except OSError:
            pass
        packaged_data_dir_path_patcher.stop()
