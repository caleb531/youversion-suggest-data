#!/usr/bin/env python3
# coding=utf-8

import sys
from functools import wraps
from io import StringIO


def redirect_stdout(func):
    """temporarily redirect stdout to new Unicode output stream"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        original_stdout = sys.stdout
        out = StringIO()
        try:
            sys.stdout = out
            # If the decorated function is a method, the `self` argument should
            # still be first
            if args and hasattr(args[0], "__class__"):
                self_arg, *rest_args = args
                return func(self_arg, out, *rest_args, **kwargs)
            else:
                return func(out, *args, **kwargs)
        finally:
            sys.stdout = original_stdout

    return wrapper
