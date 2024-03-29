#!/usr/bin/env python3
# coding=utf-8

import copy
import json
import os
import os.path

import utilities
import utilities.add_language as add_lang
from tests import YVSTestCase

LANGUAGE_ID = "swe"
BIBLE = {
    "books": [{"id": "gen", "name": "Första Moseboken"}],
    "default_version": 33,
    "versions": [{"id": 33, "name": "BSV"}, {"id": 154, "name": "B2000"}],
}


class TestSaveBible(YVSTestCase):

    def test_save_bible_new(self):
        """should save Bible data to new data file if it doesn't exist"""
        bible_file_path = os.path.join(
            utilities.PACKAGED_DATA_DIR_PATH,
            "bible",
            "bible-{}.json".format(LANGUAGE_ID),
        )
        add_lang.save_bible(language_id=LANGUAGE_ID, bible=BIBLE)
        self.assertTrue(os.path.exists(bible_file_path))
        with open(bible_file_path, "r") as bible_file:
            saved_bible = json.load(bible_file)
            self.assertEqual(saved_bible, BIBLE)

    def test_save_bible_existing(self):
        """should update Bible data in existing data file"""
        bible_file_path = os.path.join(
            utilities.PACKAGED_DATA_DIR_PATH,
            "bible",
            "bible-{}.json".format(LANGUAGE_ID),
        )
        with open(bible_file_path, "w") as bible_file:
            json.dump(BIBLE, bible_file)
        new_bible = copy.deepcopy(BIBLE)
        new_bible["default_version"] = 154
        add_lang.save_bible(language_id=LANGUAGE_ID, bible=new_bible)
        self.assertTrue(os.path.exists(bible_file_path))
        with open(bible_file_path, "r") as bible_file:
            saved_bible = json.load(bible_file)
            self.assertEqual(saved_bible, new_bible)
