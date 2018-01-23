# clove

version number: 0.0.1


## Overview

Clove is a library that makes atomic swaps between chains easy.


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

### Generating documentation

    $ pip install -e '.[docs]'
    $ cd docs
    $ make html
