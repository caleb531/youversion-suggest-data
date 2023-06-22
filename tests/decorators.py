#!/usr/bin/env python3
# coding=utf-8

import sys
from contextlib import contextmanager
from io import StringIO


@contextmanager
def redirect_stdout(func):
    """temporarily redirect stdout to new Unicode output stream"""
    original_stdout = sys.stdout
    out = StringIO()
    try:
        sys.stdout = out
        yield
    finally:
        sys.stdout = original_stdout
