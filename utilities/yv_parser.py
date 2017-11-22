# yvs.yv_parser
# coding=utf-8

from __future__ import unicode_literals

from htmlentitydefs import name2codepoint
from HTMLParser import HTMLParser


# A base class for parsing YouVersion HTML
class YVParser(HTMLParser):

    # Evaluates HTML character reference to its respective Unicode character
    @staticmethod
    def eval_html_charref(name):

        if name[0] == 'x':
            # Handle hexadecimal character references
            return unichr(int(name[1:], 16))
        elif name.isdigit():
            # Handle decimal character references
            return unichr(int(name))
        else:
            # Otherwise, assume character reference is a named reference
            return unichr(name2codepoint[name])

    # Handle named character references; pass evaluated characters to
    # handle_data method to simplify the parsing of data between HTML tags
    def handle_entityref(self, name):
        self.handle_data(self.__class__.eval_html_charref(name))

    # Handle decimal and hexadecimal character references
    def handle_charref(self, name):
        self.handle_data(self.__class__.eval_html_charref(name))
