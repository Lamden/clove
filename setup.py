from codecs import open
from os import path

from setuptools import find_packages, setup

version = __import__('clove').__version__

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='clove',
    version=version,
    description='Clove is a library that makes atomic swaps between chains easy.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'python-altcoinlib==0.9.1',
        'colorama==0.3.9',
        'coloredlogs==9.0',
        'web3==4.0.0b11',
        'ecdsa==0.13',

        # fixed requirements of ethereum
        'eth-account==0.1.0a2',
        'eth-rlp==0.1.0',
        'rlp==0.6.0',

        'ethereum==2.3.0',
    ],
    extras_require={
        'testing': [
            'tox==2.9.1',
            'pytest==3.3.2',
            'isort==4.3.4',
            'flake8==3.5.0',
            'freezegun==0.3.9',
            'validators==0.12.0',
            'pytest-cov==2.5.1',
            'requests==2.18.4',
        ],
        'dev': [
            'pyquery==1.4.0',
            'bumpversion==0.5.3',
        ],
    },
    url='https://github.com/Lamden/clove',
    download_url=f'https://github.com/Lamden/clove/tarball/{version}',
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
    author_email='team@lamden.io'
)
