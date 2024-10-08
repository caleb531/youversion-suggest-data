# YouVersion Suggest Data v6.1.0

*Copyright 2014-2024 Caleb Evans*  
*Code released under the MIT license*

[![tests](https://github.com/caleb531/youversion-suggest-data/actions/workflows/tests.yml/badge.svg)](https://github.com/caleb531/youversion-suggest-data/actions/workflows/tests.yml)
[![Coverage Status](https://coveralls.io/repos/caleb531/youversion-suggest-data/badge.svg?branch=master)](https://coveralls.io/r/caleb531/youversion-suggest-data?branch=master)

This repository consists of Bible language data gathered from the YouVersion
website, for use by my [Alfred workflow][alfred], [Raycast extension][raycast],
and my [JavaScript library][api].

[api]: https://github.com/caleb531/youversion-suggest-api
[alfred]: https://alfred.app/workflows/caleb531/youversion-suggest/
[raycast]: https://www.raycast.com/caleb531/youversion-suggest

## Disclaimer

This project is not affiliated with YouVersion, and all Bible content is
copyright of the respective publishers.

This tool also retrieves Bible metadata directly from YouVersion. However,
please be aware that this functionality does not fully comply with YouVersion's
Terms of Use.

## Setup

```sh
# Install virtualenv package globally
pip3 install virtualenv
# Set up virtualenv for project
virtualenv --python=python3 ./.virtualenv
source ./.virtualenv/bin/activate
# Install project dependencies
pip install -r requirements.txt
```

## Available Utilities

### Add new language to dataset

You can add support for a new language to the Bible dataset by running the
`add_language` utility. Just supply an [RFC 5646][rfc] language code as the only
argument (supported YouVersion language codes can be found
[here][language-list]), and the script will do the rest.

[rfc]: https://www.rfc-editor.org/rfc/rfc5646.html
[language-list]: https://www.bible.com/languages

```sh
python3 -m utilities.add_language kud
```

You can explicitly set a default version for this Bible language file by passing
the `--default-version` option. If you do not supply this option, the version
with the lowest numeric ID will be used as the default version

```sh
# Versions from <https://www.bible.com/languages/tgl>
python3 -m utilities.add_language tgl --default-version 2195
```

### Update Bible data for existing language in dataset

You can fetch the latest Bible data for an existing language in this repository
by running the `update_language` utility. Just supply the language code of a
language in this repository's `bible/languages.json`.

```sh
python3 -m utilities.update_language spa_es
```

You can also change the default version for that language by supplying the
`--default-version` option with the numeric ID of your new default version:

```sh
# Versions from <https://www.bible.com/languages/eng>
python3 -m utilities.update_language eng --default-version 59
```

### Update Bible data for all languages in dataset

You can fetch the latest Bible data for all language in this repository by
running the `update_languages` utility.

```sh
python3 -m utilities.update_languages
```

## Including YVS Data in another project

To include this project's Bible data in another project, add
`youversion-suggest-data` as a Git submodule to your consuming project's
repository:

```sh
git submodule add https://github.com/caleb531/youversion-suggest-data.git
```

To update the submodule to the latest release of YVS data:

```sh
git submodule update --recursive --remote
```
