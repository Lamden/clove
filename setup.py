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
        'bitcoinlib==0.3.29',
    ],
    extras_require={
        'testing': [
            'tox==2.9.1',
            'pytest==3.3.2',
            'isort==4.2.15',
            'flake8==3.5.0',
            'validators==0.12.0',
        ],
        'docs': [
            'Sphinx==1.6.6',
            'sphinx-rtd-theme==0.2.4',
            'recommonmark==0.4.0',
        ],
    },
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
