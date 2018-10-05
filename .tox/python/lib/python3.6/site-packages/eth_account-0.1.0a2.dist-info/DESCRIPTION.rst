eth-account
===========

|Join the chat at https://gitter.im/ethereum/eth-account|

|Build Status|

Sign Ethereum transactions and messages with local private keys

-  Python 3.5+ support

Read more in the `documentation on
ReadTheDocs <http://eth-account.readthedocs.io/>`__. `View the change
log on Github <docs/releases.rst>`__.

Quickstart
----------

.. code:: sh

    pip install eth-account

Developer setup
---------------

If you would like to hack on eth-account, please check out the `Ethereum
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


    git clone git@github.com:ethereum/eth-account.git
    cd eth-account
    virtualenv -p python3 venv
    . venv/bin/activate
    pip install -e .[dev]

Testing Setup
~~~~~~~~~~~~~

During development, you might like to have tests run on every file save.

Show flake8 errors on file change:

.. code:: sh

    # Test flake8
    when-changed -v -s -r -1 eth_account/ tests/ -c "clear; flake8 eth_account tests && echo 'flake8 success' || echo 'error'"

Run multi-process tests in one command, but without color:

.. code:: sh

    # in the project root:
    pytest --numprocesses=4 --looponfail --maxfail=1
    # the same thing, succinctly:
    pytest -n 4 -f --maxfail=1

Run in one thread, with color and desktop notifications:

.. code:: sh

    cd venv
    ptw --onfail "notify-send -t 5000 'Test failure ⚠⚠⚠⚠⚠' 'python 3 test on eth-account failed'" ../tests ../eth_account

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

.. |Join the chat at https://gitter.im/ethereum/eth-account| image:: https://badges.gitter.im/ethereum/eth-account.svg
   :target: https://gitter.im/ethereum/eth-account?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |Build Status| image:: https://travis-ci.org/ethereum/eth-account.png
   :target: https://travis-ci.org/ethereum/eth-account


