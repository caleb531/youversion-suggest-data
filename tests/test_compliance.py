#!/usr/bin/env python3
# coding=utf-8

import glob
import json
import os
import os.path

import jsonschema
import radon.complexity as radon

from tests import YVSTestCase


class TestCompliance(YVSTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_complexity(self):
        """All source and test files should have a low cyclomatic complexity"""
        file_paths = glob.iglob("*/*.py")
        for file_path in file_paths:
            with open(file_path, "r") as file_obj:
                blocks = radon.cc_visit(file_obj.read())
            for block in blocks:
                fail_msg = "{} ({}) has a cyclomatic complexity of {}".format(
                    block.name, file_path, block.complexity
                )
                yield self.assertLessEqual, block.complexity, 10, fail_msg

    def test_json(self):
        """All JSON files should comply with the respective schemas"""
        schemas = {
            "schema-languages": "bible/languages.json",
            "schema-book-metadata": "bible/book-metadata.json",
            "schema-bible": "bible/bible-*.json",
        }
        for schema_name, data_path_glob in schemas.items():
            schema_path = "schemas/{}.json".format(schema_name)
            with open(schema_path) as schema_file:
                schema = json.load(schema_file)
            data_paths = glob.iglob(data_path_glob)
            for data_path in data_paths:
                with open(data_path) as data_file:
                    data = json.load(data_file)
                yield jsonschema.validate, data, schema

    def test_language_id_correspondence(self):
        """Language IDs in languages.json should have a corresponding data file"""
        with open("bible/languages.json", "r") as languages_file:
            languages = json.load(languages_file)
        for language in languages:
            self.assertTrue(
                os.path.exists(
                    os.path.join("bible", "bible-{}.json".format(language["id"]))
                ),
                "bible-{}.json does not exist".format(language["id"]),
            )
