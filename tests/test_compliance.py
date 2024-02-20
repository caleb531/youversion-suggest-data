#!/usr/bin/env python3
# coding=utf-8

import glob
import json
import os
import os.path
import unittest

import isort
import jsonschema
import radon.complexity as radon

case = unittest.TestCase()


def test_complexity():
    """All source and test files should have a low cyclomatic complexity"""
    file_paths = glob.iglob("*/*.py")
    for file_path in file_paths:
        with open(file_path, "r") as file_obj:
            blocks = radon.cc_visit(file_obj.read())
        for block in blocks:
            fail_msg = "{} ({}) has a cyclomatic complexity of {}".format(
                block.name, file_path, block.complexity
            )
            yield case.assertLessEqual, block.complexity, 10, fail_msg


def test_json():
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


def test_import_order():
    """All source file imports should be properly ordered/formatted."""
    file_paths = glob.iglob("*/*.py")
    for file_path in file_paths:
        with open(file_path, "r") as file_obj:
            file_contents = file_obj.read()
        new_file_contents = isort.code(file_contents)
        fail_msg = "{} imports are not compliant".format(file_path)
        yield case.assertEqual, new_file_contents, file_contents, fail_msg


def test_language_id_correspondence():
    """Language IDs in languages.json should have a corresponding data file"""
    with open("bible/languages.json", "r") as languages_file:
        languages = json.load(languages_file)
    for language in languages:
        case.assertTrue(
            os.path.exists(
                os.path.join("bible", "bible-{}.json".format(language["id"]))
            ),
            "bible-{}.json does not exist".format(language["id"]),
        )
