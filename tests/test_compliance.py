#!/usr/bin/env python3
# coding=utf-8

import glob
import json
import os
import os.path

import jsonschema
import pytest
import radon.complexity as radon


def get_code_blocks():
    for file_path in glob.iglob("*/*.py"):
        with open(file_path, "r") as file_obj:
            for block in radon.cc_visit(file_obj.read()):
                yield file_path, block


@pytest.mark.parametrize(("file_path", "block"), get_code_blocks())
def test_complexity(file_path, block):
    """All source and test files should have a low cyclomatic complexity"""
    fail_msg = "{} ({}) has a cyclomatic complexity of {}".format(
        block.name, file_path, block.complexity
    )
    assert block.complexity <= 10, fail_msg


def get_schema_cases():
    schemas = {
        "schema-languages": "bible/languages.json",
        "schema-book-metadata": "bible/book-metadata.json",
        "schema-bible": "bible/bible-*.json",
    }
    for schema_name, data_path_glob in schemas.items():
        schema_path = "schemas/{}.json".format(schema_name)
        for data_path in glob.iglob(data_path_glob):
            yield schema_path, data_path


@pytest.mark.parametrize(("schema_path", "data_path"), get_schema_cases())
def test_json(schema_path, data_path):
    """All JSON files should comply with the respective schemas"""
    with open(schema_path) as schema_file:
        schema = json.load(schema_file)
    with open(data_path) as data_file:
        data = json.load(data_file)
    jsonschema.validate(data, schema)


def load_languages():
    with open("bible/languages.json", "r") as languages_file:
        return json.load(languages_file)


@pytest.mark.parametrize("language", load_languages())
def test_language_id_correspondence(language):
    """Language IDs in languages.json should have a corresponding data file"""
    data_path = os.path.join("bible", "bible-{}.json".format(language["id"]))
    assert os.path.exists(data_path), "{} does not exist".format(data_path)
