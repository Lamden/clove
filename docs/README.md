# Clove [![Build Status](https://travis-ci.com/Lamden/clove.svg?token=ZJstcVy9cUkAxLqvqRuL&branch=master)](https://travis-ci.com/Lamden/clove)

<img src="https://raw.githubusercontent.com/Lamden/clove/master/docs/clove.jpg" align="right" title="Clove" width="300" height="450">

version number: 1.2.16


## Overview


Clove is a library that makes atomic swaps between chains easy.


Documentation available at [lamden.github.io/clove](https://lamden.github.io/clove).


## Installation

To install use pip:

    $ pip install clove


Or clone the repo:

    $ git clone https://github.com/Lamden/clove.git
    $ python setup.py install


## Development

### Getting started

    $ git clone https://github.com/Lamden/clove.git
    $ cd clove
    $ virtualenv venv --python=python3.6
    $ . venv/bin/activate
    $ python setup.py develop

### Running tests
CRYPTOID_API_KEY and INFURA_TOKEN environment variables need to be set.  If you are running sudo then they also need to be running in that environment.

Install requirements:

    $ pip install -e '.[testing]'

To run all linters and tests:

    $ tox

If you want to run a specyfic test

    $ py.test -k test_name -q --CRYPTOID_API_KEY $CRYPTOID_API_KEY --INFURA_TOKEN $INFURA_TOKEN -vv

### Documentation

Installing requirements:

    $ pip install -e '.[docs]'

Documentation preview:

    $ make livedocs

Updating docs for `master` branch

    $ make gh-pages
