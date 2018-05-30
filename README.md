# clove [![Build Status](https://travis-ci.com/Lamden/clove.svg?token=ZJstcVy9cUkAxLqvqRuL&branch=master)](https://travis-ci.com/Lamden/clove)

version number: 1.1.1


## Overview

Clove is a library that makes atomic swaps between chains easy.


Documentation available at [lamden.github.io/clove](https://lamden.github.io/clove).


## Installation

To install use pip:

    $ pip install clove


Or clone the repo:

    $ git clone https://github.com/Landen/clove.git
    $ python setup.py install


## Development

### Getting started

    $ git clone https://github.com/Landen/clove.git
    $ cd clove
    $ virtualenv venv --python=python3.6
    $ . venv/bin/activate
    $ python setup.py develop

### Running tests

Install requirements:

    $ pip install -e '.[testing]'

To run all linters and tests:

    $ tox

If you want to run a specyfic test

    $ py.test -k test_name
