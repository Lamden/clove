from codecs import open
from os import path

from setuptools import find_packages, setup

__version__ = '0.0.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='clove',
    version=__version__,
    description='Clove is a library that makes atomic swaps between chains easy.',
    long_description=long_description,
    install_requires=[
        'colorama==0.3.9',
        'coloredlogs==9.0',
        'pycrypto==2.6.1',
        'python_bitcoinlib',
    ],
    extras_require={
        'testing': [
            'tox==2.9.1',
            'pytest==3.3.2',
            'isort==4.2.15',
            'flake8==3.5.0',
            'freezegun==0.3.9',
            'validators==0.12.0',
        ],
        'docs': [
            'Sphinx==1.6.6',
            'sphinx-rtd-theme==0.2.4',
            'recommonmark==0.4.0',
        ],
    },
    dependency_links=[
        # waiting for this fix to be released:
        # https://github.com/petertodd/python-bitcoinlib/commit/1a089d67f5a0b64ae9f2ffcac786b87b56a0551b
        'https://github.com/lamden/python-bitcoinlib/archive/master.zip#egg=python_bitcoinlib'
    ],
    url='https://github.com/Landen/clove',
    download_url='https://github.com/Landen/clove/tarball/' + __version__,
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Lamden Team',
    author_email='team@landen.io'
)
