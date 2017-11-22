#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

import requests

response = requests.get('https://www.bible.com/bible/111/JHN.1')

print(type(response.text))
