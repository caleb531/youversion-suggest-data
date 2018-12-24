#!/usr/bin/env python

# This language utility updates all existing Bible data files

from __future__ import print_function, unicode_literals

import glob
import re

from update_language import update_language


# Updates the Bible data file for every stored language
def update_languages():

    for file_path in glob.iglob('bible/language-*.json'):
        language_id = re.search('language-(.*?).json', file_path).group(1)
        update_language(language_id)
        print('')


def main():

    try:
        update_languages()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
