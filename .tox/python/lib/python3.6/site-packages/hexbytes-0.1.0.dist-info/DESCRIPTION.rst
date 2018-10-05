HexBytes
========

|Join the chat at https://gitter.im/ethereum/web3.py| |Build Status|
|PyPI version| |Python versions| |Docs build|

Python ``bytes`` subclass that decodes hex, with a readable console
output

-  Python 3.5+ support

Read more in the `documentation on
ReadTheDocs <http://hexbytes.readthedocs.io/>`__. `View the change
log <http://hexbytes.readthedocs.io/en/latest/releases.html>`__.

Quickstart
----------

.. code:: sh

    pip install hexbytes

.. code:: py

    # convert from bytes to a prettier representation at the console
    >>> HexBytes(b"\x03\x08wf\xbfh\xe7\x86q\xd1\xeaCj\xe0\x87\xdat\xa1'a\xda\xc0 \x01\x1a\x9e\xdd\xc4\x90\x0b\xf1;")
    HexBytes('0x03087766bf68e78671d1ea436ae087da74a12761dac020011a9eddc4900bf13b')

    # HexBytes accepts the hex string representation as well, ignoring case and 0x prefixes
    >>> hb = HexBytes('03087766BF68E78671D1EA436AE087DA74A12761DAC020011A9EDDC4900BF13B')
    HexBytes('0x03087766bf68e78671d1ea436ae087da74a12761dac020011a9eddc4900bf13b')

    # get the first byte:
    >>> hb[0]
    3

    # show how many bytes are in the value
    >>> len(hb)
    32

    # cast back to the basic `bytes` type
    >>> bytes(hb)
    b"\x03\x08wf\xbfh\xe7\x86q\xd1\xeaCj\xe0\x87\xdat\xa1'a\xda\xc0 \x01\x1a\x9e\xdd\xc4\x90\x0b\xf1;"

Developer setup
---------------

If you would like to hack on hexbytes, please check out the `Ethereum
Development Tactical
Manual <https://github.com/pipermerriam/ethereum-dev-tactical-manual>`__
for information on how we do:

-  Testing
-  Pull Requests
-  Code Style
-  Documentation

Development Environment Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can set up your dev environment with:

.. code:: sh


    git clone git@github.com:carver/hexbytes.git
    cd hexbytes
    virtualenv -p python3 venv
    . venv/bin/activate
    pip install -e .[dev]

Testing Setup
~~~~~~~~~~~~~

During development, you might like to have tests run on every file save.

Show flake8 errors on file change:

.. code:: sh

    # Test flake8
    when-changed -v -s -r -1 hexbytes/ tests/ -c "clear; flake8 hexbytes tests && echo 'flake8 success' || echo 'error'"

Run multi-process tests in one command, but without color:

.. code:: sh

    # in the project root:
    pytest --numprocesses=4 --looponfail --maxfail=1
    # the same thing, succinctly:
    pytest -n 4 -f --maxfail=1

Run in one thread, with color and desktop notifications:

.. code:: sh

    cd venv
    ptw --onfail "notify-send -t 5000 'Test failure ⚠⚠⚠⚠⚠' 'python 3 test on hexbytes failed'" ../tests ../hexbytes

Release setup
~~~~~~~~~~~~~

For Debian-like systems:

::

    apt install pandoc

To release a new version:

.. code:: sh

    make release bump=$$VERSION_PART_TO_BUMP$$

How to bumpversion
^^^^^^^^^^^^^^^^^^

The version format for this repo is ``{major}.{minor}.{patch}`` for
stable, and ``{major}.{minor}.{patch}-{stage}.{devnum}`` for unstable
(``stage`` can be alpha or beta).

To issue the next version in line, specify which part to bump, like
``make release bump=minor`` or ``make release bump=devnum``.

If you are in a beta version, ``make release bump=stage`` will switch to
a stable.

To issue an unstable version when the current version is stable, specify
the new version explicitly, like
``make release bump="--new-version 4.0.0-alpha.1 devnum"``

.. |Join the chat at https://gitter.im/ethereum/web3.py| image:: https://badges.gitter.im/ethereum/web3.py.svg
   :target: https://gitter.im/ethereum/web3.py?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Build Status| image:: https://travis-ci.org/carver/hexbytes.png
   :target: https://travis-ci.org/carver/hexbytes
.. |PyPI version| image:: https://badge.fury.io/py/hexbytes.svg
   :target: https://badge.fury.io/py/hexbytes
.. |Python versions| image:: https://img.shields.io/pypi/pyversions/hexbytes.svg
   :target: https://pypi.python.org/pypi/hexbytes
.. |Docs build| image:: https://readthedocs.org/projects/hexbytes/badge/?version=latest
   :target: http://hexbytes.readthedocs.io/en/latest/?badge=latest


