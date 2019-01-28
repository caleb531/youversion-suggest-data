# tests.test_compliance

import glob
import json
import os.path

import isort
import jsonschema
import nose.tools as nose
import pycodestyle
import radon.complexity as radon


def test_pycodestyle():
    """All source and test files should comply with PEP 8"""
    file_paths = glob.iglob('*/*.py')
    for file_path in file_paths:
        style_guide = pycodestyle.StyleGuide(quiet=True)
        total_errors = style_guide.input_file(file_path)
        fail_msg = '{} does not comply with PEP 8'.format(file_path)
        yield nose.assert_equal, total_errors, 0, fail_msg


def test_complexity():
    """All source and test files should have a low cyclomatic complexity"""
    file_paths = glob.iglob('*/*.py')
    for file_path in file_paths:
        with open(file_path, 'r') as file_obj:
            blocks = radon.cc_visit(file_obj.read())
        for block in blocks:
            fail_msg = '{} ({}) has a cyclomatic complexity of {}'.format(
                block.name, file_path, block.complexity)
            yield nose.assert_less_equal, block.complexity, 10, fail_msg


def test_json():
    """All JSON files should comply with the respective schemas"""
    schemas = {
        'schema-languages': 'bible/languages.json',
        'schema-defaults': 'preferences/defaults.json',
        'schema-chapters': 'bible/chapters.json',
        'schema-language': 'bible/language-*.json'
    }
    for schema_name, data_path_glob in schemas.iteritems():
        schema_path = 'schemas/{}.json'.format(schema_name)
        with open(schema_path) as schema_file:
            schema = json.load(schema_file)
        data_paths = glob.iglob(data_path_glob)
        for data_path in data_paths:
            with open(data_path) as data_file:
                data = json.load(data_file)
            yield jsonschema.validate, data, schema


def test_import_order():
    """All source file imports should be properly ordered/formatted."""
    file_paths = glob.iglob('*/*.py')
    for file_path in file_paths:
        with open(file_path, 'r') as file_obj:
            file_contents = file_obj.read()
        new_file_contents = isort.SortImports(
            file_contents=file_contents).output
        fail_msg = '{} imports are not compliant'.format(
            file_path)
        yield nose.assert_equal, new_file_contents, file_contents, fail_msg


def test_language_id_correspondence():
    """Language IDs in languages.json should have a corresponding data file"""
    with open('bible/languages.json', 'r') as languages_file:
        languages = json.load(languages_file)
    for language in languages:
        nose.assert_true(
            os.path.exists(os.path.join(
                'bible', 'language-{}.json'.format(language['id']))),
            'language-{}.json does not exist'.format(language['id']))
